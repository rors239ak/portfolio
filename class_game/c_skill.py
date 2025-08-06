import random

class Skill:
  #行動可能かどうか  
  def can_act(self, target=None, use_mp=0):
    if not self.user.is_alive():
      print(f"{self.user.name}は倒れていて攻撃できない！")
      return False
    if self.user.frozen:
      print(f"{self.user.name}は凍っていて動けない")
      self.user.frozen = False
      return False
    if target is not None and not target.is_alive():
      print(f"{target.name}はもう倒れている…")
      return False
    if not self.MP_check(use_mp):
      print(f"その技はMPが足りなくて使えなかった")
      return False
    return True
    

  #蘇生可能かどうか  
  def can_revival(self, target=None, use_mp=0):
    if not self.user.is_alive():
      print(f"{self.user.name}は倒れていて攻撃できない！")
      return False
    if self.user.frozen:
      print(f"{self.user.name}は凍っていて動けない")
      self.user.frozen = False
      return False
    if not self.MP_check(use_mp):
      print(f"その技はMPが足りなくて使えなかった")
      return False
    if target is None or target.is_alive():
        print(f"{target.name}は倒れてないから蘇生できない！")
        return False
    if target is None:
        print("ターゲットが指定されてないから蘇生できない！")
        return False
    return True
  

  #生きている状態
  def is_alive(self):
    return self.user.hp > 0
  
  # MP確認
  def MP_check(self, use_mp):
    return self.user.mp >= use_mp 

  



# 単体攻撃スキル
class Fireball(Skill):
  
  def __init__(self, user, cost=15):
    self.user = user
    self.cost = cost 
  
  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    damage = random.randint(15, 30)
    target.hp = max(0, target.hp - damage)
    self.user.mp -= self.cost
    print(f"{self.user.name}のファイヤーボール、{target.name}に{damage}のダメージを与えた！")
    return True



  # 単体攻撃スキル行動デバフ
class Ice_shard(Skill):
  def __init__(self, user, cost=20):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    damage = random.randint(10, 20)
    target.hp = max(0, target.hp - damage)
    target.frozen = True
    self.user.mp -= self.cost
    print(f"{self.user.name}のアイスシャード、{target.name}に{damage}のダメージ！{target.name}は凍って1ターン動けない")
    return True
    


  # 2回攻撃スキル
class Double_punch(Skill):
  def __init__(self, user, cost=4):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    self.user.mp -= self.cost
    damage1 = random.randint(5, 30)
    target.hp = max(0, target.hp - damage1)
    print(f"{self.user.name}のダブルパンチ、{target.name}に{damage1}のダメージを与えた！")
    damage2 = random.randint(5, 30)
    target.hp = max(0, target.hp - damage2)
    print(f"{self.user.name}のダブルパンチ、{target.name}に{damage2}のダメージを与えた！")
    return True
    


  # メガトンパンチ0か10か50のうちランダムでダメージ
class Megaton_punch(Skill):
  def __init__(self, user, cost=5):
    self.user = user
    self.cost = cost 

  def use(self,target):
    if not self.can_act(target, self.cost):
      return False
    self.user.mp -= self.cost
    damage_list = [0, 10, 50]
    damage = random.choice(damage_list)
    target.hp = max(0, target.hp - damage)
    print(f"{self.user.name}のメガトンパンチ！{target.name}に{damage}のダメージを与えた！")



  # 単体回復スキル
class Heal(Skill):
  def __init__(self, user, cost=10):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    target.hp += 30
    self.user.mp -= self.cost
    print(f"{self.user.name}は{target.name}を30回復した！")
    return True
    


  # 蘇生スキル
class Revival(Skill):
  def __init__(self, user, cost=30):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_revival(target, self.cost):
      return False
    target.hp = 25
    self.user.mp -= self.cost
    print(f"{self.user.name}は{target.name}を蘇生した！")
    return True
    


  # 10連矢スキル
class Shotgun(Skill):
  def __init__(self, user, cost=20):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    self.user.mp -= self.cost
    total_damage = []
    for damage in range(10):
      damage = random.randint(1, 10)
      total_damage.append(damage)
      target.hp = max(0, target.hp - damage)
    print(f"{self.user.name}の10連ショットガン！{target.name}に{total_damage} 合計{sum(total_damage)}のダメージを与えた！")
    return True
        


  # 五月雨全体攻撃
class Samidare(Skill):
  def __init__(self, user, cost=20):
    self.user = user
    self.cost = cost 

  def use(self, targets):
    if not self.can_act(target=None, use_mp=self.cost):
      return False
    self.user.mp -= self.cost
    for target in targets:
      damage = random.randint(5, 20)
      target.hp = max(0, target.hp - damage)
      print(f"{self.user.name}の五月雨！{target.name}に{damage}のダメージを与えた！")
    return True
    


  # 即死ワザ
class One_shot_kill(Skill):
  def __init__(self, user, cost=40):
    self.user = user
    self.cost = cost 

  def use(self, target):
    if not self.can_act(target, self.cost):
      return False
    if target.hp >= 200:
      print("相手が強すぎて攻撃が効かなかった")
    else:  
      self.user.mp -= self.cost
      damage = target.hp
      target.hp -= damage
      print(f"{self.user.name}の一撃必殺！{target.name}に{damage}の即死ダメージを与えた！")
    return True
    
  # 瞑想
class Meditation(Skill):
  def __init__(self, user, cost=0):
    self.user = user
    self.cost = cost
  def use(self):
    if not self.can_act(target=None, use_mp=0):
      return False
    self.user.mp += 20
    print("瞑想をしてMPを20回復した")
    return True
    


  # 挑発スキルターゲットを自分に集中
class Taunt(Skill):
  def __init__(self, user, cost=10):
    self.user = user
    self.cost = cost 

  def use(self):
    if not self.can_act(target=None, use_mp=self.cost):
      return False
    self.user.mp -= self.cost
    self.user.hp += 40
    self.user.taunt_active = True
    print(f"{self.user.name}は挑発を使った！HPを40回復し敵の攻撃は全て{self.user.name}に向く")
    return True



  # ブレイドシェアMP分けるスキル
class Blade_share(Skill):
  def __init__(self, user):
    self.user = user

  def use(self, targets):
    if not self.can_act(use_mp=60):
      return False
    share_targets = [target for target in targets if target.name != self.user.name]
    if not share_targets:
        print("MPを分ける相手がいなかった")
        return True

    share = 60 // len(share_targets)
    self.user.mp -= 60
    for target in share_targets:
        target.mp += share
        print(f"{self.user.name}の‼ブレイドシェア！{target.name}にMPを{share}分け与えた！")
    return True