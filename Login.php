<?php
// Include the database connection
include('connection.php');

// Start the session
session_start();

// Check if the user is already logged in, then redirect to home
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    header("Location: home.php");
    exit;
}

// If login is successful, set the session variable
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get username and password from the form
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Query to find the user by username
    $stmt = $pdo->prepare('SELECT password FROM users WHERE username = ?');
    $stmt->execute([$username]);
    $stored_hash = $stmt->fetchColumn();
    
    // Check if password is correct
    if ($stored_hash && password_verify($password, $stored_hash)) {
        $_SESSION['loggedin'] = true;
        header("Location: home.php");
        exit;
    } else {
        echo "Invalid login credentials.";
    }
}
?>

<!-- Login form -->
<form method="POST">
    Username: <input type="text" name="username"><br>
    Password: <input type="password" name="password"><br>
    <input type="submit" value="Login">
</form>
