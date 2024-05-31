document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("postJobForm");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const city = document.getElementById("city").value;
        const duration = document.getElementById("duration").value;
        const price = document.getElementById("price").value;

        if (title && description && city && duration && price) {
            const formData = new FormData();
            formData.append('title', title);
            formData.append('description', description);
            formData.append('city', city);
            formData.append('duration', duration);
            formData.append('price', price);

            fetch('http://localhost:5000/save_task', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = '../get-job/get-job.html';
                } else {
                    alert('Failed to save the task. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            alert('Please fill out all fields.');
        }
    });
});
