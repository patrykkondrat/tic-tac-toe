# import b


# class Testing(b.ComputerPlayer, b.HumanPlayer):
#     pass

# test = b.Game()

# test.state = [['x', 0, 0], [0, 0, 0], [0, 0, 0]]

# pl1 = b.ComputerPlayer('x')
# pl2 = b.ComputerPlayer('o')

# print(test.do_game(test, pl1, pl2))


class Meow:
    def __init__(self) -> None:
        state = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

class How:
    def __init__(self) -> None:
        self.sign = 'x'
    def make_move(self, state):
        
        state = [[0, 0, 0], [0, 'x', 0], [0, 0, 0]]

How.make_move(Meow.state)