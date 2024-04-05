// script.js

$(document).ready(function() {
    $('#send-message-form').submit(function(e) {
      e.preventDefault();
      var form = $(this);
      $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data) {
          console.log(data);
          // Handle success
        },
        error: function(xhr, textStatus, errorThrown) {
          console.error(xhr.responseText);
          // Handle error
        }
      });
    });
  });
  