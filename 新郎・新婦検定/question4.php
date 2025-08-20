<?php
session_start();
// 直アクセス防止：question3が未回答なら戻す
if (!isset($_SESSION['question3'])) {
  header('Location: question3.php');
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
    <h1>4問目</h1>
    <div class="center">
      <p class="p">平野家でのみ流行っている口癖は？
      </p>
      <form action="check4.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question4" value="～しん">～しん
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question4" value="ニキ・ネキ">ニキ・ネキ
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question4" value="にゃんちゅう">にゃんちゅう
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question4" value="なんちゃって">なんちゃって
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