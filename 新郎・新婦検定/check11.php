<?php
session_start();


if (!isset($_POST['question11'])) {
  header('Location: question11.php');
  exit;
}

// セッションに保存
$_SESSION['question11'] = $_POST['question11'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question12.php');
exit;
