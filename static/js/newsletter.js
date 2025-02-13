document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletter-form');
    const messageDiv = document.getElementById('newsletter-message');

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            
            // Disable submit button and show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subscribing...';

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Show message
                messageDiv.textContent = data.message;
                messageDiv.className = `alert alert-${data.status === 'success' ? 'success' : 'danger'} mt-3`;
                messageDiv.style.display = 'block';

                // Reset form if subscription was successful
                if (data.status === 'success') {
                    newsletterForm.reset();
                }

                // Scroll message into view
                messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = 'An error occurred. Please try again later.';
                messageDiv.className = 'alert alert-danger mt-3';
                messageDiv.style.display = 'block';
                messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            })
            .finally(() => {
                // Re-enable submit button and restore original text
                submitButton.disabled = false;
                submitButton.innerHTML = originalButtonText;
            });
        });
    }
});