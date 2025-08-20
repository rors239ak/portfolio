<?php
session_start();


if (!isset($_POST['question6'])) {
  header('Location: question6.php');
  exit;
}

// セッションに保存
$_SESSION['question6'] = $_POST['question6'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question7.php');
exit;
