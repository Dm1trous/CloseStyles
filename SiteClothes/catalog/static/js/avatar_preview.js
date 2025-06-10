document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('avatar-preview');
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(event) {
            if (event.target.files && event.target.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                }

                reader.readAsDataURL(event.target.files[0]);
            }
        });
    }
});