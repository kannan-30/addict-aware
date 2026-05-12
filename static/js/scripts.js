/**
 * Antigravity — Addict Aware
 * Client-Side JavaScript
 * Animations, interactions, and UI enhancements
 */

// ========================================
// NAVBAR SCROLL EFFECT
// ========================================
(function () {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    // Mobile nav toggle
    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            const links = document.querySelector('.nav-links');
            if (links) {
                links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
                links.style.flexDirection = 'column';
                links.style.position = 'absolute';
                links.style.top = '64px';
                links.style.right = '20px';
                links.style.background = 'rgba(15,23,42,0.95)';
                links.style.padding = '20px';
                links.style.borderRadius = '12px';
                links.style.backdropFilter = 'blur(20px)';
                links.style.border = '1px solid rgba(148,163,184,0.12)';
            }
        });
    }
})();

// ========================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ========================================
// PASSWORD TOGGLE
// ========================================
function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    if (input) {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        const icon = btn.querySelector('i');
        if (icon) {
            icon.className = isPassword ? 'bi bi-eye-slash' : 'bi bi-eye';
        }
    }
}

// ========================================
// AUTO-DISMISS FLASH MESSAGES
// ========================================
(function () {
    const flashContainer = document.getElementById('flashContainer');
    if (flashContainer) {
        setTimeout(() => {
            flashContainer.querySelectorAll('.flash-alert').forEach((alert, i) => {
                setTimeout(() => {
                    alert.style.transition = 'all 0.4s ease';
                    alert.style.opacity = '0';
                    alert.style.transform = 'translateX(60px)';
                    setTimeout(() => alert.remove(), 400);
                }, i * 200);
            });
        }, 4000);
    }
})();

// ========================================
// SCROLL REVEAL ANIMATION
// ========================================
(function () {
    const animateElements = document.querySelectorAll('.feature-card, .hiw-step, .tip-card');
    if (animateElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    animateElements.forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${i * 0.08}s`;
        observer.observe(el);
    });
})();

// ========================================
// HERO PARTICLES (subtle floating dots)
// ========================================
(function () {
    const container = document.getElementById('heroParticles');
    if (!container) return;

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: rgba(108, 99, 255, ${Math.random() * 0.3 + 0.1});
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation: particleFloat ${Math.random() * 8 + 6}s ease-in-out infinite;
            animation-delay: ${Math.random() * 4}s;
        `;
        container.appendChild(particle);
    }

    // Add particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
            25% { transform: translate(${Math.random() * 40 - 20}px, -30px) scale(1.2); opacity: 0.6; }
            50% { transform: translate(${Math.random() * 60 - 30}px, -50px) scale(0.8); opacity: 0.4; }
            75% { transform: translate(${Math.random() * 40 - 20}px, -20px) scale(1.1); opacity: 0.5; }
        }
    `;
    document.head.appendChild(style);
})();

// ========================================
// DARK/LIGHT THEME TOGGLE
// ========================================
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme');
    html.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark');
    localStorage.setItem('theme', html.getAttribute('data-theme'));
}

// Load saved theme
(function () {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    }
})();

// ========================================
// FORM VALIDATION FEEDBACK
// ========================================
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('blur', function () {
        if (this.required && !this.value.trim()) {
            this.style.borderColor = '#FF6B81';
        } else {
            this.style.borderColor = '';
        }
    });

    input.addEventListener('focus', function () {
        this.style.borderColor = '';
    });
});

console.log('%c◈ Addict Aware', 'color: #6C63FF; font-size: 16px; font-weight: bold;');
console.log('%cDigital Wellness Platform', 'color: #00F5D4; font-size: 12px;');
