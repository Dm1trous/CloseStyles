document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort-by');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            this.closest('form').submit();
        });
    }

    const paginationLinks = document.querySelectorAll('.pagination a.page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const currentParams = new URLSearchParams(window.location.search);

            const pageUrl = new URL(this.href);
            const pageNumber = pageUrl.searchParams.get('page');

            currentParams.set('page', pageNumber);

            window.location.href = `${window.location.pathname}?${currentParams.toString()}`;
        });
    });
});