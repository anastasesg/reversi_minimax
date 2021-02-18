WHITE, WHITE_STR = 1, "\u25cb"
BLACK, BLACK_STR = -1, "\u25cf"
EMPTY, EMPTY_STR = 0, " "


class Game:
    """
    Every state of the game will be an instant of the class.
    It contains every relavent information of the game.
    """
    def __init__(self):
        self.current_player = BLACK
        self.board = [[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, BLACK, WHITE, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, WHITE, BLACK, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]]
        self.__directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]

    def __getString(self, x, y):
        """
        Returns the coresponding string respresenting each player
        :param x: Indicates the row of the board
        :param y: Indicates the column of the board
        """
        if self.board[x][y] == BLACK:
            return BLACK_STR
        elif self.board[x][y] == WHITE:
            return WHITE_STR
        else:
            return EMPTY_STR

    def __str__(self):
        """
        Overrides the original print statement in order to print the board when calling 'print(Game())'
        """
        string = ["    1   2   3   4   5   6   7   8\n", "  +---+---+---+---+---+---+---+---+\n"]
        for x in range(8):
            string.append("{} ".format(x + 1))
            for y in range(8):
                string.append("| {} ".format(self.__getString(x, y)))
            string.append("|\n")
            string.append("  +---+---+---+---+---+---+---+---+\n")
        return "".join(string)

    @staticmethod
    def __isOnBoard(move):
        """
        Returns true if the move is inside the board and false otherwise
        :param move: a tuple containg the position of the square the player wishes to place a token
        """
        return 0 <= move[0] < 8 and 0 <= move[1] < 8
    
    def __isEmpty(self, move):
        """
        Returns true if move is inside the board and false otherwise
        :param move: a tuple containg the position of the square the player wishes to place a token
        """
        return self.board[move[0]][move[1]] == EMPTY

    def __incrementUntilSameColor(self, origin, direction):
        """
        This method is to help the method '__flipsTiles()' check if a given move generates a list of
        coordinates of squares whose tokens must flip colors. It returns the coordinates of the end 
        suare and true if such list exists and (none, false) otherwise.
        :param origin: The starting position of the method
        :param direction: A given direction which the method will "move" towards to in order to complete the check.
        """
        current_square = origin
        current_square = [x + y for x, y in zip(current_square, direction)]

        while self.__isOnBoard(current_square) and self.board[current_square[0]][current_square[1]] == -self.current_player:
            current_square = [x + y for x, y in zip(current_square, direction)]
        
        if self.__isOnBoard(current_square) and self.board[current_square[0]][current_square[1]] == self.current_player:
            return True, current_square
        else:
            return False, None

    def __flipsTiles(self, move):
        """
        Returns a list containing the position of the squares which contain the opponent's token which must cange color 
        :param move: a tuple containg the position of the square the player wishes to place a token
        """
        toBeFlipped = list()
        for direction in self.__directions:
            found, end = self.__incrementUntilSameColor(move, direction)
            while found and (not end == move):
                end = [x - y for x, y in zip(end, direction)]
                if not end == move:
                    toBeFlipped.append(end)
        return toBeFlipped

    def isValid(self, move):
        """
        Returns true if a move is valid and false otherwise
        :param move: a tuple containg the position of the square the player wishes to place a token
        """
        return self.__isOnBoard(move) and len(self.__flipsTiles(move)) > 0 and self.__isEmpty(move)
    
    def hasValid(self):
        """
        Returns true if the current player has any valid moves and false otherwise
        """
        for x in range(8):
            for y in range(8):
                if self.isValid([x, y]):
                    return True
        return False
    
    def getValid(self):
        """
        Returns a list containing every valid move the current player can make
        """
        validList = list()
        for x in range(8):
            for y in range(8):
                if self.isValid([x, y]):
                    validList.append([x, y])
        return validList

    def makeMove(self, move):
        """
        Executes the give move, updates the board and switches current player to it's opponent
        """
        if self.isValid(move):
            toBeFliped = self.__flipsTiles(move)
            self.board[move[0]][move[1]] = self.current_player
            for x, y in toBeFliped:
                self.board[x][y] = self.current_player
            self.current_player = -self.current_player

    def isFinished(self):
        """
        Returns true if the game is over and false otherwise
        """
        for x in range(8):
            for y in range(8):
                if self.__isEmpty([x, y]):
                    return False
        return True