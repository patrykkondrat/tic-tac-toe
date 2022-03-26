import b


class Testing(b.ComputerPlayer, b.HumanPlayer):
    pass

test = b.Game()

test.state = [['x', 0, 0], [0, 0, 0], [0, 0, 0]]

pl1 = b.ComputerPlayer('x')
pl2 = b.ComputerPlayer('o')

print(test.do_game(test, pl1, pl2))