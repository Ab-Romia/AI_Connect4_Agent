"""
Connect 4 AI - Hugging Face Gradio Interface
An intelligent Connect 4 game with adjustable AI difficulty
"""

import gradio as gr
import numpy as np
from PIL import Image, ImageDraw
from Board import Connect4Board
from MiniMax import minimax
import time

# Game state (using a class to maintain state across function calls)
class GameState:
    def __init__(self):
        self.board = Connect4Board()
        self.current_player = 1
        self.game_over = False
        self.move_history = []
        self.ai_depth = 4
        self.message = "Your turn! Click a column to play."

    def reset(self):
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.move_history = []
        self.message = "Your turn! Click a column to play."

# Global game state
game = GameState()

# Color scheme
COLORS = {
    'board': (0, 116, 217),      # Blue
    'empty': (255, 255, 255),    # White
    'player1': (255, 65, 54),    # Red (Human)
    'player2': (255, 220, 0),    # Yellow (AI)
    'bg': (240, 240, 240),       # Light gray background
    'text': (51, 51, 51),        # Dark gray text
    'border': (0, 0, 0)          # Black border
}

def create_board_image(board):
    """Create a PIL image of the current board state"""
    ROWS, COLS = 6, 7
    CELL_SIZE = 100
    PADDING = 10
    RADIUS = (CELL_SIZE - PADDING * 2) // 2

    width = COLS * CELL_SIZE
    height = (ROWS + 1) * CELL_SIZE

    # Create image
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    # Draw board background
    board_top = CELL_SIZE
    draw.rectangle([0, board_top, width, height], fill=COLORS['board'])

    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = (ROWS - row) * CELL_SIZE + CELL_SIZE // 2

            # Check piece state from bitboard
            bit_position = 1 << (row * 7 + col)
            if board.player1 & bit_position:
                color = COLORS['player1']
            elif board.player2 & bit_position:
                color = COLORS['player2']
            else:
                color = COLORS['empty']

            # Draw piece
            x0 = center_x - RADIUS
            y0 = center_y - RADIUS
            x1 = center_x + RADIUS
            y1 = center_y + RADIUS
            draw.ellipse([x0, y0, x1, y1], fill=color, outline=COLORS['border'], width=2)

    # Draw column indicators at top
    for col in range(COLS):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = CELL_SIZE // 2
        draw.text((center_x - 10, center_y - 15), str(col + 1), fill=COLORS['text'])

    return img

def get_game_status():
    """Get current game status message"""
    if game.game_over:
        p1_score = game.board.connect_4s(1)
        p2_score = game.board.connect_4s(2)
        if p1_score > p2_score:
            return "🎉 You win! Congratulations!"
        elif p2_score > p1_score:
            return "🤖 AI wins! Better luck next time!"
        else:
            return "🤝 It's a draw!"
    elif game.current_player == 1:
        return "🔴 Your turn! Click a column (1-7) to play."
    else:
        return "🟡 AI is thinking..."

def get_score_display():
    """Get score display"""
    p1_score = game.board.connect_4s(1)
    p2_score = game.board.connect_4s(2)

    p1_indicator = " 🏆" if p1_score > p2_score and game.game_over else ""
    p2_indicator = " 🏆" if p2_score > p1_score and game.game_over else ""

    return f"You (Red): {p1_score}{p1_indicator} | AI (Yellow): {p2_score}{p2_indicator}"

def make_ai_move():
    """Make AI move"""
    if game.game_over:
        return

    valid_moves = game.board.valid_moves()
    if not valid_moves:
        game.game_over = True
        return

    # AI makes a move (Player 2)
    start_time = time.time()
    best_col, _, _ = minimax(
        game.board,
        depth=game.ai_depth,
        alpha=float('-inf'),
        beta=float('inf'),
        maximizing_player=True,
        return_tree=False
    )
    time_taken = time.time() - start_time

    if best_col is not None:
        game.board.move(best_col, 2)
        game.move_history.append((best_col, 2))

        # Check if game is over
        if not game.board.valid_moves():
            game.game_over = True
        else:
            game.current_player = 1

def play_move(column):
    """Handle a player's move"""
    try:
        col_idx = int(column) - 1  # Convert to 0-indexed

        if game.game_over:
            return (
                create_board_image(game.board),
                get_game_status(),
                get_score_display(),
                "Game is over! Click 'New Game' to play again."
            )

        if game.current_player != 1:
            return (
                create_board_image(game.board),
                get_game_status(),
                get_score_display(),
                "Please wait for AI to finish its move."
            )

        if col_idx not in game.board.valid_moves():
            return (
                create_board_image(game.board),
                get_game_status(),
                get_score_display(),
                f"Column {column} is full or invalid! Try another column."
            )

        # Player makes a move
        game.board.move(col_idx, 1)
        game.move_history.append((col_idx, 1))

        # Check if game is over after player move
        if not game.board.valid_moves():
            game.game_over = True
            return (
                create_board_image(game.board),
                get_game_status(),
                get_score_display(),
                "Move successful!"
            )

        # Switch to AI
        game.current_player = 2

        # AI makes its move
        make_ai_move()

        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            f"You played column {column}. AI responded!"
        )

    except ValueError:
        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            "Please enter a valid column number (1-7)."
        )
    except Exception as e:
        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            f"Error: {str(e)}"
        )

def reset_game(difficulty):
    """Reset the game with selected difficulty"""
    game.reset()

    # Set AI depth based on difficulty
    difficulty_map = {
        "Easy (2 moves ahead)": 2,
        "Medium (4 moves ahead)": 4,
        "Hard (6 moves ahead)": 6,
        "Expert (8 moves ahead)": 8,
        "Insane (10 moves ahead)": 10
    }
    game.ai_depth = difficulty_map.get(difficulty, 4)

    return (
        create_board_image(game.board),
        get_game_status(),
        get_score_display(),
        f"New game started with {difficulty} difficulty!"
    )

def undo_move():
    """Undo the last move (both AI and player)"""
    if len(game.move_history) < 2 or game.game_over:
        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            "Cannot undo - not enough moves or game is over."
        )

    try:
        # Undo AI move
        last_col, last_player = game.move_history.pop()
        game.board.undo(last_col, last_player)

        # Undo player move
        last_col, last_player = game.move_history.pop()
        game.board.undo(last_col, last_player)

        game.current_player = 1
        game.game_over = False

        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            "Last move undone!"
        )
    except Exception as e:
        return (
            create_board_image(game.board),
            get_game_status(),
            get_score_display(),
            f"Error undoing move: {str(e)}"
        )

# Create Gradio interface
with gr.Blocks(title="Connect 4 AI - Play Against Intelligent AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎮 Connect 4 AI - Powered by Minimax Algorithm

        Play against an intelligent AI opponent! The AI uses the minimax algorithm with alpha-beta pruning
        to make optimal moves. Adjust the difficulty to control how many moves ahead the AI thinks.

        **How to Play:**
        - You are Red (Player 1), AI is Yellow (Player 2)
        - Enter a column number (1-7) and click "Play Move" to drop your piece
        - Connect 4 pieces horizontally, vertically, or diagonally to win!
        - The game ends when the board is full - highest score wins!
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            board_display = gr.Image(
                value=create_board_image(game.board),
                label="Game Board",
                type="pil"
            )
            status_text = gr.Textbox(
                value=get_game_status(),
                label="Game Status",
                interactive=False
            )
            score_text = gr.Textbox(
                value=get_score_display(),
                label="Score",
                interactive=False
            )

        with gr.Column(scale=1):
            gr.Markdown("### 🎯 Controls")

            difficulty = gr.Radio(
                choices=[
                    "Easy (2 moves ahead)",
                    "Medium (4 moves ahead)",
                    "Hard (6 moves ahead)",
                    "Expert (8 moves ahead)",
                    "Insane (10 moves ahead)"
                ],
                value="Medium (4 moves ahead)",
                label="AI Difficulty",
                info="Higher difficulty = stronger AI (but slower)"
            )

            column_input = gr.Textbox(
                label="Column to Play",
                placeholder="Enter 1-7",
                value="4"
            )

            play_button = gr.Button("🎯 Play Move", variant="primary", size="lg")

            with gr.Row():
                reset_button = gr.Button("🔄 New Game", variant="secondary")
                undo_button = gr.Button("⬅️ Undo", variant="secondary")

            message_box = gr.Textbox(
                label="Message",
                value="Ready to play!",
                interactive=False
            )

            gr.Markdown(
                """
                ### 📊 Game Info

                **Difficulty Levels:**
                - **Easy**: Thinks 2 moves ahead
                - **Medium**: Thinks 4 moves ahead (balanced)
                - **Hard**: Thinks 6 moves ahead
                - **Expert**: Thinks 8 moves ahead (challenging)
                - **Insane**: Thinks 10 moves ahead (very slow but optimal)

                **Scoring:** The game counts all Connect-4 patterns on the board.
                Vertical connections are worth more points!

                ---
                Made with ❤️ using Python, Gradio, and Minimax AI
                """
            )

    # Event handlers
    play_button.click(
        fn=play_move,
        inputs=[column_input],
        outputs=[board_display, status_text, score_text, message_box]
    )

    reset_button.click(
        fn=reset_game,
        inputs=[difficulty],
        outputs=[board_display, status_text, score_text, message_box]
    )

    undo_button.click(
        fn=undo_move,
        inputs=[],
        outputs=[board_display, status_text, score_text, message_box]
    )

    # Allow Enter key to play move
    column_input.submit(
        fn=play_move,
        inputs=[column_input],
        outputs=[board_display, status_text, score_text, message_box]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
