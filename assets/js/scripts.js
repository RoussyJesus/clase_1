/**
 * Script para gestionar el enlace de navegación activo.
 *
 * Este script se ejecuta cuando el contenido de la página está cargado.
 * Compara la ruta actual del navegador con los enlaces de la barra
 * de navegación y aplica la clase 'active' al enlace correspondiente.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Obtiene la ruta de la página actual (ej. "/Pagina1")
    const currentPath = window.location.pathname;

    // Obtiene todos los enlaces de navegación
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        // Usa el objeto URL para obtener fácilmente la ruta del enlace
        const linkPath = new URL(link.href).pathname;

        // Comprueba si la ruta del enlace coincide con la ruta actual
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active'); // Asegura que los otros no estén activos
        }
    });
});