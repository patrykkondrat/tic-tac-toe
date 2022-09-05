from main import Game, ComputerPlayer, HumanPlayer, QPlayer, AnnelingQPlayer, plot_games
from collections import Counter


if __name__ == '__main__':
    stats = []
    stats2 = []
    stats3 = []

    qplayer1 = QPlayer('x')
    qplayer2 = QPlayer('o')
    computerplayer1 = ComputerPlayer('x')
    computerplayer2 = ComputerPlayer('o')
    humanplayer1 = HumanPlayer('x')
    humanplayer2 = HumanPlayer('o')
    aqplayer1 = AnnelingQPlayer('x')
    aqplayer2 = AnnelingQPlayer('o')

    for i in range(500):
        b = Game()
        b.do_game(qplayer1, computerplayer2, stats, plot=False)


    for i in range(500):
        e = Game()
        e.do_game(aqplayer1, computerplayer2, stats2, plot=False)

    for i in range(500):
        f = Game()
        f.do_game(aqplayer1, qplayer2, stats3, plot=False)

    print('qplayer:', Counter(stats))
    print('comp:', Counter(stats2))
    print('aqplayer:', Counter(stats3))

    plot_games(stats, 'QPlayer', 'ComputePlayer', False)
    plot_games(stats2, 'AnnelingQPlayer', 'ComputePlayer', False)
    plot_games(stats3, 'AnnelingQPlayer', 'QPlayer', False)
