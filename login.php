<?php
// Establish a connection to your MySQL database
$mysqli = new mysqli('localhost', 'username', 'password', 'database_name');

// Check for connection errors
if ($mysqli->connect_errno) {
    die('Connection Error: ' . $mysqli->connect_error);
}

// Get username and password from the POST request
$username = $_POST['email'];
$password = $_POST['password'];

// Query the database to check if the user exists
$query = "SELECT * FROM users WHERE username = ? AND password = ?";
$stmt = $mysqli->prepare($query);
$stmt->bind_param('ss', $username, $password);
$stmt->execute();
$result = $stmt->get_result();

// Check if any rows were returned
if ($result->num_rows === 1) {
    // User exists and credentials are correct
    echo 'success';
} else {
    // User does not exist or credentials are incorrect
    echo 'failure';
}

// Close the prepared statement and the database connection
$stmt->close();
$mysqli->close();
?>
