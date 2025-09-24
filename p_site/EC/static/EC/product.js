// 画像クリックで main-image を差し替える
document.addEventListener('DOMContentLoaded', function(){
  const main = document.getElementById('main-image');
  if (!main) return;
  const thumbs = document.querySelectorAll('.thumb-btn');
  thumbs.forEach(btn=>{
    btn.addEventListener('click', ()=> {
      const src = btn.dataset.src;
      if (!src) return;
      // プレースホルダ読み込みをスムーズにするために一度 new Image() を作る
      const img = new Image();
      img.onload = ()=> {
        main.src = src;
        // アクティブクラスの更新
        document.querySelectorAll('.thumb-btn.active').forEach(el=>el.classList.remove('active'));
        btn.classList.add('active');
      };
      img.src = src;
    });
    // キーボード対応
    btn.addEventListener('keydown', (e)=> {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });
  });
});