// 安全ガード：重複初期化を防ぐ
if (!window.__productGalleryInitialized) {
  window.__productGalleryInitialized = true;

  document.addEventListener('DOMContentLoaded', function () {
    // ページ内の全てのサムネリストを処理
    document.querySelectorAll('.thumbnail-list').forEach(list => {
      // このリストに対応するメイン画像を決定（カード内の .card-main 優先、無ければグローバル #main-image）
      const card = list.closest('.product-card');
      const mainImg = card ? card.querySelector('.card-main') : document.getElementById('main-image');
      if (!mainImg) return;

      // クリックで差し替え（委譲）
      list.addEventListener('click', function (e) {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        const src = btn.dataset.src || (btn.querySelector('img') && btn.querySelector('img').src);
        if (!src) return;

        const img = new Image();
        img.onload = () => {
          mainImg.src = src;
          // このリスト内の active を更新
          list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        };
        img.onerror = () => console.warn('product_gallery: preload failed', src);
        img.src = src;
      });

      // キーボード対応（Enter / Space）
      list.addEventListener('keydown', function (e) {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });

      // 初期状態: 最初のサムネを active（必要なら main も合わせる）
      const first = list.querySelector('.thumb-btn');
      if (first) {
        list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
        first.classList.add('active');
        const firstSrc = first.dataset.src || (first.querySelector('img') && first.querySelector('img').src);
        if (firstSrc && mainImg.src !== firstSrc) {
          // 即時差し替え（プリロード不要）
          mainImg.src = firstSrc;
        }
      }
    });
  });
}