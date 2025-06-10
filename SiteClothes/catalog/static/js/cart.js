function updateCartCounter(count) {
    const counters = document.querySelectorAll('.cart-counts');
    counters.forEach(counter => {
        if (typeof count !== 'undefined') {
            counter.textContent = count;
            counter.classList.add('counter-bounce');
            setTimeout(() => counter.classList.remove('counter-bounce'), 500);
        }
    });
}

function addToCart(productId, sizeId, urlTemplate, productTitle) {
    if (typeof closeModal === 'function') {
        closeModal(productId);
    }

    const addUrl = urlTemplate.replace('0', productId) + `?size_id=${sizeId}`;

    fetch(addUrl, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            showNotification('Добавлено в корзину', productTitle, 'success');
            updateCartCounter(data.total_quantity);
        } else {
            showNotification('Ошибка', data.message || 'Произошла ошибка', 'error');
        }
    }).catch(() => showNotification('Ошибка', 'Не удалось добавить товар', 'error'));
}