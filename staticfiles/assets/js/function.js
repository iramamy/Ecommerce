
// Add review comment
$('#commentForm').submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(), 
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function(response){

            if(response.bool){
                $('#review-response-div').show();
                $('.add-review-text').hide();
                $('.review-form').hide();
                $('#review-response').html('Review added successfully');

                let review_html = '<div class="single-comment justify-content-between d-flex mb-30">'
                review_html += '<div class="user d-flex justify-content-between">'
                review_html += '<div class="thumb text-center">'
                review_html += '<img src="https://www.w3schools.com/howto/img_avatar2.png" alt="" />'
                review_html += '<a href="#" class="font-heading text-brand" >' + response.context.user + '</a>'
                review_html += '</div>'
                review_html += '<div class="desc w-100">'
                review_html += '<div class="d-flex justify-content-between mb-10" >'
                review_html += '<div class="d-flex align-items-center">'
                review_html += '<span class="font-xs text-muted" >'+ response.context.date +'</span>'
                review_html += '</div>'

                for(var i=1; i<=response.context.rating; i++){
                    review_html += '<i class="fas fa-star text-warning"></i>';
                }

                review_html += '</div>'
                review_html += '<p class="mb-10">' +response.context.review +'</p>'
                review_html += '</div>'
                review_html += '</div>'
                review_html += '</div>'

                $('.comment-list').prepend(review_html);
            };

        }
    })
})

// Add to cart
$(document).on('click', '.add-to-cart-btn', function() {

    let this_val = $(this);

    let _index = this_val.attr("data-index");

    let quantity = $('.product-quantity-' + _index).val();
    let product_title = $(".product-title-" + _index).val();
    let category = $(".product-category-" + _index).val();
    let product_id = $(".product-id-" + _index).val();
    let product_price = $(".current-price-" + _index).text().replace('$', '');
    let product_image = $(".product-image-" + _index).val();

    $.ajax({
        url: '/cart/add-to-cart/',
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
            console.log('Product sent to cart');
        },
        success: function(response) {
            
            if (response.redirect) {
                window.location.href = response.redirect;

            } else {
                this_val.html('<i class="fa-solid fa-check"></i>');
                $(".cart-item-count").text(response.total_items);
            }
        },
    });
});


// Remove from cart
$(document).on('click', '.delete-product', function() {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product id", product_id);

    $.ajax({
        url: '/cart/delete-from-cart/',
        method: 'GET',
        data: {
            'product_id': product_id
        },
        dataType: 'json',
        beforeSend: function() {
            this_val.hide();
        },
        success: function(response) {
            this_val.show();

            $(".cart-item-count").text(response.total_items);

            $("#cart-list").html(response.data);
        }
    });
});

// Update cart
$(document).on('input', '.update-product', function() {
    const quantity = $(this).val();
    const product_id = $(this).attr('data-product-update');
    const subtotalElement = $(`#subtotal-${product_id}`);

    if (quantity === '' || quantity === '0') {
        return;
    }
    console.log('quantity', quantity);
    
    $.ajax({
        url: '/cart/update-cart/',
        method: 'GET',
        data: {
            'product_id': product_id,
            'quantity': quantity
        },
        dataType: 'json',
        success: function(response) {
            $("#table-cart-amount").html(response.data);

            if (subtotalElement.length) {
                subtotalElement.text(`$${response.item.subtotal}`);
            }
        }
    });
});

