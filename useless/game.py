import random

state = (('x','o','x'),
         ('x','o','x'),
         ('o','o','x'))

class Game:
    def __init__(self):
        pass

    def cell(self, c):
        try:
            if c == 'x':
                return '  X  '
            if c == 'o':
                return '  O  '
        except:
            pass
        return '     '
    
    def is_full(self, state):
        for col in state:
            for i in col:
                if i != 'x' and i != 'o':
                    return False
        return True
    
    def who_won(self, state):
        players = ['x', 'o']
        for i in [0, 1]:
            for row in state:
                if row[0] and row[1] and row[0] == players[i]:
                    return i, True
            
            for cols in [0, 1, 2]:
                if state[0][cols] == state[1][cols] and state[0][cols] == state[2][cols] and state[0][cols] == players[i]:
                    return i, True

            if state[0][0]==state[1][1] and state[0][0]==state[2][2] and state[0][0]==players[i]:
                return i, True

            if state[2][0]==state[1][1] and state[2][0]==state[0][2] and state[0][2]==players[i]:
                return i, True 
        
        return -1, False
        

    def is_valid_move(self, state, x, y):
        row = state[x]
        if row[y] != 'x' and row[y] != 'o':
            return True
        return False

    def new_state(self, state, x, y, character):
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

class HumanPlayer(Game, Player):
    def __init__(self, character):
        self.character = character

    def move(self, state):
        flag = False
        while not flag:
            x = int(input(f'{self.character} row: '))
            y = int(input(f'{self.character} col: '))
            flag = self.is_valid_move(state, x, y)

        return self.new_state(state, x, y, self.character)

class RandomPlayer(Game, Player):
    def __init__(self, character):
        self.character=character
        
    def move(self, state):
        flag = False
        while not flag:
            x = random.randrange(3)
            y = random.randrange(3)
            flag = self.is_valid_move(state, x, y)
       
        return self.new_state(state, x, y, self.character)


def do_game(player1, player2, stats=[]):
    state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    ended = False
    full = False
    
    while not ended or not full:
        state = player1.move(state)
        won, ended = Game.who_won(state)
        full = self.is_full(state)        
        if not ended or not full:
            state = player2.move(state)
            won, ended = Game.who_won(state)
            full = is_full(state) 
        
    if ended:
        stats.append('Win 0' if won == 0 else 'Win 1')
        player1.learn(1.0 if won==0 else 0.0)
        player2.learn(1.0 if won==1 else 0.0)
    if full and not ended:
        stats.append("DRAW")    
        player1.learn(0.5)
        player2.learn(0.5)
a = HumanPlayer('x')
b = HumanPlayer('o')
ap = []
print(do_game(a, b, ap))