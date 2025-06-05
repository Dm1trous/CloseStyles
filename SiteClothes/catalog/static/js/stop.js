window.onbeforeunload = function(event) {
    var currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
    localStorage.setItem('scrollPosition', currentScrollPosition);
};
document.addEventListener('DOMContentLoaded', function() {
    var savedScrollPosition = parseInt(localStorage.getItem('scrollPosition'));
    if (!isNaN(savedScrollPosition)) {
        window.scrollTo(0, savedScrollPosition);
    }
});