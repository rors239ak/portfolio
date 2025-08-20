<?php
session_start();


if (!isset($_POST['question2'])) {
  header('Location: question2.php');
  exit;
}

// セッションに保存
$_SESSION['question2'] = $_POST['question2'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question3.php');
exit;
