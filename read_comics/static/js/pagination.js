$(document).ready(function () {
  let p = $('#pagination');
  p.twbsPagination({
    totalPages             : Number(p.attr('data-page-count')),
    startPage              : Number(p.attr('data-current-page')),
    visiblePages           : 10,
    initiateStartPageClick : false,
    paginationClass        : 'pagination justify-content-center pagination-borderless',
    href                   : true,
    pageVariable           : 'page',
    first                  : '<i class="fad fa-chevron-double-left"></i>',
    prev                   : '<i class="fad fa-chevron-left"></i>',
    next                   : '<i class="fad fa-chevron-right"></i>',
    last                   : '<i class="fad fa-chevron-double-right"></i>',
  });
});
