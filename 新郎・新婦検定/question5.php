<?php
session_start();
// 直アクセス防止：question4が未回答なら戻す
if (!isset($_SESSION['question4'])) {
  header('Location: question4.php');
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
    <h1>5問目</h1>
    <div class="center">
      <p class="p">新婦の好きな花は？
      </p>
      <form action="check5.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question5" value="バラ">バラ
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question5" value="朝顔">朝顔
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question5" value="ゆり">ゆり
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question5" value="ひまわり">ひまわり
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