document.addEventListener('DOMContentLoaded', function(){
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : null;
  }

  // modal 要素
  const backdrop = document.getElementById('modal-backdrop');
  const modalBody = document.getElementById('modal-body');
  const btnNew = document.getElementById('modal-new');
  const btnHome = document.getElementById('modal-home');

  function openModal(){ if(!backdrop) return; backdrop.style.display='flex'; backdrop.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function closeModal(){ if(!backdrop) return; backdrop.style.display='none'; backdrop.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }
  if (btnNew) btnNew.addEventListener('click', ()=>{ closeModal(); const form = document.getElementById('product-form'); if(form) form.reset(); });
  if (btnHome) btnHome.addEventListener('click', ()=> location.href = '/EC/');

  // 画像削除（個別）: delegated
  document.addEventListener('click', async function(e){
    const btn = e.target.closest('.img-delete');
    if(!btn) return;
    if(!confirm('この画像を削除します。よろしいですか？')) return;
    const url = btn.dataset.url;
    if(!url) return alert('削除 URL がありません');
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {'X-Requested-With':'XMLHttpRequest','X-CSRFToken':getCookie('csrftoken')},
        credentials: 'same-origin'
      });
      const data = await res.json().catch(()=>null);
      if(res.ok && data && data.success){
        const node = btn.closest('.existing-thumb');
        if(node) node.remove();
      } else {
        alert('画像の削除に失敗しました: ' + (data?.error || res.status));
      }
    } catch(err){
      console.error(err);
      alert('通信エラーが発生しました');
    }
  });

  // 既存画像グリッドの選択 / 一括削除ロジック
  const existingContainer = document.querySelector('.existing-images');
  if (existingContainer){
    const bulkBtn = document.getElementById('bulk-delete');
    const selectAllBtn = document.getElementById('select-all');
    const clearBtn = document.getElementById('clear-selection');

    function updateBulkUI(){
      const sel = existingContainer.querySelectorAll('.thumb-check:checked');
      const n = sel.length;
      if (bulkBtn){ bulkBtn.disabled = n === 0; bulkBtn.textContent = `選択を削除（${n}）`; }
      existingContainer.querySelectorAll('.existing-thumb').forEach(el=>{
        const ck = el.querySelector('.thumb-check');
        if(ck && ck.checked) el.classList.add('selected'); else el.classList.remove('selected');
      });
    }

    // checkbox change はそのまま反映
    existingContainer.addEventListener('change', function(e){
      if(e.target.matches('.thumb-check')) updateBulkUI();
    });

    // thumbクリックは checkbox 以外でトグル（checkbox 自体のクリックはブラウザ挙動を尊重）
    existingContainer.addEventListener('click', function(e){
      const el = e.target.closest('.existing-thumb');
      if(!el) return;
      if (e.target.closest('.thumb-check')) return; // checkbox 自体はスキップ
      if (e.target.closest('.img-delete')) return; // 削除ボタンはスキップ
      const ck = el.querySelector('.thumb-check');
      if(ck){ ck.checked = !ck.checked; updateBulkUI(); }
    });

    if(selectAllBtn) selectAllBtn.addEventListener('click', ()=>{ existingContainer.querySelectorAll('.thumb-check').forEach(c=>c.checked=true); updateBulkUI(); });
    if(clearBtn) clearBtn.addEventListener('click', ()=>{ existingContainer.querySelectorAll('.thumb-check').forEach(c=>c.checked=false); updateBulkUI(); });

    if(bulkBtn){
      bulkBtn.addEventListener('click', async function(){
        const selected = Array.from(existingContainer.querySelectorAll('.thumb-check:checked')).map(i=>i.value);
        if(!selected.length) return;
        if(!confirm(`${selected.length} 件の画像を削除します。よろしいですか？`)) return;

        // 安定的に bulk endpoint を作る：現在の編集ページが .../product/<pk>/edit/ を想定
        let url = window.location.pathname.replace(/\/edit\/?$/,'/images/delete/');
        if(!url.endsWith('/images/delete/')) url = url + '/images/delete/';

        try {
          const fd = new FormData();
          selected.forEach(id => fd.append('img_pks[]', id));
          const res = await fetch(url, {
            method: 'POST',
            headers: {'X-Requested-With':'XMLHttpRequest','X-CSRFToken':getCookie('csrftoken')},
            body: fd,
            credentials: 'same-origin'
          });
          const data = await res.json().catch(()=>null);
          if(res.ok && data && data.success){
            selected.forEach(id=>{
              const node = existingContainer.querySelector(`.existing-thumb[data-img-pk="${id}"]`);
              if(node) node.remove();
            });
            // main image 更新があるなら反映（編集画面のメイン表示がある場合）
            if (data.new_main_url){
              const main = document.getElementById('main-image');
              if(main) main.src = data.new_main_url;
            }
            updateBulkUI();
          } else {
            alert('削除に失敗しました: ' + (data?.error || res.status));
          }
        } catch(err){
          console.error(err);
          alert('通信エラーが発生しました');
        }
      });
    }
    updateBulkUI();
  }

  // フォーム送信（出品/編集）：重複バインド防止・多重送信ガード・複数ファイル対応
  const form = document.getElementById('product-form');
  if (form){
    if (form.dataset.submitHandlerAttached === '1'){
      console.warn('product_create.js: submit handler already attached - skipping');
    } else {
      form.dataset.submitHandlerAttached = '1';
      form.addEventListener('submit', async function(e){
        e.preventDefault();
        console.debug('product_create.js: submit invoked');

        if (form.dataset.submitting === '1'){
          console.warn('product_create.js: blocked duplicate submit');
          return;
        }
        form.dataset.submitting = '1';
        const submitButtons = Array.from(form.querySelectorAll('[type="submit"]'));
        submitButtons.forEach(b => b.disabled = true);

        // 明示的に FormData を組み立てる（ファイルを複数 append）
        const fd = new FormData();
        Array.from(form.elements).forEach(el=>{
          if(!el.name) return;
          if(el.type === 'file') return;
          if((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
          fd.append(el.name, el.value);
        });
        const fileInput = form.querySelector('input[type="file"][name="photos"]');
        if(fileInput && fileInput.files && fileInput.files.length){
          for(let i=0;i<fileInput.files.length;i++) fd.append('photos', fileInput.files[i]);
        }

        try {
          console.debug('product_create.js: sending fetch');
          const res = await fetch(form.action || window.location.pathname, {
            method: 'POST',
            headers: {'X-Requested-With':'XMLHttpRequest','X-CSRFToken':getCookie('csrftoken')},
            body: fd,
            credentials: 'same-origin'
          });
          if(!res.ok){
            const err = await res.json().catch(()=>null);
            alert(err?.errors ? JSON.stringify(err.errors) : 'エラーが発生しました');
            return;
          }
          const data = await res.json().catch(()=>null);
          if(data && data.success){
            const p = data.product || {};
            let html = '';
            if (p.photo_url) html += '<div class="thumb"><img src="'+p.photo_url+'" alt=""></div>';
            html += '<div><strong style="font-size:1.05em">'+(p.name||'')+'</strong></div>';
            html += '<div style="margin-top:6px">価格: ¥'+(p.price||'')+'</div>';
            if (p.category) html += '<div>カテゴリ: '+p.category+'</div>';
            if (p.description) html += '<div style="margin-top:8px;text-align:center;white-space:pre-wrap;">'+(p.description||'')+'</div>';
            if (modalBody) modalBody.innerHTML = html;
            openModal();
          } else {
            alert('保存に失敗しました');
          }
        } catch(err){
          console.error(err);
          alert('通信エラーが発生しました');
        } finally {
          form.dataset.submitting = '0';
          submitButtons.forEach(b => b.disabled = false);
        }
      });
    }
  }

}); // DOMContentLoaded end