document.querySelector('.login.form form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('login.php', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Handle response from the server
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
