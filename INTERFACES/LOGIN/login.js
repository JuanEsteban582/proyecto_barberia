document.addEventListener("DOMContentLoaded", function() {
    // Obtener referencias a los elementos del formulario y mensajes de error
    const form = document.getElementById("datos-log");
    const campoEmail = document.getElementById("email");
    const emailError = document.getElementById("email-error");
    const campoContra = document.getElementById("contrasena");
    const contraError = document.getElementById("contra-error");
    const campoRol = document.getElementById("rol");
    const rolError = document.getElementById("rol-error");

    // Bloquear la barra espaciadora en el campo de contraseña y correo
    function bloqueoBarra(evento) {
        if (evento.keyCode === 32) {
            evento.preventDefault();
        }
    }

    campoEmail.addEventListener('keydown', bloqueoBarra);
    campoContra.addEventListener('keydown', bloqueoBarra);

    // Función para validar el formato del correo electrónico
    function validarEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Función para validar la longitud de la contraseña
    function validarContrasena(contrasena) {
        return contrasena.length >= 8;
    }

    // Función para mostrar un mensaje de error en el campo correspondiente
    function mostrarError(campo, mensaje) {
        campo.textContent = mensaje;
    }

    // Función para limpiar los mensajes de error
    function limpiarErrores() {
        emailError.textContent = "";
        contraError.textContent = "";
        rolError.textContent = "";
    }

    // Validaciones que deben cumplirse antes de enviar el formulario
    form.addEventListener("submit", function(evento) {
        evento.preventDefault(); // Evitar el envío del formulario por defecto

        // Obtener los valores de los campos
        const email = campoEmail.value.trim();
        const contrasena = campoContra.value.trim();
        const rol = campoRol.value.trim();

        let valido = true; // Variable para verificar si todos los campos son válidos

        limpiarErrores(); // Limpiar los mensajes de error antes de realizar nuevas validaciones

        // Validar el formato del correo electrónico
        if (!validarEmail(email)) {
            mostrarError(emailError, "Por favor ingrese un correo electrónico válido.");
            valido = false;
        }

        // Validar la longitud de la contraseña
        if (!validarContrasena(contrasena)) {
            mostrarError(contraError, "La contraseña debe tener al menos 8 caracteres.");
            valido = false;
        }

        // Validar si el campo de rol está vacío
        if (rol === "") {
            mostrarError(rolError, "Por favor seleccione un rol.");
            valido = false;
        }

        // Si todas las validaciones son correctas, enviar el formulario
        if (valido) {
            form.submit();
        }
    });
});