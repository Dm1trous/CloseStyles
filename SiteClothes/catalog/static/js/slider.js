document.addEventListener("DOMContentLoaded", function() {
    const slidesContainer = document.querySelector(".slides");
    if (!slidesContainer) return;

    const slides = slidesContainer.querySelectorAll(".slide");
    const slideCount = slides.length;
    if (slideCount <= 1) return;

    const firstSlideClone = slides[0].cloneNode(true);
    slidesContainer.appendChild(firstSlideClone);

    let currentSlideIndex = 0;
    const slideWidth = slides[0].clientWidth;

    function showNextSlide() {
        currentSlideIndex++;

        slidesContainer.style.transition = 'transform 0.7s ease-in-out';
        slidesContainer.style.transform = `translateX(-${currentSlideIndex * slideWidth}px)`;

        if (currentSlideIndex === slideCount) {
            setTimeout(() => {
                slidesContainer.style.transition = 'none';
                currentSlideIndex = 0;
                slidesContainer.style.transform = `translateX(0)`;
            }, 700);
        }
    }

    setInterval(showNextSlide, 5000);
});