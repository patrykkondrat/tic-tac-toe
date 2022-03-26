def cell(x):
    try:
        if x.lower()=="x":
            return " X "
        if x.lower()=="o":
            return " O "
    except:
        pass
    return "   "

def print_state(state):
    sep = "_"*11+"\n"
    ret = []
    n=0
    for row in state:
        ret.append("|".join(map(cell,row)))
        n+=1
        if n<3:
                ret.append(sep)
    for line in ret:
        print(line)

def has_won(state):
    players = ['x', 'o']
    for i in [0,1]:
        for row in state:
            if row==tuple(players[i]*3): # _
                return i, True
        for cols in [0, 1, 2]:
            if state[0][cols]==state[1][cols] and state[2][cols]==state[0][cols] and state[0][cols]==players[i]: # |
                return i, True
        if state[0][0]==state[1][1] and state[0][0]==state[2][2] and state[0][0]==players[i]:   # \
                return i, True
        if state[2][0]==state[1][1] and state[2][0]==state[0][2] and state[0][2]==players[i]:   # /
                return i, True
            
    return -1, False

def is_full(state):
    for row in state:
        for v in row:
            if v!="x" and v!="o":
                return False
    return True

def is_valid_move(state, x, y):
    row = state[x]
    if row[y]!="x" and row[y]!="o":
        return True
    return False

def new_state(state, x, y, character):
    l = []
    for row in state:
        l.append(list(row))
    l[x][y] = character
    return (tuple(l[0]), tuple(l[1]), tuple(l[2]))

class Player:
    def move(state):
        return state
    def learn(self, won):
        pass

class HumanPlayer(Player):
    def __init__(self, character):
        self.character=character
        
    def move(self, state):
        print_state(state)
        flag = False
        while not flag:
            print()
            x = int(input(f"({self.character}) row: "))
            y = int(input(f"({self.character}) col: "))
            flag=is_valid_move(state, x, y)
        print()
        
        return new_state(state, x, y, self.character)
    
def do_game(player0, player1, stats, verbose=False):
    state = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    ended = False
    full = False
    won_won = -1
    
    while not ended and not full:
        state = player0.move(state)
        who_won, ended = has_won(state)
        full = is_full(state)        
        if not ended and not full:
            state = player1.move(state)
            who_won, ended = has_won(state)
            full = is_full(state)
    if ended:
        stats.append("WIN 0" if who_won==0 else "WIN 1")
        player0.learn(1.0 if who_won==0 else 0.0)
        player1.learn(1.0 if who_won==1 else 0.0)
    if full and not ended:
        stats.append("DRAW")    
        player0.learn(0.5)
        player1.learn(0.5)
    if verbose:
        print("DRAW" if full and not ended else f"{who_won} has WON!")
        print()
        print_state(state)

import random

class RandomPlayer(Player):
    def __init__(self, character):
        self.character=character
        
    def move(self, state):
        flag = False
        while not flag:
            x = random.randrange(3)
            y = random.randrange(3)
            flag=is_valid_move(state, x, y)
       
        return new_state(state, x, y, self.character)

# from collections import Counter

stats = []

# for i in range(1_000):
#     do_game(RandomPlayer('x'), RandomPlayer('o'), stats, False)
    
# co = Counter(stats)
# # print(co)
# print(sorted(co.elements()))
do_game(HumanPlayer('x'), RandomPlayer('o'), stats, False)

