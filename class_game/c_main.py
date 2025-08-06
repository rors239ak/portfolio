
from c_hero import Hero, Wizard, Fighter, Healer, Archer, Assassin, Swords_fighter
from c_monster import Monster
from c_function import battle

#勇者パーティ
a = Swords_fighter("勇者")
b = Wizard("魔法使い")
c = Archer("射手")
d = Healer("聖職者")
e = Assassin("暗殺者")

party = [a, b, c, d, e]





#モンスター達
slime1 = Monster("スライムA")
slime2 = Monster("スライムB")
slime3 = Monster("スライムC")

enemies = [slime1, slime2, slime3]

battle(party,enemies)





  

