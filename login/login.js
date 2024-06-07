document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('.button[value="Login"]').addEventListener('click', login);
  document.querySelector('.button[value="Signup"]').addEventListener('click', signup);
});

function login() {
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPassword').value;
  const loginError = document.getElementById('loginError');

  fetch('http://localhost:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('sessionID', data.sessionID); // Store session ID
      window.location.href = '../home.html';
    } else {
      loginError.textContent = 'Incorrect email or password';
      document.getElementById('loginEmail').classList.add('error');
      document.getElementById('loginPassword').classList.add('error');
    }
  })
  .catch(error => console.error('Error:', error));
}



function signup() {
  const email = document.getElementById('signupEmail').value;
  const password = document.getElementById('signupPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const username = document.getElementById('signupUsername').value;
  const city = document.getElementById('signupCity').value;
  const signupError = document.getElementById('signupError');

  if (password !== confirmPassword) {
    signupError.textContent = 'Passwords do not match';
    document.getElementById('signupPassword').classList.add('error');
    document.getElementById('confirmPassword').classList.add('error');
    return;
  }

  fetch('http://localhost:5000/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password, username, city }),
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      localStorage.setItem('isLoggedIn', 'true');
      window.location.href = '../home.html';
    } else {
      signupError.textContent = 'Signup failed: ' + data.message;
      document.getElementById('signupEmail').classList.add('error');
    }
  })
  .catch(error => console.error('Error:', error));
}
