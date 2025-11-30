// Global utilities: theme toggle, toast, confetti, and modal
(function () {
  // ---------------------------
  // THEME HANDLING
  // ---------------------------
  function setThemeIcon(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }

  const saved =
    localStorage.getItem('theme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setThemeIcon(saved);

  window.toggleTheme = function () {
    const cur = document.documentElement.getAttribute('data-theme');
    const next = cur === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', next);
    setThemeIcon(next);
  };

  // ---------------------------
  // TOAST NOTIFICATION
  // ---------------------------
  window.showToast = function (msg) {
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2200);
  };

  // ---------------------------
  // MINIMAL CONFETTI EFFECT 🎉
  // ---------------------------
  window.runConfetti = function () {
    for (let i = 0; i < 40; i++) {
      const d = document.createElement('div');
      d.style.position = 'fixed';
      d.style.left = Math.random() * 100 + '%';
      d.style.top = '-10px';
      d.style.width = '8px';
      d.style.height = '8px';
      d.style.borderRadius = '50%';
      d.style.background = ['#f59e0b', '#ef4444', '#06b6d4', '#60a5fa'][
        Math.floor(Math.random() * 4)
      ];
      d.style.zIndex = 9999;
      document.body.appendChild(d);
      const target = window.innerHeight + 100;
      d.animate(
        [
          { transform: 'translateY(0)' },
          { transform: `translateY(${target}px)` }
        ],
        {
          duration: 1500 + Math.random() * 1000,
          iterations: 1
        }
      );
      setTimeout(() => d.remove(), 3000);
    }
  };

  // ---------------------------
  // SIMPLE MODAL
  // ---------------------------
  window.openModal = function (html) {
    const m = document.createElement('div');
    m.className = 'modal';
    m.innerHTML = `
      <div class="panel">
        ${html}
        <div style="text-align: right; margin-top: 12px">
          <button class="btn" onclick="this.closest('.modal').remove()">Close</button>
        </div>
      </div>`;
    document.body.appendChild(m);
  };
})();
