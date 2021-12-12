function initButtons() {
  $('.btn-skip, .btn-ignore').click(function (e) {
    let url = $(this).attr('data-href');
    $(this).tooltip('hide');
    $('.btn-skip, .btn-ignore').attr('disabled', 'disabled');
    $.ajax({
      url         : url,
      type        : 'GET'
    }).done(function (data, textStatus, jqXHR) {
      $('#table-wrapper').html(data);
      initButtons();
      $('.btn-skip, .btn-ignore').tooltip();
    }).fail(function (jqXHR, textStatus, errorThrown) {
      if (jqXHR.status === 404) {
        toastr.error("", "Please reload page");
      } else {
        toastr.error("", "Unknown error. Please contact administrator.");
      }
    });
  });
}

$(document).ready(function (){
  initButtons();
});
