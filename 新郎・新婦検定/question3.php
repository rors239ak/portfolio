<?php
session_start();
// 直アクセス防止：question2が未回答なら戻す
if (!isset($_SESSION['question2'])) {
  header('Location: question2.php');
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
    <h1>3問目</h1>
    <div class="center">
      <p class="p">新婦と新婦の喧嘩の時に新婦が最初にとる行動は？
      </p>
      <form action="check3.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question3" value="謝罪">謝罪
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question3" value="家出">家出
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question3" value="無視">無視
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question3" value="爆買い">爆買い
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