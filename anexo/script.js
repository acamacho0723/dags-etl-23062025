// Toggle para modo oscuro/claro
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Comprobar preferencia del sistema
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// Comprobar si hay preferencia guardada
const currentTheme = localStorage.getItem('theme');

if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
    body.classList.add('dark-mode');
    themeToggle.textContent = 'Modo Claro';
}

themeToggle.addEventListener('click', function() {
    body.classList.toggle('dark-mode');
    
    if (body.classList.contains('dark-mode')) {
        themeToggle.textContent = 'Modo Claro';
        localStorage.setItem('theme', 'dark');
    } else {
        themeToggle.textContent = 'Modo Oscuro';
        localStorage.setItem('theme', 'light');
    }
});

// Botón para reiniciar filtros
document.getElementById('reset-btn').addEventListener('click', function() {
    // Quitar todos los parámetros de la URL
    window.location.href = window.location.pathname;
});
