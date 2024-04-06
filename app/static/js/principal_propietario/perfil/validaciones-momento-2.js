document.addEventListener('DOMContentLoaded', function() {
    const campoCiudad = document.getElementById("ciudad");
    const ciudadError = document.getElementById("ciudad-error");
    const campoCelular = document.getElementById("celular");
    const celularError = document.getElementById("celular-error");
    let valido = true; // Asegúrate de definir la variable valido

    // Restringir la entrada de caracteres no deseados en el campo de celular
    campoCelular.oninput = () => {
        campoCelular.value = campoCelular.value.replace(/[^0-9]/g, '');
    };

    // Manejar el evento submit del formulario
    document.getElementById('datos-registro').addEventListener('submit', function(event) {
        // Validar campo de ciudad
        if (campoCiudad.value.trim() === "") {
            ciudadError.textContent = "Por favor, elige una ciudad.";
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
    });
});
