$(document).ready(function() {
    // Auto-uppercase for airport codes
    $('#id_origen, #id_destino').on('input', function() {
        this.value = this.value.toUpperCase();
    });

    // Date validation
    $('#id_fecha_ida').on('change', function() {
        const fechaIda = new Date(this.value);
        const fechaVuelta = $('#id_fecha_vuelta');
        const hoy = new Date();
        
        hoy.setHours(0, 0, 0, 0);
        
        if (fechaIda < hoy) {
            alert('La fecha de ida no puede ser anterior a hoy');
            this.value = '';
            return;
        }
        
        if (fechaVuelta.val()) {
            const fechaVueltaDate = new Date(fechaVuelta.val());
            if (fechaVueltaDate < fechaIda) {
                fechaVuelta.val('');
            }
        }
    });

    // Real-time price filtering (if using range slider)
    const priceSlider = document.getElementById('priceRange');
    if (priceSlider) {
        noUiSlider.create(priceSlider, {
            start: [0, 1000],
            connect: true,
            range: {
                'min': 0,
                'max': 1000
            },
            step: 10
        });

        priceSlider.noUiSlider.on('update', function(values) {
            const minPrice = Math.round(values[0]);
            const maxPrice = Math.round(values[1]);
            $('#minPrice').text(minPrice + '€');
            $('#maxPrice').text(maxPrice + '€');
            $('#id_precio_min').val(minPrice);
            $('#id_precio_max').val(maxPrice);
        });
    }

    // Flight card interactions
    $('.vuelo-card').hover(
        function() {
            $(this).addClass('shadow');
        },
        function() {
            $(this).removeClass('shadow');
        }
    );

    // Quick filter buttons
    $('.quick-filter').on('click', function() {
        const filterType = $(this).data('filter');
        const filterValue = $(this).data('value');
        
        switch(filterType) {
            case 'escalas':
                $('#id_escalas_maximas').val(filterValue);
                break;
            case 'duracion':
                $('#id_duracion_maxima').val(filterValue);
                break;
            case 'precio':
                $('#id_precio').val(filterValue);
                break;
        }
        
        $('#filtrosForm').submit();
    });

    // Responsive filters toggle
    $('#toggleFilters').on('click', function() {
        $('#filtersSidebar').toggleClass('d-none d-md-block');
        $(this).find('i').toggleClass('fa-filter fa-times');
    });

    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
});

// Function to format flight duration
function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
}

// Function to handle airline logo display
function getAirlineLogo(code) {
    return `https://images.kiwi.com/airlines/64/${code}.png`;
}

// API call for live pricing (if needed)
async function checkLivePricing(vueloId) {
    try {
        const response = await fetch(`/api/vuelos/${vueloId}/precio/`);
        const data = await response.json();
        return data.precio;
    } catch (error) {
        console.error('Error checking live pricing:', error);
        return null;
    }
}
