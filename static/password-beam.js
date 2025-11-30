// Password beam effect - interactive password visibility
document.addEventListener('DOMContentLoaded', function() {
    const root = document.documentElement;
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(passwordInput => {
        const wrapper = passwordInput.closest('.input-box');
        if (!wrapper) return;
        
        // Create eye button
        const eyeButton = document.createElement('button');
        eyeButton.type = 'button';
        eyeButton.className = 'password-eye';
        eyeButton.innerHTML = '<div class="eye"></div>';
        
        // Create beam element
        const beam = document.createElement('div');
        beam.className = 'password-beam';
        
        // Insert elements
        wrapper.style.position = 'relative';
        wrapper.appendChild(eyeButton);
        wrapper.appendChild(beam);
        
        let isShowingPassword = false;
        
        // Mouse move handler for beam rotation
        const handleMouseMove = (e) => {
            if (!isShowingPassword) return;
            
            const rect = beam.getBoundingClientRect();
            const mouseX = rect.right + (rect.width / 2);
            const mouseY = rect.top + (rect.height / 2);
            const rad = Math.atan2(mouseX - e.pageX, mouseY - e.pageY);
            const degrees = (rad * (20 / Math.PI) * -1) - 350;
            
            beam.style.transform = `translateY(-50%) rotate(${degrees}deg)`;
        };
        
        // Eye button click handler
        eyeButton.addEventListener('click', (e) => {
            e.preventDefault();
            isShowingPassword = !isShowingPassword;
            
            if (isShowingPassword) {
                document.body.classList.add('show-password');
                passwordInput.type = 'text';
                beam.classList.add('active');
                document.addEventListener('mousemove', handleMouseMove);
            } else {
                document.body.classList.remove('show-password');
                passwordInput.type = 'password';
                beam.classList.remove('active');
                document.removeEventListener('mousemove', handleMouseMove);
            }
            
            passwordInput.focus();
        });
    });
});
