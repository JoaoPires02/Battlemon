import random
import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

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

BASIC_ATTACK_DESC = "A simple attack with a 90% chance to hit."
ATTACK_UP_DESC = "Doubles the damage the mon deals next round."
DEFEND_DESC = "Halves the damage the mon receives this round. Is always added to the damage calculation, regardless of the speed stat."
HEAL_DESC = "Restore health points.Can only be used once in a battle."
BLIND_RAGE_DESC = "Attack with triple damage, but 50% chance to hit itself instead."
LEECH_ATTACK_DESC = "Attack with 1/4 damage, but gain it as health points."
THUNDERSHOCK_DESC = "Attack with 3/4 damage, never misses."
FISSURE_DESC = "Attack that can instantly defeat the other mon, but only has a 5% chance of hitting its objective."
MOVE_DESCRIPTIONS = [BASIC_ATTACK_DESC, ATTACK_UP_DESC, DEFEND_DESC, HEAL_DESC, BLIND_RAGE_DESC, LEECH_ATTACK_DESC, THUNDERSHOCK_DESC, FISSURE_DESC]

TYPE_CHART = [
    [1,  1,   1,   1 ],
    [1, 0.5, 0.5,  2 ],
    [1,  2,  0.5, 0.5],
    [1, 0.5,  2,  0.5]]

random.seed(40)

global mon1
global mon2 
global mon1_restart
global mon2_restart
global winner

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
        
def get_move_id(move_name):
    match move_name:
        case "basic-attack":
            return MOVE_BASIC_ATTACK
        case "attack-up":
            return MOVE_ATTACK_UP
        case "defend":
            return MOVE_DEFEND
        case "heal":
            return MOVE_HEAL
        case "blind-rage":
            return MOVE_BLIND_RAGE
        case "leech-attack":
            return MOVE_LEECH_ATTACK
        case "thundershock":
            return MOVE_THUNDERSHOCK
        case "fissure":
            return MOVE_FISSURE
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
            if (self.type == None):
                print("Error: " + self.name + " has incorrect type.")
                quit()
            self.hp = mon_data["Hp"]
            self.current_hp = self.hp
            self.attack = mon_data["Attack"]
            self.defense = mon_data["Defense"]
            self.speed = mon_data["Speed"]
            self.moves = []
            for move in mon_data["Moves"]:
                move_id = get_move_id(move["Name"])
                if (move_id == None):
                    print("Error: " + self.name + " has an incorrect move.")
                    quit()
                self.moves.append(move["Name"])

    def damage(self, damage_taken):
        if (self.defend == True):
            damage_taken = round(damage_taken / 2)
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
    print("""- help
    - Help command with no arguments. Prints the possible commands the user can
use and their descriptions in a list
- status
    - Display the current statuses of the battling mons. Print their names, types, and
current hp points
- info <arg1>
    - Display the full stats of the given mon, where <arg1> is their name. Print its
name, type, hp, attack, defense, speed, and list of moves. If no argument is
given, default to the user’s mon.
- movelist <arg1>
    - Print the movelist of the given mon, where <arg1> is their name. Print the name
of each move and its description. If no argument is given, default to the user’s
mon
- use <arg1>
    - <arg1> must be given and must be the name of a valid attack in the user’s mon’s
movelist. The user’s mon will then use that attack and advance the turns of the
battle
    - If the given attack cannot be used, notify the user and ask for a valid attack,
listing the names of the moves they can use.
- surrender
    - The user immediately loses the battle
- quit
    - Exit the program
- restart
    - Restart the battle with the same mons""")

def status():
    print("Mon1: " + mon1.name + " Type: " + TYPES[mon1.type] + " Hp: " + str(mon1.current_hp))
    print("Mon2: " + mon2.name + " Type: " + TYPES[mon2.type] + " Hp: " + str(mon2.current_hp))

def info(mon):
    if mon1.name == mon:
        print(mon1)
    elif mon2.name == mon:
        print(mon2)
    else:
        print("Error: Mon doesn't exist.")
    
def movelist(mon):
    if mon1.name == mon:
        for move in mon1.moves:
            move_desc = MOVE_DESCRIPTIONS[get_move_id(move)]
            print(move + " - " + move_desc)
    elif mon2.name == mon:
        for move in mon2.moves:
            move_desc = MOVE_DESCRIPTIONS[get_move_id(move)]
            print(move + " - " + move_desc)
    else:
        print("Error: Mon doesn't exist.")

        
def use(mon, attack):
    if attack not in mon.moves:
        print("Attack cannot be used. Choose a valid attack.")
        movelist(mon.name)
        return -1
    
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
        total_dmg = round(total_dmg)
        defending_mon.damage(total_dmg)
    else:
        print(attacking_mon.name + " missed basic-attack.")
    
def attack_up(attacking_mon, defending_mon):
    attacking_mon.attack_up = 2

def defend(attacking_mon, defending_mon):
    attacking_mon.defend = True

def heal(attacking_mon, defending_mon):
    if not attacking_mon.heal_used:
        attacking_mon.heal(attacking_mon.hp)
        attacking_mon.heal_used = True
    else:
        print(attacking_mon.name + " used heal already.")

def blind_rage(attacking_mon, defending_mon):
    if random.random() < 0.5:
        total_dmg = damage_calculator(attacking_mon, defending_mon) * 3
        total_dmg = round(total_dmg)
        defending_mon.damage(total_dmg)
    else:
        print(attacking_mon.name + " missed blind-rage.")
        total_dmg = damage_calculator(attacking_mon, attacking_mon) * 3
        total_dmg = round(total_dmg)
        attacking_mon.damage(total_dmg)

def leech_attack(attacking_mon, defending_mon):
    total_dmg = damage_calculator(attacking_mon, defending_mon) * 0.25
    total_dmg = round(total_dmg)
    defending_mon.damage(total_dmg)
    attacking_mon.heal(total_dmg)

def thundershock(attacking_mon, defending_mon):
    total_dmg = damage_calculator(attacking_mon, defending_mon) * 0.75
    total_dmg = round(total_dmg)
    defending_mon.damage(total_dmg)

def fissure(attacking_mon, defending_mon):
    if random.random() < 0.05:
        defending_mon.current_hp = 0
    else:
        print(attacking_mon.name + " missed fissure.")

move_functions = [basic_attack, attack_up, defend, heal, blind_rage, leech_attack, thundershock, fissure]

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
        mon1.attack_up -= 1
    if mon2.attack_up > 0:
        mon2.attack_up -= 1

    return 0

def play(current_player):
    if winner == 0:
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
                        move_used = use(mon, command[1])

                        if move_used != -1:
                            return move_used
                        
                    else:
                        print("Unrecognized command. Use help command to display available commands.")
                else:
                    print("Game is not in progress.")

            case "surrender":
                if (winner == 0):
                    surrender(current_player)
                    return "surrend"
                else:
                    print("Game is not in progress.")

            case "quit":
                quit()

            case "restart":
                restart()
                return "restart"

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
        quit()

    mon1 = Mon("RandMon1")
    mon2 = Mon("RandMon2")

    if len(args) > 1:
        mon1.import_mon(args[1])
    if len(args) > 2:
        mon2.import_mon(args[2])

    #Added for testing purposes
    if len(args) > 3:
        random.seed(args[3])

    mon1_restart = mon1
    mon2_restart = mon2
            
    print("Game started")

    while True:
        winner = 0
        while winner == 0:
            p1_move = play(1)
            if p1_move == "surrend":
                winner = 2
                break
            
            elif p1_move == "restart":
                continue

            if against_cpu == False:
                p2_move = play(2)
                if p2_move == "surrend":
                    winner = 1
                    break
                elif p2_move == "restart":
                    continue
            else:
                p2_move = MOVES.index("basic-attack")

            winner = play_turn(p1_move, p2_move)
            
            if winner != 0:
                print("Player " + str(winner) + " wins!")

        play(1)
