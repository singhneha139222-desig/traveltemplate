/* ============================================
   BromoRise Travel - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    Loader.init();
    Navigation.init();
    Carousels.init();
    ScrollAnimations.init();
    SmoothScroll.init();
    Forms.init();
});

/* ---------- Loader Module ---------- */
const Loader = {
    init() {
        const loader = document.getElementById('loader');
        if (!loader) return;
        
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }, 500);
        });
        
        // Fallback - hide loader after 3 seconds max
        setTimeout(() => {
            loader.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }, 3000);
    }
};

/* ---------- Navigation Module ---------- */
const Navigation = {
    init() {
        this.navbar = document.getElementById('navbar');
        this.navToggle = document.getElementById('navToggle');
        this.navMenu = document.getElementById('navMenu');
        
        if (!this.navbar) return;
        
        this.bindEvents();
        this.handleScroll();
    },
    
    bindEvents() {
        // Scroll event for navbar styling
        window.addEventListener('scroll', () => this.handleScroll());
        
        // Mobile menu toggle
        if (this.navToggle && this.navMenu) {
            this.navToggle.addEventListener('click', () => this.toggleMobileMenu());
            
            // Close menu when clicking a link
            this.navMenu.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', () => {
                    this.navMenu.classList.remove('active');
                    this.navToggle.classList.remove('active');
                });
            });
        }
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (this.navMenu && this.navMenu.classList.contains('active')) {
                if (!this.navMenu.contains(e.target) && !this.navToggle.contains(e.target)) {
                    this.navMenu.classList.remove('active');
                    this.navToggle.classList.remove('active');
                }
            }
        });
    },
    
    handleScroll() {
        const scrollY = window.scrollY;
        
        if (scrollY > 100) {
            this.navbar.classList.add('scrolled');
        } else {
            this.navbar.classList.remove('scrolled');
        }
    },
    
    toggleMobileMenu() {
        this.navMenu.classList.toggle('active');
        this.navToggle.classList.toggle('active');
    }
};

/* ---------- Carousels Module ---------- */
const Carousels = {
    init() {
        this.initDestinationsCarousel();
        this.initTestimonialsCarousel();
    },
    
    initDestinationsCarousel() {
        const track = document.querySelector('.destinations-carousel .carousel-track');
        const prevBtn = document.getElementById('destPrev');
        const nextBtn = document.getElementById('destNext');
        
        if (!track || !prevBtn || !nextBtn) return;
        
        const cardWidth = 324; // card width + gap
        
        prevBtn.addEventListener('click', () => {
            track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
        });
        
        nextBtn.addEventListener('click', () => {
            track.scrollBy({ left: cardWidth, behavior: 'smooth' });
        });
        
        // Touch/swipe support
        this.addSwipeSupport(track);
    },
    
    initTestimonialsCarousel() {
        const track = document.getElementById('testimonialsTrack');
        const prevBtn = document.getElementById('testPrev');
        const nextBtn = document.getElementById('testNext');
        const dotsContainer = document.getElementById('testimonialsDots');
        
        if (!track || !prevBtn || !nextBtn) return;
        
        const cards = track.querySelectorAll('.testimonial-card');
        const cardWidth = 430; // card width + gap
        let currentIndex = 0;
        
        // Create dots
        if (dotsContainer) {
            cards.forEach((_, index) => {
                const dot = document.createElement('div');
                dot.classList.add('dot');
                if (index === 0) dot.classList.add('active');
                dot.addEventListener('click', () => goToSlide(index));
                dotsContainer.appendChild(dot);
            });
        }
        
        const updateDots = () => {
            if (!dotsContainer) return;
            dotsContainer.querySelectorAll('.dot').forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        };
        
        const goToSlide = (index) => {
            currentIndex = Math.max(0, Math.min(index, cards.length - 1));
            track.scrollTo({ left: currentIndex * cardWidth, behavior: 'smooth' });
            updateDots();
        };
        
        prevBtn.addEventListener('click', () => goToSlide(currentIndex - 1));
        nextBtn.addEventListener('click', () => goToSlide(currentIndex + 1));
        
        // Update current index on scroll
        track.addEventListener('scroll', () => {
            currentIndex = Math.round(track.scrollLeft / cardWidth);
            updateDots();
        });
        
        // Touch/swipe support
        this.addSwipeSupport(track);
        
        // Auto-play (optional)
        // setInterval(() => goToSlide((currentIndex + 1) % cards.length), 5000);
    },
    
    addSwipeSupport(element) {
        let startX, startScrollLeft;
        
        element.addEventListener('touchstart', (e) => {
            startX = e.touches[0].pageX;
            startScrollLeft = element.scrollLeft;
        });
        
        element.addEventListener('touchmove', (e) => {
            if (!startX) return;
            const x = e.touches[0].pageX;
            const walk = (startX - x) * 1.5;
            element.scrollLeft = startScrollLeft + walk;
        });
        
        element.addEventListener('touchend', () => {
            startX = null;
        });
    }
};

/* ---------- Scroll Animations Module ---------- */
const ScrollAnimations = {
    init() {
        this.animatedElements = document.querySelectorAll('.scroll-animate, [class*="animate-"]');
        
        if (!this.animatedElements.length) return;
        
        // Create intersection observer
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Add animation class for elements that need it
                    if (entry.target.dataset.animation) {
                        entry.target.classList.add(entry.target.dataset.animation);
                    }
                }
            });
        }, observerOptions);
        
        // Observe all animated elements
        this.animatedElements.forEach(el => observer.observe(el));
        
        // Parallax effect for hero section
        this.initParallax();
    },
    
    initParallax() {
        const heroBg = document.querySelector('.hero-bg');
        if (!heroBg) return;
        
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            if (scrollY < window.innerHeight) {
                heroBg.style.transform = `translateY(${scrollY * 0.3}px)`;
            }
        });
    }
};

/* ---------- Smooth Scroll Module ---------- */
const SmoothScroll = {
    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (!target) return;
                
                e.preventDefault();
                
                const navbarHeight = document.getElementById('navbar')?.offsetHeight || 80;
                const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            });
        });
    }
};

/* ---------- Forms Module ---------- */
const Forms = {
    init() {
        this.initFormValidation();
        this.initDatePicker();
    },
    
    initFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
                let isValid = true;
                
                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        isValid = false;
                        this.showError(input, 'This field is required');
                    } else if (input.type === 'email' && !this.isValidEmail(input.value)) {
                        isValid = false;
                        this.showError(input, 'Please enter a valid email');
                    } else {
                        this.clearError(input);
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                }
            });
            
            // Real-time validation
            form.querySelectorAll('input, select, textarea').forEach(input => {
                input.addEventListener('blur', () => {
                    if (input.hasAttribute('required') && !input.value.trim()) {
                        this.showError(input, 'This field is required');
                    } else if (input.type === 'email' && input.value && !this.isValidEmail(input.value)) {
                        this.showError(input, 'Please enter a valid email');
                    } else {
                        this.clearError(input);
                    }
                });
                
                input.addEventListener('input', () => {
                    this.clearError(input);
                });
            });
        });
    },
    
    initDatePicker() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        
        dateInputs.forEach(input => {
            // Set min date to today
            const today = new Date().toISOString().split('T')[0];
            input.setAttribute('min', today);
        });
    },
    
    showError(input, message) {
        input.classList.add('error');
        
        let errorEl = input.parentElement.querySelector('.error-message');
        if (!errorEl) {
            errorEl = document.createElement('span');
            errorEl.classList.add('error-message');
            input.parentElement.appendChild(errorEl);
        }
        errorEl.textContent = message;
    },
    
    clearError(input) {
        input.classList.remove('error');
        const errorEl = input.parentElement.querySelector('.error-message');
        if (errorEl) {
            errorEl.remove();
        }
    },
    
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
};

/* ---------- Additional Utilities ---------- */

// Counter animation for stats
const animateCounter = (element, target, duration = 2000) => {
    let start = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
};

// Lazy load images
const lazyLoadImages = () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
};

// Debounce utility
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Throttle utility
const throttle = (func, limit) => {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};
