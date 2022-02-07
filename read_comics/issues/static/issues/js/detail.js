$(document).ready(function () {
  $('#mark-finished-btn').click(function () {
    $.ajax({
        type                   : 'POST',
        url                    : mark_read_url,
        contentType            : 'application/json; charset=utf-8',
        data                   : JSON.stringify({
          base_object_app_label  : base_object_app_label,
          base_object_model_name : base_object_model_name,
          base_object_slug       : base_object_slug
        })
      }
    ).done(function (response) {
      if (response.status === 'success') {
        toastr.success("You have finished " + response.issue_name + ".\n Time to read some more", "Congratulations!");
        $('#finished-mark').show();
        $('#mark-finished-btn-nav').hide();
        $('.progress-report-card').replaceWith(response.finished_stats);
        $('.volume-progress-report-card').replaceWith(response.volume_finished_stats);
      } else {
        toastr.error(response.message, "Oops! Can't mark issue as finished");
      }
    });
  });
});
