function updateFavoriteCounter(count) {
    const counters = document.querySelectorAll('.favorite-counts');
    counters.forEach(counter => {
        if (typeof count !== 'undefined') {
            counter.textContent = count;
            counter.classList.add('counter-bounce');
            setTimeout(() => counter.classList.remove('counter-bounce'), 500);
        }
    });
}

function toggleFavorite(productId, buttonElement, csrfToken) {
    const isFavorite = buttonElement.classList.contains('in-favorites');
    const url = isFavorite ? `/favorites/remove/${productId}/` : `/favorites/add/${productId}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        },
        credentials: 'same-origin'
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            buttonElement.classList.toggle('in-favorites');
            const favoriteText = buttonElement.querySelector('.favorite-text');
            if (favoriteText) {
                favoriteText.textContent = buttonElement.classList.contains('in-favorites') ? 'В избранном' : 'В избранное';
            }
            updateFavoriteCounter(data.favorites_count);
            showNotification(
                buttonElement.classList.contains('in-favorites') ? 'Добавлено в избранное' : 'Удалено из избранного',
                data.product_title,
                'success'
            );
        } else {
            showNotification('Ошибка', data.message, 'error');
        }
    });
}