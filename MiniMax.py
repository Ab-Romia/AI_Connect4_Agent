from Board import Connect4Board

class MinimaxNode:
    def __init__(self, move=None, score=0, children=None):
        self.move = move
        self.score = score
        self.children = children or []


POSITIONAL_WEIGHTS = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3]
]

COLUMN_WEIGHTS = [40, 70, 120, 200, 120, 70, 40]


def evaluate_window(board, row, col, delta_row, delta_col, player):
    pieces = []
    for i in range(4):
        r = row + i * delta_row
        c = col + i * delta_col
        if r < 0 or r >= 6 or c < 0 or c >= 7:
            return 0
        idx = r * 7 + c
        if board.player1 & (1 << idx):
            pieces.append(1)
        elif board.player2 & (1 << idx):
            pieces.append(2)
        else:
            pieces.append(0)

    opponent = 2 if player == 1 else 1
    count = pieces.count(player)
    empty = pieces.count(0)
    block = pieces.count(opponent)

    # Tactical scoring for current player
    if count == 4:
        return 100_000
    elif count == 3 and empty == 1:
        return 1000
    elif count == 2 and empty == 2:
        return 100
    elif count == 1 and empty == 3:
        return 10

    # Penalize if opponent is about to win (force blocking)
    if block == 3 and empty == 1:
        return -800  # urgent to block
    elif block == 2 and empty == 2:
        return -50
    return 0



def evaluate_board(board):
    player1_score = 0
    player2_score = 0

    for row in range(6):
        for col in range(7):
            for delta_row, delta_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                player1_score += evaluate_window(board, row, col, delta_row, delta_col, 1)
                player2_score += evaluate_window(board, row, col, delta_row, delta_col, 2)

            idx = row * 7 + col
            if board.player1 & (1 << idx):
                player1_score += POSITIONAL_WEIGHTS[row][col] + COLUMN_WEIGHTS[col]
            elif board.player2 & (1 << idx):
                player2_score += POSITIONAL_WEIGHTS[row][col] + COLUMN_WEIGHTS[col]

    # The AI is player 2
    return player2_score - player1_score



def minimax(board, depth, alpha, beta, maximizing_player, level=0, return_tree=False):
    valid_columns = board.valid_moves()
    indent = "    " * level
    is_terminal = not valid_columns

    if is_terminal or depth == 0:
        if is_terminal:
            p1_wins = board.connect_4s(1)
            p2_wins = board.connect_4s(2)
            score = (p2_wins - p1_wins) * 1_000_000
            if return_tree:
                return None, score, MinimaxNode(None, score)
            return None, score
        eval_score = evaluate_board(board)
        if return_tree:
            return None, eval_score, MinimaxNode(None, eval_score)
        return None, eval_score

    move_scores = []
    for col in valid_columns:
        board.move(col, 2 if maximizing_player else 1)
        score = evaluate_board(board)
        board.undo(col, 2 if maximizing_player else 1)
        move_scores.append((score, col))

    move_scores.sort(reverse=maximizing_player)

    best_col = move_scores[0][1]
    best_score = float('-inf') if maximizing_player else float('inf')
    node = MinimaxNode(None)

    if maximizing_player:
        for _, col in move_scores:
            board.move(col, 2)
            _, eval, child = minimax(board, depth - 1, alpha, beta, False, level + 1, return_tree)
            board.undo(col, 2)
            if return_tree:
                child.move = col
                node.children.append(child)
            if eval > best_score:
                best_score = eval
                best_col = col
                if return_tree:
                    node.score = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
    else:
        for _, col in move_scores:
            board.move(col, 1)
            _, eval, child = minimax(board, depth - 1, alpha, beta, True, level + 1, return_tree)
            board.undo(col, 1)
            if return_tree:
                child.move = col
                node.children.append(child)
            if eval < best_score:
                best_score = eval
                best_col = col
                if return_tree:
                    node.score = eval
            beta = min(beta, eval)
            if beta <= alpha:
                break

    if return_tree:
        node.move = best_col
        return best_col, best_score, node
    return best_col, best_score




