import random as rand

state = (('x','o','x'),
         ('x','o','x'),
         ('o','o','x'))

class Game:    
    def cell(c):
        try:
            if c == 'x':
                return '  X  '
            if c == 'o':
                return '  O  '
        except:
            pass
        return '     '
    
    def is_full(state):
        for col in state:
            for i in col:
                if i != 'x' and i != 'o':
                    return False
        return True
    
    def who_won(state):
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
        

    def is_valid_move(state, x, y):
        row = state[x]
        if row[y] != 'x' and row[y] != 'o':
            return True
        return False

    def do_game(player1, player2, stats=[]):
        state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
        is_end = False
        full = False
        
        while not ended and not full:
            state = player1.move(state)
            won, ended = who_won(state)
            full = is_full(state)        
            if not ended and not full:
                state = player2.move(state)
                won, ended = who_won(state)
                full = is_full(state)
            
        if ended:
            stats.append('Win 0' if won == 0 else 'Win 1')
            player1.learn(1.0 if who_won==0 else 0.0)
            player2.learn(1.0 if who_won==1 else 0.0)
        if full and not ended:
            stats.append("DRAW")    
            player1.learn(0.5)
            player2.learn(0.5)
