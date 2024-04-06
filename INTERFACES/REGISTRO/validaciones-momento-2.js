document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const btnSiguiente2 = document.getElementById("btn-siguiente-2");
    const atrasMomento2 = document.getElementById("atras-momento-2");
    const momento1 = document.getElementById("momento-1");
    const momento2 = document.getElementById("momento-2");
    const momento3 = document.getElementById("momento-3");

    // Campos de entrada y mensajes de error asociados
    const campoDepartamento = document.getElementById("departamento");
    const departamentoError = document.getElementById("departamento-error");
    const campoCiudad = document.getElementById("ciudad");
    const ciudadError = document.getElementById("ciudad-error");
    const campoCelular = document.getElementById("celular");
    const celularError = document.getElementById("celular-error");

    // Restringir la entrada de caracteres no deseados en el campo de celular
    campoCelular.oninput = () => {
        campoCelular.value = campoCelular.value.replace(/[^0-9]/g, '');
    };

    
    // Evento para retroceder al momento 1
    atrasMomento2.addEventListener("click", () => {
        momento1.classList.remove("hidden");
        momento2.classList.add("hidden");
    });

    // Evento para avanzar al momento 3 o mostrar errores
    btnSiguiente2.addEventListener("click", function(event) {
        event.preventDefault();
        let valido = true;
        // Validar campo de departamento
        if (campoDepartamento.value.trim() < 4) {
            departamentoError.textContent = "El nombre del departamento debe tener 4 caracteres o más.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            departamentoError.textContent = "";
        }
    
        // Validar campo de ciudad
        if (campoCiudad.value.trim() < 4) {
            ciudadError.textContent = "El nombre de la ciudad debe tener 4 caracteres o más.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            ciudadError.textContent = "";
        }
    
        // Validar campo de celular
        const celularValue = campoCelular.value.trim();
        if (celularValue === "") {
            celularError.textContent = "Por favor, introduce tu número de celular.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else if (celularValue.length !== 10) {
            celularError.textContent = "Tu número de celular debe tener 10 dígitos.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else if (!/^3/.test(celularValue)) {
            celularError.textContent = "Tu número de celular debe comenzar con el número 3.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            celularError.textContent = "";
        }

        if (valido) {
            momento3.classList.remove("hidden");
            momento2.classList.add("hidden");
        }
    });
    
});