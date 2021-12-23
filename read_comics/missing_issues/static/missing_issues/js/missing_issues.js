function updateBadges() {
  let allCount = $('#all-missing-count').val();
  let watchedCount = $('#watched-missing-count').val();
  let thisCount = $('#this-missing-count').val();

  if (allCount === "0") {
    $('#total-missing-count-badge').remove();
  } else {
    $('#total-missing-count-badge').text(allCount);
  }

  if (thisCount === "0") {
    $('#this-missing-count-badge').remove();
  } else {
    $('#this-missing-count-badge').text(thisCount);
  }

  if (watchedCount === "0") {
    $('#watched-missing-count-badge').remove();
  } else {
    $('#watched-missing-count-badge .badge').text(watchedCount);
  }
}

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
      updateBadges();
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
