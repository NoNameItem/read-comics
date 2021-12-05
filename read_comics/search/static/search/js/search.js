let $form = $('.search-bar #search-form');
let $categoryInput = $('.search-bar input#category');

$(document).ready(function (){
  $('a.category-select').click(function (e) {
    $categoryInput.val($(this).attr('data-category'));
    $form.submit();
  });
});
