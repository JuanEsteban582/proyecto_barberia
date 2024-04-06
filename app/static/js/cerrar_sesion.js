
        document.addEventListener('DOMContentLoaded', function() {
            var cerrarSesionBtn = document.getElementById('btn-cerrar-sesion');
            cerrarSesionBtn.addEventListener('click', function(event) {
                event.preventDefault(); // Evita que el enlace navegue a la URL del href
                window.location.href = '/cerrar_sesion'; // Redirige al usuario a la ruta de cierre de sesión
            });
        
            if (window.history && window.history.pushState) {
                window.history.pushState('', null, './login');
                window.onpopstate = function() {
                    window.history.go(1);
                };
            }
        });
    