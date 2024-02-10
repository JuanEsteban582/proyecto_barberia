var selectHoras = document.getElementById("hora");
  for (var i = 0; i < 24; i++) {
    var option = document.createElement("option");
    var hora = (i < 10) ? "0" + i : i;
    option.value = hora;
    option.text = hora;
    selectHoras.appendChild(option);
  }

  // Generar opciones para minutos (de 00 a 59)
  var selectMinutos = document.getElementById("minutos");
  for (var j = 0; j < 60; j += 15) {
    var optionMin = document.createElement("option");
    var minuto = (j < 10) ? "0" + j : j;
    optionMin.value = minuto;
    optionMin.text = minuto;
    selectMinutos.appendChild(optionMin);
  }