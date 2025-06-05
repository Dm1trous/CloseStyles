document.addEventListener("DOMContentLoaded", function() {
    const slidesElement = document.querySelector(".slides");
    const slidesCount = document.querySelectorAll(".slide").length;
    let currentSlideIndex = 0;

    function showNextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % slidesCount;
        slidesElement.style.transform = `translateX(-${currentSlideIndex * 100}vw)`;
    }

    setInterval(showNextSlide, 5000);
});


document.addEventListener("DOMContentLoaded", function() {
    const favoriteButtons = document.querySelectorAll('.btn-favorite');
    const cartButtons = document.querySelectorAll('.btn-cart');

    favoriteButtons.forEach(btn => btn.addEventListener('click'));
    cartButtons.forEach(btn => btn.addEventListener('click'));
});

