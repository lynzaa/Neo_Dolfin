const form = document.getElementById('reset-password-form');
const message = document.getElementById('message');
const emailField = document.getElementById('email');

form.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent default form submission

  const email = emailField.value.trim();

  emailField.classList.remove('error'); // Remove previous error styles

  try {
    const response = await fetch('/reset-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email }),
    });

    const data = await response.json();

    if (data.success) {
      message.textContent = 'A password reset link has been sent to your email.';
      form.reset(); // Clear form fields
    } else {
      message.textContent = data.error;
      emailField.classList.add('error'); // Add error style for invalid email
    }
  } catch (error) {
    console.error(error);
    message.textContent = 'An error occurred. Please try again later.';
  }
});
