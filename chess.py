from board import *
from piece import *
# ! C
blocked_path = "There's a piece in the path."
incorrect_path = "This piece does not move in this pattern."


class Player:
    """
    Represents a player in the game.
    """

    def __init__(self, color):
        self.color = color


class Chess:
    """
    Represents the state of a game of chess.
    """

    def __init__(self):
        self.board = Board()
        self.white_player = "W"
        self.black_player = "B"
        self.current_player = self.white_player
        self.en_passant = None

    def promotion(self, position, new_piece):
        """
        Promotes a pawn that has reached the end of the board to a new piece.
        """
        piece = self.board.get_piece(position)
        if not isinstance(piece, Pawn):
            raise ValueError("Cannot promote non-pawn piece")
        if (piece.player == self.white_player and position[0] != 0) or (piece.player == self.black_player and position[0] != 7):
            raise ValueError("Pawn has not reached the end of the board")
        self.board.set_piece(position, new_piece(piece.player))
        # ! needs to prompt the user to promote and check if it's a valid promotion

    def move(self, start, end):
        """
        Moves a piece from its current location to a destination.
        """
        piece = self.board.get_piece(start)
        if piece == piece.lower():
            new_piece = "B" + piece
        else:
            new_piece = "W" + piece
        if piece is None:
            raise ValueError("No piece at start position")
        if new_piece[0] != self.current_player:
            raise ValueError("Wrong player's turn")
        # ! error here (Board.py need to be changed) :
        # if not piece.is_valid_move(start, end, self.board):
        #     raise ValueError("Invalid move")
        self.board.move_piece(start, end)

        # Handle en passant
        if isinstance(piece, Pawn) and end == self.en_passant:
            capture_pos = (end[0] - 1 if piece.player ==
                           self.black_player else end[0] + 1, end[1])
            self.board.set_piece(capture_pos, None)

        # Handle pawn promotion
        if isinstance(piece, Pawn) and (end[0] == 0 or end[0] == 7):
            self.promotion(end, Queen)

        # Update en passant
        if isinstance(piece, Pawn) and abs(start[0] - end[0]) == 2:
            self.en_passant = ((start[0] + end[0]) // 2, start[1])
        else:
            self.en_passant = None

        # Switch the current player
        self.current_player = self.black_player if self.current_player == self.white_player else self.white_player

    def make_move(self):
        # ! needs formatting
        """
        Prompts the user for input to make a move and executes the move.
        """
        print("\033[1m\033[3m                    INFO:\033[0m")
        print("\033[91m1 - White starts first \033[0m")
        print("\033[91m2 - if you want to quit the game type : stop \033[0m")
        print("\n\n")
        chess_game.board.print_board()
        number_for_input = 0
        # ! if we input something like 7Ber and 5Bjk the programme still works while it's not a correct move so it needs to change
        while True:
            print("\n")
            piece_pos = input(
                "Enter the position of the piece to move [ROW + COLUMN] (e.g. '7B'): ")
            if piece_pos == "stop":
                break
            else:
                start = (int(piece_pos[0]) - 1, ord(piece_pos[1]) - 65)

            dest_pos = input(
                "Enter the destination position [ROW + COLUMN] (e.g. '5C'): ")
            if dest_pos == "stop":
                break
            end = (int(dest_pos[0]) - 1, ord(dest_pos[1]) - 65)

            try:
                piece = self.board.get_piece(start)
                if piece == piece.lower():
                    new_piece = "B" + piece
                else:
                    new_piece = "W" + piece
                # needs to be tested
                if piece is None:
                    raise ValueError("No piece at start position")
                if new_piece[0] != self.current_player:
                    raise ValueError("Wrong player's turn")
                # ! something wrong here
                # if not piece.is_valid_move(start, end, self.board):
                #     raise ValueError("Invalid move")
                self.move(start, end)
                print("\033[32mMove successful.\033[0m")
                print("\n")
                self.board.print_board()
            except ValueError as e:
                print(f"\033[1;31mError:\033[0m {e}")


# Example usage
chess_game = Chess()
chess_game.make_move()
