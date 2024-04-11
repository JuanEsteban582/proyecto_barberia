
document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los elementos con la clase 'flash-message'
    var flashMessages = document.querySelectorAll('.flash-message');

    // Itera sobre cada mensaje flash
    flashMessages.forEach(function(flashMessage) {
        // Establece un temporizador para cada mensaje
        setTimeout(function() {
            // Oculta el mensaje flash
            flashMessage.style.display = 'none';
        }, 5000); // 5000 milisegundos = 5 segundos
    });
});

