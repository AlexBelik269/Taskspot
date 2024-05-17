document.addEventListener("DOMContentLoaded", function () {
    const taskData = [
        { title: "Task 1", place: "Location 1", description: "Description 1", price: "$50" },
        { title: "Task 2", place: "Location 2", description: "Description 2", price: "$60" },
        { title: "Task 3", place: "Location 3", description: "Description 3", price: "$70" },
        { title: "Task 1", place: "Location 1", description: "Description 1", price: "$50" },
        { title: "Task 2", place: "Location 2", description: "Description 2", price: "$60" },
        { title: "Task 3", place: "Location 3", description: "Description 3", price: "$70" },
        { title: "Task 1", place: "Location 1", description: "Description 1", price: "$50" },
        { title: "Task 2", place: "Location 2", description: "Description 2", price: "$60" },
        { title: "Task 3", place: "Location 3", description: "Description 3", price: "$70" }
    ];  

    const taskContainer = document.getElementById("taskContainer");

    taskData.forEach(task => {
        const taskBox = document.createElement("div");
        taskBox.classList.add("task-box");

        const title = document.createElement("div");
        title.classList.add("task-title");
        title.textContent = task.title;

        const place = document.createElement("div");
        place.classList.add("task-details");
        place.textContent = "Place: " + task.place;

        const description = document.createElement("div");
        description.classList.add("task-details");
        description.textContent = "Description: " + task.description;

        const price = document.createElement("div");
        price.classList.add("task-details");
        price.textContent = "Offered Price: " + task.price;

        const takeTaskButton = document.createElement("button");
        takeTaskButton.textContent = "Take this Task!";
        takeTaskButton.classList.add("take-task-button"); // Adding the class to the button
        takeTaskButton.addEventListener("click", function() {
            // Create and display the popup window
            const popup = document.createElement("div");
            popup.classList.add("popup");

            const taskInfo = document.createElement("div");
            taskInfo.classList.add("task-info");

            const taskTitle = document.createElement("h2");
            taskTitle.textContent = task.title;

            const taskPlace = document.createElement("p");
            taskPlace.textContent = "Place: " + task.place;

            const taskDescription = document.createElement("p");
            taskDescription.textContent = "Description: " + task.description;

            const taskPrice = document.createElement("p");
            taskPrice.textContent = "Offered Price: " + task.price;

            const messageLabel = document.createElement("label");
            messageLabel.textContent = "Message:";
            const messageInput = document.createElement("textarea");
            messageInput.classList.add("message-input");

            const confirmButton = document.createElement("button");
            confirmButton.textContent = "Confirm";
            confirmButton.addEventListener("click", function() {
                // Close the popup window
                popup.remove();
                // You can add logic here to handle the confirmation
            });

            taskInfo.appendChild(taskTitle);
            taskInfo.appendChild(taskPlace);
            taskInfo.appendChild(taskDescription);
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
        taskBox.appendChild(price);
        taskBox.appendChild(takeTaskButton);

        taskContainer.appendChild(taskBox);
    });
});
