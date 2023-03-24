import board

# ! changes needed to be made :
# * 1 - if dy poses problems change it to work with alphabets


class Piece:
    """
    Represents a chess piece.
    """

    def __init__(self, color):
        self.color = color

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the piece from the start position to the end position is a valid move.
        """
        return True

    def is_white(self):
        """
        Returns True if the piece is white, and False if it is black.
        """
        return self.color == 'w'

    def __str__(self):
        """
        Returns a string representation of the piece for printing to the terminal.
        """
        return ""


class Rook(Piece):
    """
    Represents a rook chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the rook from the start position to the end position is a valid move.
        """
        if start[0] != end[0] and start[1] != end[1]:
            return False
        row, col = start
        row_dir = 0 if start[0] == end[0] else (1 if start[0] < end[0] else -1)
        col_dir = 0 if start[1] == end[1] else (1 if start[1] < end[1] else -1)
        while (row, col) != end:
            row += row_dir
            col += col_dir
            if board.get_piece((row, col)) is not None:
                return False
        return True

    def __str__(self):
        """
        Returns a string representation of the rook for printing to the terminal.
        """
        return "R"


class Knight(Piece):
    """
    Represents a knight chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the knight from the start position to the end position is a valid move.
        """
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        return (dx, dy) in [(1, 2), (2, 1)]

    def __str__(self):
        """
        Returns a string representation of the knight for printing to the terminal.
        """
        return "N"


class Bishop(Piece):
    """
    Represents a bishop chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the bishop from the start position to the end position is a valid move.
        """
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        if dx != dy:
            return False
        row, col = start
        row_dir = 1 if start[0] < end[0] else -1
        col_dir = 1 if start[1] < end[1] else -1
        while (row, col) != end:
            row += row_dir
            col += col_dir
            if board.get_piece((row, col)) is not None:
                return False
        return True

    def __str__(self):
        """
        Returns a string representation of the bishop for printing to the terminal.
        """
        return "B"


class Queen(Piece):
    """
    Represents a queen chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the queen from the start position to the end position is a valid move.
        """
        if start[0] == end[0] or start[1] == end[1]:
            # horizontal or vertical move
            return Rook(self.color).is_valid_move(start, end, board)
        else:
            # diagonal move
            return Bishop(self.color).is_valid_move(start, end, board)

    def __str__(self):
        """
        Returns a string representation of the queen for printing to the terminal.
        """
        return "Q"


class King(Piece):
    """
    Represents a king chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the king from the start position to the end position is a valid move.
        """
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        if dx <= 1 and dy <= 1:
            # normal move
            return True
        elif self.can_castle(start, end, board):
            # castling move
            return True
        else:
            # invalid move
            return False

    def can_castle(self, start, end, board):
        """
        Checks if the king can castle from the start position to the end position.
        """
        pass

    def __str__(self):
        """
        Returns a string representation of the king for printing to the terminal.
        """
        return "K"

# ! kind of already implemented but is_valid_move needs to be completed


class GhostPawn(Piece):
    """
    Represents a ghost pawn chess piece that can be taken en passant.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Returns False since a ghost pawn cannot move.
        """
        return False

    def __str__(self):
        """
        Returns a string representation of the ghost pawn for printing to the terminal.
        """
        return ""


class Pawn(Piece):
    """
    Represents a pawn chess piece.
    """

    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, start, end, board):
        """
        Checks if moving the pawn from the start position to the end position is a valid move.
        """
        dx = end[0] - start[0]
        dy = abs(end[1] - start[1])
        piece_at_end = board.get_piece(end)
        if piece_at_end is not None and piece_at_end.is_white() == self.is_white():
            # cannot capture piece of same color
            return False
        if dx == 0:
            if piece_at_end is not None:
                # cannot move forward if there is a piece in the way
                return False
            elif dy == 1:
                # normal forward move
                return True
            elif dy == 2 and start[0] in [1, 6]:
                # double forward move from starting position
                row_dir = 1 if self.color == "white" else -1
                row = start[0] + row_dir
                return board.get_piece((row, start[1])) is None and board.get_piece((end[0], end[1])) is GhostPawn(self.color).set_en_passant((row, start[1]))
                return True
            else:
                return False
        elif dx == 1 and dy == 1:
            # diagonal capture
            if piece_at_end is not None:
                return True
            else:
                # en passant capture
                ghost_pawn = board.get_piece((start[0], end[1]))
                if isinstance(ghost_pawn, GhostPawn) and ghost_pawn.en_passant == (start[0], end[1]):
                    return True
                else:
                    return False
        else:
            return False

    def __str__(self):
        """
        Returns a string representation of the pawn for printing to the terminal.
        """
        return "P"
