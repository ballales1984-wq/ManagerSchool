/**
 * RESPONSIVE JAVASCRIPT - ManagerSchool
 * Gestione interattività responsive
 */

// ========================================
// NAVIGATION MOBILE
// ========================================

function initMobileNav() {
    const toggler = document.querySelector('.navbar-toggler');
    const nav = document.querySelector('.navbar-nav');
    
    if (toggler && nav) {
        toggler.addEventListener('click', function() {
            nav.classList.toggle('mobile-active');
            
            // Toggle icon
            const icon = toggler.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-times');
            }
        });
    }
}

// ========================================
// RESPONSIVE TABLE HANDLER
// ========================================

function makeTablesResponsive() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const headers = Array.from(table.querySelectorAll('thead th'));
        
        if (headers.length > 0) {
            const tbody = table.querySelector('tbody');
            if (tbody) {
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                rows.forEach(row => {
                    const cells = Array.from(row.querySelectorAll('td'));
                    cells.forEach((cell, index) => {
                        if (index < headers.length) {
                            cell.setAttribute('data-label', headers[index].textContent);
                        }
                    });
                });
            }
        }
    });
}

// ========================================
// TOUCH GESTURES
// ========================================

function initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', function(e) {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        
        // Swipe left/right per navigation
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            if (deltaX > 0) {
                // Swipe right
                handleSwipeRight();
            } else {
                // Swipe left
                handleSwipeLeft();
            }
        }
    });
}

function handleSwipeRight() {
    const nav = document.querySelector('.navbar-nav');
    if (nav && window.innerWidth <= 768) {
        nav.classList.add('mobile-active');
    }
}

function handleSwipeLeft() {
    const nav = document.querySelector('.navbar-nav');
    if (nav && window.innerWidth <= 768) {
        nav.classList.remove('mobile-active');
    }
}

// ========================================
// VIEWPORT RESIZE HANDLER
// ========================================

function handleResize() {
    const isMobile = window.innerWidth <= 768;
    
    // Aggiorna classi responsive
    document.body.classList.toggle('mobile-view', isMobile);
    document.body.classList.toggle('desktop-view', !isMobile);
    
    // Chiudi menu mobile se si torna a desktop
    if (!isMobile) {
        const nav = document.querySelector('.navbar-nav');
        if (nav) {
            nav.classList.remove('mobile-active');
        }
    }
}

// ========================================
// LAZY LOADING IMAGES
// ========================================

function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// ========================================
// MODAL RESPONSIVE
// ========================================

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Previeni scroll
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Chiudi modal cliccando fuori
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ========================================
// LOADING STATES
// ========================================

function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="spinner"><i class="fas fa-spinner fa-spin"></i></div>';
    }
}

function hideLoading(element) {
    if (element) {
        element.innerHTML = '';
    }
}

// ========================================
// SCROLL TO TOP
// ========================================

function initScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-to-top';
    scrollButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #667eea;
        color: white;
        border: none;
        cursor: pointer;
        display: none;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    document.body.appendChild(scrollButton);
    
    // Mostra/nascondi in base allo scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });
    
    // Scroll to top
    scrollButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ========================================
// RESPONSIVE CHARTS
// ========================================

function resizeCharts() {
    window.dispatchEvent(new Event('resize'));
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔥 ManagerSchool - Responsive JS inizializzato');
    
    // Init components
    initMobileNav();
    makeTablesResponsive();
    initTouchGestures();
    initLazyLoading();
    initScrollToTop();
    
    // Resize handler
    window.addEventListener('resize', handleResize);
    handleResize(); // Chiama iniziale
    
    // Resize charts
    window.addEventListener('resize', function() {
        clearTimeout(window.chartResizeTimeout);
        window.chartResizeTimeout = setTimeout(resizeCharts, 250);
    });
});

// ========================================
// EXPORTS
// ========================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showModal,
        hideModal,
        showLoading,
        hideLoading,
        resizeCharts
    };
}

