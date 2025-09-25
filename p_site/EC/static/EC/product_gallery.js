// 安全ガード：重複初期化を防ぐ
if (!window.__productGalleryInitialized) {
  window.__productGalleryInitialized = true;

  document.addEventListener('DOMContentLoaded', function () {
    // 重複初期化防止
    if (window.__productGalleryInit) return;
    window.__productGalleryInit = true;

    const lists = Array.from(document.querySelectorAll('.thumbnail-list'));
    lists.forEach(list => {
      // クリックでメイン差替（委譲）
      list.addEventListener('click', (e) => {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        // サムネから画像URLを取得
        const src = btn.dataset.src || (btn.querySelector('img') && btn.querySelector('img').src);
        if (!src) return;

        // 対応する main 要素を探す（カード内の .card-main 優先、次に #main-image、次に .product-image）
        const card = btn.closest('.product-card');
        let mainImg = null;
        if (card) mainImg = card.querySelector('.card-main') || card.querySelector('#main-image') || card.querySelector('.product-image');
        if (!mainImg) mainImg = document.getElementById('main-image') || document.querySelector('.product-page .product-image') || document.querySelector('.card-main');

        // プリロードしてから差し替え（ちらつき防止）
        const preload = new Image();
        preload.onload = () => {
          if (!mainImg) return;
          if (mainImg.tagName && mainImg.tagName.toLowerCase() === 'img') {
            mainImg.src = src;
          } else {
            // img 要素でない場合は背景画像として反映
            mainImg.style.backgroundImage = `url("${src}")`;
            mainImg.style.backgroundSize = 'cover';
            mainImg.style.backgroundPosition = 'center';
          }
          // active クラス更新（そのリスト内のみ）
          list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        };
        preload.onerror = () => console.warn('product_gallery: preload failed', src);
        preload.src = src;
      });

      // キーボード対応：Enter/Space でクリック発火
      list.addEventListener('keydown', (e) => {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });

      // 初期 active 設定（最初のサムネをアクティブにして main を合わせる）
      const first = list.querySelector('.thumb-btn');
      if (first) {
        list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
        first.classList.add('active');
        // main をセット（遅延読み込みの影響を避けるため setTimeout）
        setTimeout(() => {
          const src = first.dataset.src || (first.querySelector('img') && first.querySelector('img').src);
          if (!src) return;
          const card = first.closest('.product-card');
          let mainImg = card ? (card.querySelector('.card-main') || card.querySelector('#main-image')) : document.getElementById('main-image');
          if (mainImg && mainImg.tagName && mainImg.tagName.toLowerCase() === 'img') {
            if (mainImg.src !== src) mainImg.src = src;
          }
        }, 30);
      }

      // 横スクロール補助（マウスホイール→横スクロール、ドラッグスクロール）は既存処理があるならそちらと併用可能
      // （必要ならここに補助コードを追加）
    });
  });
}