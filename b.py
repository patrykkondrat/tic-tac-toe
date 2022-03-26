
from random import random, randrange



class Board:
    def __init__(self):
        self.state = [[0,0,0],[0,0,0],[0,0,0]]

class Game(Board):

    def is_full(self, state):
        for i in state:
            for j in i:
                if j != 'x' or j != 'o':
                    return False
        return True

    def is_valid_move(self, x, y, state):        
        row = state[x]
        if row[y] != 'x' and row[y] != 'o':
            print(x,y)
            return True
        return False

    # def is_valid_move(self, x, y, state):        
    #     if state[x][y] == 'x' and state[x][y] == 'o':
    #         return False
    #     print(x,y)
    #     return True

    # def is_valid_move(self, x, y):
    #     row = self.state[x]
    #     if row[y] != 'x' and row[y] != 'o':
    #         return True
    #     return False

    # def make_move(self, player):
    #     flag = False
    #     while not flag:
    #         x = int(input(f'wiersz {player}:'))
    #         y = int(input(f'kolumna{player}:'))
    #         flag = self.is_valid_move(x, y)
    #     self.state[x][y] = player

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
        moves = 0
        while not ended and not full:
            player1.make_move(self.state)
            if plot is True:
                print(self.state)
            who_won, ended = self.who_win(self.state)
            moves += 1
            if not ended and not full:
                player2.make_move(self.state)
                if plot is True:
                    print(self.state)
                who_won, ended = self.who_win(self.state)
            full = self.is_full(self.state)
            moves += 1
            # if moves > 9:
            #     print('to nie tak'.upper())
            #     break


        return f'Wygrał "{self.who_win(self.state)[0]}" w liczbie ruchów {moves}'
        

class HumanPlayer(Game):
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


class ComputerPlayer(Game):
    def __init__(self, sign):
        super().__init__()
        self.sign = sign

    def make_move(self, state):
        flag = False
        while not flag:
            x = int(randrange(3))
            y = int(randrange(3))
            flag = self.is_valid_move(x, y, state)
            print(flag)
        state[x][y] = self.sign
    

b = Game()
a = HumanPlayer('o')
c = ComputerPlayer('x')
print(b.do_game(a, c))




# b.state = [[0, 'o', 0], [0, 'x', 0], [0, 'o', 0]] #kolumna 2
# print(b.is_valid_move(1,1))
#b.state = [['x', 'o', 'o'], [0, 'x', 'o'], [0, 0, 'x']] #ukos 1
#b.state = [[0,'o', 'o'], ['x', 'x', 'x'],[0, 0, 'o']] #wiersz 2

# print(b.who_win(b.state))

