// Message

setTimeout(function () {
    $("#message").fadeOut('slow')
}, 8000);

// Product filtering

$(document).ready(function () {
    function applyFilters() {
        let filter_object = {};

        // Gather checkbox values
        $('.filter-checkbox').each(function () {
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');
            filter_object[filter_key] = Array.from(
                document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')
            ).map(function (element) {
                return element.value;
            });
        });

        // Gather slider values
        const sliderValues = rangeSlider.noUiSlider.get();
        filter_object.min_price = moneyFormat.from(sliderValues[0]);
        filter_object.max_price = moneyFormat.from(sliderValues[1]);

        console.log('Filter object', filter_object);


        // Send AJAX request
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            success: function (response) {
                $("#filtered-product").html(response.data);
                $("#totall-product").html(response.product_count);                
            }
        });
    }

    // Handle checkbox click
    $(".filter-checkbox").on("click", function () {
        applyFilters();
    });

    // Slider Range JS
    if ($("#slider-range").length) {
        $(".noUi-handle").on("click", function () {
            $(this).width(50);
        });

        var minPrice = parseInt(document.getElementById("min-price").innerText.trim());
        var maxPrice = parseInt(document.getElementById("max-price").innerText.trim()) + 50;

        var rangeSlider = document.getElementById("slider-range");
        var moneyFormat = wNumb({
            decimals: 0,
            thousand: ",",
            prefix: "$"
        });
        noUiSlider.create(rangeSlider, {
            start: [minPrice, maxPrice],
            step: 1,
            range: {
                min: [minPrice],
                max: [maxPrice]
            },
            format: moneyFormat,
            connect: true
        });

        // Set visual min and max values and also update value hidden form inputs
        rangeSlider.noUiSlider.on("update", function (values, handle) {
            document.getElementById("slider-range-value1").innerHTML = values[0];
            document.getElementById("slider-range-value2").innerHTML = values[1];
            document.getElementsByName("min-value").value = moneyFormat.from(values[0]);
            document.getElementsByName("max-value").value = moneyFormat.from(values[1]);
        });

        // Apply filters on slider change
        rangeSlider.noUiSlider.on("change", function (values, handle) {
            applyFilters();
        });
    }
});
