import random
from c_skill import Fireball, Ice_shard, Double_punch, Megaton_punch, Heal, Revival, Shotgun, Samidare, One_shot_kill, Meditation, Taunt, Blade_share


#勇者クラス
class Hero:
  def __init__(self, name):
    self.name = name
    self.hp = 100
    self.mp = 30
    self.attack = 10
    self.speed = 10
    self.frozen = False

  
  #ステータス確認
  def show_status(self):
    print(f"{self.name}のステータス")
    print(f"HP:{self.hp}")
    print(f"MP:{self.mp}")
    print(f"攻撃力:{self.attack}")
    if not self.is_alive():
      print(f"{self.name}は倒れている…")

  #通常攻撃
  def attack_to(self, target):
    # 剣士の挑発スキルをFalseに
    if isinstance(self, Swords_fighter):
      self.taunt_active = False
    if not self.can_act(target):
      return False
    damage = self.attack + random.randint(-5, 5)
    damage = max(0, damage)
    target.hp = max(0, target.hp - damage)
    print(f"{self.name}は{target.name}に{damage}のダメージを与えた！")
    return True

  #生きている状態
  def is_alive(self):
    return self.hp > 0
    
  # MP確認
  def MP_check(self, use_mp):
    return self.mp >= use_mp 

  #行動可能かどうか  
  def can_act(self, target=None, use_mp=0):
    if not self.is_alive():
      print(f"{self.name}は倒れていて攻撃できない！")
      return False
    if self.frozen:
      print(f"{self.name}は凍っていて動けない")
      self.frozen = False
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
    if not self.is_alive():
      print(f"{self.name}は倒れていて攻撃できない！")
      return False
    if self.frozen:
      print(f"{self.name}は凍っていて動けない")
      self.frozen = False
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

  
  







# 魔法使いクラス
class Wizard(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 60
    self.mp = 100
    self.attack = 5
    self.speed = 15

    # スキル
    self.fireball = Fireball(self)
    self.ice_shard = Ice_shard(self)

  
  
# ファイタークラス
class Fighter(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 120
    self.mp = 10
    self.attack = 20
    self.speed = 17

    self.double_punch = Double_punch(self)
    self.megaton_punch = Megaton_punch(self)



# 聖職者クラス
class Healer(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 80
    self.mp = 80
    self.attack = 5
    self.speed = 7

    self.heal = Heal(self)
    self.revival = Revival(self)



# 射手クラス
class Archer(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 110
    self.mp = 40
    self.attack = 15
    self.speed = 13

    self.shotgun = Shotgun(self)
    self.samidare = Samidare(self)



# 暗殺者クラス
class Assassin(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 60
    self.mp = 40
    self.attack = 40
    self.speed = 20

    self.one_shot_kill = One_shot_kill(self)
    self.meditation = Meditation(self)



# 剣士クラス
class Swords_fighter(Hero):
  def __init__(self, name):
    super().__init__(name)
    self.hp = 200
    self.mp = 200
    self.attack = 5
    self.speed = 5
    self.taunt_active = False

    self.taunt = Taunt(self)
    self.blade_share = Blade_share(self)
