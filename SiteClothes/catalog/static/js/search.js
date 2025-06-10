document.addEventListener('DOMContentLoaded', function() {
    const searchForms = document.querySelectorAll('form.search-form');

    searchForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const searchInput = form.querySelector('input[name="q"]');
            if (!searchInput) return;

            const query = searchInput.value.trim();

            const articleMatch = query.match(/^CLOSE-(\d+)$/i);

            if (articleMatch) {
                event.preventDefault();
                const productId = articleMatch[1];
                window.location.href = `/product/${productId}/`;
            }
        });
    });
});