// Message

setTimeout(function(){
    $("#message").fadeOut('slow')
}, 8000);

// Filter data
$(document).ready(function(){
    $(".filter-checkbox").on("click", function(){
        console.log('You check the checkbox');
        let filter_object = {}

        $('.filter-checkbox').each(function(){
            let filter_value = $(this).val();
            let filter_key = $(this).data('filter');
            filter_object[filter_key] = Array.from(
                document.querySelectorAll('input[data-filter='+ filter_key +']:checked')
                ).map(function(element){
                    return element.value
                })
        });
        console.log('Filter object', filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            success: function(response){
                $("#filtered-product").html(response.data);
            }
        });
    });
});
