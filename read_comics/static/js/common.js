let csrftoken = Cookies.get('csrftoken'); // Получаем csrf-токен из куки

/**
 * @summary Проверяет, требует ли метод передачи csrf-токена
 * @param method - проверяемый метод
 * @returns {*|boolean} - Проверяемый метод не требует передачи csrf-токена
 */
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function showFullSize(elem) {
  let src = $(elem).attr('data-full-size-src') || $(elem).attr('src');
  $('#full-size-image').attr('src', src);
  $('#full-size-image-modal').modal('show');
}

// Добавляем в идентификацию ajax-запросов csrf-токен там, где это необходимо
$.ajaxSetup({
  beforeSend : function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

toastr.error_ = toastr.error;
toastr.error = function (a, b, c) {
  c = c || {};
  c.timeOut = 0;
  c.extendedTimeOut = 0;
  toastr.error_(a, b, c);
};

toastr.danger = toastr.error;

$(document).ready(function () {
  $('.image-full-size').click(function (e){
    showFullSize(e.target);
  });
})
