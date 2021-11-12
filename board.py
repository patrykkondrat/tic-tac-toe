

class CreatBoard:
    def __init__(self):
            self.size = 17

    def board(self):
        height = '#' + ' ' * int(((self.size - 2) / 3)*2) + '#'
        line = height.center(self.size * 2 - 2 ) + '\n'
        out = ''
        for i in range(1,self.size+1):
            if i % int(((self.size - 2) / 3)+1) == 0:
                out += (self.size * 2 - 2 ) * '#' + '\n'
            else:
                out += line
        return out

        

        

        