<?php
session_start();


if (!isset($_POST['question8'])) {
  header('Location: question8.php');
  exit;
}

// セッションに保存
$_SESSION['question8'] = $_POST['question8'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question9.php');
exit;
