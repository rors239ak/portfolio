<?php
// ← 先頭に空白や改行ナシ！
if (session_status() === PHP_SESSION_NONE) session_start();

if (!isset($_SESSION['start_time'])) {
  header('Location: index.php'); exit;
}

// 【仮】終了時刻いまこの瞬間（本番は end.php から渡す）
$end = microtime(true);
$elapsed = $end - $_SESSION['start_time'];

// 次のためにクリア（連打で壊れないように）
unset($_SESSION['start_time']);

// mm:ss.mmm に整形
$min = (int)floor($elapsed / 60);
$sec = $elapsed - ($min * 60);
$disp = sprintf('%02d:%06.3f', $min, $sec);



$count = 0;
if($_SESSION["question1"] == "ボードゲームカフェ"){$count += 1;}
if($_SESSION["question2"] == "歯"){$count += 1;}
if($_SESSION["question3"] == "無視"){$count += 1;}
if($_SESSION["question4"] == "にゃんちゅう"){$count += 1;}
if($_SESSION["question5"] == "ひまわり"){$count += 1;}
if($_SESSION["question6"] == "焼肉屋"){$count += 1;}
if($_SESSION["question7"] == "結婚して？"){$count += 1;}
if($_SESSION["question8"] == "アイス"){$count += 1;}
if($_SESSION["question9"] == "King & Prince"){$count += 1;}
if($_SESSION["question10"] == "アクアリウム"){$count += 1;}
if($_SESSION["question11"] == "大阪"){$count += 1;}
if($_SESSION["question12"] == "春巻き"){$count += 1;}

$total = ($count / $_SESSION["question_count"] * 100);

// 経過秒数（float値）
$elapsed = (float)$_SESSION['elapsed_s'];

// 経過時間を mm:ss.mmm に整形
$min = (int)floor($elapsed / 60);
$sec = $elapsed - ($min * 60);
$disp = sprintf('%02d:%06.3f', $min, $sec);

// 🔽 追加：5秒ごとに1ポイント加算
$bonus = floor($elapsed / 5);  

$last_total = 0;
//50秒以内なら減点なし
$last_total = $total - $bonus + 10;
// 100を超えないようにする
$last_total = round(min($last_total, 100));
$last_total = round(max($last_total, 0));
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
    <div class="center">
      <p><?php echo "{$_SESSION["name"]}さんの点数は{$last_total}です！" ;?></p>
      <p><?php
        if ($last_total >= 65){
          echo "おめでとうございます！新郎・新婦検定1級合格です！<br>詳しすぎません！？<br>こんな私たちですがこれからもよろしくお願いします。";
        }elseif($last_total >= 55){
          echo "おめでとうございます！新郎・新婦検定準1級合格です！<br>こんなに仲良くしてくれる人がいるなんて私たちは幸せです！";
        }elseif($last_total >= 45){
          echo "おめでとうございます！新郎・新婦検定2級合格です！<br>これからもずっと仲良くしていってください！";
        }elseif($last_total >= 35){
          echo "おめでとうございます！新郎・新婦検定準2級合格です！<br>今日はい～っぱい楽しんでいってくださいね！";
        }else{
          echo "新郎・新婦検定3級合格です！<br>今度うちに遊びに来てくださいね！";
        }
        ?>
      </p>
      <table border="1">
        <tr>
          <th>問題</th>
          <th><?php echo $_SESSION["name"] ?>さんの回答</th>
          <th>結果</th>
          <th>正解は…</th>
        </tr>
        <tr>
          <td>質問1</td>
          <td><?php echo $_SESSION["question1"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question1"] == "ボードゲームカフェ"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>ボードゲームカフェ</td>
        </tr>
        <tr>
          <td>質問2</td>
          <td><?php echo $_SESSION["question2"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question2"] == "歯"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>歯</td>
        </tr>
        <tr>
          <td>質問3</td>
          <td><?php echo $_SESSION["question3"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question3"] == "無視"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>無視</td>
        </tr>
        <tr>
          <td>質問4</td>
          <td><?php echo $_SESSION["question4"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question4"] == "にゃんちゅう"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>にゃんちゅう</td>
        </tr>
        <tr>
          <td>質問5</td>
          <td><?php echo $_SESSION["question5"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question5"] == "ひまわり"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>ひまわり</td>
        </tr>
        <tr>
          <td>質問6</td>
          <td><?php echo $_SESSION["question6"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question6"] == "焼肉屋"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>焼肉屋</td>
        </tr>
        <tr>
          <td>質問7</td>
          <td><?php echo $_SESSION["question7"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question7"] == "結婚して？"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>結婚して？</td>
        </tr>
        <tr>
          <td>質問8</td>
          <td><?php echo $_SESSION["question8"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question8"] == "アイス"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>アイス</td>
        </tr>
        <tr>
          <td>質問9</td>
          <td><?php echo $_SESSION["question9"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question9"] == "King & Prince"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>King & Prince</td>
        </tr>
        <tr>
          <td>質問10</td>
          <td><?php echo $_SESSION["question10"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question10"] == "アクアリウム"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>アクアリウム</td>
        </tr>
        <tr>
          <td>質問11</td>
          <td><?php echo $_SESSION["question11"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question11"] == "大阪"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>大阪</td>
        </tr>
        <tr>
          <td>質問12</td>
          <td><?php echo $_SESSION["question12"]; ?></td>
          <td>
            <?php 
            if($_SESSION["question12"] == "春巻き"){
              echo "〇";
            }else{
              echo "✕";
            } 
            ?>
          </td>
          <td>春巻き</td>
        </tr>
      </table>

      <p>かかった時間：<?= htmlspecialchars($disp, ENT_QUOTES, 'UTF-8') ?></p>
    </div>
    <p class="home"><a href="index.php">最初に戻る</a></p>
  </main>

  <footer>
    <a href="index.php"><img src="image/image.png" alt="ロゴ" class="logo"></a> 
  </footer>
</body>
</html>