// PWA Installation Handler for IntervYou
let deferredPrompt;
let installButton;

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
  initPWA();
});

function initPWA() {
  // Register service worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js')
      .then((registration) => {
        console.log('✅ Service Worker registered:', registration.scope);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New service worker available
              showUpdateNotification();
            }
          });
        });
      })
      .catch((error) => {
        console.error('❌ Service Worker registration failed:', error);
      });
  }

  // Handle install prompt
  window.addEventListener('beforeinstallprompt', (e) => {
    console.log('💾 Install prompt available');
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
  });

  // Track installation
  window.addEventListener('appinstalled', () => {
    console.log('✅ PWA installed successfully');
    deferredPrompt = null;
    hideInstallButton();
    showToast('✅ App installed! You can now use IntervYou offline.');
  });

  // Check if already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('✅ Running as installed PWA');
    hideInstallButton();
  }
}

function showInstallButton() {
  // Create install button if it doesn't exist
  if (!installButton) {
    installButton = document.createElement('button');
    installButton.id = 'pwa-install-btn';
    installButton.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      <span>Install App</span>
    `;
    installButton.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 50px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.3s ease;
      animation: slideIn 0.5s ease;
    `;
    
    // Add hover effect
    installButton.addEventListener('mouseenter', () => {
      installButton.style.transform = 'translateY(-2px)';
      installButton.style.boxShadow = '0 6px 25px rgba(102, 126, 234, 0.5)';
    });
    
    installButton.addEventListener('mouseleave', () => {
      installButton.style.transform = 'translateY(0)';
      installButton.style.boxShadow = '0 4px 20px rgba(102, 126, 234, 0.4)';
    });
    
    installButton.addEventListener('click', installPWA);
    document.body.appendChild(installButton);
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideIn {
        from {
          transform: translateX(200px);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }
    `;
    document.head.appendChild(style);
  }
  
  installButton.style.display = 'flex';
}

function hideInstallButton() {
  if (installButton) {
    installButton.style.display = 'none';
  }
}

async function installPWA() {
  if (!deferredPrompt) {
    return;
  }

  // Show install prompt
  deferredPrompt.prompt();
  
  // Wait for user response
  const { outcome } = await deferredPrompt.userChoice;
  console.log(`User response: ${outcome}`);
  
  if (outcome === 'accepted') {
    console.log('✅ User accepted install');
  } else {
    console.log('❌ User dismissed install');
  }
  
  deferredPrompt = null;
  hideInstallButton();
}

function showUpdateNotification() {
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    background: white;
    padding: 16px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    gap: 12px;
    max-width: 350px;
    animation: slideDown 0.3s ease;
  `;
  
  notification.innerHTML = `
    <div style="flex: 1;">
      <div style="font-weight: 600; margin-bottom: 4px;">Update Available</div>
      <div style="font-size: 14px; color: #666;">A new version of IntervYou is ready!</div>
    </div>
    <button id="update-btn" style="
      background: #667eea;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
    ">Update</button>
  `;
  
  document.body.appendChild(notification);
  
  document.getElementById('update-btn').addEventListener('click', () => {
    window.location.reload();
  });
  
  // Auto-remove after 10 seconds
  setTimeout(() => {
    notification.remove();
  }, 10000);
}

function showToast(message) {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    z-index: 10000;
    animation: fadeIn 0.3s ease;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Add CSS animations
const animationStyles = document.createElement('style');
animationStyles.textContent = `
  @keyframes slideDown {
    from {
      transform: translateY(-100px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
  }
`;
document.head.appendChild(animationStyles);

// Network status indicator
window.addEventListener('online', () => {
  showToast('✅ Back online!');
});

window.addEventListener('offline', () => {
  showToast('📡 You\'re offline. Some features may be limited.');
});
