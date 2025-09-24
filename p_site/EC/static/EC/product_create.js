document.addEventListener('DOMContentLoaded', function(){
  function getCookie(name){
    const v = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
    return v ? decodeURIComponent(v.pop()) : null;
  }

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
});