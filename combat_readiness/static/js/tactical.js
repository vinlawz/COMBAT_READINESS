/**
 * Tactical UI Components for Combat Readiness System
 * This file contains all the interactive elements and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initBackToTop();
    initTooltips();
    initSidebar();
    initRadar();
    initSystemAlerts();
    
    // Add animation to stat cards on scroll
    animateOnScroll();
    
    // Listen for theme changes
    initThemeSwitcher();
});

/**
 * Initialize back to top button
 */
function initBackToTop() {
    const backToTopButton = document.getElementById('backToTop');
    
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            trigger: 'hover'
        });
    });
}

/**
 * Initialize sidebar functionality with collapsible behavior and mobile support
 */
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebarToggler = document.getElementById('sidebarToggler');
    const mainContent = document.getElementById('mainContent');
    const profileToggle = document.querySelector('.profile-toggle');
    const profileMenu = document.querySelector('.profile-menu');
    
    // Check for saved sidebar state
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    // Initialize sidebar state
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
    }
    
    // Toggle sidebar collapse
    function toggleSidebar() {
        const isCollapsing = !sidebar.classList.contains('collapsed');
        sidebar.classList.toggle('collapsed');
        
        // Update the toggle button icon
        const icon = sidebarCollapse.querySelector('.icon');
        if (isCollapsing) {
            icon.setAttribute('data-lucide', 'chevron-right');
        } else {
            icon.setAttribute('data-lucide', 'chevron-left');
        }
        lucide.createIcons();
        
        // Save state to localStorage
        localStorage.setItem('sidebarCollapsed', isCollapsing);
    }
    
    // Toggle profile menu
    function toggleProfileMenu() {
        profileMenu.classList.toggle('active');
        const icon = profileToggle.querySelector('i');
        if (profileMenu.classList.contains('active')) {
            icon.setAttribute('data-lucide', 'chevron-up');
        } else {
            icon.setAttribute('data-lucide', 'chevron-down');
        }
        lucide.createIcons();
    }
    
    // Event listeners
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', toggleSidebar);
    }
    
    if (sidebarToggler) {
        sidebarToggler.addEventListener('click', () => {
            sidebar.classList.toggle('show');
        });
    }
    
    if (profileToggle && profileMenu) {
        profileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleProfileMenu();
        });
    }
    
    // Close profile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (profileMenu && profileMenu.classList.contains('active') && 
            !e.target.closest('.user-profile')) {
            toggleProfileMenu();
        }
    });
    
    // Handle window resize for responsive behavior
    function handleResize() {
        if (window.innerWidth <= 992) {
            sidebar.classList.remove('collapsed');
            sidebar.classList.remove('show');
        } else {
            // Restore collapsed state on desktop
            if (isCollapsed) {
                sidebar.classList.add('collapsed');
            }
        }
    }
    
    // Add resize listener
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial check
    
    // Close sidebar when clicking on a nav link on mobile
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 992) {
                sidebar.classList.remove('show');
            }
        });
    });
}

/**
 * Initialize radar animation with sweep effect
 */
function initRadar() {
    const radarElements = document.querySelectorAll('.radar-scan');
    
    radarElements.forEach((radar, index) => {
        // Create radar scan effect
        const scanLine = document.createElement('div');
        scanLine.className = 'radar-scan-line';
        radar.appendChild(scanLine);
        
        // Add radar circle guides
        const circles = [0.3, 0.6, 0.9]; // Relative sizes for concentric circles
        circles.forEach(size => {
            const circle = document.createElement('div');
            circle.className = 'radar-circle';
            circle.style.width = `${size * 100}%`;
            circle.style.height = `${size * 100}%`;
            circle.style.border = '1px solid rgba(199, 255, 65, 0.2)';
            circle.style.borderRadius = '50%';
            circle.style.position = 'absolute';
            circle.style.top = '50%';
            circle.style.left = '50%';
            circle.style.transform = 'translate(-50%, -50%)';
            radar.insertBefore(circle, radar.firstChild);
        });
        
        // Add crosshairs
        const crosshair = document.createElement('div');
        crosshair.className = 'radar-crosshair';
        crosshair.style.position = 'absolute';
        crosshair.style.top = '0';
        crosshair.style.left = '0';
        crosshair.style.width = '100%';
        crosshair.style.height = '100%';
        crosshair.style.background = `
            linear-gradient(90deg, transparent calc(50% - 0.5px), rgba(199, 255, 65, 0.2) calc(50% - 0.5px), rgba(199, 255, 65, 0.2) calc(50% + 0.5px), transparent calc(50% + 0.5px)),
            linear-gradient(0deg, transparent calc(50% - 0.5px), rgba(199, 255, 65, 0.2) calc(50% - 0.5px), rgba(199, 255, 65, 0.2) calc(50% + 0.5px), transparent calc(50% + 0.5px))
        `;
        radar.insertBefore(crosshair, radar.firstChild);
        
        // Start with random blips
        for (let i = 0; i < 5; i++) {
            setTimeout(() => createRadarBlip(radar), Math.random() * 2000);
        }
        
        // Continue adding random blips
        setInterval(() => {
            if (Math.random() > 0.7) { // 30% chance to create a new blip
                createRadarBlip(radar);
            }
        }, 2000);
    });
    
    // Initialize particle effects
    initParticles();
}

/**
 * Create a radar blip at a random position
 */
function createRadarBlip(radar) {
    const blip = document.createElement('div');
    blip.className = 'radar-blip';
    blip.style.position = 'absolute';
    
    // Random position within radar
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * 0.8 + 0.1; // Keep away from edges
    const x = 50 + Math.cos(angle) * distance * 40;
    const y = 50 + Math.sin(angle) * distance * 40;
    
    blip.style.left = `${x}%`;
    blip.style.top = `${y}%`;
    blip.style.transform = 'translate(-50%, -50%)';
    
    // Random size and opacity for variety
    const size = Math.random() * 8 + 4;
    const opacity = Math.random() * 0.6 + 0.4;
    blip.style.width = `${size}px`;
    blip.style.height = `${size}px`;
    blip.style.opacity = opacity;
    
    // Add pulsing animation
    blip.style.animation = `pulse ${Math.random() * 2 + 1}s infinite`;
    
    radar.appendChild(blip);
    
    // Remove blip after animation
    setTimeout(() => {
        blip.style.opacity = '0';
        blip.style.transition = 'opacity 0.5s';
        setTimeout(() => blip.remove(), 500);
    }, 3000);
}

/**
 * Initialize particle effects for the tactical background
 */
function initParticles() {
    const container = document.querySelector('.main-content');
    if (!container) return;
    
    // Create particle container
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'tactical-particles';
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.pointerEvents = 'none';
    particlesContainer.style.zIndex = '-1';
    particlesContainer.style.overflow = 'hidden';
    
    // Add to the beginning of the main content
    container.insertBefore(particlesContainer, container.firstChild);
    
    // Create particles
    const particleCount = 50;
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
    
    // Add CSS for particles if not already added
    if (!document.getElementById('tactical-particles-style')) {
        const style = document.createElement('style');
        style.id = 'tactical-particles-style';
        style.textContent = `
            @keyframes float {
                0%, 100% { transform: translate(0, 0) rotate(0deg); }
                25% { transform: translate(5px, 5px) rotate(1deg); }
                50% { transform: translate(0, 10px) rotate(0deg); }
                75% { transform: translate(-5px, 5px) rotate(-1deg); }
            }
            
            .tactical-particle {
                position: absolute;
                background: rgba(199, 255, 65, 0.05);
                border-radius: 50%;
                pointer-events: none;
                animation: float 15s infinite ease-in-out;
                filter: blur(0.5px);
            }
            
            .radar-scan {
                position: relative;
                border: 1px solid rgba(199, 255, 65, 0.3);
                border-radius: 50%;
                overflow: hidden;
            }
            
            .radar-scan-line {
                position: absolute;
                top: 0;
                left: 50%;
                width: 1px;
                height: 100%;
                background: linear-gradient(to bottom, 
                    transparent, 
                    rgba(199, 255, 65, 0.3), 
                    transparent);
                transform-origin: top;
                animation: radar-sweep 4s infinite linear;
            }
            
            .radar-blip {
                position: absolute;
                background: #c7ff41;
                border-radius: 50%;
                transform: translate(-50%, -50%);
                box-shadow: 0 0 10px 2px rgba(199, 255, 65, 0.7);
            }
            
            @keyframes radar-sweep {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes pulse {
                0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
                50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Create a single particle with random properties
 */
function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'tactical-particle';
    
    // Random size between 1px and 4px
    const size = Math.random() * 3 + 1;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    
    // Random position
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    
    // Random animation duration and delay
    const duration = Math.random() * 20 + 10; // 10-30 seconds
    const delay = Math.random() * -20; // Start at random point in animation
    particle.style.animationDuration = `${duration}s`;
    particle.style.animationDelay = `${delay}s`;
    
    // Random opacity
    particle.style.opacity = Math.random() * 0.1 + 0.05;
    
    container.appendChild(particle);
    
    // Make particles move around randomly
    setInterval(() => {
        if (Math.random() > 0.98) { // 2% chance to change direction
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            particle.style.transition = 'all 10s linear';
            particle.style.left = `${x}%`;
            particle.style.top = `${y}%`;
        }
    }, 1000);
}

/**
 * Create a radar blip animation
 */
function createRadarBlip(radar) {
    const blip = document.createElement('div');
    blip.className = 'radar-blip';
    
    // Random position within radar
    const posX = Math.random() * 80 + 10; // 10% to 90%
    const posY = Math.random() * 80 + 10; // 10% to 90%
    
    blip.style.left = `${posX}%`;
    blip.style.top = `${posY}%`;
    
    // Random delay for the blip to appear
    const delay = Math.random() * 2000;
    
    setTimeout(() => {
        radar.appendChild(blip);
        
        // Remove blip after animation
        setTimeout(() => {
            if (blip.parentNode === radar) {
                radar.removeChild(blip);
            }
        }, 1000);
    }, delay);
}

/**
 * Initialize system alerts
 */
function initSystemAlerts() {
    // Check for critical system status
    checkSystemStatus();
    
    // Check status every 5 minutes
    setInterval(checkSystemStatus, 300000);
}

/**
 * Check system status and show alerts if needed
 */
async function checkSystemStatus() {
    try {
        // Example: Fetch system status from API
        // const response = await fetch('/api/system/status/');
        // const data = await response.json();
        
        // For demo purposes, we'll simulate a response
        const data = {
            status: 'operational',
            alerts: [
                // Uncomment to simulate an alert
                // { type: 'warning', message: 'Low inventory: Ammunition at 15%' }
            ]
        };
        
        // Process alerts
        if (data.alerts && data.alerts.length > 0) {
            showSystemAlert(data.alerts[0]);
        }
    } catch (error) {
        console.error('Error checking system status:', error);
    }
}

/**
 * Show a system alert
 */
function showSystemAlert(alert) {
    const alertBanner = document.getElementById('systemAlert');
    const alertMessage = document.getElementById('alertMessage');
    
    if (alertBanner && alertMessage) {
        // Update alert content
        alertMessage.textContent = `SYSTEM ALERT: ${alert.message}`;
        
        // Set alert type class
        alertBanner.className = 'system-alert';
        alertBanner.classList.add(`alert-${alert.type}`);
        
        // Show the alert
        alertBanner.style.display = 'block';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            alertBanner.style.display = 'none';
        }, 10000);
    }
}

/**
 * Initialize theme switcher
 */
function initThemeSwitcher() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        // Check for saved theme preference or use system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Set initial theme
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
            updateThemeIcon(savedTheme === 'dark');
        } else {
            const theme = systemPrefersDark ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            updateThemeIcon(systemPrefersDark);
        }
        
        // Toggle theme on button click
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Update theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update icon
            updateThemeIcon(newTheme === 'dark');
        });
    }
}

/**
 * Update theme icon based on current theme
 */
function updateThemeIcon(isDark) {
    const themeIcon = document.getElementById('themeToggle')?.querySelector('i');
    if (themeIcon) {
        themeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}

/**
 * Animate elements when they come into view
 */
function animateOnScroll() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
}

/**
 * Show a toast notification
 */
function showToast(message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) return;
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Get icon based on type
    let icon = 'info-circle';
    if (type === 'success') icon = 'check-circle';
    else if (type === 'danger') icon = 'exclamation-circle';
    else if (type === 'warning') icon = 'exclamation-triangle';
    
    // Set toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${icon} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: duration
    });
    
    bsToast.show();
    
    // Remove from DOM after hiding
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
    
    return toast;
}

// Export functions for use in other modules
window.TacticalUI = {
    showToast,
    showSystemAlert,
    checkSystemStatus
};

// Show a welcome message when the page loads
window.addEventListener('load', () => {
    // Uncomment to show a welcome toast
    // showToast('Combat Readiness System initialized', 'success');
});
