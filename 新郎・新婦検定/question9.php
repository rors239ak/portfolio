<?php
session_start();
// 直アクセス防止：question8が未回答なら戻す
if (!isset($_SESSION['question8'])) {
  header('Location: question8.php');
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
    <h1>9問目</h1>
    <div class="center">
      <p class="p">新婦の好きなアイドルは？
      </p>
      <form action="check9.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question9" value="嵐">嵐
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question9" value="SnowMan">SnowMan
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question9" value="King & Prince">King & Prince
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question9" value="timelesz">timelesz
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