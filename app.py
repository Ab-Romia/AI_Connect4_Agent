"""
Connect 4 AI - Hugging Face Gradio Interface
An intelligent Connect 4 game with adjustable AI difficulty
Fixed version with proper state management
"""

import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from Board import Connect4Board
from MiniMax import minimax
import time
import copy

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

def create_initial_state():
    """Create initial game state dictionary"""
    return {
        'board': Connect4Board(),
        'current_player': 1,
        'game_over': False,
        'move_history': [],
        'ai_depth': 4,
        'winner': None,
        'moves_count': 0
    }

def create_board_image(board_state):
    """Create a PIL image of the current board state"""
    ROWS, COLS = 6, 7
    CELL_SIZE = 100
    PADDING = 10
    RADIUS = (CELL_SIZE - PADDING * 2) // 2

    board = board_state['board']

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
            draw.ellipse([x0, y0, x1, y1], fill=color, outline=COLORS['board'], width=3)

    # Draw column numbers at top
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()

    for col in range(COLS):
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = CELL_SIZE // 2
        text = str(col + 1)
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((center_x - text_width//2, center_y - text_height//2),
                 text, fill=COLORS['text'], font=font)

    return img

def get_game_status(state):
    """Get current game status message"""
    if state['game_over']:
        p1_score = state['board'].connect_4s(1)
        p2_score = state['board'].connect_4s(2)
        if p1_score > p2_score:
            return "🎉 You win! Congratulations!"
        elif p2_score > p1_score:
            return "🤖 AI wins! Better luck next time!"
        else:
            return "🤝 It's a draw!"
    elif state['current_player'] == 1:
        return "🔴 Your turn! Click a column number to play."
    else:
        return "🟡 AI is thinking..."

def get_score_display(state):
    """Get score display"""
    p1_score = state['board'].connect_4s(1)
    p2_score = state['board'].connect_4s(2)

    p1_indicator = " 🏆" if p1_score > p2_score and state['game_over'] else ""
    p2_indicator = " 🏆" if p2_score > p1_score and state['game_over'] else ""

    return f"You (Red): {p1_score}{p1_indicator} | AI (Yellow): {p2_score}{p2_indicator}"

def check_game_over(state):
    """Check if game is over and update state"""
    if not state['board'].valid_moves():
        state['game_over'] = True
        p1_score = state['board'].connect_4s(1)
        p2_score = state['board'].connect_4s(2)
        if p1_score > p2_score:
            state['winner'] = 'player1'
        elif p2_score > p1_score:
            state['winner'] = 'player2'
        else:
            state['winner'] = 'draw'
        return True
    return False

def make_ai_move(state):
    """Make AI move and update state"""
    if state['game_over'] or state['current_player'] != 2:
        return state

    valid_moves = state['board'].valid_moves()
    if not valid_moves:
        state['game_over'] = True
        return state

    try:
        # AI makes a move (Player 2)
        best_col, _ = minimax(
            state['board'],
            depth=state['ai_depth'],
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=True,
            return_tree=False
        )

        if best_col is not None and best_col in valid_moves:
            state['board'].move(best_col, 2)
            state['move_history'].append((best_col, 2))
            state['moves_count'] += 1

            # Check if game is over
            if not check_game_over(state):
                state['current_player'] = 1
    except Exception as e:
        print(f"AI Error: {e}")
        # If AI fails, make a random valid move
        import random
        col = random.choice(valid_moves)
        state['board'].move(col, 2)
        state['move_history'].append((col, 2))
        state['moves_count'] += 1
        if not check_game_over(state):
            state['current_player'] = 1

    return state

def play_column(col_num, state, difficulty):
    """Handle a player's move in a specific column"""
    # Create a deep copy of state to avoid mutations
    state = copy.deepcopy(state)

    try:
        col_idx = col_num - 1  # Convert to 0-indexed (col_num is already 0-6 from buttons)

        if state['game_over']:
            return (
                state,
                create_board_image(state),
                get_game_status(state),
                get_score_display(state),
                "Game is over! Click 'New Game' to play again."
            )

        if state['current_player'] != 1:
            return (
                state,
                create_board_image(state),
                get_game_status(state),
                get_score_display(state),
                "Please wait for AI to finish its move."
            )

        valid_moves = state['board'].valid_moves()
        if col_idx not in valid_moves:
            return (
                state,
                create_board_image(state),
                get_game_status(state),
                get_score_display(state),
                f"❌ Column {col_num} is full! Try another column."
            )

        # Player makes a move
        state['board'].move(col_idx, 1)
        state['move_history'].append((col_idx, 1))
        state['moves_count'] += 1

        # Check if game is over after player move
        if check_game_over(state):
            return (
                state,
                create_board_image(state),
                get_game_status(state),
                get_score_display(state),
                "✓ Move successful! Game Over!"
            )

        # Switch to AI
        state['current_player'] = 2

        # AI makes its move
        state = make_ai_move(state)

        return (
            state,
            create_board_image(state),
            get_game_status(state),
            get_score_display(state),
            f"✓ You played column {col_num}. AI responded!"
        )

    except Exception as e:
        return (
            state,
            create_board_image(state),
            get_game_status(state),
            get_score_display(state),
            f"❌ Error: {str(e)}"
        )

def reset_game(difficulty, state):
    """Reset the game with selected difficulty"""
    # Create completely new state
    state = create_initial_state()

    # Set AI depth based on difficulty
    difficulty_map = {
        "Easy (2 moves)": 2,
        "Medium (4 moves)": 4,
        "Hard (6 moves)": 6,
        "Expert (8 moves)": 8,
    }
    state['ai_depth'] = difficulty_map.get(difficulty, 4)

    return (
        state,
        create_board_image(state),
        get_game_status(state),
        get_score_display(state),
        f"✓ New game started with {difficulty}!"
    )

def undo_move(state):
    """Undo the last move (both AI and player)"""
    state = copy.deepcopy(state)

    if len(state['move_history']) < 2:
        return (
            state,
            create_board_image(state),
            get_game_status(state),
            get_score_display(state),
            "❌ Cannot undo - not enough moves made."
        )

    if state['game_over']:
        state['game_over'] = False
        state['winner'] = None

    try:
        # Undo AI move (if exists)
        if len(state['move_history']) >= 1:
            last_col, last_player = state['move_history'].pop()
            state['board'].undo(last_col, last_player)
            state['moves_count'] -= 1

        # Undo player move
        if len(state['move_history']) >= 1:
            last_col, last_player = state['move_history'].pop()
            state['board'].undo(last_col, last_player)
            state['moves_count'] -= 1

        state['current_player'] = 1
        state['game_over'] = False

        return (
            state,
            create_board_image(state),
            get_game_status(state),
            get_score_display(state),
            "✓ Last moves undone!"
        )
    except Exception as e:
        return (
            state,
            create_board_image(state),
            get_game_status(state),
            get_score_display(state),
            f"❌ Error undoing move: {str(e)}"
        )

# Create Gradio interface
with gr.Blocks(title="Connect 4 AI", theme=gr.themes.Soft()) as demo:

    # Game state (persisted across interactions)
    game_state = gr.State(create_initial_state())

    gr.Markdown(
        """
        # 🎮 Connect 4 AI - Powered by Minimax Algorithm

        Play against an intelligent AI! Connect 4 pieces horizontally, vertically, or diagonally to win.
        **You are Red**, **AI is Yellow**. Click a column number (1-7) to drop your piece!
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            # Board display
            board_display = gr.Image(
                value=create_board_image(create_initial_state()),
                label="Game Board",
                type="pil",
                interactive=False
            )

            # Column buttons
            with gr.Row():
                col_buttons = []
                for i in range(1, 8):
                    btn = gr.Button(str(i), size="lg", variant="primary")
                    col_buttons.append(btn)

            status_text = gr.Textbox(
                value=get_game_status(create_initial_state()),
                label="Game Status",
                interactive=False,
                lines=1
            )

            score_text = gr.Textbox(
                value=get_score_display(create_initial_state()),
                label="Score",
                interactive=False,
                lines=1
            )

            message_box = gr.Textbox(
                label="Message",
                value="Ready to play! Click a column number to start.",
                interactive=False,
                lines=2
            )

        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Game Controls")

            difficulty = gr.Radio(
                choices=[
                    "Easy (2 moves)",
                    "Medium (4 moves)",
                    "Hard (6 moves)",
                    "Expert (8 moves)",
                ],
                value="Medium (4 moves)",
                label="AI Difficulty",
                info="Higher = Stronger AI (slower)"
            )

            with gr.Row():
                reset_button = gr.Button("🔄 New Game", variant="secondary", size="lg")
                undo_button = gr.Button("⬅️ Undo", variant="secondary", size="lg")

            gr.Markdown(
                """
                ### 📖 How to Play

                1. Click a column number (1-7)
                2. Your piece falls to the lowest spot
                3. Connect 4 to win!
                4. AI responds automatically

                ### 🎯 Difficulty Levels
                - **Easy**: Thinks 2 moves ahead
                - **Medium**: Thinks 4 moves ahead ⭐
                - **Hard**: Thinks 6 moves ahead
                - **Expert**: Thinks 8 moves ahead (slow)

                ### 📊 Scoring
                Game counts all Connect-4 patterns.
                Most patterns wins if board fills up!
                """
            )

    # Connect column button events
    def create_column_handler(column_number):
        """Create a handler function for a specific column"""
        def handler(state, diff):
            return play_column(column_number, state, diff)
        return handler

    for i, btn in enumerate(col_buttons):
        btn.click(
            fn=create_column_handler(i+1),
            inputs=[game_state, difficulty],
            outputs=[game_state, board_display, status_text, score_text, message_box]
        )

    # Connect control button events
    reset_button.click(
        fn=reset_game,
        inputs=[difficulty, game_state],
        outputs=[game_state, board_display, status_text, score_text, message_box]
    )

    undo_button.click(
        fn=undo_move,
        inputs=[game_state],
        outputs=[game_state, board_display, status_text, score_text, message_box]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()
