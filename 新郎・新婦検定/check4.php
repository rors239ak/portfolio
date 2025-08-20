<?php
session_start();


if (!isset($_POST['question4'])) {
  header('Location: question4.php');
  exit;
}

// セッションに保存
$_SESSION['question4'] = $_POST['question4'];
$_SESSION['question_count'] += 1;
// 次のページへ
header('Location: question5.php');
exit;
