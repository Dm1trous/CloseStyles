document.addEventListener('DOMContentLoaded', function() {
    const promocodeForm = document.getElementById('promocode-form');
    if (!promocodeForm) return;

    promocodeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelector('.cart-promo').textContent = `- ${data.discount_amount} ₽`;
                document.querySelector('.cart-title-summ').textContent = `${data.final_total} ₽`;
                this.querySelector('button').textContent = 'Обновить';

                document.querySelector('.promocode-applied-group')?.remove();
                this.insertAdjacentHTML('afterend', `
                    <div class="promocode-applied-group">
                        <p class="promocode-applied">Применен: ${data.promocode_code} (скидка ${data.discount_percentage}%)</p>
                    </div>`);

                showNotification('Промокод применен!', `Ваша скидка: ${data.discount_amount} ₽`, 'success');
            } else {
                showNotification('Ошибка', data.message || 'Неверный промокод', 'error');
            }
        })
        .catch(() => showNotification('Сетевая ошибка', 'Не удалось применить промокод.', 'error'));
    });
});
