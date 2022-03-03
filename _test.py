from b import Game
import datetime as dt
import random
from collections import Counter

b = Game()

test_game = {'cross':[['o', 'x','o'],
                    ['x', 'o','o'],
                    ['x', 'x','o']],
            'col': [['o', 'x','o'],
                    ['x', 'x','o'],
                    ['o', 'x','x']],
            'row': [['x', 'o','x'],
                    ['x', 'x','x'],
                    ['o', 'x','o']]}
n = 100
for j in range(n):
    options = ['x', 'o']
    out = []
    for i in range(3):
        out.append([random.choice(options),random.choice(options),random.choice(options)])
    test_game[str(j)] = out

for i in test_game:
    b.state = test_game[i]
    print(f'{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {i} test: {b.who_win(b.state)}')
    if b.who_win(b.state) == (-1, False):
        print(b.state)

# for i in test_game:
#     print(test_game[i])

# with open('test.txt', 'w+') as f:
#     for i in test_game:
#         f.write(str(test_game[i] + '\n'))