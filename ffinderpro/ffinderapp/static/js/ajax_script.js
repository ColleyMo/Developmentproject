// ajax_script.js

$(document).ready(function() {
    $('#ajax-button').click(function() {
        $.ajax({
            url: '/path/to/endpoint',
            type: 'GET',
            data: {
                key1: 'value1',
                key2: 'value2'
            },
            success: function(response) {
                console.log(response);
                // Handle the response data
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                // Handle the error
            }
        });
    });
});
