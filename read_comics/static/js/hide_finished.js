let $hideFinished = $('#hide_finished');

$(document).ready(function () {
  $hideFinished.change(function () {
    if ($hideFinished.prop("checked"))
      window.location.href = '?hide_finished=yes'
    else
      window.location.href = '?hide_finished=no'
  })
});
