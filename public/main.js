
/* ================== Typed Text Section ================== */

var typed = new Typed(".autoType", {
  strings: ["Popular", "Bestselling"],
  typespeed: 0, 
  backspeed: 0,
  loop: true
})


/* ================== Hamburger ================== */

/* ================== Swiper Section ================== */

var swiper = new Swiper(".mySwiper", {
  slidesPerView: 1,
  spaceBetween: 30,
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});



