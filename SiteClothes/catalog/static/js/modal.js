// modal.js - обновленная версия

// Функции для работы с модальными окнами
function showModal(productId) {
    const modal = document.getElementById("cart-modal-" + productId);
    modal.style.display = "block";
}

function closeModal(productId) {
    const modal = document.getElementById("cart-modal-" + productId);
    modal.style.display = "none";
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        const modals = document.getElementsByClassName('modal');
        for (let i = 0; i < modals.length; i++) {
            modals[i].style.display = "none";
        }
    }
};

// Унифицированная функция показа уведомления
function showNotification(productTitle) {
    const notification = document.getElementById('notification');
    const notificationTitle = document.getElementById('notification-product-title');

    notificationTitle.textContent = productTitle;
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

// Функция добавления в корзину
function addToCart(productId, sizeId, addToCartUrl) {
    const productTitle = document.querySelector(`#cart-modal-${productId} .modal-title`).textContent;

    fetch(addToCartUrl.replace('0', productId) + '?size_id=' + sizeId, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            closeModal(productId);
            showNotification(productTitle);

            // Обновляем счетчик корзины в шапке (если есть)
            if (data.total_quantity) {
                const cartCounter = document.querySelector('.cart-counter');
                if (cartCounter) {
                    cartCounter.textContent = data.total_quantity;
                }
            }
        } else {
            alert(data.message || 'Произошла ошибка при добавлении товара в корзину');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при добавлении товара в корзину');
    });
}

// Обработка поиска по артикулу
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchQuery = this.querySelector('input[name="q"]').value.trim();

            // Проверяем, если поиск по артикулу (формат CLOSE-123)
            if (searchQuery.match(/^CLOSE-\d+$/i)) {
                e.preventDefault();
                const productId = searchQuery.split('-')[1];
                window.location.href = `/product/${productId}/`;
            }
        });
    }
});