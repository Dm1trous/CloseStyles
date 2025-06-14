window.addEventListener('beforeunload', function() {
    localStorage.setItem('scrollPosition', window.pageYOffset);
});

document.addEventListener('DOMContentLoaded', function() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition, 10));
        localStorage.removeItem('scrollPosition');
    }
});