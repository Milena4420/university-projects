from interfaces import Token, Strategy, Board
import copy


class Rules:
    def __init__(self, board):
        self.board = board

    def is_full(self) -> bool:
        """Vérifie si le plateau est complètement rempli de jetons."""
        for col in range(self.board.width):
            if self.board.column(col)[0] == Token.EMPTY:
                return False
        return True

    def has_win(self) -> bool:
        """Détermine si un joueur a gagné en formant un alignement de quatre jetons."""
        red = Token.RED
        yellow = Token.YELLOW
        win = [(red, red, red, red), (yellow, yellow, yellow, yellow)]

        # Alignement horizontal
        for i in range(self.board.height):
            li = self.board.line(i)
            for k in range(len(li) - 3):
                if tuple(li[k:k + 4]) in win:
                    return True

        # Alignement vertical
        for i in range(self.board.width):
            col = self.board.column(i)
            for k in range(len(col) - 3):
                if tuple(col[k:k + 4]) in win:
                    return True
        # Alignement diagonal
        for i in self.board.diagonals():
            for k in range(len(i) - 3):
                if tuple(i[k:k + 4]) in win:
                    return True
        return False


def evaluate(current_rules: Rules, p: Token) -> int:
    """ Définit un score selon l'état du plateau et du jeton à poser.
     Voici les variables: p = player, o = oppenent, n = neutral"""

    score = 0

    if p == Token.YELLOW:
        o = Token.RED
    else:
        o = Token.YELLOW

    n = Token.EMPTY
    weights = {
        (o, o, o, o): -10000,
        (p, p, p, p): 10000,
        (n, n, n, n): 0,
        (o, o, o, n): -5000,
        (p, p, p, n): 1000,
        (n, o, o, o): -5000,
        (n, p, p, p): 1000,
        (o, n, o, n): -45,
        (p, n, p, n): 45,
        (n, o, n, o): -40,
        (n, p, n, p): 40,
        (o, n, n, o): -35,
        (p, n, n, p): 35,
        (n, p, p, n): 50,
        (n, o, o, n): -50,
        (n, n, o, o): -50,
        (n, n, p, p): 60,
        (o, o, n, n): -50,
        (p, p, n, n): 60,
        (p, n, n, n): 25,
        (o, n, n, n): -25,
        (n, o, n, n): -25,
        (n, p, n, n): 25,
        (n, n, o, n): -25,
        (n, n, p, n): 25,
        (n, n, n, o): -25,
        (n, n, n, p): 25,
        (o, p, o, p): 10,
        (p, o, p, o): -10,
        (p, p, p, o): 40,
        (o, o, o, p): -40,
        (p, o, o, o): -45,
        (o, p, p, p): 45,
        (o, p, p, o): 30,
        (p, o, o, p): -30,
        (p, p, o, o): 0,
        (o, o, p, p): 0,
        (p, n, o, n): 0,
        (o, n, p, n): 0,
        (o, n, n, p): 0,
        (p, n, n, o): 0,
        (o, p, n, n): 10,
        (p, o, n, n): -10,
        (n, p, o, n): 0,
        (n, o, p, n): 0,
        (n, n, o, n): -25,
        (o, o, p, o): -60,
        (o, o, p, n): -30,
        (o, o, n, o): -5000,
        (o, o, n, p): -40,
        (o, p, o, o): -30,
        (o, p, o, n): -20,
        (o, p, n, o): -20,
        (o, p, n, p): 20,
        (o, n, o, o): -5000,
        (o, n, o, p): -40,
        (o, n, p, o): -30,
        (o, n, p, p): 60,
        (p, o, o, n): -40,
        (p, o, p, p): 50,
        (p, o, p, n): 20,
        (p, o, n, o): -30,
        (p, o, n, p): 20,
        (p, p, o, p): 70,
        (p, p, o, n): 50,
        (p, p, n, o): 60,
        (p, p, n, p): 1000,
        (p, n, o, o): -60,
        (p, n, o, p): 20,
        (p, n, p, o): 30,
        (p, n, p, p): 1000,
        (n, o, o, p): -60,
        (n, o, p, o): -30,
        (n, o, p, p): 40,
        (n, o, n, p): -10,
        (n, p, o, o): -40,
        (n, p, o, p): 15,
        (n, p, p, o): 60,
        (n, p, n, o): 10,
        (n, n, o, p): -20,
        (n, n, p, o): 20
    }

    # alignement horizontal
    for i in range(current_rules.board.height):
        li = current_rules.board.line(i)
        for k in range(len(li) - 3):
            combination = (li[k], li[k + 1], li[k + 2], li[k + 3])
            if combination in weights.keys():
                score += weights[combination]

    # alignement vertical
    for i in range(current_rules.board.width):
        col = current_rules.board.column(i)
        for k in range(len(col) - 3):
            combination = (col[k], col[k + 1], col[k + 2], col[k + 3])
            if combination in weights.keys():
                score += weights[combination]

    # alignement diagonal
    for i in current_rules.board.diagonals():
        for k in range(len(i) - 3):
            combination = (i[k], i[k + 1], i[k + 2], i[k + 3])
            if combination in weights.keys():
                score += weights[combination]

    return score


class IntegraleDeRiemannStrategy(Strategy):
    def __init__(self):
        self.max_depth = 5

    def authors(self):
        return "Gnanaseelan, Loreto, Santos"

    def minimax(self, board, depth, maximizing_player, alpha, beta, your_token, opponent_token) -> tuple:
        """ Implémentation de l'algorithme Minimax et l'élagage Alpha-Beta """
        current_rules = Rules(board)
        if depth == 0 or current_rules.is_full():
            if current_rules.has_win():
                return (float('inf'), None) if maximizing_player else (float('-inf'), None)
            else:
                return evaluate(current_rules, your_token), None
        best_col = None
        if maximizing_player:
            max_eval = float('-inf')
            # Exploration de chaque colonne possible à jouer
            for col in range(current_rules.board.width):
                if current_rules.board.column(col)[0] == Token.EMPTY:
                    new_board = copy.deepcopy(current_rules.board)
                    new_board.play(col, your_token)
                    eval_score, _ = self.minimax(new_board, depth - 1, False, alpha, beta,
                                                 your_token, opponent_token)
                    # Mise à jour du meilleur score et de la meilleure colonne si le score est amélioré
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_col = col
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval, best_col

        else:
            min_eval = float('inf')
            # Exploration de chaque colonne possible pour jouer
            for col in range(current_rules.board.width):
                if current_rules.board.column(col)[0] == Token.EMPTY:
                    new_board = copy.deepcopy(current_rules.board)
                    new_board.play(col, opponent_token)
                    eval_score, _ = self.minimax(new_board, depth - 1, True, alpha, beta,
                                                 your_token, opponent_token)
                    # Mise à jour du score minimal et de la meilleure colonne si le score est réduit
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_col = col
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval, best_col

    def play(self, current_board: Board, p: Token) -> int:
        """Sélectionne le meilleur coup à jouer pour le joueur actuel. """
        if p == Token.YELLOW:
            o = Token.RED
        else:
            o = Token.YELLOW
        # Vérifier si c'est le premier coup et jouer au centre
        if all(current_board.column(c)[-1] == Token.EMPTY for c in range(current_board.width)):
            return current_board.width // 2

        # Vérifier si un coup gagnant immédiat est disponible
        for col in range(current_board.width):
            if current_board.column(col)[0] == Token.EMPTY:
                test_board = copy.deepcopy(current_board)
                test_board.play(col, p)
                test_rules = Rules(test_board)
                if test_rules.has_win():
                    return col

        score, col = self.minimax(copy.deepcopy(current_board), self.max_depth, True,
                                  float('-inf'), float('inf'), p, o)

        try:
            new_board = copy.deepcopy(current_board)
            new_board.play(col, p)
        except ValueError:
            available_col = []
            for k in range(current_board.width):
                c = current_board.column(k)
                if c[0] == Token.EMPTY:
                    available_col.append(k)
            col = available_col[0]
            for c in available_col:
                if abs(3 - c) < abs(3 - col):
                    col = c
        return col
