// 安全ガード：重複初期化を防ぐ
if (!window.__productGalleryInitialized) {
  window.__productGalleryInitialized = true;

  document.addEventListener('DOMContentLoaded', function () {
    const lists = Array.from(document.querySelectorAll('.thumbnail-list'));
    // 再計算関数（マイページのリストのみ3枚分の見た目に制限）
    function applyConstraint(list) {
      if (!list.closest('body.account-page')) {
        list.style.maxWidth = '';
        list.style.overflowX = '';
        list.style.flexWrap = '';
        return;
      }

      const firstBtn = list.querySelector('.thumb-btn');
      if (!firstBtn) {
        list.style.maxWidth = '';
        list.style.overflowX = 'auto';
        list.style.flexWrap = 'nowrap';
        return;
      }
      const btnRect = firstBtn.getBoundingClientRect();
      const btnWidth = Math.round(btnRect.width) || 56;
      const style = window.getComputedStyle(list);
      let gap = 8;
      const rawGap = style.getPropertyValue('column-gap') || style.getPropertyValue('gap') || '';
      gap = rawGap ? parseFloat(rawGap) : gap;
      if (isNaN(gap)) gap = 8;
      const paddingRight = parseFloat(style.paddingRight) || 0;
      const paddingLeft = parseFloat(style.paddingLeft) || 0;
      const maxWidth = btnWidth * 3 + gap * 2 + paddingLeft + paddingRight;
      list.style.maxWidth = Math.round(maxWidth) + 'px';
      list.style.overflowX = 'auto';
      list.style.overflowY = 'visible';
      list.style.flexWrap = 'nowrap';
      list.style.webkitOverflowScrolling = 'touch';
    }

    // 初期処理
    lists.forEach(list => {
      // 対応する main を決定（カード内優先）
      const card = list.closest('.product-card');
      const mainImg = card ? card.querySelector('.card-main') : document.getElementById('main-image');

      // クリックで差し替え（委譲）
      list.addEventListener('click', function (e) {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        const src = btn.dataset.src || (btn.querySelector('img') && btn.querySelector('img').src);
        if (!src) return;
        const img = new Image();
        img.onload = () => {
          if (mainImg) mainImg.src = src;
          list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        };
        img.onerror = () => console.warn('product_gallery: preload failed', src);
        img.src = src;
      });

      // keyboard support
      list.addEventListener('keydown', function (e) {
        const btn = e.target.closest('.thumb-btn');
        if (!btn) return;
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });

      // 初期active（main を合わせる）
      const first = list.querySelector('.thumb-btn');
      if (first) {
        list.querySelectorAll('.thumb-btn').forEach(b => b.classList.remove('active'));
        first.classList.add('active');
        const firstSrc = first.dataset.src || (first.querySelector('img') && first.querySelector('img').src);
        if (firstSrc && mainImg && mainImg.src !== firstSrc) mainImg.src = firstSrc;
      }

      // 横スクロール補助（ホイール→横スクロール、ドラッグ）
      list.addEventListener('wheel', function (e) {
        if (Math.abs(e.deltaY) > 0) {
          list.scrollLeft += e.deltaY;
          e.preventDefault();
        }
      }, { passive: false });

      let isDown = false, startX = 0, scrollStart = 0;
      list.addEventListener('pointerdown', function (e) {
        isDown = true;
        try { list.setPointerCapture(e.pointerId); } catch (_) {}
        startX = e.clientX;
        scrollStart = list.scrollLeft;
        list.classList.add('dragging');
      });
      list.addEventListener('pointermove', function (e) {
        if (!isDown) return;
        const dx = e.clientX - startX;
        list.scrollLeft = scrollStart - dx;
      });
      const endDrag = function (e) {
        if (!isDown) return;
        isDown = false;
        try { if (e && e.pointerId) list.releasePointerCapture(e.pointerId); } catch (_) {}
        list.classList.remove('dragging');
      };
      list.addEventListener('pointerup', endDrag);
      list.addEventListener('pointercancel', endDrag);
      list.addEventListener('pointerleave', endDrag);

      // 制約適用（マイページのみ）
      applyConstraint(list);

      // 画像読み込み後にも再計算：画像が多い場合に幅が変わるため
      const imgs = Array.from(list.querySelectorAll('img'));
      imgs.forEach(img => {
        if (img.complete) return;
        img.addEventListener('load', () => applyConstraint(list), { once: true });
      });
    });

    // window load でも再計算（遅延画像やフォントの影響対策）
    window.addEventListener('load', () => lists.forEach(l => applyConstraint(l)));

    // ウィンドウリサイズ時に再計算（マイページのサムネ幅が変わるため）
    let resizeTimer = null;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        lists.forEach(l => applyConstraint(l));
      }, 120);
    });
  });
}