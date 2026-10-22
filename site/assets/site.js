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
