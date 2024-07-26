// Address view
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

// Change billing address view
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


// Change shipping address view
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

// Save billing address
$(document).on('click', '#billing-address-btn', function(event){
    event.preventDefault();

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

    var formData = $("#billingForm").serializeArray();
    var email = $('input[name="email"]').val();
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    var url = '/user/billing-address/';
    var isValid = true;

    $('input').removeClass('error');

    // required input validation
    formData.forEach(function(field) {
        var element = $('[name="' + field.name + '"]');
        if (element.prop('required') && !field.value.trim()) {
          isValid = false;
          element.addClass('error');
        }
      });

    // Email input validation
    if (!emailPattern.test(email)) {
        isValid = false;
        $('input[name="email"]').addClass('error');
    }

    // Convert it to json
    if (isValid){
        var formDataJson = {};
        formData.forEach(function(field) {
            formDataJson[field.name] = field.value;
        });

        sendData();

        function sendData() {
            fetch( url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                  },
                body: JSON.stringify(formDataJson),
            })
            .then((response) => response.json())
            .then((data) => {

                console.log("CLICK BILLING ADDRESS", data.data)
                $('#billing-address').html(data.data);
                $('.address-message-popup').show()
            })
        }
    };
})