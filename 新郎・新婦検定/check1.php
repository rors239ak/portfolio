<?php
session_start();

// 未選択ガード
if (!isset($_POST['question1'])) {
  // 未選択なら戻す
  header('Location: question1.php');
  exit;
}

// セッションに保存
$_SESSION['question1'] = $_POST['question1'];
$_SESSION['question_count'] += 1;

// 次のページへ
header('Location: question2.php');
exit;
