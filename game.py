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
    
    def is_valid_move(state):
        for col in state:
            for i in col:
                if i != 'x' and i != 'o':
                    return False
        return True
    
    def 