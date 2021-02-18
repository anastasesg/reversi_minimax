import subprocess
import sys

from game import *
from players import *


def play():
    subprocess.call('clear')
    game = Game()

    choice = input('Do you want to play first: ')
    player = BLACK * (choice == 'Yes') + WHITE * (choice == 'No')

    choice = input('Choose the maximum search depth: ')
    depth = int(choice)

    subprocess.call('clear')

    last_move = [-1, -1]
    tokens = getTokens(game)
    while not game.isFinished():
        print(game)
        if game.current_player == player:
            print("The last move was {} and the score is {}".format([x + 1 for x in last_move], tokens))
            humanPlayer(game)
        else:
            last_move = aiPlayer(game, float('-inf'), float('inf'), depth, True)
            tokens = getTokens(game)
        subprocess.call('clear')
    score = getScore(game)
    if score[player] > score[-player]:
        print("Congratulations! You Won!\n")
        print("Black: {} and White: {}".format(score[BLACK], score[WHITE]))
    elif score[player] < score[-player]:
        print("The agent won!\n")
        print("Black: {} and White: {}".format(score[BLACK], score[WHITE]))
    else:
        print("It's a tie!")
    return None


if __name__ == '__main__':
    play()
    sys.exit()