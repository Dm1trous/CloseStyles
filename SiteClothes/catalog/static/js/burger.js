// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- Логика для мобильного меню (ИСПРАВЛЕННАЯ ВЕРСИЯ) ---
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const body = document.body;

    // Проверяем, что все элементы существуют на странице
    if (menuToggle && mobileMenu) {

        menuToggle.addEventListener('click', function(event) {
            // Предотвращаем "прокликивание" на элементы под кнопкой
            event.stopPropagation();

            // Переключаем классы для анимаций
            mobileMenu.classList.toggle('active');
            menuToggle.classList.toggle('active');

            // Блокируем или разблокируем прокрутку страницы
            if (mobileMenu.classList.contains('active')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        });

        // Добавляем обработчик, чтобы закрыть меню при клике ВНЕ его области
        document.addEventListener('click', function(event) {
            // Проверяем, что меню открыто и клик был не по меню и не по кнопке
            const isClickInsideMenu = mobileMenu.contains(event.target);
            const isClickOnToggle = menuToggle.contains(event.target);

            if (mobileMenu.classList.contains('active') && !isClickInsideMenu && !isClickOnToggle) {
                mobileMenu.classList.remove('active');
                menuToggle.classList.remove('active');
                body.style.overflow = '';
            }
        });
    }

    // --- Сюда можно будет перенести другие ваши глобальные функции ---

});