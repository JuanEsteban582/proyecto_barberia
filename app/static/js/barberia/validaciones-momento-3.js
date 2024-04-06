document.addEventListener("DOMContentLoaded", function() {

    const formulario = document.getElementById("datos-registro");

    const atrasMomento3 = document.getElementById("atras-momento-3");

    const momento2 = document.getElementById("momento-2");
    const momento3 = document.getElementById("momento-3");

    const campoApertura = document.getElementById("hora-apertura");
    const aperturaError = document.getElementById("apertura-error");

    const campoCierre = document.getElementById("hora-cierre");
    const cierreError = document.getElementById("cierre-error");

    // Validar el formulario antes de enviar
    formulario.addEventListener("submit", function(event) {
        event.preventDefault();
        let formValido = true;

        if (campoApertura.value.trim() === "") {
            aperturaError.textContent = "Por favor, elige una hora.";
            formValido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            aperturaError.textContent = "";
        }
    
        if (campoCierre.value.trim() === "") {
            cierreError.textContent = "Por favor, elige una hora.";
            formValido = false;
            event.preventDefault(); // Evitar que se avance al siguiente momento
        } else {
            cierreError.textContent = "";
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