$(document).ready(function(){
    $('#hora_inicio').timepicker({
        timeFormat: 'HH:mm',
        interval: 30,
        minTime: '0',
        maxTime: '23:30',
        defaultTime: '0',
        startTime: '00:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});

$(document).ready(function(){
    $('#hora_fin').timepicker({
        timeFormat: 'HH:mm',
        interval: 30,
        minTime: '0',
        maxTime: '23:30',
        defaultTime: '0',
        startTime: '00:00',
        dynamic: false,
        dropdown: true,
        scrollbar: true
    });
});
