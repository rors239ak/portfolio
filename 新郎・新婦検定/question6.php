<?php
session_start();
// 直アクセス防止：question5が未回答なら戻す
if (!isset($_SESSION['question5'])) {
  header('Location: question5.php');
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
    <h1>6問目</h1>
    <div class="center">
      <p class="p">新郎と新婦の出会いの場はどこでしょう？
      </p>
      <form action="check6.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question6" value="焼肉屋">焼肉屋
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question6" value="バー">バー
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question6" value="ビアガーデン">ビアガーデン
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question6" value="ネットゲーム">ネットゲーム
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