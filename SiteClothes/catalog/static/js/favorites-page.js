function removeFromFavoritesPage(productId, csrfToken) {
    event.preventDefault();

    const url = `/favorites/remove/${productId}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const itemToRemove = document.querySelector(`.favorite-item[data-product-id="${productId}"]`);
            if (itemToRemove) {
                itemToRemove.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                itemToRemove.style.opacity = '0';
                itemToRemove.style.transform = 'scale(0.95)';

                setTimeout(() => {
                    itemToRemove.remove();
                    checkIfFavoritesEmpty();
                }, 300);
            }

            updateFavoriteCounter(data.favorites_count);
            showNotification('Удалено из избранного', data.product_title, 'success');
        } else {
            showNotification('Ошибка', data.message || 'Не удалось удалить товар.', 'error');
        }
    })
    .catch(error => {
        showNotification('Ошибка', 'Не удалось выполнить запрос. Попробуйте обновить страницу.', 'error');
    });
}

function addToCartFromFavorites(productId, urlTemplate) {
    const sizeSelect = document.getElementById(`sizeSelect${productId}`);
    const sizeError = document.getElementById(`sizeError${productId}`);
    const selectedSizeId = sizeSelect.value;

    if (!selectedSizeId) {
        sizeError.textContent = 'Пожалуйста, выберите размер';
        return;
    }

    sizeError.textContent = '';

    const productTitleElement = document.querySelector(`.favorite-item[data-product-id="${productId}"] .item-title a`);
    const productTitle = productTitleElement ? productTitleElement.textContent.trim() : 'Товар';

    if (typeof addToCart === 'function') {
        addToCart(productId, selectedSizeId, urlTemplate, productTitle);
    } else {
        showNotification('Ошибка', 'Функция добавления в корзину не найдена.', 'error');
    }
}

function checkIfFavoritesEmpty() {
    const container = document.querySelector('.favorites-items');
    if (container && container.children.length === 0) {
        const favoritesContainer = document.querySelector('.favorites-container');
        const emptyFavoritesHTML = `
            <div class="empty-favorites">
                <div class="empty-icon">❤</div>
                <h3>Ваш список избранного пуст</h3>
                <p>Добавляйте понравившиеся товары, нажимая на соответствующую кнопку</p>
                <a href="/products/" class="browse-btn">Перейти в каталог</a>
            </div>`;

        if(favoritesContainer) {
            favoritesContainer.innerHTML = emptyFavoritesHTML;
        }
    }
}