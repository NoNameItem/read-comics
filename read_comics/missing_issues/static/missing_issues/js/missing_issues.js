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
      initCopy();
      $('[data-toggle="tooltip"]').tooltip();
    }).fail(function (jqXHR, textStatus, errorThrown) {
      if (jqXHR.status === 404) {
        toastr.error("", "Please reload page");
      } else {
        toastr.error("", "Unknown error. Please contact administrator.");
      }
    });
  });
}
function initCopy() {
  $('.space-path').click(function (){
    navigator.clipboard.writeText($(this).text());
  });
}

$(document).ready(function (){
  initButtons();
  initCopy();
});
