from pieces import *

chess_pieces = {'black': {'rook': '<:blackrook:1188399333670920232>', 'knight': '<:blackknight:1188399267828744222>',
                          'bishop': '<:blackbishop:1188399220223385740>', 'queen': '<:blackqueen:1188399311512424579>',
                          'king': '<:blackking:1188399232353304586>', 'pawn': '<:blackpawn:1188399277786017802>'},
                'white': {'rook': '<:whiterook:1188399342877409360>', 'knight': '<:whiteknight:1188399255958859776>',
                          'bishop': '<:whitebishop:1188399205400727552>', 'queen': '<:whitequeen:1188399322744754186>',
                          'king': '<:whiteking:1188399246207090688>', 'pawn': '<:whitepawn:1188399288519241778>'}
                }
nums = {'number_1': '1️⃣', 'number_2': '2️⃣', 'number_3': '3️⃣', 'number_4': '4️⃣',
        'number_5': '5️⃣', 'number_6': '6️⃣', 'number_7': '7️⃣', 'number_8': '8️⃣', }
blank = ['🟦', ':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:',
         ':regional_indicator_e:', ':regional_indicator_f:', ':regional_indicator_g:', ':regional_indicator_h:']
white_square = '⬜'
black_square = '⬛'
names = ["pawn", "bishop", "knight", "rook", "queen", "king"]


def assign_piece(color, role, position):
    if role == 'pawn':
        return Pawn(position, color, chess_pieces[color][role], role, True)
    elif role == 'rook':
        return Rook(position, color, chess_pieces[color][role], role, True)
    elif role == 'knight':
        return Knight(position, color, chess_pieces[color][role], role, True)
    elif role == 'bishop':
        return Bishop(position, color, chess_pieces[color][role], role, True)
    elif role == 'queen':
        return Queen(position, color, chess_pieces[color][role], role, True)
    else:
        return King(position, color, chess_pieces[color][role], role, True)


def getDiagonal(row, col):
    oms = []
    for _x in range(0, 9):
        oms.append((row - _x, col - _x))
        oms.append((row - _x, col + _x))
        oms.append((row + _x, col - _x))
        oms.append((row + _x, col + _x))
    return oms


def get_square_color(pos2_row, pos2_col):
    pos2_row = abs(8 - pos2_row)
    pos2_col = abs(8 - pos2_col)
    return 'White' if (pos2_row % 2 == 0 and pos2_col % 2 != 0 or pos2_row % 2 != 0
                       and pos2_col % 2 == 0) else 'Black'


def boardRows(i, color):
    row = []
    letters = list(letters_dict.keys())
    i = 9 - i
    if i in [1, 8]:
        for letter in letters:
            if letter in ('a', 'h'):
                row.append(assign_piece(color, 'rook', f"{letter}{i}"))
            elif letter in ('b', 'g'):
                row.append(assign_piece(color, 'knight', f"{letter}{i}"))
            elif letter in ('c', 'f'):
                row.append(assign_piece(color, 'bishop', f"{letter}{i}"))
            elif letter == "d":
                row.append(assign_piece(color, 'queen', f"{letter}{i}"))
            else:
                row.append(assign_piece(color, 'king', f"{letter}{i}"))
    else:
        for letter in letters:
            row.append(assign_piece(color, 'pawn', f"{letter}{i}"))
    return row


def valid_rook_move(board, pos1, pos2):
    if pos1[0] == pos2[0]:
        for i in range(pos1[1] + 1, pos2[1]) if pos2[1] > pos1[1] else range(pos2[1] + 1, pos1[1]):
            if isinstance(board[pos1[0]][i], ChessPiece):
                return False
    elif pos1[1] == pos2[1]:
        for i in range(pos1[0] + 1, pos2[0]) if pos2[0] > pos1[0] else range(pos2[0] + 1, pos1[0]):
            if isinstance(board[i][pos1[1]], ChessPiece):
                return False
    return True


def valid_bishop_move(board, pos1, pos2):
    distance = abs(pos2[0] - pos1[0])
    if distance == 1:
        return True

    row_increment = 1 if pos2[0] > pos1[0] else -1
    col_increment = 1 if pos2[1] > pos1[1] else -1
    for i in range(1, distance):
        row = pos1[0] + i * row_increment
        col = pos1[1] + i * col_increment
        if isinstance(board[row][col], ChessPiece):
            return False
    return True


def legal_move(chosen_piece: ChessPiece, board, pos1, pos2):
    role = chosen_piece.piece

    # These two following if statements will check if a move is within a-h or 1-8
    if (pos1[2][0] not in letters_dict or pos2[2][0] not in letters_dict or
            (8 < int(pos1[2][1]) or int(pos1[2][1]) < 1) or (8 < int(pos2[2][1]) or int(pos2[2][1]) < 1)):
        return False

    # Check if the pos2 square is occupied and if the pieces are the same color
    occupied = isinstance(board[pos2[0]][pos2[1]], ChessPiece)
    if occupied and board[pos2[0]][pos2[1]].color == chosen_piece.color:
        return False

    # For same values of pos1 and pos2
    if pos1 == pos2:
        return False

    move_result = chosen_piece.move(pos1[2], pos2[2])

    # Pawn move issue in TO-DO File
    if role in ['knight', 'king']:
        return move_result

    elif role == 'pawn':
        if occupied and pos1[1] == pos2[1]:
            return False
        return move_result

    elif role == 'rook':
        return move_result and valid_rook_move(board, pos1, pos2)

    elif role == 'bishop':
        return move_result and valid_bishop_move(board, pos1, pos2)

    return move_result and (valid_bishop_move(board, pos1, pos2) if (pos2[0], pos2[1]) in getDiagonal(pos1[0], pos1[1])
                            else valid_rook_move(board, pos1, pos2))


'''
down -> to positive
up -> to negative
right -> positive
left -> negative

⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜
⬜⬛⬜⬛⬜⬛⬜⬛
⬛⬜⬛⬜⬛⬜⬛⬜

a8 b8 c8 d8 e8 f8 g8 h8
a7 b7 c7 d7 e7 f7 g7 h7
a6 b6 c6 d6 e6 f6 g6 h6
a5 b5 c5 d5 e5 f5 g5 h5
a4 b4 c4 d4 e4 f4 g4 h4
a3 b3 c3 d3 e3 f3 g3 h3
a2 b2 c2 d2 e2 f2 g2 h2
a1 b1 c1 d1 e1 f1 g1 h1

a8 - h8 is (0, 0) - (0, 7)
a1 - h1 is (7, 0) - (7, 7)

'''
