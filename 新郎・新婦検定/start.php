<?php
if (session_status() === PHP_SESSION_NONE) session_start();

$_SESSION['start_time'] = microtime(true);   // 開始時刻を保存
$_SESSION['name'] = $_POST['name'];

// まずは動作確認のために結果へ（後でここを question1.php に変えればOK）
header('Location: question1.php');
exit;
