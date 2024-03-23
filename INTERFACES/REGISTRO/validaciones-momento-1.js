document.addEventListener("DOMContentLoaded", function(){
    // Seleccionar elementos del DOM
    const btnSiguiente1 = document.getElementById("btn-siguiente-1"); // Botón siguiente
    const momento1 = document.getElementById("momento-1"); // Primer formulario
    const momento2 = document.getElementById("momento-2"); // Segundo formulario

    // Campos de entrada y mensajes de error asociados
    const campoNombre = document.getElementById("nombre");
    const nombreError = document.getElementById("nombre-error");
    const campoApellidos = document.getElementById("apellidos");
    const apellidosError = document.getElementById("apellidos-error");
    const campoCedula = document.getElementById("cedula");
    const cedulaError = document.getElementById("cedula-error");
    const campoFecNac = document.getElementById("f_nacimiento");
    const fecNacError = document.getElementById("f_nacimiento-error");

    // Obtener la fecha actual y establecer la fecha mínima para la fecha de nacimiento
    const hoy = new Date();
    const fechaCalendario = new Date(hoy.getFullYear() - 18, hoy.getMonth(), hoy.getDate());
    const fechaMinima = fechaCalendario.toISOString().split('T')[0];
    campoFecNac.setAttribute("max", fechaMinima);

    // Función para restringir la entrada de caracteres no deseados en los campos de texto
    campoCedula.oninput = function(){
        this.value = this.value.replace(/[^0-9]/g, '');
    };

    campoNombre.oninput = campoApellidos.oninput = function(){
        this.value = this.value.replace(/[^A-Za-z ]/g, '');
    };

    // Función para calcular la edad a partir de la fecha de nacimiento
    function calcularEdad(fechaNacimiento){
        const hoy = new Date();
        const fechaNac = new Date(fechaNacimiento);
        let edad = hoy.getFullYear() - fechaNac.getFullYear();
        const mes = hoy.getMonth() - fechaNac.getMonth();

        if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNac.getDate())){
            edad--;
        }

        return edad;
    }

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
        const apellidosValido = validarCampo(campoApellidos.value, 3, "Tu apellido debe tener al menos 3 caracteres.", apellidosError);
        const cedulaValida = validarCampo(campoCedula.value, 6, "Tu número de identificación debe tener al menos 6 números.", cedulaError);
        const fecNacValida = validarCampo(campoFecNac.value, 1, "Debes seleccionar tu fecha de nacimiento.", fecNacError);
        // Si el formulario es válido, ocultar el primer formulario y mostrar el segundo
        if (nombreValido && apellidosValido && cedulaValida && fecNacValida) {
            momento1.classList.add("hidden");
            momento2.classList.remove("hidden");
        }
    });
});
