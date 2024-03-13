document.addEventListener("DOMContentLoaded", function() {

    const form = document.getElementById("datos-log");
    const campoEmail = document.getElementById("email");
    const emailError = document.getElementById("email-error");
    const campoContra = document.getElementById("contrasena");
    const contraError = document.getElementById("contra-error");

    form.addEventListener("submit", function(evento) {
        evento.preventDefault(); // Evita que el formulario se envíe por defecto

        const email = campoEmail.value.trim();
        const contrasena = campoContra.value.trim();    

        // Expresión regular para validar el formato de un correo electrónico
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        let valido = true; // Variable para verificar si todos los campos son válidos

        if (!emailRegex.test(email)) {
            emailError.textContent = "Por favor ingrese un correo electrónico válido.";
            valido = false;
        } else {
            emailError.textContent = "";
        }

        if (contrasena.length < 8) {
            contraError.textContent = "La contraseña debe tener al menos 8 caracteres.";
            valido = false;
        } else {
            contraError.textContent = "";
        }

        if (valido) {
            form.submit();
        }
    });

});