import math
from random import randrange, sample
from collections import Counter
from copy import deepcopy

class Board:
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]
        self.board = '''
     +     +     
     +     +     
     +     +     
=================
     +     +     
     +     +     
     +     +     
=================
     +     +     
     +     +     
     +     +     
'''
    def cell(self, x):
        try:
            if x.lower()=="x":
                return " X "
            if x.lower()=="o":
                return " O "
        except:
            pass
        return "   "

    def print_state(self, state):
        sep = "_"*11+"\n"
        ret = []
        n=0
        for row in state:
            ret.append("|".join(map(self.cell,row)))
            n+=1
            if n<3:
                    ret.append(sep)
        for line in ret:
            print(line)
    # def print_move(self):
    #     # rows, cols = 1+x*4, 2+y*6  
    #     # self.board = ''.join()
    #     # self.board[1+x*4][2+y*6] = sign
    #     s = ''
    #     for i in self.board:
    #         s += str(i) + '\n'
    #     print(s)

class Game(Board):
    def is_full(self, state):
        for i in state:
            for j in i:
                if j != 'x' and j != 'o':
                    return False
        return True

    def is_valid_move(self, x, y, state):        
        if x > 2 or y > 2:
            return False
        row = state[x]
        if row[y] != 'x' and row[y] != 'o':
            return True
        return False

    def who_win(self, state):
        player = ['x', 'o']
        for winner in ['x', 'o']:            
            for row in self.state:
                if row == list(3 * winner):
                    return winner, True

            for col in [0, 1, 2]:
                if self.state[0][col] == self.state[1][col] and self.state[0][col] == self.state[2][col] and self.state[0][col] == winner:
                    return winner, True
            
            if self.state[0][0] == self.state[1][1] and self.state[0][0] == self.state[2][2] and self.state[0][0] == winner:
                    return winner, True
            
            if self.state[0][2] == self.state[1][1] and self.state[0][2] == self.state[2][0] and self.state[0][2] == winner:
                    return winner, True
        
        return -1, False
    
    def do_game(self, player1, player2, stats = [], plot = True):
        ended = False
        full = False
        moves = 0
        while not ended and not full:
            player1.make_move(self.state)
            if plot == True:
                print(self.print_state(self.state))
            who_won, ended = self.who_win(self.state)
            full = self.is_full(self.state)
            moves += 1
            if not ended and not full:
                state = player2.make_move(self.state)
                if plot == True:
                    print(self.print_state(self.state))
                who_won, ended = self.who_win(self.state)
                full = self.is_full(self.state)
                moves += 1
        if ended:
            stats.append("WIN 0" if who_won=="x" else "WIN 1")
            player1.learn(1.0 if who_won==0 else 0.0)
            player2.learn(1.0 if who_won==1 else 0.0)
        if full and not ended:
            stats.append("DRAW")    
            player1.learn(0.5)
            player2.learn(0.5)


        if who_won != -1:
            print(f'Wygrał {who_won}')
        else:
            print('Remis')
        
class Player:
    def move(state):
        return state
    def learn(self, won):
        pass

class HumanPlayer(Game, Player):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign
    
    def make_move(self, state):
        flag = False
        while not flag:
            x = int(input(f'wiersz {self.sign}:'))
            y = int(input(f'kolumna{self.sign}:'))
            flag = self.is_valid_move(x, y, state)
        state[x][y] = self.sign


class ComputerPlayer(Game, Player):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

    def make_move(self, state):
        flag = False
        while not flag:
            x = int(randrange(3))
            y = int(randrange(3))
            flag = self.is_valid_move(x, y, state)
        state[x][y] = self.sign

class QPlayer(Game, Player):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign                     
        self.q_table = {}
        self.alfa = 0.15
        self.beta = 0.60
        self.gamma = 0.99
        self.previous_state = None
        self.current_state = ((0,0,0),(0,0,0),(0,0,0))

    def list2tuple(self, l):
        return tuple(tuple(x) for x in l)

    def tuple2list(self, t):
        return [list(x) for x in t]

    def add_move2state(self, state, x, y, sign):
        newstate = deepcopy(state)
        newstate[x][y] = sign
        return newstate

    def initialize_q_table(self, state):
        '''
        state -> list_state create tuple_state
        '''   
        actions = {}
        for x in range(3):
            for y in range(3):
                if self.is_valid_move(x, y, state):
                    actions[self.list2tuple(self.add_move2state(state, x, y, self.sign))] = self.beta
        self.q_table[self.list2tuple(state)] = actions

        return actions

    def make_move(self, state):
        '''
        state -> list_state create tuple_state
        '''
        if self.previous_state:
            actions = self.q_table.get(self.current_state, {})
            if self.list2tuple(state) not in actions.keys():
                actions[self.list2tuple(state)] = self.beta
                self.q_table[self.current_state] = actions
            
        actions = self.q_table.get(self.list2tuple(state))
        if not actions:
            actions = self.initialize_q_table(state)

        best_q = max(actions.values())

        best_actions = [ action for action, q in actions.items() if q==best_q ]
 
        self.previous_state = state
        self.current_state = sample(best_actions, 1)[0]

        state = self.tuple2list(self.current_state)

    def learn(self, learned_weight):
        
        self.q_table[self.list2tuple(self.previous_state)][self.list2tuple(self.current_state)] = learned_weight
        self.previous_state = None
        
        for state, actions in self.q_table.items():
            for next_move, q in actions.items():
                next_move_actions = self.q_table.get(next_move)
                if next_move_actions:
                    best_next_q = max(next_move_actions.values())
                   
                    actions[next_move] = (1 - self.alfa) * q + self.gamma * self.alfa * best_next_q                     
                    self.q_table[state] = actions

stats = []
# for i in range(3):
#     print(f'###################  {i+1}   ###################')
#     b = Game()
#     a = ComputerPlayer('x')
#     c = ComputerPlayer('o')
#     b.do_game(a, c, stats)



# # print('Koniec')
b = Game()
# a = HumanPlayer('x')
# d = ComputerPlayer('o')
c = QPlayer('o')
# b.do_game(d, c, stats, plot=True)

state = [[0,'x',0],[0,'x',0],['o',0,0]]
print(c.initialize_q_table(state))

# b.state = [['x', 'x', 'x'], ['x', 'x', 'x'], ['x', 'x', 'x']]
# print(c.state)
# print(b.state)

# print(a.initialize_q_table([[0, 'o', 0], [0, 'x', 0], [0, 'o', 0]]))
# print(a.q_table)

print(Counter(stats))








# b.state = [[0, 'o', 0], [0, 'x', 0], [0, 'o', 0]] #kolumna 2
# print(b.is_valid_move(1,1))
#b.state = [['x', 'o', 'o'], [0, 'x', 'o'], [0, 0, 'x']] #ukos 1
#b.state = [[0,'o', 'o'], ['x', 'x', 'x'],[0, 0, 'o']] #wiersz 2

# print(b.who_win(b.state))



# b = Game()
# a = HumanPlayer('x')
# c = ComputerPlayer('o')
# print(b.do_game(a, c))


