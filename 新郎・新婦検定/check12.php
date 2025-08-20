<?php
session_start();


if (!isset($_POST['question12'])) {
  header('Location: question12.php');
  exit;
}

// セッションに保存
$_SESSION['question12'] = $_POST['question12'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: end.php');
exit;
