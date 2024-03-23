document.addEventListener("DOMContentLoaded", function(){
    //Elementos del DOM
    let btnAdministrar = document.getElementById('btn-administrar-barberos');
    let btnActividad = document.querySelectorAll('.btn-actividad-barbero');
    let btnEliminar = document.querySelectorAll('.btn-eliminar-barbero');
    let btnAgregar = document.getElementById('btn-agregar-barbero');

    let modoAdministrar = true;

    btnAdministrar.addEventListener("click", function(){
        if (modoAdministrar) {
            // Cambia a modo "Guardar cambios"
            btnAgregar.classList.remove("esconder");
            btnAdministrar.textContent = "Guardar cambios";
            modoAdministrar = false;
            btnEliminar.forEach(function(eliminar){
                eliminar.classList.remove("esconder");
            });
        } else {
            // Cambia a modo "Administrar barberos"
            btnAgregar.classList.add("esconder");
            btnAdministrar.textContent = "Administrar barberos";
            modoAdministrar = true;
            btnEliminar.forEach(function(eliminar){
                eliminar.classList.add("esconder");
            });
        }
    });
});