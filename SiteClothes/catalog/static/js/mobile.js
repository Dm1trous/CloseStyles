// static/js/mobile.js

document.addEventListener('DOMContentLoaded', function() {

    const body = document.body;

    // --- 1. Логика для мобильного меню (бургер) ---
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const headerIcons = document.querySelector('.buy-profil');

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function(event) {
            event.stopPropagation();

            const isActive = mobileMenu.classList.toggle('active');
            menuToggle.classList.toggle('active', isActive);

            body.style.overflow = isActive ? 'hidden' : '';
            if (headerIcons) {
                headerIcons.style.display = isActive ? 'none' : 'flex';
            }
        });
    }

    // --- 2. Логика для мобильных фильтров в каталоге ---
    const openFiltersBtn = document.getElementById('open-mobile-filters');
    const closeFiltersBtn = document.getElementById('close-mobile-filters');
    const sidebar = document.getElementById('mobile-sidebar'); // Убедитесь, что у сайдбара есть этот ID

    if (openFiltersBtn && sidebar) {
        openFiltersBtn.addEventListener('click', function() {
            sidebar.classList.add('active');
            body.style.overflow = 'hidden';
        });
    }

    if (closeFiltersBtn && sidebar) {
        closeFiltersBtn.addEventListener('click', function() {
            sidebar.classList.remove('active');
            body.style.overflow = '';
        });
    }

    // --- 3. Общая логика для закрытия меню/фильтров по клику на фон ---
    document.addEventListener('click', function(event) {

        // Закрываем мобильное меню
        if (mobileMenu && mobileMenu.classList.contains('active')) {
            const isClickInsideMenu = mobileMenu.contains(event.target);
            const isClickOnToggle = menuToggle.contains(event.target);

            if (!isClickInsideMenu && !isClickOnToggle) {
                mobileMenu.classList.remove('active');
                menuToggle.classList.remove('active');
                body.style.overflow = '';
                if (headerIcons) headerIcons.style.display = 'flex';
            }
        }

        // Закрываем мобильные фильтры
        if (sidebar && sidebar.classList.contains('active')) {
            const isClickInsideSidebar = sidebar.contains(event.target);
            const isClickOnOpenBtn = openFiltersBtn.contains(event.target);

            if (!isClickInsideSidebar && !isClickOnOpenBtn) {
                 sidebar.classList.remove('active');
                 body.style.overflow = '';
            }
        }
    });

});