// Add to wishlist
$(document).on('click', '.add-to-wishlist-btn', function(){
    console.log('ok ok ok ok ok ok');

    let this_val = $(this);

    let _index = this_val.attr("data-index");
    let quantity = $('.product-quantity-' + _index).val();
    let product_title = $(".product-title-" + _index).val();
    let category = $(".product-category-" + _index).val();
    let product_id = $(".product-id-" + _index).val();
    let product_price = $(".current-price-" + _index).text().replace('$', '');
    let product_image = $(".product-image-" + _index).val();

    console.log(
        'this_val', this_val
    );

    $.ajax({
        url: '/wishlist/add-to-wishlist/',
        method: 'GET',
        data: {
            'product_id': product_id,
            'quantity': quantity,
            'product_title': product_title,
            'product_price': product_price,
            'image': product_image,
            'category': category
        },
        dataType: 'json',
        beforeSend: function() {
            console.log('Product sent to wishlist');
        },
        success: function(response) {

            if (response.redirect) {
                window.location.href = response.redirect;
                
            } else {
                this_val.html('<i class="fa-solid fa-check"></i>');
                this_val.attr('aria-label', 'Added to wishlist');

                $(".wishlist-item-count").text(response.total_items);
            };
        },
    })
});

// Remove from cart

$(document).on('click', '.delete-product-wishlist', function() {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    $.ajax({
        url: '/wishlist/delete-from-wishlist/',
        data: {
            'product_id': product_id
        },
        dataType: 'json',
        beforeSend: function() {
            this_val.hide();
        },
        success: function(response) {
            this_val.show();

            // Update the cart item count
            $(".wishlist-item-count").text(response.total_items);
            
            // Update the cart list HTML
            $("#wish-list").html(response.data);

            // console.log("SUCCESS");
        }
    });
});