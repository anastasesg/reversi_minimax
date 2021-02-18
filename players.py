from random import shuffle
from copy import deepcopy

BLACK = -1
WHITE = 1
WEIGHTS = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]


def minimax(state_name, alpha, beta, depth, is_maximizing):
    children, moves = getChildren(state_name)
    player = state_name.current_player
    score = getScore(state_name)
    shuffle(children)

    if is_maximizing:
        max_value, max_move = float('-inf'), [-1, -1]

        if state_name.isFinished() or depth == 0:
            return score[player] - score[-player], max_move

        for num, child in enumerate(children):
            min_value, min_move = minimax(child, alpha, beta, depth - 1, False)
            if min_value > max_value:
                max_value, max_move = min_value, moves[num]
            if max_value >= beta:
                return max_value, max_move
            alpha = max(alpha, max_value)

        return max_value, max_move
    else:
        min_value, min_move = float('inf'), [-1, -1]

        if state_name.isFinished() or depth == 0:
            return score[player] - score[-player], min_move

        for num, child in enumerate(children):
            max_value, max_move = minimax(child, alpha, beta, depth - 1, True)
            if max_value < min_value:
                min_value, min_move = max_value, moves[num]
            if min_value <= alpha:
                return min_value, min_move
            beta = min(beta, min_value)

        return min_value, min_move


def getChildren(state_name):
    children = list()
    moves = state_name.getValid()

    for move in moves:
        temporary_game = deepcopy(state_name)
        temporary_game.makeMove(move)
        children.append(temporary_game)
    return children, moves


def getTokens(state_name):
    black_tokens = 0
    white_tokens = 0

    for i in range(8):
        for j in range(8):
            if state_name.board[i][j] == BLACK:
                black_tokens += 1
            elif state_name.board[i][j] == WHITE:
                white_tokens += 1
    return {'Black': black_tokens, 'White': white_tokens}


def getScore(state_name):
    black_score = 0
    white_score = 0

    for i in range(8):
        for j in range(8):
            if state_name.board[i][j] == BLACK:
                black_score += WEIGHTS[i][j]
            elif state_name.board[i][j] == WHITE:
                white_score += WEIGHTS[i][j]
    return {BLACK: black_score, WHITE: white_score}


def humanPlayer(state_name):
    while True:
        if state_name.hasValid():
            move = [int(num) - 1 for num in input("Where do you want to place your token: ").split(',')]
            if state_name.isValid(move):
                state_name.makeMove(move)
                break
            else:
                print("The move you made isn't valid. Please give a valid move")
        else:
            print("I'm sorry you don't have any valid moves.")
            state_name.current_player = - state_name.current_player
            break


def aiPlayer(state_name, alpha, beta, depth, is_maximizing):
    if state_name.hasValid():
        value, move = minimax(state_name, alpha, beta, depth, is_maximizing)
        print('The AI decided to place a token on [{}, {}]'.format(move[0] + 1, move[1] + 1))
        state_name.makeMove(move)
        return move
    else:
        print("The AI has no valid moves. It's your turn to play.")
        state_name.current_player = -state_name.current_player
        return None
