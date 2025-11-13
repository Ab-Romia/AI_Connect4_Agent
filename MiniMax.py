"""
Connect 4 AI Engine using Minimax with Alpha-Beta Pruning

This module implements an intelligent AI opponent for Connect 4 using:
- Minimax algorithm for optimal decision-making
- Alpha-beta pruning for performance optimization
- Sophisticated position evaluation with tactical scoring
- Move ordering for enhanced pruning efficiency
"""

from Board import Connect4Board


class MinimaxNode:
    """
    Represents a node in the minimax decision tree.

    Used for visualization of the AI's decision-making process.

    Attributes:
        move (int): Column index of the move (0-6)
        score (int): Evaluation score for this position
        children (list): List of child MinimaxNode objects
    """
    def __init__(self, move=None, score=0, children=None):
        self.move = move
        self.score = score
        self.children = children or []


# Positional weights favor center columns and middle rows (max value: 13)
POSITIONAL_WEIGHTS = [
    [3, 4, 5, 7, 5, 4, 3],   # Bottom row
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5], # Middle rows (highest value)
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3]    # Top row
]

# Column weights heavily favor the center column (max value: 200)
COLUMN_WEIGHTS = [40, 70, 120, 200, 120, 70, 40]


def evaluate_window(board, row, col, delta_row, delta_col, player):
    """
    Evaluate a 4-piece window for tactical scoring.

    Analyzes a sequence of 4 positions in a given direction and assigns scores based on:
    - Number of player's pieces
    - Number of empty spaces
    - Opponent threats that need blocking

    Args:
        board (Connect4Board): Current board state
        row (int): Starting row (0-5)
        col (int): Starting column (0-6)
        delta_row (int): Row increment (-1, 0, or 1)
        delta_col (int): Column increment (-1, 0, or 1)
        player (int): Player to evaluate for (1 or 2)

    Returns:
        int: Score for this window
            +100,000 = Win (4 in a row)
            +1,000 = 3 in a row with 1 empty
            +100 = 2 in a row with 2 empty
            +10 = 1 piece with 3 empty
            -800 = Opponent has 3 in a row (urgent block)
            -50 = Opponent has 2 in a row
            0 = No tactical value
    """
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
        return 100_000  # Winning position
    elif count == 3 and empty == 1:
        return 1000     # Strong threat
    elif count == 2 and empty == 2:
        return 100      # Building opportunity
    elif count == 1 and empty == 3:
        return 10       # Weak potential

    # Penalize if opponent is about to win (force blocking)
    if block == 3 and empty == 1:
        return -800  # Urgent to block!
    elif block == 2 and empty == 2:
        return -50   # Minor opponent threat
    return 0



def evaluate_board(board):
    """
    Evaluate the entire board position.

    Combines tactical window evaluation with positional scoring to determine
    the overall value of a board state from Player 2 (AI)'s perspective.

    Scoring components:
    1. Tactical patterns (from evaluate_window for all directions)
    2. Positional weights (favor center positions)
    3. Column weights (heavily favor center column)

    Args:
        board (Connect4Board): Current board state

    Returns:
        int: Net score (positive favors AI/Player 2, negative favors Player 1)
    """
    player1_score = 0
    player2_score = 0

    for row in range(6):
        for col in range(7):
            # Evaluate all 4-piece windows in all directions
            for delta_row, delta_col in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                player1_score += evaluate_window(board, row, col, delta_row, delta_col, 1)
                player2_score += evaluate_window(board, row, col, delta_row, delta_col, 2)

            # Add positional bonuses
            idx = row * 7 + col
            if board.player1 & (1 << idx):
                player1_score += POSITIONAL_WEIGHTS[row][col] + COLUMN_WEIGHTS[col]
            elif board.player2 & (1 << idx):
                player2_score += POSITIONAL_WEIGHTS[row][col] + COLUMN_WEIGHTS[col]

    # Return net score from AI's (Player 2) perspective
    return player2_score - player1_score



def minimax(board, depth, alpha, beta, maximizing_player, level=0, return_tree=False):
    """
    Minimax algorithm with alpha-beta pruning for optimal move selection.

    Recursively searches the game tree to find the best move by:
    1. Evaluating positions at terminal nodes (depth=0 or game over)
    2. Maximizing score for AI, minimizing for opponent
    3. Pruning branches that can't affect the outcome (alpha-beta)
    4. Using move ordering to enhance pruning efficiency

    Args:
        board (Connect4Board): Current board state
        depth (int): How many moves to look ahead (0 = evaluate immediately)
        alpha (float): Best score maximizing player can guarantee
        beta (float): Best score minimizing player can guarantee
        maximizing_player (bool): True if AI's turn (maximize), False if opponent (minimize)
        level (int): Current depth in tree (for debugging/visualization)
        return_tree (bool): Whether to return decision tree for visualization

    Returns:
        tuple: (best_column, best_score, tree_root)
            - best_column (int): Optimal column to play (0-6)
            - best_score (int): Expected score of that move
            - tree_root (MinimaxNode): Decision tree (if return_tree=True)
    """
    valid_columns = board.valid_moves()
    indent = "    " * level
    is_terminal = not valid_columns

    # Base case: terminal node (game over or depth limit reached)
    if is_terminal or depth == 0:
        if is_terminal:
            # Game over - score based on who has more Connect-4s
            p1_wins = board.connect_4s(1)
            p2_wins = board.connect_4s(2)
            score = (p2_wins - p1_wins) * 1_000_000
            if return_tree:
                return None, score, MinimaxNode(None, score)
            return None, score
        # Depth limit - evaluate position heuristically
        eval_score = evaluate_board(board)
        if return_tree:
            return None, eval_score, MinimaxNode(None, eval_score)
        return None, eval_score

    # Move ordering: evaluate moves first to explore promising branches earlier
    # This significantly improves alpha-beta pruning efficiency
    move_scores = []
    for col in valid_columns:
        board.move(col, 2 if maximizing_player else 1)
        score = evaluate_board(board)
        board.undo(col, 2 if maximizing_player else 1)
        move_scores.append((score, col))

    # Sort moves: best moves first for maximizer, worst first for minimizer
    move_scores.sort(reverse=maximizing_player)

    best_col = move_scores[0][1]
    best_score = float('-inf') if maximizing_player else float('inf')
    node = MinimaxNode(None)

    if maximizing_player:
        for _, col in move_scores:
            board.move(col, 2)
            if return_tree:
                _, eval, child = minimax(board, depth - 1, alpha, beta, False, level + 1, return_tree)
                child.move = col
                node.children.append(child)
            else:
                _, eval = minimax(board, depth - 1, alpha, beta, False, level + 1, return_tree)
            board.undo(col, 2)
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
            if return_tree:
                _, eval, child = minimax(board, depth - 1, alpha, beta, True, level + 1, return_tree)
                child.move = col
                node.children.append(child)
            else:
                _, eval = minimax(board, depth - 1, alpha, beta, True, level + 1, return_tree)
            board.undo(col, 1)
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




