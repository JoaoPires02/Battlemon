NIKACHU_HP = 560
NIKACHU_ATTACK = 256
NIKACHU_DEFENSE = 100
CHARIZORD_HP = 1000
CHARIZORD_ATTACK = 420
CHARIZORD_DEFENSE = 50

def calc(attack, defense):
    return round((attack / defense) * 25)

print(calc(NIKACHU_ATTACK, CHARIZORD_DEFENSE))

