let $onlyWithIssues = $('#only_with_issues');

$(document).ready(function () {
  $onlyWithIssues.change(function () {
    if ($onlyWithIssues.prop("checked"))
      window.location.href = '?only-with-issues=yes'
    else
      window.location.href = '?only-with-issues=no'
  })
});
