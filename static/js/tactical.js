// Tactical JavaScript - Military-Grade Interactive Components

class TacticalUI {
    constructor() {
        this.init();
    }

    init() {
        this.initializeComponents();
        this.setupEventListeners();
        this.startAnimations();
        this.initializeTooltips();
        this.setupNotifications();
    }

    initializeComponents() {
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        // Initialize sidebar
        this.sidebar = new TacticalSidebar();
        
        // Initialize theme switcher
        this.themeSwitcher = new TacticalThemeSwitcher();
        
        // Initialize HUD clock
        this.hudClock = new TacticalHUDClock();
        
        // Initialize status monitor
        this.statusMonitor = new TacticalStatusMonitor();
    }

    setupEventListeners() {
        // Setup global click handlers
        document.addEventListener('click', this.handleGlobalClick.bind(this));
        
        // Setup keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
        
        // Setup scroll effects
        window.addEventListener('scroll', this.handleScroll.bind(this));
        
        // Setup resize handlers
        window.addEventListener('resize', this.handleResize.bind(this));
    }

    startAnimations() {
        // Add fade-in animations to elements
        this.addFadeInAnimations();
        
        // Start status indicator animations
        this.startStatusAnimations();
        
        // Initialize radar scan effect
        this.initializeRadarScan();
    }

    initializeTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    setupNotifications() {
        // Setup notification polling
        this.notificationPoller = new TacticalNotificationPoller();
    }

    handleGlobalClick(event) {
        // Handle dropdown toggles
        if (event.target.closest('[data-bs-toggle="dropdown"]')) {
            return;
        }

        // Close dropdowns when clicking outside
        const dropdowns = document.querySelectorAll('.dropdown-menu.show');
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(event.target)) {
                const dropdownInstance = bootstrap.Dropdown.getInstance(dropdown.previousElementSibling);
                if (dropdownInstance) {
                    dropdownInstance.hide();
                }
            }
        });
    }

    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + K for quick search
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            this.openQuickSearch();
        }

        // Escape to close modals
        if (event.key === 'Escape') {
            this.closeAllModals();
        }

        // Ctrl/Cmd + / for keyboard shortcuts help
        if ((event.ctrlKey || event.metaKey) && event.key === '/') {
            event.preventDefault();
            this.showKeyboardShortcuts();
        }
    }

    handleScroll() {
        // Handle navbar scroll effects
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }

        // Handle back to top button
        this.handleBackToTopButton();
    }

    handleResize() {
        // Handle responsive sidebar
        if (window.innerWidth <= 768) {
            this.sidebar.collapse();
        }
    }

    addFadeInAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.card-tactical, .stat-card, .btn-tactical').forEach(el => {
            observer.observe(el);
        });
    }

    startStatusAnimations() {
        // Animate status indicators
        document.querySelectorAll('.status-indicator').forEach(indicator => {
            indicator.classList.add('pulse');
        });
    }

    initializeRadarScan() {
        const radarElements = document.querySelectorAll('.radar-scan');
        radarElements.forEach(radar => {
            this.createRadarScanEffect(radar);
        });
    }

    createRadarScanEffect(radarElement) {
        const scan = document.createElement('div');
        scan.className = 'radar-scan-line';
        scan.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            width: 50%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--tactical-gold));
            transform-origin: left center;
            animation: radarScan 3s linear infinite;
        `;
        radarElement.appendChild(scan);

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes radarScan {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }

    openQuickSearch() {
        // Implement quick search modal
        console.log('Opening quick search...');
    }

    closeAllModals() {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }

    showKeyboardShortcuts() {
        // Show keyboard shortcuts help
        console.log('Showing keyboard shortcuts...');
    }

    handleBackToTopButton() {
        const backToTopButton = document.getElementById('backToTop');
        if (backToTopButton) {
            if (window.scrollY > 300) {
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.style.display = 'none';
            }
        }
    }

    // Utility methods
    showNotification(message, type = 'info', duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        const container = document.getElementById('toast-container');
        if (container) {
            container.appendChild(toast);
            const bsToast = new bootstrap.Toast(toast, { delay: duration });
            bsToast.show();

            toast.addEventListener('hidden.bs.toast', () => {
                toast.remove();
            });
        }
    }

    updateSystemStatus(status) {
        const statusElements = document.querySelectorAll('.system-status');
        statusElements.forEach(element => {
            element.textContent = status;
            element.className = `system-status status-indicator ${status}`;
        });
    }
}

// Tactical Sidebar Component
class TacticalSidebar {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.toggleButton = document.getElementById('sidebarToggle');
        this.collapseButton = document.getElementById('sidebarCollapse');
        this.init();
    }

    init() {
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', () => this.toggle());
        }
        if (this.collapseButton) {
            this.collapseButton.addEventListener('click', () => this.collapse());
        }
    }

    toggle() {
        if (this.sidebar) {
            this.sidebar.classList.toggle('collapsed');
        }
    }

    collapse() {
        if (this.sidebar) {
            this.sidebar.classList.add('collapsed');
        }
    }

    expand() {
        if (this.sidebar) {
            this.sidebar.classList.remove('collapsed');
        }
    }
}

// Tactical Theme Switcher
class TacticalThemeSwitcher {
    constructor() {
        this.themeToggle = document.getElementById('themeToggle');
        this.themeIcon = document.getElementById('theme-icon');
        this.init();
    }

    init() {
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
        
        // Load saved theme
        this.loadTheme();
    }

    toggleTheme() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        this.updateIcon(newTheme);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateIcon(savedTheme);
    }

    updateIcon(theme) {
        if (this.themeIcon) {
            this.themeIcon.setAttribute('data-lucide', theme === 'dark' ? 'moon' : 'sun');
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }
}

// Tactical HUD Clock
class TacticalHUDClock {
    constructor() {
        this.clockElements = {
            time: document.getElementById('currentTime'),
            date: document.getElementById('currentDate'),
            missionTime: document.getElementById('mission-time')
        };
        this.init();
    }

    init() {
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);
    }

    updateClock() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
        const dateStr = now.toLocaleDateString('en-US', { 
            day: '2-digit', 
            month: 'short', 
            year: 'numeric' 
        }).toUpperCase();
        const missionTimeStr = now.toISOString().split('T')[1].split('.')[0] + 'Z';

        if (this.clockElements.time) {
            this.clockElements.time.textContent = timeStr;
        }
        if (this.clockElements.date) {
            this.clockElements.date.textContent = dateStr;
        }
        if (this.clockElements.missionTime) {
            this.clockElements.missionTime.textContent = missionTimeStr;
        }
    }
}

// Tactical Status Monitor
class TacticalStatusMonitor {
    constructor() {
        this.statusUrl = '/api/system/status/';
        this.init();
    }

    init() {
        this.checkStatus();
        setInterval(() => this.checkStatus(), 30000); // Check every 30 seconds
    }

    async checkStatus() {
        try {
            const response = await fetch(this.statusUrl);
            const data = await response.json();
            this.updateStatusDisplay(data);
        } catch (error) {
            console.error('Error checking system status:', error);
        }
    }

    updateStatusDisplay(data) {
        // Update system status indicators
        const statusBadge = document.querySelector('.system-status-badge');
        if (statusBadge) {
            statusBadge.textContent = data.status || 'UNKNOWN';
            statusBadge.className = `badge bg-${data.status === 'OPERATIONAL' ? 'success' : 'warning'}`;
        }

        // Update readiness percentage
        const readinessBar = document.querySelector('.readiness-progress');
        if (readinessBar) {
            readinessBar.style.width = `${data.readiness || 0}%`;
            readinessBar.textContent = `${data.readiness || 0}%`;
        }
    }
}

// Tactical Notification Poller
class TacticalNotificationPoller {
    constructor() {
        this.notificationUrl = '/api/notifications/';
        this.pollInterval = 10000; // 10 seconds
        this.init();
    }

    init() {
        this.pollNotifications();
        setInterval(() => this.pollNotifications(), this.pollInterval);
    }

    async pollNotifications() {
        try {
            const response = await fetch(this.notificationUrl);
            const data = await response.json();
            this.updateNotificationDisplay(data);
        } catch (error) {
            console.error('Error polling notifications:', error);
        }
    }

    updateNotificationDisplay(data) {
        // Update notification badge
        const badge = document.querySelector('.notification-badge');
        if (badge && data.unread_count > 0) {
            badge.textContent = data.unread_count;
            badge.style.display = 'inline-block';
        } else if (badge) {
            badge.style.display = 'none';
        }

        // Update notification dropdown
        const dropdown = document.querySelector('.notifications-dropdown');
        if (dropdown && data.recent_notifications) {
            this.renderNotifications(dropdown, data.recent_notifications);
        }
    }

    renderNotifications(container, notifications) {
        const list = container.querySelector('.dropdown-menu');
        if (!list) return;

        let html = '';
        notifications.forEach(notification => {
            html += `
                <a class="dropdown-item ${!notification.is_read ? 'unread' : ''}" href="${notification.link || '#'}">
                    <div class="d-flex justify-content-between">
                        <span>${notification.message}</span>
                        <small class="text-muted">${notification.created_at}</small>
                    </div>
                </a>
            `;
        });

        list.innerHTML = html || '<span class="dropdown-item text-muted">No notifications</span>';
    }
}

// Initialize Tactical UI when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.tacticalUI = new TacticalUI();
});

// Export for global access
window.TacticalUI = TacticalUI;
