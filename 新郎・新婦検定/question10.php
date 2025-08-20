<?php
session_start();
// 直アクセス防止：question9が未回答なら戻す
if (!isset($_SESSION['question9'])) {
  header('Location: question9.php');
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
    <h1>10問目</h1>
    <div class="center">
      <p class="p">新郎の最近はまっている趣味は？
      </p>
      <form action="check10.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question10" value="飲み歩き">飲み歩き
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question10" value="アクアリウム">アクアリウム
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question10" value="キャンプ">キャンプ
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question10" value="ビリヤード">ビリヤード
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