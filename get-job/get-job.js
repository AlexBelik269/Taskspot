document.addEventListener("DOMContentLoaded", function () {
    fetch('http://localhost:5000/tasks')
        .then(response => response.json())
        .then(taskData => {
            const taskContainer = document.getElementById("taskContainer");

            taskData.forEach(task => {
                const taskBox = document.createElement("div");
                taskBox.classList.add("task-box");

                const title = document.createElement("div");
                title.classList.add("task-title");
                title.textContent = task.title;

                const place = document.createElement("div");
                place.classList.add("task-details");
                place.textContent = "Place: " + task.city;

                const description = document.createElement("div");
                description.classList.add("task-details");
                description.textContent = "Description: " + task.description;

                const duration = document.createElement("div");
                duration.classList.add("task-duration");
                duration.textContent = "Duration: " + task.duration;

                const price = document.createElement("div");
                price.classList.add("task-details");
                price.textContent = "Offered Price: " + task.price;

                const takeTaskButton = document.createElement("button");
                takeTaskButton.textContent = "Take this Task!";
                takeTaskButton.classList.add("take-task-button");
                takeTaskButton.addEventListener("click", function() {
                    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
                    if (!isLoggedIn) {
                        showModal();
                        return;
                    }

                    // Create and display the popup window
                    const popup = document.createElement("div");
                    popup.classList.add("popup");

                    const taskInfo = document.createElement("div");
                    taskInfo.classList.add("task-info");

                    const taskTitle = document.createElement("h2");
                    taskTitle.textContent = task.title;

                    const taskPlace = document.createElement("p");
                    taskPlace.textContent = "Place: " + task.city;

                    const taskDescription = document.createElement("p");
                    taskDescription.textContent = "Description: " + task.description;

                    const taskDuration = document.createElement("p");
                    taskDuration.textContent = "Duration: " + task.duration;

                    const taskPrice = document.createElement("p");
                    taskPrice.textContent = "Offered Price: " + task.price;

                    const messageLabel = document.createElement("label");
                    messageLabel.textContent = "Message:";
                    const messageInput = document.createElement("textarea");
                    messageInput.classList.add("message-input");

                    const confirmButton = document.createElement("button");
                    confirmButton.textContent = "Confirm";
                    confirmButton.addEventListener("click", function() {
                        const messageText = messageInput.value;
                        
                        // Send message to the server
                        const formData = new FormData();
                        formData.append('text', messageText);
                        formData.append('fk_taskID', task.taskID);

                        fetch('http://localhost:5000/save_message', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Success:', data);
                            // Close the popup window
                            popup.remove();
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                    });

                    taskInfo.appendChild(taskTitle);
                    taskInfo.appendChild(taskPlace);
                    taskInfo.appendChild(taskDescription);
                    taskInfo.appendChild(taskDuration);
                    taskInfo.appendChild(taskPrice);

                    popup.appendChild(taskInfo);
                    popup.appendChild(messageLabel);
                    popup.appendChild(messageInput);
                    popup.appendChild(confirmButton);

                    document.body.appendChild(popup);
                });

                taskBox.appendChild(title);
                taskBox.appendChild(place);
                taskBox.appendChild(description);
                taskBox.appendChild(duration);
                taskBox.appendChild(price);
                taskBox.appendChild(takeTaskButton);

                taskContainer.appendChild(taskBox);
            });
        })
        .catch(error => console.error('Error fetching tasks:', error));
});


function showModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('loginModal');
    modal.style.display = 'none';
}

