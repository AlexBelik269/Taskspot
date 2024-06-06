document.addEventListener('DOMContentLoaded', function() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    updateNavLinks(isLoggedIn);
});

function updateNavLinks(isLoggedIn) {
    const navLinks = document.getElementById('nav-links');
    navLinks.innerHTML = ''; // Clear existing links

    if (isLoggedIn) {
        navLinks.innerHTML += '<li><a href="myPosts/myPost.html">My Job Postings  </a></li>';
        navLinks.innerHTML += '<li><a href="#" onclick="handleLogout()">   Logout</a></li>';
    } else {
        navLinks.innerHTML += '<li><a href="login/login.html">Login/Signup <i class="fas fa-sign-in-alt"></i></a></li>';
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

function handleLogout() {
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'home.html';
}
