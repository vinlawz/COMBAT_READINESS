document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    const currentTheme = localStorage.getItem('theme');
    const icon = document.getElementById('theme-icon');

    // Check for saved theme preference or use system preference
    if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (icon) icon.className = 'fas fa-sun';
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        if (icon) icon.className = 'fas fa-moon';
    }

    // Toggle theme when button is clicked
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Update theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            // Update icon
            if (icon) {
                icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
            
            // Dispatch custom event for any components that need to know about theme changes
            document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
        });
    }

    // Listen for system theme changes
    prefersDarkScheme.addEventListener('change', e => {
        if (!localStorage.getItem('theme')) { // Only if user hasn't set a preference
            const newTheme = e.matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            if (icon) {
                icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    });

    // Add smooth transition when changing themes
    const style = document.createElement('style');
    style.textContent = `
        * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }
        .no-transition {
            transition: none !important;
        }
    `;
    document.head.appendChild(style);
});
