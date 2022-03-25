
from random import random, randrange



class Board:
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]
        self.board = '''     |     |     
     |     |     
     |     |     
-----------------
     |     |     
     |     |     
     |     |     
-----------------
     |     |     
     |     |     
     |     |     '''
        self._board = '''     |     |     
     |     |     
     |     |     
-----------------
     |     |     
     |     |     
     |     |     
-----------------
     |     |     
     |     |     
     |     |     '''


class Game(Board):
    def is_full(self, state):
        for i in state:
            for j in i:
                if j != 'x' or j != 'o':
                    return False
        return True

    def is_valid_move(self, x, y):
        row = self.state[x]
        if row[y]!="x" and row[y]!="o":
            return True
        return False

    def make_move(self, player):
        flag = False
        while not flag:
            x = int(input(f'wiersz {player}:'))
            y = int(input(f'kolumna{player}:'))
            flag = self.is_valid_move(x, y)
        self.state[x][y] = player

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
    
    def do_game(self,player1, player2, plot = True):
        ended = False
        full = False
        while not ended and not full:
            player1.make_move()
            if plot is True:
                print(self.state)
            who_won, ended = self.who_win(self.state)
            if not ended and not full:
                player2.make_move()
                who_won, ended = self.who_win(self.state)    
            full = self.is_full(self.state)


        return print(f'Wygrał {self.who_win(self.state)[0]}')
        

class HumanPlayer(Game):
    def __init__(self, sign):
        self.sign = sign
    
    def make_move(self, state):
        flag = False
        while not flag:
            x = int(input(f'wiersz {player}:'))
            y = int(input(f'kolumna{player}:'))
            flag = self.is_valid_move(x, y)
        state[x][y] = self.sign


class ComputerPlayer(Game):
    def __init__(self, sign):
        self.sign = sign
    
    def make_move(self ):
        flag = False
        while not flag:
            x = randrange(3)
            y = randrange(3)
            flag = self.is_valid_move(x, y)
        self.state[x][y] = self.sign

b = Game()
a = ComputerPlayer('o')
c = ComputerPlayer('x')
print(b.do_game(a, c))

# b.state = [[0,'x', 'o'], ['o','x', 0],[0, 'x', 0]] #kolumna 2
#b.state = [['x', 'o', 'o'], [0, 'x', 'o'], [0, 0, 'x']] #ukos 1
#b.state = [[0,'o', 'o'], ['x', 'x', 'x'],[0, 0, 'o']] #wiersz 2

# print(b.who_win(b.state))

