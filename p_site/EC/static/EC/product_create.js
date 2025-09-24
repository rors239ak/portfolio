document.addEventListener('DOMContentLoaded', function(){
  // getCookie 関数 が既にあるなら省略して同じものを使用
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : null;
  }

  // 既存画像の削除ボタン（.img-delete）が押されたら AJAX POST で削除
  document.addEventListener('click', async function(e){
    const btn = e.target.closest('.img-delete');
    if (!btn) return;
    if (!confirm('この画像を削除します。よろしいですか？')) return;

    const url = btn.dataset.url;
    if (!url) return alert('削除 URL が設定されていません');

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'same-origin'
      });
      const data = await res.json().catch(()=>null);
      if (res.ok && data && data.success) {
        // DOM から削除
        const thumb = btn.closest('.existing-thumb');
        if (thumb) thumb.remove();

        // main-image が存在し、new_main_url があれば差し替え
        if (data.new_main_url) {
          const main = document.getElementById('main-image');
          if (main) main.src = data.new_main_url;
        } else {
          // 画像が全て無くなった場合はプレースホルダにする（任意）
          const main = document.getElementById('main-image');
          if (main) main.src = '';
        }
      } else {
        alert('画像の削除に失敗しました: ' + (data?.error || res.status));
      }
    } catch (err) {
      console.error(err);
      alert('通信エラーが発生しました');
    }
  });

  const form = document.getElementById('product-form');
  const backdrop = document.getElementById('modal-backdrop');
  const modalBody = document.getElementById('modal-body');
  const btnNew = document.getElementById('modal-new');
  const btnHome = document.getElementById('modal-home');

  function openModal(){ backdrop.style.display='flex'; backdrop.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function closeModal(){ backdrop.style.display='none'; backdrop.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }

  if (form){
    form.addEventListener('submit', async function(e){
      e.preventDefault();

      // 明示的に FormData を組み立てる（ファイルを複数 append）
      const fd = new FormData();

      // 非ファイル要素を追加
      Array.from(form.elements).forEach(el => {
        if (!el.name) return;
        if (el.type === 'file') return;
        if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
        fd.append(el.name, el.value);
      });

      // photos input のファイルをすべて append
      const fileInput = form.querySelector('input[type="file"][name="photos"]');
      if (fileInput && fileInput.files && fileInput.files.length) {
        for (let i = 0; i < fileInput.files.length; i++){
          fd.append('photos', fileInput.files[i]);
        }
      }

      try {
        const res = await fetch(form.action || window.location.pathname, {
          method: 'POST',
          headers: {
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: fd,
          credentials: 'same-origin'
        });

        if (!res.ok) {
          const err = await res.json().catch(()=>null);
          alert(err?.errors ? JSON.stringify(err.errors) : 'エラーが発生しました');
          return;
        }

        const data = await res.json().catch(()=>null);
        if (data && data.success){
          const p = data.product || {};
          let html = '';
          if (p.photo_url) html += '<div class="thumb"><img src="'+p.photo_url+'" alt=""></div>';
          html += '<div><strong style="font-size:1.05em">'+(p.name||'')+'</strong></div>';
          html += '<div style="margin-top:6px">価格: ¥'+(p.price||'')+'</div>';
          if (p.category) html += '<div>カテゴリ: '+p.category+'</div>';
          if (p.description) html += '<div style="margin-top:8px;text-align:center;white-space:pre-wrap;">'+(p.description||'')+'</div>';
          modalBody.innerHTML = html;
          openModal();
        } else {
          alert('保存に失敗しました');
        }
      } catch(err){
        console.error(err);
        alert('通信エラーが発生しました');
      }
    });
  }

  if (btnNew) btnNew.addEventListener('click', function(){ closeModal(); if(form) form.reset(); });
  if (btnHome) btnHome.addEventListener('click', function(){ location.href = '/EC/'; });

  // モーダル ESC で閉じる
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && backdrop && backdrop.style.display === 'flex') closeModal(); });

  // 選択状態管理
  const existingContainer = document.querySelector('.existing-images');
  if (existingContainer){
    const checkboxes = Array.from(existingContainer.querySelectorAll('.thumb-check'));
    const bulkBtn = document.getElementById('bulk-delete');
    const selectAllBtn = document.getElementById('select-all');
    const clearBtn = document.getElementById('clear-selection');

    function updateBulkUI(){
      const sel = existingContainer.querySelectorAll('.thumb-check:checked');
      const n = sel.length;
      if (bulkBtn) {
        bulkBtn.disabled = n === 0;
        bulkBtn.textContent = `選択を削除（${n}）`;
      }
      // visual
      existingContainer.querySelectorAll('.existing-thumb').forEach(el=>{
        const ck = el.querySelector('.thumb-check');
        if (ck && ck.checked) el.classList.add('selected'); else el.classList.remove('selected');
      });
    }

    // checkbox click
    existingContainer.addEventListener('change', function(e){
      if (e.target.matches('.thumb-check')){
        updateBulkUI();
      }
    });

    // click on thumb toggles checkbox
    existingContainer.addEventListener('click', function(e){
      const el = e.target.closest('.existing-thumb');
      if (!el) return;
      // ignore clicks on individual delete button
      if (e.target.closest('.img-delete')) return;
      const ck = el.querySelector('.thumb-check');
      if (ck){
        ck.checked = !ck.checked;
        updateBulkUI();
      }
    });

    if (selectAllBtn){
      selectAllBtn.addEventListener('click', function(){ checkboxes.forEach(c=>c.checked=true); updateBulkUI(); });
    }
    if (clearBtn){
      clearBtn.addEventListener('click', function(){ checkboxes.forEach(c=>c.checked=false); updateBulkUI(); });
    }

    // 一括削除
    if (bulkBtn){
      bulkBtn.addEventListener('click', async function(){
        const selected = Array.from(existingContainer.querySelectorAll('.thumb-check:checked')).map(i=>i.value);
        if (!selected.length) return;
        if (!confirm(`${selected.length} 件の画像を削除します。よろしいですか？`)) return;

        const url = window.location.pathname.replace(/\/edit\/?$/,'') + 'images/delete/'; // /EC/product/<pk>/images/delete/
        // fallback: data attribute could be used if needed
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
          if (res.ok && data && data.success){
            // remove DOM nodes
            selected.forEach(id=>{
              const node = existingContainer.querySelector(`.existing-thumb[data-img-pk="${id}"]`);
              if (node) node.remove();
            });
            // update main image if provided
            if