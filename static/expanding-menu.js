// Expanding Menu - Interactive Navigation
document.addEventListener('DOMContentLoaded', function() {
    // Get current page path
    const currentPath = window.location.pathname;
    
    // Find all menu links
    const menuLinks = document.querySelectorAll('.menu-link');
    
    // Set active state based on current path
    menuLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
        
        // Add click handler
        link.addEventListener('click', function(e) {
            // Remove active from all links
            menuLinks.forEach(l => l.classList.remove('active'));
            // Add active to clicked link
            this.classList.add('active');
        });
    });
    
    // Keyboard navigation
    menuLinks.forEach((link, index) => {
        link.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' && index < menuLinks.length - 1) {
                e.preventDefault();
                menuLinks[index + 1].focus();
            } else if (e.key === 'ArrowLeft' && index > 0) {
                e.preventDefault();
                menuLinks[index - 1].focus();
            }
        });
    });
});
