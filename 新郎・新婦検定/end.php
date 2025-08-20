<?php
session_start();
$_SESSION['end_time']  = microtime(true);
$_SESSION['elapsed_s'] = $_SESSION['end_time'] - $_SESSION['start_time'];
header('Location: result.php');
?>