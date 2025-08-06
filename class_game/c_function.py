import time, random
from c_hero import Hero, Wizard, Fighter, Healer, Archer, Assassin, Swords_fighter 
from c_monster import Monster


# 対象候補の表示と選択関数（partyやenemiesのどっちでも使える）
def choose_target(target_list):
    print("攻撃対象を選んでね！")
    for i, target in enumerate(target_list, start=1):
        print(f"{i}: {target.name} (HP: {target.hp})")
    while True:
        try:
            choice = int(input("▶︎ 番号を入力: "))
            if 1 <= choice <= len(target_list):
                return target_list[choice - 1]
            else:
                print("正しい番号を入力してね！")
        except ValueError:
            print("数字を入力してね！")


# バトル
def battle(party, enemies):
  print("\n--- モンスターと遭遇した ---")
  turn = 1
  # どちらかのパーティが生きている間ずっと
  while any(member.is_alive() for member in party) and any(enemy.is_alive() for enemy in enemies):
    print(f"\n========== ターン {turn} ==========")

    all_characters = [chara for chara in party + enemies if chara.is_alive()]
    all_characters.sort(key=lambda chara: chara.speed, reverse=True)
    alive_party = [chara for chara in party if chara.is_alive()]
    for actor in all_characters:
      if isinstance(actor, Hero):
        if not actor.is_alive():
          continue
        alive_target = [e_chara for e_chara in enemies if e_chara.is_alive()]
        if alive_target:
          print("\n==============================\n")
          for enemy in enemies:
            enemy.show_status()
          print("\n")
          actor.show_status()

          print(f"\n{actor.name}のターン！")
          print("1: 通常攻撃")
          if isinstance(actor, Wizard):
              print("2: ファイヤーボール (MP消費15)")
              print("3: アイスシャード (MP消費20)")
          elif isinstance(actor, Fighter):
              print("2: ダブルパンチ (MP消費4)")
              print("3: メガトンパンチ (MP消費5)")
          elif isinstance(actor, Healer):
              print("2: ヒール（MP消費10 単体30回復）")
              print("3: 蘇生(MP消費30 単体蘇生)")
          elif isinstance(actor, Archer):
              print("2: 10連ショットガン (MP消費20)")
              print("3: 五月雨(MP消費20 全体攻撃)")
          elif isinstance(actor, Assassin):
              print("2: 一撃必殺 (MP消費40)")
              print("3: 瞑想")
          elif isinstance(actor, Swords_fighter):
              print("2: 挑発 (MP消費10)")
              print("3: ブレイドシェア (MP消費60)")
          try:
            while True:
              choice = input("▶︎ 行動を選んでね（数字を入力）: ")
              if choice == "1":
                target = choose_target(alive_target)
                if actor.attack_to(target): break
              elif choice == "2":
                if isinstance(actor, Wizard):
                  target = choose_target(alive_target)
                  if actor.fireball.use(target): break
                elif isinstance(actor, Fighter):
                   target = choose_target(alive_target)
                   if actor.double_punch.use(target):break
                elif isinstance(actor, Healer):
                  target = choose_target(alive_party)
                  if actor.heal.use(target):break
                elif isinstance(actor, Archer):
                  target = choose_target(alive_target)
                  if actor.shotgun.use(target):break
                elif isinstance(actor, Assassin):
                  target = choose_target(alive_target)
                  if actor.one_shot_kill.use(target):break
                elif isinstance(actor, Swords_fighter) and actor.taunt.use():
                    break
                else:continue
              elif choice == "3" :
                if isinstance(actor, Wizard):
                  target = choose_target(alive_target)
                  if actor.ice_shard.use(target): break 
                elif isinstance(actor, Fighter):
                  target = choose_target(alive_target)
                  if actor.megaton_punch.use(target): break
                elif isinstance(actor, Healer):
                  target = choose_target(alive_party)
                  if actor.revival.use(target):break
                elif isinstance(actor, Archer) and actor.samidare.use(alive_target):
                    break
                elif isinstance(actor, Assassin) and actor.meditation.use():
                    break
                elif isinstance(actor, Swords_fighter) and actor.blade_share.use(alive_party):
                    break
                else:continue
              else:
                print("正しい数値を入力してください")        
          except ValueError:
            print("正しい数値を入力してください")    
      elif isinstance(actor, Monster):
        if not actor.is_alive():
          continue
        alive_target = [p_chara for p_chara in party if p_chara.is_alive()]
        alive_taunt = [p_chara for p_chara in party if isinstance(p_chara, Swords_fighter) and p_chara.taunt_active and p_chara.is_alive()]
        print("\n==============================\n")
        
        print(f"\n{actor.name}のターン！")
        if alive_taunt:
          target = alive_taunt[0]
          actor.attack_to(target)
        else: 
          target = random.choice(alive_target)
          actor.attack_to(target)
    
      time.sleep(1)

    print("\n--- 味方ステータス ---")
    for member in party:
      member.show_status()
    time.sleep(1)
    print("\n--- 敵ステータス ---")
    for enemy in enemies:
      enemy.show_status()
    time.sleep(1)

    turn += 1
    print("-" * 30)
    
    if all(not p.is_alive() for p in party):
      print(f"勇者達はバトルに負けてしまった…")
    elif all(not e.is_alive() for e in enemies):
      print(f"勇者たちはバトルに勝った！") 
    else: 
      input("▶︎ Enterキーで次のターンへ…")
