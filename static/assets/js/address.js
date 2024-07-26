// Address
$(document).ready(function() {
    $('#address-tab').on('click', function() {
        
        $.ajax({
            url: "/user/address/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                $('#billing-address').html(response.data);
            },
        });
    });
});

// Change billing address
$(document).ready(function() {
    $('#billing-address').on('click', '#edit-billing-address-btn', function() {
        $.ajax({
            url: "/user/billing-address/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                $('#billing-address').html(response.data);
            },
        });
    });
});

// Change shipping address
$(document).ready(function() {
    $('#billing-address').on('click', '#edit-shipping-address-btn', function() {
        
        $.ajax({
            url: "/user/shipping-address/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                $('#billing-address').html(response.data);
            },
        });
    });
});