document.addEventListener("DOMContentLoaded", function(){
    // Seleccionar elementos del DOM
    const btnSiguiente1 = document.getElementById("btn-siguiente-1"); // Botón siguiente
    const momento1 = document.getElementById("momento-1"); // Primer formulario
    const momento2 = document.getElementById("momento-2"); // Segundo formulario

    // Campos de entrada y mensajes de error asociados
    const campoNombre = document.getElementById("nombre");
    const nombreError = document.getElementById("nombre-error");
    const campoDireccion = document.getElementById("direccion");
    const direccionError = document.getElementById("direccion-error");
    const campoCelular = document.getElementById("celular");
    const celularError = document.getElementById("celular-error");

    // Función para restringir la entrada de caracteres no deseados en los campos de texto
    campoCelular.oninput = function(){
        this.value = this.value.replace(/[^0-9]/g, '');
    };

    campoNombre.oninput = function(){
        this.value = this.value.replace(/[^A-Za-z ]/g, '');
    };

    // Función para validar un campo de entrada y mostrar mensajes de error
    function validarCampo(valor, minCaracteres, mensajeError, errorElement){
        if (valor.trim().length < minCaracteres) {
            errorElement.textContent = mensajeError;
            return false;
        } else {
            errorElement.textContent = "";
            return true;
        }
    }

    // Evento de clic en el botón "Siguiente"
    btnSiguiente1.addEventListener("click", function(event){
        event.preventDefault();

        const nombreValido = validarCampo(campoNombre.value, 3, "Tu nombre debe tener al menos 3 caracteres.", nombreError);
        const direccionValida = validarCampo(campoDireccion.value, 3, "Tu dirección debe tener al menos 3 caracteres.", direccionError);
        const celularValido = validarCampo(campoCelular.value, 10, "Tu número de celular debe tener 10 números.", celularError);
        // Si el formulario es válido, ocultar el primer formulario y mostrar el segundo
        if (nombreValido && direccionValida && celularValido) {
            momento1.classList.add("hidden");
            momento2.classList.remove("hidden");
        }
    });
});
