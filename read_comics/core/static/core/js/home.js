$(document).ready(function () {
  $('.started_not_finished').slick({
    dots           : true,
    infinite       : true,
    speed          : 300,
    slidesToShow   : 4,
    slidesToScroll : 4,
    autoplay       : true,
    autoplaySpeed  : 6000,
    arrows         : false,
    responsive     : [
      {
        breakpoint : 2500,
        settings   : {
          slidesToShow   : 3,
          slidesToScroll : 3,

        }
      },
      {
        breakpoint : 2000,
        settings   : {
          slidesToShow   : 2,
          slidesToScroll : 2,

        }
      },
      {
        breakpoint : 900,
        settings   : {
          slidesToShow   : 3,
          slidesToScroll : 3,

        }
      },
      {
        breakpoint : 600,
        settings   : {
          slidesToShow   : 2,
          slidesToScroll : 2,
        }
      },
      {
        breakpoint : 400,
        settings   : {
          slidesToShow   : 1,
          slidesToScroll : 1,
          dots           : false
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });
});
