<?php
session_start();

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
    <h1>1問目</h1>
    <div class="center">
      <p class="p">新郎と新婦の初めてのデート先はどこでしょう？</p>
      <form action="check1.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question1" value="映画館">映画館
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question1" value="ボードゲームカフェ">ボードゲームカフェ
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question1" value="海">海
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question1" value="油山の夜景">油山の夜景
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