<?php
session_start();


if (!isset($_POST['question7'])) {
  header('Location: question7.php');
  exit;
}

// セッションに保存
$_SESSION['question7'] = $_POST['question7'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question8.php');
exit;
