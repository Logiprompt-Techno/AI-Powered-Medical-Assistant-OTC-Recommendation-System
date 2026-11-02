function toggleTheme() {
    const currentTheme = localStorage.getItem('theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    if (newTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        document.documentElement.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    }
    
    updateThemeIcons(newTheme);
}

function updateThemeIcons(theme) {
    const btns = document.querySelectorAll('.theme-toggle-btn');
    btns.forEach(btn => {
        if (theme === 'dark') {
            btn.innerHTML = '☀️';
            btn.title = 'Switch to Light Mode';
        } else {
            btn.innerHTML = '🌙';
            btn.title = 'Switch to Dark Mode';
        }
    });
}

// On load, update icons (the HTML head script handles adding the class immediately)
document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'light';
    updateThemeIcons(theme);
});
