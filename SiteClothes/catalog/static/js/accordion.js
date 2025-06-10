document.addEventListener('DOMContentLoaded', function () {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.nextElementSibling;
            const icon = button.querySelector('span:last-child');
            const isCurrentlyOpen = answer.style.maxHeight;
            document.querySelectorAll('.faq-answer').forEach(el => {
                if (el !== answer) {
                    el.style.maxHeight = null;
                    const otherIcon = el.previousElementSibling.querySelector('span:last-child');
                    if (otherIcon) {
                        otherIcon.textContent = '+';
                    }
                }
            });
            if (isCurrentlyOpen) {
                answer.style.maxHeight = null;
                if (icon) {
                    icon.textContent = '+';
                }
            } else {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                if (icon) {
                    icon.textContent = '−';
                }
            }
        });
    });
});