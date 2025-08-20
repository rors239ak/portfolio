<?php
session_start();
// 直アクセス防止：question10が未回答なら戻す
if (!isset($_SESSION['question10'])) {
  header('Location: question10.php');
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
    <h1>11問目</h1>
    <div class="center">
      <p class="p">新婚旅行はどこ？
      </p>
      <form action="check11.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question11" value="大阪">大阪
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question11" value="東京">東京
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question11" value="山口">山口
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question11" value="大分">大分
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