document.addEventListener('DOMContentLoaded', function() {
    const notificationTrigger = document.getElementById('order-success-notification');

    if (notificationTrigger) {
        const message = notificationTrigger.dataset.message;

        if (message) {
            showNotification('Заказ оформлен!', message, 'success');
        }
    }
});