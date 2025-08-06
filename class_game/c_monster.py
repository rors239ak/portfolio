import random

#敵モンスタークラス
class Monster:
  def __init__(self, name):
    self.name = name
    self.hp = random.randint(50, 150)
    self.mp = random.randint(100, 150)
    self.attack = random.randint(5, 20)
    self.speed = random.randint(5, 20)
    self.frozen = False

  # ステータス確認
  def show_status(self):
    print(f"{self.name}のステータス")
    print(f"HP:{self.hp}")
    print(f"攻撃力:{self.attack}")
    if not self.is_alive():
      print(f"{self.name}は倒れている…")

  # 通常攻撃
  def attack_to(self, target):
    if not self.can_act(target):
      return
    damage = self.attack + random.randint(-5, 5)
    damage = max(0, damage)
    target.hp = max(0, target.hp - damage)
    print(f"{self.name}は{target.name}に{damage}のダメージを与えた！")

  # 生きているか確認
  def is_alive(self):
    return self.hp > 0
  
  # 行動可能か
  def can_act(self, target=None):
    if not self.is_alive():
      print(f"{self.name}は倒れていて攻撃できない！")
      return False
    if self.frozen:
      print(f"{self.name}は凍っていて動けない")
      self.frozen = False
      return False
    if not target.is_alive():
      print(f"{target.name}はもう倒れている…")
      return False
    return True