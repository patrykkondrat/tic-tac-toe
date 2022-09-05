from pickle import FALSE
from random import randrange, sample, choice
from collections import Counter
from copy import deepcopy
import matplotlib.pyplot as plt
from pprint import pprint
import json, sys, os, math

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
        # self.state = [[0,0,0],[0,0,0],[0,0,0]]
        ended = False
        full = False
        moves = 0
        while not ended and not full:
            player1.make_move(self.state)
            if plot == True:
                print(self.print_state(self.state))
            who_won, ended = self.who_win(self.state)
            full = self.is_full(self.state)
            if not ended and not full:
                state = player2.make_move(self.state)
                if plot == True:
                    print(self.print_state(self.state))
                who_won, ended = self.who_win(self.state)
                full = self.is_full(self.state)
        if ended:
            stats.append("WIN 0" if who_won=="x" else "WIN 1")
            player1.learn(1.0 if who_won==player1.sign else 0.0)
            player2.learn(1.0 if who_won==player2.sign else 0.0)
        if full and not ended:
            stats.append("DRAW")    
            player1.learn(0.5)
            player2.learn(0.5)

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
               
        if os.path.isfile('./q.table.json'):
            self.q_table = json.load('./q.table.json')
        else:
            self.q_table = {}

        self.sign = sign 
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

    def is_diff_move(self, state, state1):
        for x in range(3):
            for y in range(3):
                if state[x][y] != state1[x][y]:
                    return True, (x, y)
        return False

    def make_move(self, state):
        '''
        state -> list_state creates tuple_state
        '''
        state_copy = deepcopy(self.list2tuple(state))
        if self.previous_state:
            actions = self.q_table.get(self.current_state, {})
            if state_copy not in actions.keys():
                actions[state_copy] = self.beta
                self.q_table[self.current_state] = actions
        
        actions = self.q_table.get(state_copy)
        if not actions:
            actions = self.initialize_q_table(state)

        best_q = max(actions.values())
        
        best_actions = [action for action, q in actions.items() if q==best_q]

        self.previous_state = state_copy
        self.current_state = sample(best_actions, 1)[0]

        state[:] = self.tuple2list(self.current_state)

    def learn(self, learned_weight):
        
        self.q_table[self.previous_state][self.current_state] = learned_weight
        self.previous_state = None

        for state, actions in self.q_table.items():
            for next_move, q in actions.items():
                next_move_actions = self.q_table.get(next_move)
                if next_move_actions:
                    best_next_q = max(next_move_actions.values())

                    actions[next_move] = (1 - self.alfa) * q + self.gamma * self.alfa * best_next_q                     
                    self.q_table[state] = actions
        
        if os.path.exists('./q_table.json'):
            pass
        else:
            with open('q_table.json', 'a') as f:
                f.write(str(self.q_table))

class AnnelingQPlayer(QPlayer):
    def __init__(self, sign):
        super().__init__(sign)

    def learn(self, learned_weight):
        global alfa
        self.alfa *= self.gamma
        super().learn(learned_weight)

def plot_games(qstats, label0, label1, save=False):
    games = range(40, len(qstats), 20)
    won0 = [ Counter(qstats[:x])['WIN 0']/x for x in games]
    won1 = [ Counter(qstats[:x])['WIN 1']/x for x in games]
    draw = [ Counter(qstats[:x])['DRAW']/x for x in games]


    fig = plt.figure()
    plt.figure(figsize=(20,10))
    plt.title('Results ratio')
    player0, = plt.plot(games, won0, label=label0)
    player1, = plt.plot(games, won1, label=label1)
    draws, = plt.plot(games, draw, label="Draws")
    plt.legend(handles=[player0, player1,  draws], frameon=True, loc="best",  fontsize=16)
    plt.show()
    if save is True:
        plt.savefig()



