<?php
session_start();
// 直アクセス防止：question11が未回答なら戻す
if (!isset($_SESSION['question11'])) {
  header('Location: question11.php');
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
    <h1>12問目</h1>
    <div class="center">
      <p class="p">新郎の好きな新婦のご飯は？
      </p>
      <form action="check12.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question12" value="春巻き">春巻き
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question12" value="肉じゃが">肉じゃが
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question12" value="オムライス">オムライス
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question12" value="カルボナーラ">カルボナーラ
          </label>
        </p>
        <p class="last_check">これで問題は以上となります。<br>
          答えのボタンを押すとすぐに点数が出ます。</p>
        <input type="submit" value="答え" class="anser">
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