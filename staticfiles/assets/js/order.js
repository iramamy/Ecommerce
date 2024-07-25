// Order

$(document).ready(function() {
    $('#orders-tab').on('click', function() {
        // event.preventDefault();
        
        $.ajax({
            url: "/user/dashboard-order/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                console.log("GREAT")
                if (response.orders_count===0){
                    console.log("IT IS ")
                // console.log('data', response.orders_count);
                    $("#order-detail-container").hide()
                };
                $('#order-detail-container').html(response.data);
            },
        });
    });
});


// Order Product detail
$(document).ready(function() {
    $(document).on('click', '.view-order-detail', function(event) {
        event.preventDefault();
        var orderID = $(this).data('order-id');
        console.log('ORDER', orderID)

        $.ajax({
            url: "/user/order-detail/" + orderID + "/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                console.log('data', response.data);
                $('#order-detail-container').html(response.data);
            },
        });
    });
});
