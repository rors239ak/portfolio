<?php
session_start();


if (!isset($_POST['question9'])) {
  header('Location: question9.php');
  exit;
}

// セッションに保存
$_SESSION['question9'] = $_POST['question9'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question10.php');
exit;
