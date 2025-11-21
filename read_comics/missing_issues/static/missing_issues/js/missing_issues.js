let treeInitiated = false;

function updateBadges() {
  let allCount = $('#all-missing-count').val();
  let watchedCount = $('#watched-missing-count').val();
  let thisCount = $('#this-missing-count').val();

  const $title = $('title');

  if (allCount === "0") {
    $('#total-missing-count-badge').remove();
  } else {
    $('#total-missing-count-badge').text(allCount);
  }

  if (thisCount === "0") {
    $('#this-missing-count-badge').remove();
    $title.text($title.text().replace(/\([0-9,]+\)/, ""));
  } else {
    $('#this-missing-count-badge').text(thisCount);
    $title.text($title.text().replace(/\([0-9,]+\)/, "(" + thisCount + ")"));
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
    const scrollPosition = $('#inner-table-wrapper').scrollTop();
    $.ajax({
      url  : url,
      type : 'GET'
    }).done(function (data, textStatus, jqXHR) {
      $('#table-wrapper').html(data);
      $('#inner-table-wrapper').scrollTop(scrollPosition);
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
  $('.space-path').click(function () {
    navigator.clipboard.writeText($(this).text());
  });
}

function startReload(){
  let checked = $('#jstree_do').jstree(true).get_checked(true);
  let data = [];
  for (let i=0; i<checked.length; i++) {
    data.push({
      'key'   : checked[i].original.full_name,
      'size'   : checked[i].original.size,
      'level' : checked[i].parents.length
    });
  }

  console.debug(data);

  if (data.length > 0) {
    $.ajax({
      url         : start_reload_url,
      type        : 'POST',
      contentType : 'application/json; charset=utf-8',
      data        : JSON.stringify({data : data})
    }).done(function (data, textStatus, jqXHR) {
      if (data.status === 'success') {
        toastr.success("Reload started");
      } else {
        toastr.error(data.error, "Could not start reload");
      }
    }).fail(function (jqXHR, textStatus, errorThrown) {
      if (jqXHR.status === 404 || jqXHR.status === 500) {
        toastr.error("", "Please refresh page");
      }
    });
  }
}

$(document).ready(function () {
  initButtons();
  initCopy();

  $('#doReloadModal').on('shown.bs.modal', function () {
    if (!treeInitiated) {
      $('#jstree_do').jstree({
          "plugins"  : ["checkbox"],
          "checkbox" : {
            "three_state" : false,

          },
          'core'     : {
            'data' : {
              'url' : function (node) {
                return node.id === '#' ?
                  do_root_url :
                  node.original.children_link;
              },
            }
          }
        }
      );
    }
  });

  $('#start-reload-btn').click(startReload);

  $('#purge-deleted-btn').click(function () {
    $.ajax({
        type : 'POST',
        url  : purge_deleted_url
      }
    ).done(function (response) {
      if (response.status === 'success') {
        toastr.success("Purge of deleted issues started");
      } else {
        toastr.error( response.message, "Oops! Can't start purge of deleted issues");
      }
    })
  });

});
