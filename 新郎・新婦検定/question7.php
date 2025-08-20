<?php
session_start();
// 直アクセス防止：question6が未回答なら戻す
if (!isset($_SESSION['question6'])) {
  header('Location: question6.php');
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
    <h1>7問目</h1>
    <div class="center">
      <p class="p">ポロポーズの言葉は？
      </p>
      <form action="check7.php" method="post" class="in_form">
        <p>
          <label>
            <input type="radio" name="question7" value="結婚して？">結婚して？
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question7" value="一緒のお墓に入ってください">一緒のお墓に入ってください
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question7" value="毎日お味噌汁作ってくれますか？">毎日お味噌汁作ってくれますか？
          </label>
        </p>
        <p>
          <label>
            <input type="radio" name="question7" value="僕と結婚してください！">僕と結婚してください！
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