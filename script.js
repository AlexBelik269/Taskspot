document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in (this can be replaced with real authentication logic)
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    updateNavLinks(isLoggedIn);
});

function updateNavLinks(isLoggedIn) {
    const navLinks = document.getElementById('nav-links');
    navLinks.innerHTML = ''; // Clear existing links

    if (isLoggedIn) {
        navLinks.innerHTML += '<li><a href="myJob.html">My Job Post</a></li>';
    } else {
        navLinks.innerHTML += '<li><a href="login/login.html">Login/Register <i class="fas fa-sign-in-alt"></i></a></li>';
    }
}

function handleGetJob() {
    window.location.href = 'get-job/get-job.html';
}

function handlePostJob() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (isLoggedIn) {
        window.location.href = 'post-job/post-job.html';
    } else {
        showModal();
    }
}

function showModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'none';
}