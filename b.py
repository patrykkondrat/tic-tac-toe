
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
                if self.state[0][col] == self.state[1][col] and self.state[0][col] == self.state[2][col] and self.state[0] == winner:
                    return winner, True
            
            if self.state[0][0] == self.state[1][1] and self.state[0][0] == self.state[2][2] and self.state[0][0] == winner:
                    return winner, True
            
            if self.state[0][2] == self.state[1][1] and self.state[0][2] == self.state[2][0] and self.state[0][2] == winner:
                    return winner, True
        
        return -1, False

    def do_game(self, plot = True):
        ended = False
        full = False
        while not ended and not full:
            try:
                for i in ['x', 'o']:
                    self.make_move(i)
                    if plot == True:
                        print(self.state)
                    who_won, ended = self.who_win(self.state)
                    full = self.is_full(self.state)
            except IndexError:
                 print('Źle')
        return print(f'Wygrał {self.who_win(self.state)[0]}')
        

class HumanPlayer(Game):
    pass

class ComputerPlayer(HumanPlayer):
    pass

b = Game()
# print(b.do_game())

# b.state = [[0,'x', 'o'], ['o','x', 0],[0, 'x', 0]]
# print(b.who_win(b.state))

b.do_game()