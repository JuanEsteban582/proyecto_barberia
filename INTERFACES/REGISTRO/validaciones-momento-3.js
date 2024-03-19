document.addEventListener("DOMContentLoaded", function() {

    const formulario = document.getElementById("datos-registro");
    const btnSubmit = document.getElementById("btn-submit");

    const atrasMomento3 = document.getElementById("atras-momento-3");

    const momento2 = document.getElementById("momento-2");
    const momento3 = document.getElementById("momento-3");

    const campoRol = document.getElementById("rol");
    const rolError = document.getElementById("rol-error");

    const campoCorreo = document.getElementById("correo");
    const correoError = document.getElementById("correo-error");
    
    const campoContrasena = document.getElementById("contrasena");
    const requerContra = document.getElementById("requer-contra");
    const requerLongitud = document.getElementById("long-min");
    const requerMayus = document.getElementById("mayus");
    const requerMinus = document.getElementById("minus");

    const campoConfirmarContra = document.getElementById("confirmar-contrasena");
    const confirmarContraError = document.getElementById("conf-contrasena-error");

    // Bloquear la barra espaciadora en el campo de contraseña y correo
    function bloqueoBarra(evento) {
        if (evento.keyCode === 32) {
            evento.preventDefault();
        }
    }

    campoCorreo.addEventListener('keydown', bloqueoBarra);
    campoContrasena.addEventListener('keydown', bloqueoBarra);
    campoConfirmarContra.addEventListener('keydown', bloqueoBarra);

    // Ocultar la lista de requisitos de contraseña al cargar la página
    requerContra.style.display = "none";

    // Mostrar la lista de requisitos cuando se hace clic en el campo de contraseña
    campoContrasena.addEventListener("focus", function() {
        requerContra.style.display = "block";
    });

    // Ocultar la lista de requisitos cuando el usuario deja de estar en el campo de contraseña
    campoContrasena.addEventListener("blur", function() {
        requerContra.style.display = "none";
    });

    // Función para verificar si la contraseña cumple con los requisitos
    function verificarRequisitos() {
        let cumplido = true;

        // Verificar longitud mínima
        if (campoContrasena.value.length < 8) {
            requerLongitud.style.display = "block";
            cumplido = false;
        } else {
            requerLongitud.style.display = "none";
        }

        // Verificar presencia de mayúscula
        if (!/[A-Z]/.test(campoContrasena.value)) {
            requerMayus.style.display = "block";
            cumplido = false;
        } else {
            requerMayus.style.display = "none";
        }

        // Verificar presencia de minúscula
        if (!/[a-z]/.test(campoContrasena.value)) {
            requerMinus.style.display = "block";
            cumplido = false;
        } else {
            requerMinus.style.display = "none";
        }

        // Si todos los requisitos se cumplen, ocultar la lista
        if (cumplido) {
            requerContra.style.display = "none";
        }
    }

    // Agregar evento de escucha al campo de contraseña para verificar los requisitos
    campoContrasena.addEventListener("input", verificarRequisitos);

    // Validar el formulario antes de enviar
    formulario.addEventListener("submit", function(event) {
        event.preventDefault();
        let formValido = true;

        // Validación para el campo de selección de rol
        if (campoRol.value === "") {
            rolError.textContent = "Por favor, seleccione un rol.";
            formValido = false;
        } else {
            rolError.textContent = ""; // Limpiar mensaje de error si es válido
        }

        // Validación para el campo de correo electrónico
        const correoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoValido.test(campoCorreo.value)) {
            correoError.textContent = "Por favor, ingrese un correo electrónico válido.";
            formValido = false;
        } else {
            correoError.textContent = ""; // Limpiar mensaje de error si es válido
        }

        // Validación para el campo de contraseña
        if (campoContrasena.value.length < 8 || !/[A-Z]/.test(campoContrasena.value) || !/[a-z]/.test(campoContrasena.value)) {
            // Si no se cumplen los requisitos, prevenir el envío del formulario
            formValido = false;
            // Mostrar la lista de requisitos
            requerContra.style.display = "block";
            // Verificar y mostrar los requisitos que no se cumplen
            verificarRequisitos();
        }

        // Validación para el campo de confirmación de contraseña
        if (campoConfirmarContra.value !== campoContrasena.value) {
            confirmarContraError.textContent = "Las contraseñas no coinciden.";
            formValido = false;
        } else {
            confirmarContraError.textContent = ""; // Limpiar mensaje de error si coinciden
        }

        // Si el formulario es válido, enviarlo
        if (formValido) {
            this.submit();
        }
    });


    atrasMomento3.addEventListener("click", function(){
        momento2.classList.remove("hidden");
        momento3.classList.add("hidden");
    });


});