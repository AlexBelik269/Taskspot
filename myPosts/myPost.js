document.addEventListener('DOMContentLoaded', function () {
    fetchUserData();
    fetchUserMessages();
    fetchUserJobPosts();
});

function fetchUserData() {
    fetch('http://localhost:5000/user')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                document.getElementById('user-username').textContent = data.username;
            }
        })
        .catch(error => console.error('Error fetching user data:', error));
}

function fetchUserMessages() {
    fetch('http://localhost:5000/user_messages')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const messageList = document.getElementById('message-list');
            if (messageList) {
                messageList.innerHTML = '';
                if (data.messages && data.messages.length) {
                    data.messages.forEach(message => createMessageItem(message, messageList));
                } else {
                    messageList.textContent = 'No messages yet.';
                }
            }
        })
        .catch(error => console.error('Error fetching messages:', error));
}

function fetchUserJobPosts() {
    fetch('http://localhost:5000/user_job_posts')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const jobPostList = document.getElementById('job-post-list');
            if (jobPostList) {
                jobPostList.innerHTML = '';
                if (data.jobPosts && data.jobPosts.length) {
                    data.jobPosts.forEach(post => createJobPostItem(post, jobPostList));
                } else {
                    jobPostList.textContent = 'No job posts yet.';
                }
            }
        })
        .catch(error => console.error('Error fetching job posts:', error));
}




function createMessageItem(message, container) {
    const messageItem = document.createElement('div');
    messageItem.classList.add('message-item');

    const messageText = document.createElement('p');
    messageText.textContent = `From ${message.sender}: ${message.text}`;

    const messageFeedback = document.createElement('div');
    messageFeedback.classList.add('message-feedback');

    const feedbackIcon = document.createElement('i');
    feedbackIcon.classList.add('fas');
    setFeedbackIcon(feedbackIcon, message.feedback);

    messageFeedback.appendChild(feedbackIcon);
    messageItem.appendChild(messageText);
    messageItem.appendChild(messageFeedback);
    container.appendChild(messageItem);
}

function setFeedbackIcon(icon, feedback) {
    switch (feedback) {
        case 'accepted':
            icon.classList.add('fa-check', 'accepted');
            break;
        case 'rejected':
            icon.classList.add('fa-times', 'rejected');
            break;
        default:
            icon.classList.add('fa-question', 'pending');
            break;
    }
}

function createJobPostItem(jobPost, container) {
    const jobPostItem = document.createElement('div');
    jobPostItem.classList.add('job-post-item');

    const jobPostTitle = document.createElement('h4');
    jobPostTitle.textContent = jobPost.title;
    jobPostItem.appendChild(jobPostTitle);

    if (jobPost.messages.length === 0) {
        const noMessagesText = document.createElement('p');
        noMessagesText.textContent = 'No messages yet.';
        jobPostItem.appendChild(noMessagesText);
    } else {
        jobPost.messages.forEach(message => createJobPostMessageItem(message, jobPostItem));
    }

    container.appendChild(jobPostItem);
}

function createJobPostMessageItem(message, container) {
    const messageItem = document.createElement('div');
    messageItem.classList.add('message-item');

    const messageText = document.createElement('p');
    messageText.textContent = `${message.sender}: ${message.text}`;

    const messageControls = document.createElement('div');
    messageControls.classList.add('message-controls');

    const acceptIcon = document.createElement('i');
    acceptIcon.classList.add('fas', 'fa-check');
    acceptIcon.addEventListener('click', () => handleFeedback(message.messageID, 'accepted'));

    const rejectIcon = document.createElement('i');
    rejectIcon.classList.add('fas', 'fa-times');
    rejectIcon.addEventListener('click', () => handleFeedback(message.messageID, 'rejected'));

    messageControls.appendChild(acceptIcon);
    messageControls.appendChild(rejectIcon);

    messageItem.appendChild(messageText);
    messageItem.appendChild(messageControls);

    container.appendChild(messageItem);
}

function handleFeedback(messageID, feedback) {
    fetch('http://localhost:5000/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messageID, feedback }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Feedback sent:', data);
        window.location.reload();
    })
    .catch(error => console.error('Error sending feedback:', error));
}
