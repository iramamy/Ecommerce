// Add review comment
console.log('Cool cool cool cool!')

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
$("#add-to-cart-btn").on('click', function(){
    let quantity = $('#product-quantity').val();
    let product_title = $(".product-title").val();
    let product_id = $(".product-id").val();
    let product_price = $(".current-price").text().replace('$', '');;
    let this_val = $(this);

    console.log("Quantity:", quantity);
    console.log("Product Title:", product_title);
    console.log("Product ID:", product_id);
    console.log("Product Price:", product_price);
    console.log("this_val :", this_val);

    $.ajax({
        url: '/cart/add-to-cart/',
        data: {
            'product_id': product_id,
            'quantity': quantity,
            'product_title': product_title,
            'product_price': product_price
        },
        dataType: 'json',
        beforeSend: function(){
            console.log('Product sent to cart')
        },
        success: function(response){
            this_val.html('Added to cart!');
            console.log('Success');
            $(".cart-item-count").text(response.total_items);
        },
    })
})