function showModal(productId) {
    const modal = document.getElementById(`cart-modal-${productId}`);
    if (modal) {
        modal.style.display = "block";
    }
}

function closeModal(productId) {
    const modal = document.getElementById(`cart-modal-${productId}`);
    if (modal) {
        modal.style.display = "none";
    }
}

window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
});