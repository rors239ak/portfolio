<?php
session_start();


if (!isset($_POST['question5'])) {
  header('Location: question5.php');
  exit;
}

// セッションに保存
$_SESSION['question5'] = $_POST['question5'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question6.php');
exit;
