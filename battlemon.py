import random
import json
import sys

TYPE_NORMAL = 0
TYPE_FIRE = 1
TYPE_WATER = 2
TYPE_GRASS = 3
TYPES = ["Normal", "Fire", "Water", "Grass"]

MOVE_BASIC_ATTACK = 0
MOVE_ATTACK_UP = 1
MOVE_DEFEND = 2
MOVE_HEAL = 3
MOVE_BLIND_RAGE = 4
MOVE_LEECH_ATTACK = 5
MOVE_THUNDERSHOCK = 6
MOVE_FISSURE = 7
MOVES = ["basic-attack", "attack-up", "defend", "heal", "blind-rage", "leech-attack", "thundershock", "fissure"]

TYPE_CHART = [
    [1,  1,   1,   1 ],
    [1, 0.5, 0.5,  2 ],
    [1,  2,  0.5, 0.5],
    [1, 0.5,  2,  0.5]]

mon1 = None
mon2 = None
mon1_restart = None
mon2_restart = None
winner = 0

def get_type_id(type):
    match type:
        case "Normal":
            return TYPE_NORMAL
        case "Fire":
            return TYPE_FIRE
        case "Water":
            return TYPE_WATER
        case "Grass":
            return TYPE_GRASS
        case _:
            return None

class Mon:
    def __init__(self, name="empty"):
        self.name = name
        self.type = random.randint(0, 3)
        self.hp = random.randint(1, 200)
        self.current_hp = self.hp
        self.attack = random.randint(1, 200)
        self.defense = random.randint(1, 200)
        self.speed = random.randint(0, 200)
        self.moves = [MOVES[MOVE_BASIC_ATTACK]]
        self.moves += random.sample(MOVES[1:7],3)

        self.attack_up = 0
        self.defend = False
        self.heal_used = False
       

    def import_mon(self, mon_file):
        with open(mon_file, 'r') as file:
            mon_data = json.load(file)
            self.name = mon_data["Name"]
            self.type = get_type_id(mon_data["Type"])
            self.hp = mon_data["Hp"]
            self.attack = mon_data["Attack"]
            self.defense = mon_data["Defense"]
            self.speed = mon_data["Speed"]
            for e in mon_data["Moves"]:
                self.moves += [e["Name"]]

    def damage(self, damage_taken):
        if (self.defend == True):
            damage_taken = damage_taken / 2
        self.current_hp -= damage_taken
        if self.current_hp < 0:
            self.current_hp = 0

    def heal(self, hp_healed):
        self.current_hp += hp_healed
        if self.current_hp > self.hp:
            self.current_hp = self.hp


    def __str__(self):
        return "Mon: " + self.name + " Type: " + TYPES[self.type] + " Hp: " + str(self.hp) + " Attack: " + str(self.attack) + " Defense: " + str(self.defense) + " Speed: " + str(self.speed) + " Moves: " + ", ".join(self.moves)



# COMMANDS FUNCTIONS
def help():
    print("I will write this later")

def status():
    print("Mon1: " + mon1.name + " Type: " + TYPES[mon1.type] + " Hp: " + str(mon1.hp))
    print("Mon2: " + mon2.name + " Type: " + TYPES[mon2.type] + " Hp: " + str(mon2.hp))

def info(mon):
    if mon1.name == mon:
        print(mon1)
    elif mon2.name == mon:
        print(mon2)
    else:
        print("Error: Mon doesn't exist.")
    
def movelist(mon):
    if mon1.name == mon:
        for move in mon.moves:
            print(move)
    elif mon2.name == mon:
        for move in mon.moves:
            print(move)
    else:
        print("Error: Mon doesn't exist.")

        
def use(mon, attack):
    if attack not in mon.moves:
        print("Attack cannot be used. Choose a valid attack.\n" + movelist(mon))
    
    return MOVES.index(attack)


def surrender(current_player):
    print("Player " + str(current_player) + " gave up.")
        
    
def quit():
    exit()

def restart():
    print("Game restarted.")
    mon1 = mon1_restart
    mon2 = mon2_restart
    winner = 0




def damage_calculator(attacking_mon, defending_mon):
    total_dmg = (attacking_mon.attack / defending_mon.defense) * 25
    total_dmg *= TYPE_CHART[attacking_mon.type][defending_mon.type]
    if (attacking_mon.attack_up > 0):
            total_dmg = total_dmg * 2
    return total_dmg

def basic_attack(attacking_mon, defending_mon):
    if random.random() < 0.9:
        total_dmg = damage_calculator(attacking_mon, defending_mon)
        defending_mon.damage(total_dmg)
    else:
        print("Basic-Attack missed.")
    
def attack_up(attacking_mon, defending_mon):
    attacking_mon.attack_up = 2

def defend(attacking_mon, defending_mon):
    attacking_mon.defend = True

def heal(attacking_mon, defending_mon):
    if not attacking_mon.heal_used:
        attacking_mon.heal(attacking_mon.hp)
    else:
        print("Heal already used.")

def blind_rage(attacking_mon, defending_mon):
    if random.random() < 0.5:
        total_dmg = damage_calculator(attacking_mon, defending_mon) * 3
        defending_mon.damage(total_dmg)
    else:
        total_dmg = damage_calculator(attacking_mon, attacking_mon) * 3
        attacking_mon.damage(total_dmg)

def leech_atack(attacking_mon, defending_mon):
    total_dmg = damage_calculator(attacking_mon, defending_mon) * 0.25
    defending_mon.damage(total_dmg)
    attacking_mon.heal(total_dmg)

def thundershock(attacking_mon, defending_mon):
    total_dmg = damage_calculator(attacking_mon, defending_mon) * 0.75
    defending_mon.damage(total_dmg)

def fissure(attacking_mon, defending_mon):
    if random.random() < 0.05:
        defending_mon.damage(defending_mon.hp)
    else:
        print("Fissure failed.")

move_functions = [basic_attack, attack_up, defend, heal, blind_rage, leech_atack, thundershock, fissure]

def play_turn(mon1_move, mon2_move):
    # verify who is faster
    if mon1.speed != mon2.speed:
        faster, slower = (mon1, mon2) if mon1.speed > mon2.speed else (mon2, mon1)
    else:
        faster, slower = (mon1, mon2) if random.random() < 0.5 else (mon2, mon1)
    if mon2_move == MOVE_DEFEND and mon1_move != MOVE_DEFEND:
        faster, slower = (mon2, mon1)
    if mon1_move == MOVE_DEFEND and mon2_move != MOVE_DEFEND:
        faster, slower = (mon1, mon2)

    if mon1 == faster:
        move_functions[mon1_move](faster, slower)
        if mon1.current_hp == 0: return 2
        if mon2.current_hp == 0: return 1
        move_functions[mon2_move](slower, faster)
        if mon1.current_hp == 0: return 2
        if mon2.current_hp == 0: return 1
    
    else:
        move_functions[mon2_move](faster, slower)
        if mon1.current_hp == 0: return 2
        if mon2.current_hp == 0: return 1
        move_functions[mon1_move](slower, faster)
        if mon1.current_hp == 0: return 2
        if mon2.current_hp == 0: return 1

    mon1.defend = False
    mon2.defend = False

    if mon1.attack_up > 0:
        mon1.attackup -= 1
    if mon2.attack_up > 0:
        mon2.attackup -= 1

    return 0

def play(current_player):
    print("Player" + str(current_player) +"'s turn")
    while True:
        command = input("Write your command: \n")
        command = command.split(" ")

        match command[0]:
            case "help":
                help()

            case "status":
                status()

            case "info":
                if len(command) == 2:
                    info(command[1])
                elif len(command) == 1:
                    if current_player == 1: info(mon1.name)
                    elif current_player == 2: info(mon2.name)
                else:
                    print("Unrecognized command. Use help command to display available commands.") 

            case "movelist":
                if len(command) == 2:
                    movelist(command[1])
                elif len(command) == 1:
                    if current_player == 1: movelist(mon1.name)
                    elif current_player == 2: movelist(mon2.name)
                else:
                    print("Unrecognized command. Use help command to display available commands.") 

            case "use":
                if (winner == 0):
                    if len(command) == 2:
                        if current_player == 1: mon = mon1
                        else: mon = mon2
                        return use(mon, command[1])
                    else:
                        print("Unrecognized command. Use help command to display available commands.")
                else:
                    print("Game is not in progress.")

            case "surrender":
                if (winner == 0):
                    surrender(current_player)
                    return 1
                else:
                    print("Game is not in progress.")

            case "quit":
                quit()

            case "restart":
                restart()
                return 2

            case _:
                print("Unrecognized command. Use help command to display available commands.")

            
                    


if __name__ == "__main__":
    args = sys.argv[1:]
    against_cpu = False

    if args[0] == "y" or args[0] == "Y":
        against_cpu = True

    elif args[0] == "n" or args[0] == "N":
        against_cpu = False

    else:
        print("Invalid input")
        exit

    mon1 = Mon("RandMon1")
    mon2 = Mon("RandMon2")

    if len(args) > 1:
        mon1 = mon1.import_mon(args[1])
        mon1_restart = mon1
    if len(args) > 2:
        mon2 = mon2.import_mon(args[2])
        mon2_restart = mon2
        
    print("Game started")

    while True:
        while winner == 0:
            p1_move = play(1)
            if p1_move == 1:
                winner = 2
                break
            
            elif p1_move == 2:
                continue

            if against_cpu == False:
                p2_move = play(2)
                if p2_move == 1:
                    winner = 1
                    break
                elif p1_move == 2:
                    continue
            else:
                #random cpu move
                p2_move = random.sample(mon2.moves ,1)
                p2_move = MOVES.index(p2_move)

            winner = play_turn(p1_move, p2_move)

        play(1)

            
        

    


