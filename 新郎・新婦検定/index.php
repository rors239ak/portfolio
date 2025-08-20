<?php 
session_start();
$_SESSION["question_count"] = 0; ?>
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
    <h1>新郎・新婦検定</h1>
      <form action="start.php" method="post">
        <div class="name1"><p class="name">名前</p>
        <input type="text" class="textbox" name="name"></div>
          <div class="center">
            <p>下の【スタート】を押すと問題が4択で表示されますので、できるだけ早くお答えください。<br>なお、【スタート】を押してから【終了】を押すまでの時間が計測されていますのでそれによって点数も変わってきます。</p> 
            <p>それでは準備はいいですか？</p>
            <button class="btn" type="submit">スタート</button>
          </div>
      </form>
  </main>

  <footer>
    <a href="index.php"><img src="image/image.png" alt="ロゴ" class="logo"></a> 
  </footer>
</body>
</html>