from game import BLACK, WHITE
from random import shuffle
from copy import deepcopy

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


def getChildren(game_name):
    children = list()
    moves = game_name.getValid()

    for move in moves:
        temporary_game = deepcopy(game_name)
        temporary_game.makeMove(move)
        children.append(temporary_game)
    return children, moves

def getTokens(game_name):
    black_tokens = 0
    white_tokens = 0

    for i in range(8):
        for j in range(8):
            if game_name.board[i][j] == BLACK:
                black_tokens += 1
            elif game_name.board[i][j] == WHITE:
                white_tokens += 1
    return {'Black': black_tokens, 'White': white_tokens}

def getScore(game_name):
    black_score = 0
    white_score = 0

    for i in range(8):
        for j in range(8):
            if game_name.board[i][j] == BLACK:
                black_score += WEIGHTS[i][j]
            elif game_name.board[i][j] == WHITE:
                white_score += WEIGHTS[i][j]
    return {BLACK: black_score, WHITE: white_score}

def minimax(game_name, alpha, beta, depth, is_maximizing):
    children, moves = getChildren(game_name)
    player = game_name.current_player
    score = getScore(game_name)
    shuffle(children)

    if is_maximizing:
        max_value, max_move = float('-inf'), [-1, -1]

        if game_name.isFinished() or depth == 0:
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

        if game_name.isFinished() or depth == 0:
            return score[player] - score[-player], min_move

        for num, child in enumerate(children):
            max_value, max_move = minimax(child, alpha, beta, depth - 1, True)
            if max_value < min_value:
                min_value, min_move = max_value, moves[num]
            if min_value <= alpha:
                return min_value, min_move
            beta = min(beta, min_value)

        return min_value, min_move

def human_play(game_name):
    while True:
        if game_name.hasValid():
            move = [int(num) - 1 for num in input("Where do you want to place your token: ").split(',')]
            if game_name.isValid(move):
                game_name.makeMove(move)
                break
            else:
                print("The move you made isn't valid. Please give a valid move")
        else:
            print("I'm sorry you don't have any valid moves.")
            game_name.current_player = -game_name.current_player
            break

def ai_play(game_name, alpha, beta, depth, is_maximizing):
    if game_name.hasValid():
        value, move = minimax(game_name, alpha, beta, depth, is_maximizing)
        print('The AI decided to place a token on [{}, {}]'.format(move[0] + 1, move[1] + 1))
        game_name.makeMove(move)
        return move
    else:
        print("The AI has no valid moves. It's your turn to play.")
        game_name.current_player = -game_name.current_player
        return None
        
