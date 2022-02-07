$(document).ready(function (){
  $('#mark-finished-btn').click(function () {
    $.ajax({
        type : 'POST',
        url  : mark_read_url
      }
    ).done(function (response) {
      if (response.status === 'success') {
        toastr.success("You have finished " + response.volume_name + ".\n Time to read some more", "Congratulations!");
        $('#finished-mark').show();
        $('#mark-finished-btn-nav').hide();
        $('.progress-report-card').replaceWith(response.finished_stats);
      } else {
        toastr.error( response.message, "Oops! Can't mark volume as finished");
      }
    })
  });
});
