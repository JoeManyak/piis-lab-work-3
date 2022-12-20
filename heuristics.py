import chess

# took tables from https://github.com/maksimKorzh/wukongJS/blob/dfc687d585a02e08fbe9c92d2c30b70da00c766d/wukong.js#L926
pawnMatrix = [
    0, 0, 0, 0, 0, 0, 0, 0,
    -4, 68, 61, 47, 47, 49, 45, -1,
    6, 16, 25, 33, 24, 24, 14, -6,
    0, -1, 9, 28, 20, 8, -1, 11,
    6, 4, 6, 14, 14, -5, 6, -6,
    -1, -8, -4, 4, 2, -12, -1, 5,
    5, 16, 16, -14, -14, 13, 15, 8,
    0, 0, 0, 0, 0, 0, 0, 0,
]

knightMatrix = [
    -55, -40, -30, -28, -26, -30, -40, -50,
    -37, -15, 0, -6, 4, 3, -17, -40,
    -25, 5, 16, 12, 11, 6, 6, -29,
    -24, 5, 21, 14, 18, 9, 11, -26,
    -36, -5, 9, 23, 24, 21, 2, -24,
    -32, -1, 4, 19, 20, 4, 11, -25,
    -38, -22, 4, -1, 8, -5, -18, -34,
    -50, -46, -32, -24, -36, -25, -34, -50,
]

bishopMatrix = [
    -16, -15, -12, -5, -10, -12, -10, -20,
    -13, 5, 6, 1, -6, -5, 3, -6,
    -16, 6, -1, 16, 7, -1, -6, -5,
    -14, -1, 11, 14, 4, 10, 11, -13,
    -4, 5, 12, 16, 4, 6, 2, -16,
    -15, 4, 14, 8, 16, 4, 16, -15,
    -5, 6, 6, 6, 3, 6, 9, -7,
    -14, -4, -15, -4, -9, -4, -12, -14,
]

rookMatrix = [
    5, -2, 6, 2, -2, -6, 4, -2,
    8, 13, 11, 15, 11, 15, 16, 4,
    -6, 3, 3, 6, 1, -2, 3, -5,
    -10, 5, -4, -4, -1, -6, 3, -2,
    -4, 3, 5, -2, 4, 1, -5, 1,
    0, 1, 1, -3, 5, 6, 1, -9,
    -10, -1, -4, 0, 5, -6, -6, -9,
    -1, -2, -6, 9, 9, 5, 4, -5,
]

queenMatrix = [
    -25, -9, -11, -3, -7, -13, -10, -17,
    -4, -6, 4, -5, -1, 6, 4, -5,
    -8, -5, 2, 0, 7, 6, -4, -5,
    0, -4, 7, -1, 7, 11, 0, 1,
    -6, 4, 7, 1, -1, 2, -6, -2,
    -15, 11, 11, 11, 4, 11, 6, -15,
    -5, -6, 1, -6, 3, -3, 3, -10,
    -15, -4, -13, -8, -3, -16, -8, -24
]

kingMatrix = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -37, -43, -49, -50, -39, -40, -30,
    -32, -41, -40, -46, -49, -40, -46, -30,
    -32, -38, -39, -52, -54, -39, -39, -30,
    -20, -33, -29, -42, -44, -29, -30, -19,
    -10, -18, -17, -20, -22, -21, -20, -13,
    14, 18, -1, -1, 4, -1, 15, 14,
    21, 35, 11, 6, 1, 14, 32, 22
]


# heuristic is a function that returns heuristic games "score"
def heuristic(board: chess.Board):
    # --- checking for game end ---
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    # --- defining lens for material ---
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    rook_score = sum([rookMatrix[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + \
                 sum([-rookMatrix[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])

    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    knight_score = sum([knightMatrix[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + \
                   sum([-knightMatrix[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])

    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    bishop_score = sum([bishopMatrix[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + \
                   sum([-bishopMatrix[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])

    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    queen_score = sum([queenMatrix[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + \
                  sum([-queenMatrix[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    pawn_score = sum([pawnMatrix[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + \
                 sum([-pawnMatrix[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])

    king_score = sum([kingMatrix[i] for i in board.pieces(chess.KING, chess.WHITE)]) + \
                 sum([-kingMatrix[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
    # --- heuristic calculations ---

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    heuristicTotalScore = material + pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score

    if board.turn:
        return heuristicTotalScore
    else:
        return -heuristicTotalScore
