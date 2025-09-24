document.addEventListener('DOMContentLoaded', function(){
  const main = document.getElementById('main-image');
  if (!main) return;
  const thumbs = Array.from(document.querySelectorAll('.thumb-btn'));
  if (!thumbs.length) return;

  // クリックで差し替え、先読みしてアクティブクラス更新
  thumbs.forEach(btn => {
    btn.addEventListener('click', () => {
      const src = btn.dataset.src;
      if (!src) return;
      const img = new Image();
      img.onload = () => {
        main.src = src;
        thumbs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      };
      img.onerror = () => {
        console.warn('画像読み込み失敗', src);
      };
      img.src = src;
    });

    // キーボード対応
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });

    // アクセシビリティ：フォーカスで薄い枠
    btn.addEventListener('focus', () => btn.classList.add('focus'));
    btn.addEventListener('blur',  () => btn.classList.remove('focus'));
  });
});