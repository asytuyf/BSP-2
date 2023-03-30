
# ! next week goals :
# 1) code taking moves (done)
# 2) code a beta version of an evaluation function (done)

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
            'X', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X',
            'X', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'X',
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
        index = row * 10 + col  # Changed from *8 to *10
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
        for i in range(2, 10):
            # for i in range(9, 1, -1):
            row = ""
            for j in range(1, 9):
                row = row+self.board[i*10+j]
            print(row)

    def findWhiteMoves(self, pos):
        """
        Finds all the available moves for some white piece defined by it's position
        """
        res = []
        # Taking function :

        def can_take_w(target_pos):
            return self.board[target_pos] != "X" and self.board[target_pos].isupper()
        # KING:
        if self.board[pos] == 'k':
            k_moves = [-1, +1, -10, +10, -9, -11, +11, +9]
            for m in k_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " " or can_take_w(pos+m):
                    res.append(('k', pos, pos+m))
        # KNIGHT:
        elif self.board[pos] == 'n':
            n_moves = [-21, +21, -19, +19, -12, +12, -8, +8]
            for m in n_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " " or can_take_w(pos+m):
                    res.append(('n', pos, pos+m))
        # ROOK:
        elif self.board[pos] == 'r':
            r_moves = [-10, +10, -1, +1]
            for m in r_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this it gives me error :
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('r', pos, new_pos))
                        elif self.board[new_pos].isupper():
                            res.append(('r', pos, new_pos))
                            break
                        elif self.board[new_pos].islower():
                            break

        # BISHOP :
        elif self.board[pos] == 'b':
            b_moves = [-11, +11, -9, +9]
            for m in b_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this it gives me error :
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('b', pos, new_pos))
                        elif self.board[new_pos].isupper():
                            res.append(('b', pos, new_pos))
                            break
                        elif self.board[new_pos].islower():
                            break

        # QUEEN :
        elif self.board[pos] == 'q':
            # Combines rook and bishop moves
            q_moves = [-10, +10, -1, +1, -11, +11, -9, +9]

            for m in q_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this it gives me error :
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('q', pos, new_pos))
                        elif self.board[new_pos].isupper():
                            res.append(('q', pos, new_pos))
                            break
                        elif self.board[new_pos].islower():
                            break
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
                if m == -10 and 31 <= pos <= 89 and self.board[new_pos] == " ":
                    res.append(('p', pos, new_pos))
            # Diagonal captures
            diagonal_moves = [-9, -11]
            for m in diagonal_moves:
                new_pos = pos + m
                if can_take_w(new_pos):
                    res.append(('p', pos, new_pos))
        return res

    def findAllWHiteMoves(self):
        """
        Using the function findWhiteMoves this function goes through all of the white pieces and finds all the available moves for the white pieces
        """
        def can_take_b(target_pos):
            return self.board[target_pos] != "X" and self.board[target_pos].isupper()

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

    def findBlackMoves(self, pos):
        """
        Finds all the available moves for some black piece defined by it's position
        """
        res = []
        # Taking function :

        def can_take_b(target_pos):
            return self.board[target_pos] != "X" and self.board[target_pos].islower()
        # KING:
        if self.board[pos] == 'K':
            k_moves = [-1, +1, -10, +10, -9, -11, +11, +9]
            for m in k_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " " or can_take_b(pos+m):
                    res.append(('K', pos, pos+m))
        # KNIGHT:
        elif self.board[pos] == 'N':
            n_moves = [-21, +21, -19, +19, -12, +12, -8, +8]
            for m in n_moves:
                if self.board[pos+m] != "X" and self.board[pos+m] == " " or can_take_b(pos+m):
                    res.append(('N', pos, pos+m))
        # ROOK:
        elif self.board[pos] == 'R':
            r_moves = [-10, +10, -1, +1]
            for m in r_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this it gives me error
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('R', pos, new_pos))
                        elif self.board[new_pos].islower():
                            res.append(('R', pos, new_pos))
                            break
                        elif self.board[new_pos].isupper():
                            break
        # BISHOP :
        elif self.board[pos] == 'B':
            b_moves = [-11, +11, -9, +9]
            for m in b_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this it gives me error
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('B', pos, new_pos))
                        elif self.board[new_pos].islower():
                            res.append(('B', pos, new_pos))
                            break
                        elif self.board[new_pos].isupper():
                            break

        # QUEEN :
        elif self.board[pos] == 'Q':
            # Combines rook and bishop moves
            q_moves = [-10, +10, -1, +1, -11, +11, -9, +9]

            for m in q_moves:
                for i in range(1, 8):
                    new_pos = pos + m * i
                    # ! If i delete this i get error
                    if not (21 <= new_pos <= 98):
                        break
                    if self.board[new_pos] != 'X':
                        if self.board[new_pos] == " ":
                            res.append(('Q', pos, new_pos))
                        elif self.board[new_pos].islower():
                            res.append(('Q', pos, new_pos))
                            break
                        elif self.board[new_pos].isupper():
                            break
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
            # Diagonal captures
            diagonal_moves = [9, 11]
            for m in diagonal_moves:
                new_pos = pos + m
                if can_take_b(new_pos):
                    res.append(('P', pos, new_pos))
        return res

    def findAllBlackMoves(self):
        """
        Using the function findBlackMoves this function goes through all of the white pieces and finds all the available moves for the white pieces
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

    def evaluate_score(board):
        """
        This function evaluates the position of the pieces on the chess board and returns two values indicating the total value of the white pieces and the total value of the black pieces respectively. (some pieces hold more value than others)
        """
        piece_values = {'P': 1, 'N': 3, 'B': 3.5, 'R': 5, 'Q': 10, 'K': 100,
                        'p': -1, 'n': -3, 'b': -3.5, 'r': -5, 'q': -10, 'k': -100}
        white_eval = 0
        black_eval = 0
        for i in range(2, 10):
            for j in range(1, 9):
                piece = board.get_piece((i, j))
                if piece != 'X' and piece != ' ':
                    piece_value = piece_values[piece]
                    if piece.isupper():
                        black_eval += piece_value
                    else:
                        white_eval += piece_value

        return f"White_eval: {white_eval}\nBlack_eval: {black_eval}"

    def captured_pieces(self):
        """
        A function that checks how many pieces were captured from a player and tells you which ones were captured
        """
        black_pieces = 'RNBQKP'
        white_pieces = 'rnbqkp'

        total_white_pieces = 16  # Total number of white pieces at the start
        total_black_pieces = 16  # Total number of black pieces at the start

        current_white_pieces = 0
        current_black_pieces = 0

        current_piece_count = {'R': 0, 'N': 0, 'B': 0, 'Q': 0, 'K': 0,
                               'P': 0, 'r': 0, 'n': 0, 'b': 0, 'q': 0, 'k': 0, 'p': 0}

        for cell in self.board:
            if cell in white_pieces:
                current_white_pieces += 1
                current_piece_count[cell] += 1
            elif cell in black_pieces:
                current_black_pieces += 1
                current_piece_count[cell] += 1

        captured_white_pieces = total_white_pieces - current_white_pieces
        captured_black_pieces = total_black_pieces - current_black_pieces
        initial_piece_count = {'R': 2, 'N': 2, 'B': 2, 'Q': 1, 'K': 1, 'P': 8,
                               'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'p': 8}

        captured_pieces = {}
        for piece, count in current_piece_count.items():
            captured_count = initial_piece_count[piece] - count
            if captured_count > 0:
                captured_pieces[piece] = captured_count

        return captured_white_pieces, captured_black_pieces, captured_pieces


my_board = Board()
my_board.print_board()
print("Black moves : ", my_board.findAllBlackMoves())
print("White moves : ", my_board.findAllWHiteMoves())
print(my_board.evaluate_score())


captured_white_pieces, captured_black_pieces, captured_pieces = my_board.captured_pieces()
print("The number of captured white pieces:", captured_white_pieces)
print("The number of captured black pieces:", captured_black_pieces)
print("The captured pieces are :", captured_pieces)
