document.addEventListener('DOMContentLoaded', function () {
    let selectedSizeId = null;

    const addToCartBtn = document.getElementById('addToCartBtn');
    const sizeOptionsContainer = document.getElementById('sizeOptionsContainer');
    const sizeErrorMessage = document.getElementById('sizeErrorMessage');
    const tabsContainer = document.querySelector('.tabs-header');

    if (sizeOptionsContainer) {
        sizeOptionsContainer.addEventListener('click', function(event) {
            const target = event.target;
            if (target.classList.contains('js-size-select')) {
                sizeOptionsContainer.querySelectorAll('.js-size-select').forEach(btn => {
                    btn.classList.remove('selected');
                });
                target.classList.add('selected');
                selectedSizeId = target.dataset.sizeId;
                if (addToCartBtn) {
                    addToCartBtn.disabled = false;
                }
                if (sizeErrorMessage) {
                    sizeErrorMessage.textContent = '';
                }
            }
        });
    }

    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function() {
            if (!selectedSizeId) {
                if (sizeErrorMessage) {
                    sizeErrorMessage.textContent = 'Пожалуйста, выберите размер';
                }
                return;
            }
            const productId = this.dataset.productId;
            const productTitle = this.dataset.productTitle;
            const urlTemplate = this.dataset.urlTemplate;

            if (typeof addToCart === 'function') {
                addToCart(productId, selectedSizeId, urlTemplate, productTitle);
            }
        });
    }

    if (tabsContainer) {
        tabsContainer.addEventListener('click', function(event) {
            const target = event.target;
            if (target.classList.contains('js-tab-btn')) {
                const tabId = target.dataset.tab;

                tabsContainer.querySelectorAll('.js-tab-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

                target.classList.add('active');
                const contentToShow = document.getElementById(`${tabId}-content`);
                if(contentToShow) {
                    contentToShow.classList.add('active');
                }
            }
        });
    }
});