// User Profile view
$(document).ready(function() {
    $('#profile-tab').on('click', function() {
        
        $.ajax({
            url: "/user/profile/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                console.log('data profile', response.data)
                $('#user-profile').html(response.data);
            },
        });
    });
});

// Edit user Profile
$(document).ready(function() {
    $('#user-profile').on('click', '#edit-profile-user-btn', function() {
        
        $.ajax({
            url: "/user/edit-profile/",
            method: "GET",
            dataType: 'json',
            success: function(response) {
                $('#user-profile').html(response.data);
            },
        });
    });
});


// Save Edited user Profile
$(document).ready(function() {
    $('#user-profile').on('click', '#save-profile', function(event) {
        
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

        var formData = new FormData(document.getElementById('profile-form'));
        var email = $('input[name="email"]').val();
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        var url = '/user/save-profile/';
        var username = $("#profile-username").val();
        var isValid = true;
        var input_username = $('input[name="user_name"]').val();
    
        $('input').removeClass('profile_error');
    
        // required input validation
        formData.forEach(function(field) {
            var element = $('[name="' + field.name + '"]');
            if (element.prop('required') && !field.value.trim()) {
              isValid = false;
              element.addClass('profile_error');
            }
          });
    
        // Email input validation
        if (!emailPattern.test(email)) {
            isValid = false;
            $('input[name="email"]').addClass('profile_error');
        }

        // Username validation
        if (username.includes(input_username)) {
            isValid = false;
            $('input[name="user_name"]').addClass('profile_error');
            $(".username-exist").show();
        } else {
            $(".username-exist").hide();
        }

        if (isValid){
            sendData();
        };

        function sendData() {
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                // Handle response data
                console.log(data.data)
                $('#user-profile').html(data.data);
                $('.profile-update-popup').show();
            })
            ;
        }
    });
});
