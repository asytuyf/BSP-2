
# ! next week goals :
# 1) code taking moves
# 2) code a beta version of an evaluation function

class Board:
    """
    Represents the configuration of a chess board.
    """

    def __init__(self):
        # This board isn't in it's initial state it's like this for testing purposes
        self.board = [

            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
            'X', 'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 'X',
            'X', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', 'b', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', 'q', 'r', 'k', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', 'p', 'p', ' ', ' ', ' ', 'p', ' ', ' ', 'X',
            'X', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'X',
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
            'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
        ]

    def get_piece(self, position):
        """
        Gets the piece at the given position.
        """
        row, col = position
        # converts 2D coordinate to 1D index :
        index = row * 8 + col
        return self.board[index]

    def set_piece(self, position, piece):
        """
        Sets the piece at the given position.
        """
        row, col = position
        index = row * 8 + col  # convert 2D coordinate to 1D index
        self.board[index] = piece

    def move_piece(self, start, end):
        """
        Moves the piece from the start position to the end position.
        """
        piece = self.get_piece(start)
        self.set_piece(start, "")
        self.set_piece(end, piece)

    def print_board(self):
        """
        Prints the board in the terminal
        """
        # for i in range(2, 10):
        for i in range(9, 1, -1):
            row = ""
            for j in range(1, 9):
                row = row+self.board[i*10+j]
            print(row)

    def findBlackMoves(self, pos):
        """
        Finds all the available moves for some black piece defined by it's position
        """
        res = []
        # KING:
        if self.board[pos] == 'k':
            k_moves = [-1, +1, -10, +10, -9, -11, +11, +9]
            for m in k_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " ":
                    res.append(('k', pos, pos+m))
        # KNIGHT:
        elif self.board[pos] == 'n':
            n_moves = [-21, +21, -19, +19, -12, +12, -8, +8]
            for m in n_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " ":
                    res.append(('n', pos, pos+m))
        # ROOK:
        elif self.board[pos] == 'r':
            r_moves = [-10, +10, -1, +1]
            for m in r_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # if not (21 <= new_pos <= 98):
                    #    break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('r', pos, new_pos))

        # BISHOP :
        elif self.board[pos] == 'b':
            b_moves = [-11, +11, -9, +9]
            for m in b_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # if not (21 <= new_pos <= 98):
                    #    break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('b', pos, new_pos))

        # QUEEN :
        elif self.board[pos] == 'q':
            # Combines rook and bishop moves
            q_moves = [-10, +10, -1, +1, -11, +11, -9, +9]

            for m in q_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # if not (21 <= new_pos <= 98):
                    #    break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('q', pos, new_pos))
        # PAWN:
        elif self.board[pos] == 'p':
            p_moves = [-10, -20]

            for m in p_moves:
                new_pos = pos + m
                # Double move forward from starting position
                # checks if pawn is at its starting position + if there's a piece blocking the move
                if m == -20 and 81 <= pos <= 88:
                    if self.board[new_pos] == " " and self.board[new_pos + 10] == " ":
                        res.append(('p', pos, new_pos))

                # Single move forward
                if m == -10 and 31 <= pos <= 88 and self.board[new_pos] == " ":
                    res.append(('p', pos, new_pos))

        return res

    def findAllBlackMoves(self):
        """
        Using the function findWhiteMoves this function goes through all of the white pieces and finds all the available moves for the white pieces
        """
        def chess_notation(pos):
            """Translate the pos to chess coordinations"""
            # Convert the column number to its corresponding letter
            col = chr((pos % 10) + 96)
            # Convert the row number to a string
            row = str(10 - (pos // 10))
            return col + row
        res = []
        for i in range(2, 10):
            for j in range(1, 9):
                moves = self.findBlackMoves(i * 10 + j)
                for move in moves:
                    piece, start, end = move
                    start_notation = chess_notation(start)
                    end_notation = chess_notation(end)
                    res.append((piece, start_notation, end_notation))
        return res

    def findWhiteMoves(self, pos):
        """
        Finds all the available moves for some black piece defined by it's position
        """
        res = []
        # KING:
        if self.board[pos] == 'K':
            k_moves = [-1, +1, -10, +10, -9, -11, +11, +9]
            for m in k_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " ":
                    res.append(('K', pos, pos+m))
        # KNIGHT:
        elif self.board[pos] == 'N':
            n_moves = [-21, +21, -19, +19, -12, +12, -8, +8]
            for m in n_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " ":
                    res.append(('N', pos, pos+m))
        # ROOK:
        elif self.board[pos] == 'R':
            r_moves = [-10, +10, -1, +1]
            for m in r_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('R', pos, new_pos))

        # BISHOP :
        elif self.board[pos] == 'B':
            b_moves = [-11, +11, -9, +9]
            for m in b_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('B', pos, new_pos))

        # QUEEN :
        elif self.board[pos] == 'Q':
            # Combines rook and bishop moves
            q_moves = [-10, +10, -1, +1, -11, +11, -9, +9]

            for m in q_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != " ":
                        break
                    if self.board[new_pos] != 'X' and self.board[new_pos] == " ":
                        res.append(('Q', pos, new_pos))

        # PAWN:
        elif self.board[pos] == 'P':
            p_moves = [+10, +20]

            for m in p_moves:
                new_pos = pos + m
                # Double move forward from starting position :
                # checks if pawn is at its starting position + if there's a piece blocking the move
                if m == 20 and 31 <= pos <= 38:
                    if self.board[new_pos] == " " and self.board[new_pos - 10] == " ":
                        res.append(('P', pos, new_pos))
                # Single move forward :
                if m == 10 and 31 <= pos <= 98 and self.board[new_pos] == " ":
                    res.append(('P', pos, new_pos))

        return res

    def findAllWhiteMoves(self):
        """
        Using the function findWhiteMoves this function goes through all of the white pieces and finds all the available moves for the white pieces
        """
        def chess_notation(pos):
            """Translate the pos to chess coordinations"""
            # Convert the column number to its corresponding letter
            col = chr((pos % 10) + 96)
            # Convert the row number to a string
            row = str(10 - (pos // 10))
            return col + row
        res = []
        for i in range(2, 10):
            for j in range(1, 9):
                moves = self.findWhiteMoves(i * 10 + j)
                for move in moves:
                    piece, start, end = move
                    start_notation = chess_notation(start)
                    end_notation = chess_notation(end)
                    res.append((piece, start_notation, end_notation))
        return res


my_board = Board()
my_board.print_board()
print(my_board.findWhiteMoves(76))
print("Black moves : ", my_board.findAllBlackMoves())
print("White moves : ", my_board.findAllWhiteMoves())
