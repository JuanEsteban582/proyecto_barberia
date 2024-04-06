document.addEventListener("DOMContentLoaded", function(){
    // Obtener referencias de los elementos del formulario y sus mensajes de error
    const form = document.getElementById("datos-res");

    const campoRol = document.getElementById("rol");
    const rolError = document.getElementById("rol-error");

    const campoCedula = document.getElementById("cedula_user");
    const cedulaError = document.getElementById("cedula-error");

    const campoFecNac = document.getElementById("f_nacimiento");
    const fecNacError = document.getElementById("f_nacimiento-error");

    const campoContra = document.getElementById("contrasena");
    const requerContra = document.getElementById("requer-contra");
    const requerLongitud = document.getElementById("long-min");
    const requerMayus = document.getElementById("mayus");
    const requerMinus = document.getElementById("minus");
    /* const requerNum = document.getElementById("numero");
     const requerCar = document.getElementById("car-especial") */

    const campoConfirmarContra = document.getElementById("confirmar-contra");
    const confirmarContraError = document.getElementById("confirmar-contra-error");

    const avisoError = document.getElementById("aviso-error");

    const btnRestaurar = document.getElementById("btn")

    // Obtener la fecha actual y establecer la fecha mínima para la fecha de nacimiento
    const hoy = new Date();
    const fechaCalendario = new Date(hoy.getFullYear() - 18, hoy.getMonth(), hoy.getDate());
    const fechaMinima = fechaCalendario.toISOString().split('T')[0];
    campoFecNac.setAttribute("max", fechaMinima);

    // Función para evitar el uso de la barra espaciadora
    function bloqueoBarra(evento) {
        if (evento.keyCode === 32) {
            evento.preventDefault();
        }
    }

    campoContra.addEventListener('keydown', bloqueoBarra);
    campoConfirmarContra.addEventListener('keydown', bloqueoBarra);

    // Función para restringir la entrada de caracteres no deseados en los campos de texto
    campoCedula.oninput = function(){
        this.value = this.value.replace(/[^0-9]/g, '');
    };

     // Función para validar la contraseña
     function validarContra() {
        const contra = campoContra.value;

        return contra.length >= 8 && /[A-Z]/.test(contra) && /[a-z]/.test(contra);
    }

    // Estableciendo los requisitos de la contraseña
    requerContra.style.display = 'none';
    campoContra.addEventListener('input', function(){
        const contra = this.value;

        requerLongitud.style.display = contra.length >= 8 ? 'none' : 'block';
        requerMayus.style.display = /[A-Z]/.test(contra) ? 'none' : 'block';
        requerMinus.style.display = /[a-z]/.test(contra) ? 'none' : 'block';
        requerContra.style.display = validarContra() ? 'none' : 'block';
        /* requerNum.style.display = /\d/.test(contra) ? 'none' : 'block';
        requerCar.style.display = /[^A-Za-z0-9]/.test(contra) ? 'none': 'block'; */
        
        // && /\d/.test(password) && /[^A-Za-z0-9]/.test(password)
        if (campoContra.length >= 8 && /[A-Z]/.test(campoContra) && /[a-z]/.test(campoContra)) {
            requerContra.style.display = 'none';
        } else {
            requerContra.style.display = 'block';
        }

    });

    campoContra.addEventListener('focus', function(){
        requerContra.style.display = 'block';
    });
    campoContra.addEventListener('blur', function(){
        requerContra.style.display = 'none';
    });

    // Función para validar que las contraseñas coincidan
    function coincidenciaContra() {
        const contra = campoContra.value;
        const confirmarContra = campoConfirmarContra.value;

        if (contra !== confirmarContra) {
            confirmarContraError.textContent = 'Las contraseñas no coinciden.';
        } else {
            confirmarContraError.textContent = ''
        }
    }

    campoConfirmarContra.addEventListener('input', coincidenciaContra);

    // Función para validar la longitud de la cédula
    function validarCedula() {
        if (campoCedula.value.length < 6) {
            cedulaError.textContent = 'Tu número de identificación debe tener al menos 6 números.';
        } else {
            cedulaError.textContent = '';
        }
    }

    // Función para validar si se seleccionó una fecha de nacimiento
    function validarFechaNacimiento() {
        if (!campoFecNac.value) {
            fecNacError.textContent = 'Por favor, seleccione su fecha de nacimiento.';
        } else {
            fecNacError.textContent = '';
        }
    }

    function validarCampoRol() {
        if (campoRol.value === "") {
            rolError.textContent = 'Por favor, escoja el rol.'
        } else {
            rolError.textContent = '';
        }
    }

    // Agregar evento al botón para validar la cédula antes de enviar el formulario
    btnRestaurar.addEventListener('click', function(event) {
        validarCedula();
        validarFechaNacimiento();
        coincidenciaContra();
        validarCampoRol();
        // Si hay errores, prevenir el envío del formulario
        if (campoCedula.value.trim() === '' || campoFecNac.value.trim() === '' || campoContra.value.trim() === '' || campoConfirmarContra.value.trim() === '' || campoRol.value.trim() === '') {
            avisoError.textContent = 'Debe llenar todos los campos.';
            event.preventDefault();
        } else if (!validarContra() || cedulaError.textContent !== '' || fecNacError.textContent !== '' || confirmarContraError.textContent !== '') {
            avisoError.textContent = 'Debe cumplir con los requisitos de la contraseña.';
            event.preventDefault();
        } else {
            avisoError.textContent = ''; // Limpiar el mensaje de error si todo está bien
        }
    });
});