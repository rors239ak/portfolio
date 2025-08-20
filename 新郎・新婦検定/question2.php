<?php
session_start();
// 直アクセス防止：question1が未回答なら戻す
if (!isset($_SESSION['question1'])) {
  header('Location: question1.php');
  exit;
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <title>新郎・新婦検定</title>
</head>
<body>  
  <header>
    <a href="index.php"><img src="image/image.png" alt="ロゴ" class="logo"></a>  
  </header>

  <main>
    <h1>2問目</h1>
    <div class="center">
      <p class="p">新郎が一番好きな新婦のチャームポイントは？
      </p>
      <form action="check2.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question2" value="髪質">髪質
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question2" value="目">目
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question2" value="歯">歯
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question2" value="脚">脚
          </label>
        </p>
        <input type="submit" value="次へ" class="next">
      </form>
    </div>
    <p class="home"><a href="index.php">最初に戻る</a></p>
  </main>
  </main>

  <footer>
    <a href="index.php"><img src="image/image.png" alt="ロゴ" class="logo"></a> 
  </footer>
</body>
</html>