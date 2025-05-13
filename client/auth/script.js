// Only for enhancing form submission UX - auth is handled server-side
document.addEventListener('DOMContentLoaded', () => {
  // Form submission indicators
  const setLoading = (form, isLoading) => {
      const button = form.querySelector('button[type="submit"]');
      if (button) {
          button.disabled = isLoading;
          button.textContent = isLoading ? 'Processing...' : button.dataset.originalText;
      }
  };

  // Initialize all forms
  document.querySelectorAll('form').forEach(form => {
      const button = form.querySelector('button[type="submit"]');
      if (button) button.dataset.originalText = button.textContent;

      form.addEventListener('submit', () => {
          setLoading(form, true);
      });
  });

  // Flash message fade-out
  const flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach(msg => {
      setTimeout(() => {
          msg.style.opacity = '0';
          setTimeout(() => msg.remove(), 500);
      }, 3000);
  });
});