$(document).on('click', '#checkout-btn', function(event){

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

    event.preventDefault();
    var formData = $("#userForm").serializeArray();
    var email = $('input[name="email"]').val();
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    var url = '/checkout/';
    var isValid = true;

    $('input, textarea').removeClass('error');

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
            .then((respone) => respone.json())
            .then((data) => {
                // console.log("YES", data.data)
                $('#checkout-btn').hide();
                $('#paypal-button-container').show();
                $('#order2checkout').html(data.data);
            })
        }
    };
})