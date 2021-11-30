$(document).ready(function (){
  $('#mark-finished-btn').click(function () {
    $.ajax({
        type : 'POST',
        url  : mark_read_url
      }
    ).done(function (response) {
      if (response.status === 'success') {
        toastr.success("You have finished " + response.issue_name + ".\n Time to read some more", "Congratulations!");
        $('#finished-mark').show();
        $('#mark-finished-btn-nav').hide();
      } else {
        toastr.error( response.message, "Oops! Can't mark issue as finished");
      }
    })
  });
});
