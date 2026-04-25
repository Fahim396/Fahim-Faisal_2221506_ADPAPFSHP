/**
 * SmartHarvest — Main JavaScript
 * Handles navigation toggle, message auto-dismiss, and UI interactions.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Mobile Navigation Toggle ───────────────────────────────
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            // Animate hamburger
            this.classList.toggle('active');
        });

        // Close menu on link click (mobile)
        navMenu.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // ─── Auto-dismiss Messages ──────────────────────────────────
    const messages = document.querySelectorAll('.message');
    messages.forEach(function (msg, index) {
        setTimeout(function () {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(function () {
                msg.remove();
            }, 300);
        }, 4000 + (index * 500)); // Stagger dismissal
    });

    // ─── Navbar Scroll Effect ───────────────────────────────────
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 10) {
                navbar.style.boxShadow = '0 4px 6px -1px rgba(0,0,0,0.1)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }

    // ─── Animate Stat Cards on Scroll ───────────────────────────
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const animateOnScroll = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                animateOnScroll.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Animate cards, stats, and feature items
    const animatables = document.querySelectorAll(
        '.stat-card, .feature-card, .benefit-card, .action-card, .dashboard-card'
    );
    animatables.forEach(function (el, index) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.5s ease ' + (index * 0.08) + 's';
        animateOnScroll.observe(el);
    });

    // ─── Risk Factor Bar Animation ──────────────────────────────
    const factorBars = document.querySelectorAll('.factor-bar');
    factorBars.forEach(function (bar) {
        var score = parseFloat(bar.getAttribute('data-score'));
        if (!isNaN(score)) {
            // Set initial width to 0, then animate
            var targetWidth = Math.round(score * 100);
            bar.style.width = '0%';
            setTimeout(function () {
                bar.style.width = targetWidth + '%';
            }, 300);
        }
    });

    // ─── Chart Bar Animation ────────────────────────────────────
    const chartBars = document.querySelectorAll('.chart-bar');
    chartBars.forEach(function (bar) {
        var currentWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function () {
            bar.style.width = currentWidth;
        }, 500);
    });

    // ─── File Upload Preview ────────────────────────────────────
    const fileInput = document.getElementById('farm-pest-image');
    const uploadArea = document.getElementById('file-upload-area');

    if (fileInput && uploadArea) {
        fileInput.addEventListener('change', function () {
            var placeholder = uploadArea.querySelector('.upload-placeholder');
            if (this.files && this.files[0]) {
                var fileName = this.files[0].name;
                var fileSize = (this.files[0].size / 1024 / 1024).toFixed(2);
                placeholder.innerHTML =
                    '<span class="upload-icon">✅</span>' +
                    '<p>' + fileName + '</p>' +
                    '<span class="upload-hint">' + fileSize + ' MB</span>';
                uploadArea.style.borderColor = 'var(--primary-500)';
                uploadArea.style.background = 'var(--primary-50)';
            }
        });
    }

    // ─── Confidence Circle Animation ────────────────────────────
    const confidenceFill = document.querySelector('.confidence-fill');
    if (confidenceFill) {
        var value = parseFloat(confidenceFill.getAttribute('data-value'));
        if (!isNaN(value)) {
            var circumference = 2 * Math.PI * 50; // r=50
            var offset = circumference - (value * circumference);
            confidenceFill.style.strokeDasharray = circumference;
            confidenceFill.style.strokeDashoffset = circumference;
            setTimeout(function () {
                confidenceFill.style.transition = 'stroke-dashoffset 1.5s ease';
                confidenceFill.style.strokeDashoffset = offset;
            }, 300);
        }
    }
});
