// datepickers.js

$(document).ready(function() {
    // Escucha el cambio en los botones de radio
    $('input[name="periodo"]').change(function() {
        mostrarOcultarDatepickers();
    });

    function mostrarOcultarDatepickers() {
        var periodoSeleccionado = $('input[name="periodo"]:checked').val();

        if (periodoSeleccionado === 'rango') {
            $('#rango-datepickers').show();
            $('#fecha_picker').hide();
            $('label[for="fecha_picker"]').hide();
        } else {
            $('#rango-datepickers').hide();
            $('#fecha_picker').show();
            $('label[for="fecha_picker"]').show();
        }
    }

    // Obtener la fecha actual
    var fechaActual = new Date();
    var fechaActualString = fechaActual.getFullYear() + '-' + ('0' + (fechaActual.getMonth() + 1)).slice(-2) + '-' + ('0' + fechaActual.getDate()).slice(-2);

    // Configurar el datepicker para fecha_picker
    $('#fecha_picker').datepicker({
    format: 'yyyy-mm-dd',
    startDate: new Date('2023-09-01'), // Fecha mínima como un objeto Date
    endDate: new Date(fechaActualString), // Fecha máxima como un objeto Date
    autoclose: true          // Cerrar automáticamente después de seleccionar la fecha
});


    // Configurar el datepicker para fecha_inicio
    $('#fecha_inicio').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '2023-09-01', // Fecha mínima
        endDate: fechaActualString, // Fecha máxima (fecha actual)
        autoclose: true          // Cerrar automáticamente después de seleccionar la fecha
    });

    // Configurar el datepicker para fecha_fin
    $('#fecha_fin').datepicker({
        format: 'yyyy-mm-dd',
        startDate: '2023-09-01', // Fecha mínima
        endDate: fechaActualString, // Fecha máxima (fecha actual)
        autoclose: true          // Cerrar automáticamente después de seleccionar la fecha
    });

    // Agregar un controlador de eventos para el cambio de fecha en fecha_inicio
    $('#fecha_inicio').on('changeDate', function(e) {
        var selectedDate = e.date;
        var fechaFin = $('#fecha_fin').datepicker('getDate');

        // Validar que fecha_inicio no sea mayor que fecha_fin
        if (selectedDate >= fechaFin) {
            // Configurar fecha_fin un día después de fecha_inicio
            fechaFin.setDate(selectedDate.getDate() + 1);
            $('#fecha_fin').datepicker('setDate', fechaFin);
        }
    });
});
