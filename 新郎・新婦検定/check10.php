<?php
session_start();


if (!isset($_POST['question10'])) {
  header('Location: question10.php');
  exit;
}

// セッションに保存
$_SESSION['question10'] = $_POST['question10'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question11.php');
exit;
