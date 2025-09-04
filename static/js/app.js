// JavaScript para funcionalidades de MiComparador
$(document).ready(function() {
    // Auto-complete para aeropuertos
    $('input[name="origen"], input[name="destino"]').on('input', function() {
        const query = $(this).val();
        if (query.length > 2) {
            // Aquí iría la llamada a la API de autocomplete
            console.log('Buscando:', query);
        }
    });

    // Validación de fechas
    $('input[type="date"]').on('change', function() {
        const fechaIda = $('input[name="fecha_ida"]').val();
        const fechaVuelta = $('input[name="fecha_vuelta"]').val();
        
        if (fechaIda && fechaVuelta && fechaVuelta < fechaIda) {
            alert('La fecha de vuelta no puede ser anterior a la fecha de ida');
            $('input[name="fecha_vuelta"]').val('');
        }
    });

    // Smooth scrolling
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top
        }, 500);
    });

    // Mostrar/ocultar formularios
    $('#searchTabs button').on('click', function() {
        const target = $(this).data('bsTarget');
        $('.search-form').hide();
        $(target + ' .search-form').show();
    });

    // Cargar precios sugeridos
    function cargarPreciosSugeridos() {
        $.ajax({
            url: '/api/precios-sugeridos/',
            method: 'GET',
            success: function(data) {
                // Actualizar precios en las tarjetas de destinos
                data.forEach(function(destino) {
                    $(`#precio-${destino.ciudad}`).text(`Desde €${destino.precio}`);
                });
            }
        });
    }

    // Inicializar
    cargarPreciosSugeridos();
});
