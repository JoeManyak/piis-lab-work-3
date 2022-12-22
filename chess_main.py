import chess
from heuristics import heuristic


class AIEngine:
    def __init__(self, board: chess.Board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def negaMax(self, depth):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if depth == 0:
            return heuristic(self.board), None
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * (self.negaMax(depth - 1)[0])
            if score > bestScore:
                bestScore = score
                bestMove = move
            self.board.pop()
        return bestScore, bestMove

    def negaScout(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if depth == 0:
            return heuristic(self.board), None

        def getMaxScore(depth, alpha, beta):
            if depth == 0:
                return heuristic(self.board)
            a = alpha
            b = beta
            i = 1

            for move in self.board.legal_moves:
                self.board.push(move)
                t = -1 * (self.negaScout(depth - 1, -b, -alpha)[0])
                self.board.pop()
                if alpha < t < beta and i > 1 and depth < self.maxDepth - 1:
                    a = -1 * (self.negaScout(depth - 1, -beta, -t)[0])
                a = max(a, t)
                if a >= beta:
                    return a
                b = a + 1
                i = i + 1
            return a

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * (getMaxScore(depth - 1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestScore, bestMove

    def PVS(self, depth, alpha, beta):
        bestMove = chess.Move.null()
        bestScore = float('-inf')
        if depth == 0:
            return heuristic(self.board), None

        def getPVSScore(depth, alpha, beta):
            if depth == 0:
                return heuristic(self.board)

            bSearchPv = True
            for move in self.board.legal_moves:
                self.board.push(move)
                if bSearchPv:
                    score = -1 * (getPVSScore(depth - 1, -beta, -alpha))
                else:
                    score = -1 * (getPVSScore(depth - 1, -alpha - 1, -alpha))
                    if alpha < score < beta:
                        score = -1 * (getPVSScore(depth - 1, -beta, -alpha))
                self.board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
                    bSearchPv = False

            return alpha

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * (getPVSScore(depth - 1, alpha, beta))
            self.board.pop()

            if score > bestScore:
                bestScore = score
                bestMove = move

        return bestScore, bestMove


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playPlayerMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")
        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method, alpha, beta):
        engine = AIEngine(self.board, maxDepth, color)

        if method == negamaxNumber:
            bestMove = engine.negaMax(maxDepth)[1]

        elif method == negascoutNumber:
            bestMove = engine.negaScout(maxDepth, alpha, beta)[1]

        else:
            bestMove = engine.PVS(maxDepth, alpha, beta)[1]

        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print(">>> STARTING THE GAME <<<\n")
        print("You playing with white units")

        maxDepth = 3
        alpha = float('-inf')
        beta = float('inf')

        turn = chess.WHITE
        while not self.board.is_checkmate():
            print(self.board)
            if turn == chess.WHITE:
                print('\nWhite\'s turn!\n')
                self.playPlayerMove()
                turn = chess.BLACK
                continue

            if turn == chess.BLACK:
                print('\nBlack\'s turn!\n')
                self.playAIMove(maxDepth, aiColor, method, alpha, beta)
                turn = chess.WHITE
        return


# defining keys for methods
negamaxNumber = 1
negascoutNumber = 2
PVSNumber = 3

if __name__ == '__main__':
    engine = GameEngine(chess.Board())
    print("Possible methods:\n 1. negamax\n 2. negascout\n 3. PVS")
    method = -1
    while True:
        if 0 < method < 4:
            break
        else:
            try:
                method = int(input("Choose method by entering number: "))
            except ValueError:
                print("Entered number is invalid, using negamax by default")
                method = 1

    depth = -1
    while True:
        if 1 < depth < 6:
            break
        else:
            try:
                depth = int(input("Choose depth by entering number (2-5): "))
            except ValueError:
                print("Entered number is invalid, using depth 3 by default")
                depth = 3

    engine.startGame(method)
