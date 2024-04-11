document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const btnSiguiente2 = document.getElementById("btn-siguiente-2");
    const atrasMomento2 = document.getElementById("atras-momento-2");
    const momento1 = document.getElementById("momento-1");
    const momento2 = document.getElementById("momento-2");
    const momento3 = document.getElementById("momento-3");

    // Campos de entrada y mensajes de error asociados
    const campoPais = document.getElementById("pais");
    const paisError = document.getElementById("pais-error");
    const campoDepartamento = document.getElementById("departamento");
    const departamentoError = document.getElementById("departamento-error");
    const campoCiudad = document.getElementById("ciudad");
    const ciudadError = document.getElementById("ciudad-error");

    // Evento para retroceder al momento 1
    atrasMomento2.addEventListener("click", () => {
        momento1.classList.remove("hidden");
        momento2.classList.add("hidden");
    });

    // Evento para avanzar al momento 3 o mostrar errores
    btnSiguiente2.addEventListener("click", function(event) {
        event.preventDefault();
        let valido = true;

        if (campoPais.value.trim() === "") {
            paisError.textContent = "Por favor, elige un país.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            paisError.textContent = "";
        }
        // Validar campo de departamento
        if (campoDepartamento.value.trim() === "") {
            departamentoError.textContent = "Por favor, elige un departamento.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            departamentoError.textContent = "";
        }
    
        // Validar campo de ciudad
        if (campoCiudad.value.trim() === "") {
            ciudadError.textContent = "Por favor, elige una ciudad.";
            valido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            ciudadError.textContent = "";
        }

        if (valido) {
            momento3.classList.remove("hidden");
            momento2.classList.add("hidden");
        }
    });
    
});