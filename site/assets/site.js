// Apply the theme before CSS paints; storage is optional (e.g. private browsing).
(() => {
  // A transient request failure should not require refreshing the whole page.
  const imageStates = new WeakMap();
  function loadOriginal(image) {
    const url = new URL(image.dataset.originalSrc, location.href);
    url.searchParams.set('retry', String(Date.now()));
    image.removeAttribute('srcset');
    image.src = url.href;
  }
  document.addEventListener('error', event => {
    const image = event.target;
    if (!(image instanceof HTMLImageElement) || !image.dataset.originalSrc) return;
    let state = imageStates.get(image);
    if (!state) { state = { retried: false, notice: null, timer: null }; imageStates.set(image, state); }
    if (!state.retried) {
      state.retried = true;
      state.timer = setTimeout(() => loadOriginal(image), 350);
      return;
    }
    if (state.notice) return;
    const notice = document.createElement('p');
    notice.className = 'image-error';
    notice.setAttribute('role', 'status');
    notice.append('Photo couldn’t load. ');
    const retry = document.createElement('button');
    retry.type = 'button';
    retry.textContent = 'Retry photo';
    retry.addEventListener('click', () => {
      notice.remove(); state.notice = null;
      loadOriginal(image);
    });
    notice.append(retry);
    state.notice = notice;
    (image.closest('figure, article, .pub-image, aside') || image.parentElement).append(notice);
  }, true);
  document.addEventListener('load', event => {
    const state = imageStates.get(event.target);
    if (state) { clearTimeout(state.timer); state.notice?.remove(); state.notice = null; state.retried = false; }
  }, true);
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const key = 'gbhatt-theme';
  let preference;
  try { preference = localStorage.getItem(key); } catch {}
  const savedTheme = value => value === 'light' || value === 'dark';
  let button;
  function apply(theme) {
    root.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#211e1c' : '#faf7f2');
    if (button) {
      button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to night theme');
      button.title = button.getAttribute('aria-label');
      button.querySelector('.theme-label').textContent = theme === 'dark' ? 'Light' : 'Night';
    }
  }
  apply(savedTheme(preference) ? preference : system.matches ? 'dark' : 'light');
  system.addEventListener('change', () => {
    if (!savedTheme(preference)) apply(system.matches ? 'dark' : 'light');
  });
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) {
      preference = event.newValue;
      apply(savedTheme(preference) ? preference : system.matches ? 'dark' : 'light');
    }
  });
  document.addEventListener('DOMContentLoaded', () => {
    // Balance consecutive photos into justified rows without cropping or
    // changing their left-to-right order. Dimensions are known before loading.
    document.querySelectorAll('.gallery-grid').forEach(grid => {
      const figures = [...grid.querySelectorAll('.gallery-figure')];
      const ratios = figures.map(figure => {
        const image = figure.querySelector('img');
        return Number(image.getAttribute('width')) / Number(image.getAttribute('height'));
      });
      let previousWidth = 0;
      function fitRows() {
        const width = grid.getBoundingClientRect().width;
        if (!width || width === previousWidth) return;
        previousWidth = width;
        const gap = parseFloat(getComputedStyle(grid).columnGap);
        const target = width < 500 ? 220 : 250;
        const count = figures.length;
        const costs = Array(count + 1).fill(Infinity);
        const ends = Array(count);
        costs[count] = 0;
        for (let start = count - 1; start >= 0; start--) {
          let totalRatio = 0;
          for (let end = start; end < Math.min(count, start + 5); end++) {
            totalRatio += ratios[end];
            const height = (width - gap * (end - start)) / totalRatio;
            if (end > start && ratios.slice(start, end + 1).some(ratio => ratio * height < 125)) continue;
            const cost = (height - target) ** 2 + costs[end + 1];
            if (cost < costs[start]) { costs[start] = cost; ends[start] = end + 1; }
          }
        }
        for (let start = 0; start < count;) {
          const end = ends[start];
          const totalRatio = ratios.slice(start, end).reduce((sum, ratio) => sum + ratio, 0);
          // A lone final portrait should not become an oversized cover.
          const height = Math.min(width < 500 ? 560 : 360, (width - gap * (end - start - 1)) / totalRatio);
          for (let i = start; i < end; i++) {
            const photoWidth = Math.floor(height * ratios[i] * 100) / 100;
            figures[i].style.width = `${photoWidth}px`;
            figures[i].querySelector('img').sizes = `${Math.ceil(photoWidth)}px`;
          }
          start = end;
        }
        grid.classList.add('is-fitted');
      }
      fitRows();
      if ('ResizeObserver' in window) new ResizeObserver(fitRows).observe(grid);
      else window.addEventListener('resize', fitRows);
    });
    button = document.querySelector('.theme-toggle');
    if (button) {
      apply(root.dataset.theme);
      button.hidden = false;
      button.addEventListener('click', () => {
        preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem(key, preference); } catch {}
        apply(preference);
      });
    }
  // Retain the Google Sites heading bookmarks on the migrated domain.
  const headings = {'#h.p_NWAWRf3tSU-h':'#about','#h.p_AlR-Uz4qunNC':'#news','#h.jxikun9gant8':'#publications'};
  const target = headings[window.location.hash];
  if (target) {
    history.replaceState(null, '', target);
    document.querySelector(target)?.scrollIntoView();
  }
  });
})();
