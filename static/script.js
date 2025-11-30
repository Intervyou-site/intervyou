// static/script.js — robust delegated handler for auth panel toggles
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('authContainer');

  function setRegisterMode() {
    if (!container) return;
    container.classList.add('active');
  }
  function setLoginMode() {
    if (!container) return;
    container.classList.remove('active');
  }

  // Handle clicks delegated anywhere in document for links that toggle auth mode
  document.addEventListener('click', (e) => {
    // find nearest anchor
    const a = e.target.closest && e.target.closest('a');
    if (!a) return;

    // priority: if anchor has data-mode attribute, use it
    const mode = a.dataset.mode;
    if (mode === 'register') {
      e.preventDefault();
      setRegisterMode();
      history.replaceState(null, '', '?mode=register');
      return;
    }
    if (mode === 'login') {
      e.preventDefault();
      setLoginMode();
      history.replaceState(null, '', '?mode=login');
      return;
    }

    // fallback: anchors with these classes
    if (a.classList.contains('SignUpLink') || a.href.includes('?mode=register')) {
      e.preventDefault();
      setRegisterMode();
      history.replaceState(null, '', '?mode=register');
      return;
    }
    if (a.classList.contains('SignInLink') || a.href.includes('?mode=login')) {
      e.preventDefault();
      setLoginMode();
      history.replaceState(null, '', '?mode=login');
      return;
    }

    // not a toggle link -> let it behave normally
  });

  // On load: if URL contains ?mode=register open register panel
  try {
    const params = new URLSearchParams(window.location.search);
    if (params.get('mode') === 'register') setRegisterMode();
    else setLoginMode();
  } catch (err) {
    // ignore malformed URL
  }

  // Make Back/Forward keep the UI in sync
  window.addEventListener('popstate', () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('mode') === 'register') setRegisterMode();
    else setLoginMode();
  });
});


