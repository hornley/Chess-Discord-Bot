letters_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}


class ChessPiece:
    def __init__(self, position, color, icon_id, piece, first_move):
        self.position = position
        self.color = color
        self.icon_id = icon_id
        self.piece = piece
        self.first_move = first_move

    def move(self, pos1, pos2):
        return

    def checkCurrentPositionColor(self):
        column = letters_dict[self.position[0]]
        row = int(self.position[1])

        if row % 2 == 0 and column % 2 != 0 or row % 2 != 0 and column % 2 == 0:
            return 'White'

        return 'Black'


class Pawn(ChessPiece):
    def move(self, pos1, pos2):
        pos1_row, pos2_row = abs(8 - int(pos1[1])), abs(8 - int(pos2[1]))
        move = abs(pos1_row - pos2_row)

        # Returns True if a move is valid, 1 square up or down, or 2 squares up or down for first move, otherwise False
        if move == 2 and not self.first_move or move > 2:
            return False

        if move == 1 and pos1[0] != pos2[0]:
            return True

        return True


class Rook(ChessPiece):
    def move(self, pos1, pos2):
        # For non-horizontal/vertical moves
        if (pos1[0] != pos2[0] and pos1[1] != pos2[1]) or (pos1[0] == pos2[0] and pos1[1] == pos2[1]):
            return False

        return True


class Bishop(ChessPiece):
    def move(self, pos1, pos2):
        from functions import getDiagonal
        # For same column or row
        if pos1[0] == pos2[0] or pos1[1] == pos2[1]:
            return False

        pos1_row, pos2_row = abs(8 - int(pos1[1])), abs(8 - int(pos2[1]))
        pos1_col, pos2_col = letters_dict[pos1[0]] - 1, letters_dict[pos2[0]] - 1

        pos2_color = 'White' if (pos2_row % 2 == 0 and pos2_col % 2 == 0 or pos2_row % 2 != 0
                                 and pos2_col % 2 != 0) else 'Black'

        # If bishop color is not same with the chosen move's color
        if pos2_color != self.checkCurrentPositionColor():
            return False

        # If the move is a valid diagonal move for the bishop's position
        if (pos2_row, pos2_col) not in getDiagonal(pos1_row, pos1_col):
            return False

        return True


class Knight(ChessPiece):
    def move(self, pos1, pos2):
        pos1_row, pos2_row = abs(8 - int(pos1[1])), abs(8 - int(pos2[1]))
        pos1_col, pos2_col = letters_dict[pos1[0]] - 1, letters_dict[pos2[0]] - 1

        pos2_color = 'White' if (pos2_row % 2 == 0 and pos2_col % 2 == 0 or pos2_row % 2 != 0
                                 and pos2_col % 2 != 0) else 'Black'

        if pos2_color == self.checkCurrentPositionColor():
            return False

        possible_knight_moves = [(pos1_row - 2, pos1_col - 1), (pos1_row - 1, pos1_col - 2),
                                 (pos1_row - 2, pos1_col + 1), (pos1_row - 1, pos1_col + 2),
                                 (pos1_row + 2, pos1_col - 1), (pos1_row + 1, pos1_col - 2),
                                 (pos1_row + 1, pos1_col + 2), (pos1_row + 2, pos1_col + 1)]

        if (pos2_row, pos2_col) not in possible_knight_moves:
            return False

        return True


class Queen(ChessPiece):
    def move(self, pos1, pos2):
        from functions import getDiagonal
        pos1_row, pos2_row = abs(8 - int(pos1[1])), abs(8 - int(pos2[1]))
        pos1_col, pos2_col = letters_dict[pos1[0]] - 1, letters_dict[pos2[0]] - 1

        if (pos1[0] == pos2[0] and pos1[1] != pos2[1]) or (pos1[0] != pos2[0] and pos1[1] == pos2[1]):
            return True

        if (pos2_row, pos2_col) in getDiagonal(pos1_row, pos1_col):
            return True

        return False


class King(ChessPiece):
    def move(self, pos1, pos2):
        pos1_row, pos2_row = abs(8 - int(pos1[1])), abs(8 - int(pos2[1]))
        pos1_col, pos2_col = letters_dict[pos1[0]] - 1, letters_dict[pos2[0]] - 1

        possible_king_moves = []
        for _i in range(-1, 2):
            for _j in range(-1, 2):
                if _i == 0 and _j == 0:
                    continue
                possible_king_moves.append((pos1_row + _i, pos1_col + _j))

        if (pos2_row, pos2_col) not in possible_king_moves:
            return False

        return True
