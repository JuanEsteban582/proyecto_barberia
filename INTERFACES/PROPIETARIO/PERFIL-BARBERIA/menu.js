document.addEventListener("DOMContentLoaded", function(){
    
    //Ejecutar función en el evento click
    
    //Declaramos variables
    let menuLateral = document.getElementById("menu-lateral");
    let btnMenu = document.getElementById("btn-menu");
    let body = document.getElementById("body");
    let btnCerrarMenu = document.getElementById("btn-cerrar-menu");

    btnMenu.addEventListener("click", open_close_menu);
    btnCerrarMenu.addEventListener("click", open_close_menu)
    //Evento para mostrar y ocultar menú
        function open_close_menu(){
            body.classList.toggle("body_move");
            menuLateral.classList.toggle("menu__side_move");
        }
    
    //Si el ancho de la página es menor a 1000px, ocultará el menú al recargar la página
    
    if (window.innerWidth < 1000){
    
        body.classList.add("body_move");
        menuLateral.classList.add("menu__side_move");
    }
    
    //Haciendo el menú responsive(adaptable)
    
    window.addEventListener("resize", function(){
    
        if (window.innerWidth > 1000){
    
            body.classList.remove("body_move");
            menuLateral.classList.remove("menu__side_move");
        }
    
        if (window.innerWidth < 1000){
    
            body.classList.add("body_move");
            menuLateral.classList.add("menu__side_move");
        }
    
    });
});

