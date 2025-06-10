function showNotification(title, subtitle = '', type = 'info', duration = 3000) {
    const notification = document.getElementById('global-notification');
    if (!notification) return;

    const titleEl = notification.querySelector('.notification-title');
    const subtitleEl = notification.querySelector('.notification-subtitle');
    const iconEl = notification.querySelector('.notification-icon');

    titleEl.textContent = title;
    subtitleEl.textContent = subtitle;
    subtitleEl.style.display = subtitle ? 'block' : 'none';

    switch (type) {
        case 'success': iconEl.textContent = '✓'; break;
        case 'error': iconEl.textContent = '❌'; break;
        default: iconEl.textContent = 'ℹ️'; break;
    }
    notification.className = `notification show ${type}`;

    setTimeout(() => notification.classList.remove('show'), duration);
}