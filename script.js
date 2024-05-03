
function login(event) {
    event.preventDefault(); // Prevent form submission

    // Get username and password values from the form
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Here you can add code to send a request to your server to handle the login process
    // For now, let's just display a message based on the entered credentials
    if (username === 'admin' && password === 'password') {
        alert('Login successful!');
    } else {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = 'Invalid username or password.';
        errorMessage.classList.remove('hidden');
    }
}



