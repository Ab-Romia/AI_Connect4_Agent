"""
Connect 4 AI - Beautiful Interactive Gradio Interface
An intelligent Connect 4 game with stunning visuals and intuitive gameplay
Redesigned for reliability on Hugging Face Spaces
"""

import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from Board import Connect4Board
from MiniMax import minimax
import copy

# Modern color scheme
COLORS = {
    'bg': (103, 126, 234),           # Purple gradient start
    'bg_end': (118, 75, 162),        # Purple gradient end
    'board': (30, 60, 114),          # Deep blue board
    'board_dark': (23, 42, 81),      # Darker blue for depth
    'empty': (44, 62, 80),           # Dark empty slots
    'player1': (255, 71, 87),        # Vibrant red
    'player2': (255, 165, 2),        # Vibrant orange
    'hover': (255, 255, 255, 80),    # Semi-transparent white
    'text': (255, 255, 255),         # White text
    'win': (0, 210, 255),            # Cyan for wins
    'glow': (255, 255, 255, 40)      # Subtle glow
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
        'hover_col': None
    }

def create_beautiful_board(state, hover_col=None):
    """Create a beautiful PIL image of the board with modern design"""
    ROWS, COLS = 6, 7
    CELL_SIZE = 100
    PADDING = 15
    BOARD_PADDING = 30
    RADIUS = (CELL_SIZE - PADDING * 2) // 2

    # Calculate dimensions
    width = COLS * CELL_SIZE + BOARD_PADDING * 2
    height = ROWS * CELL_SIZE + BOARD_PADDING * 2 + 80  # Extra space for column indicators

    # Create image with gradient background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw gradient background
    for y in range(height):
        ratio = y / height
        r = int(COLORS['bg'][0] + (COLORS['bg_end'][0] - COLORS['bg'][0]) * ratio)
        g = int(COLORS['bg'][1] + (COLORS['bg_end'][1] - COLORS['bg'][1]) * ratio)
        b = int(COLORS['bg'][2] + (COLORS['bg_end'][2] - COLORS['bg'][2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load font
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        col_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        col_font = ImageFont.load_default()

    # Draw title
    title = "🎮 Connect 4 AI"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, 10), title, fill=COLORS['text'], font=title_font)

    # Board top position
    board_top = 80

    # Draw board shadow (for depth)
    shadow_offset = 8
    draw.rounded_rectangle(
        [BOARD_PADDING + shadow_offset, board_top + shadow_offset,
         width - BOARD_PADDING + shadow_offset, height - BOARD_PADDING + shadow_offset],
        radius=25,
        fill=(0, 0, 0, 60)
    )

    # Draw board background
    draw.rounded_rectangle(
        [BOARD_PADDING, board_top, width - BOARD_PADDING, height - BOARD_PADDING],
        radius=25,
        fill=COLORS['board']
    )

    # Draw column hover indicator
    if hover_col is not None and 0 <= hover_col < COLS and not state['game_over']:
        col_x = BOARD_PADDING + hover_col * CELL_SIZE
        draw.rectangle(
            [col_x, board_top, col_x + CELL_SIZE, height - BOARD_PADDING],
            fill=COLORS['hover']
        )

        # Draw arrow indicator above column
        arrow_x = col_x + CELL_SIZE // 2
        arrow_y = board_top - 15
        arrow_size = 12
        draw.polygon(
            [(arrow_x, arrow_y),
             (arrow_x - arrow_size, arrow_y - arrow_size),
             (arrow_x + arrow_size, arrow_y - arrow_size)],
            fill=COLORS['player1'] if state['current_player'] == 1 else COLORS['player2']
        )

    # Draw grid and pieces
    board = state['board']
    for row in range(ROWS):
        for col in range(COLS):
            center_x = BOARD_PADDING + col * CELL_SIZE + CELL_SIZE // 2
            center_y = board_top + (ROWS - 1 - row) * CELL_SIZE + CELL_SIZE // 2

            # Check piece state from bitboard
            bit_position = 1 << (row * 7 + col)

            # Determine piece color
            if board.player1 & bit_position:
                piece_color = COLORS['player1']
                has_piece = True
            elif board.player2 & bit_position:
                piece_color = COLORS['player2']
                has_piece = True
            else:
                piece_color = COLORS['empty']
                has_piece = False

            # Draw piece with gradient effect
            if has_piece:
                # Outer glow
                for r in range(RADIUS + 8, RADIUS - 2, -2):
                    alpha = int(20 * (1 - (RADIUS + 8 - r) / 10))
                    glow_color = piece_color + (alpha,)
                    draw.ellipse(
                        [center_x - r, center_y - r, center_x + r, center_y + r],
                        fill=glow_color
                    )

                # Main piece
                draw.ellipse(
                    [center_x - RADIUS, center_y - RADIUS,
                     center_x + RADIUS, center_y + RADIUS],
                    fill=piece_color
                )

                # Highlight for 3D effect
                highlight_offset = RADIUS // 3
                highlight_radius = RADIUS // 2
                draw.ellipse(
                    [center_x - highlight_offset - highlight_radius,
                     center_y - highlight_offset - highlight_radius,
                     center_x - highlight_offset + highlight_radius,
                     center_y - highlight_offset + highlight_radius],
                    fill=COLORS['glow']
                )
            else:
                # Empty slot - create hole effect
                draw.ellipse(
                    [center_x - RADIUS, center_y - RADIUS,
                     center_x + RADIUS, center_y + RADIUS],
                    fill=COLORS['empty'],
                    outline=COLORS['board_dark'],
                    width=3
                )

    return img

def get_game_status(state):
    """Get current game status message with emoji"""
    if state['game_over']:
        p1_score = state['board'].connect_4s(1)
        p2_score = state['board'].connect_4s(2)
        if p1_score > p2_score:
            return "🎉 **You Win!** Congratulations!"
        elif p2_score > p1_score:
            return "🤖 **AI Wins!** Better luck next time!"
        else:
            return "🤝 **It's a Draw!**"
    elif state['current_player'] == 1:
        return "🔴 **Your Turn** - Click on a column above!"
    else:
        return "🟡 **AI is thinking...**"

def get_score_display(state):
    """Get score display with formatting"""
    p1_score = state['board'].connect_4s(1)
    p2_score = state['board'].connect_4s(2)

    if state['game_over']:
        if p1_score > p2_score:
            return f"### 🏆 You: **{p1_score}** | AI: {p2_score}"
        elif p2_score > p1_score:
            return f"### You: {p1_score} | AI: **{p2_score}** 🏆"
        else:
            return f"### You: {p1_score} | AI: {p2_score}"
    else:
        return f"### You: {p1_score} | AI: {p2_score}"

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
            check_game_over(state)
            if not state['game_over']:
                state['current_player'] = 1
    except Exception as e:
        print(f"AI Error: {e}")
        import random
        col = random.choice(valid_moves)
        state['board'].move(col, 2)
        state['move_history'].append((col, 2))
        check_game_over(state)
        if not state['game_over']:
            state['current_player'] = 1

    return state

def handle_click(state, difficulty, evt: gr.SelectData):
    """Handle click on board image"""
    state = copy.deepcopy(state)

    if state['game_over'] or state['current_player'] != 1:
        return (
            state,
            create_beautiful_board(state),
            get_game_status(state),
            get_score_display(state)
        )

    # Calculate which column was clicked
    # Image width = 7 * 100 + 30 * 2 = 760
    # Board starts at x=30
    BOARD_PADDING = 30
    CELL_SIZE = 100

    click_x = evt.index[0]

    # Adjust for board padding
    board_x = click_x - BOARD_PADDING

    if board_x < 0 or board_x >= 7 * CELL_SIZE:
        return (
            state,
            create_beautiful_board(state),
            get_game_status(state),
            get_score_display(state)
        )

    col = int(board_x // CELL_SIZE)

    # Validate move
    valid_moves = state['board'].valid_moves()
    if col not in valid_moves:
        return (
            state,
            create_beautiful_board(state),
            get_game_status(state),
            get_score_display(state)
        )

    # Make player move
    state['board'].move(col, 1)
    state['move_history'].append((col, 1))
    check_game_over(state)

    if not state['game_over']:
        state['current_player'] = 2
        # Make AI move
        state = make_ai_move(state)

    return (
        state,
        create_beautiful_board(state),
        get_game_status(state),
        get_score_display(state)
    )

def reset_game(difficulty, state):
    """Reset the game with selected difficulty"""
    state = create_initial_state()

    difficulty_map = {
        "Easy (2 moves)": 2,
        "Medium (4 moves)": 4,
        "Hard (6 moves)": 6,
        "Expert (8 moves)": 8,
    }
    state['ai_depth'] = difficulty_map.get(difficulty, 4)

    return (
        state,
        create_beautiful_board(state),
        get_game_status(state),
        get_score_display(state)
    )

# Custom CSS for beautiful styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.gradio-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

#main-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

#game-board {
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease;
    cursor: pointer;
}

#game-board:hover {
    transform: translateY(-5px);
}

.status-box {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    text-align: center;
}

.status-box h3 {
    color: #667eea;
    margin: 0 0 10px 0;
    font-size: 1.8em;
}

.status-box p {
    color: #2c3e50;
    font-size: 1.2em;
    margin: 10px 0;
}

.controls-box {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
}

.instructions {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    color: white;
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
}

.instructions h3 {
    color: white;
    margin-top: 0;
}

button {
    border-radius: 25px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
}
"""

# Create Gradio interface
with gr.Blocks(css=custom_css, title="Connect 4 AI - Beautiful Edition", theme=gr.themes.Soft()) as demo:

    game_state = gr.State(create_initial_state())

    with gr.Column(elem_id="main-container"):
        gr.HTML("""
            <div style="text-align: center; color: white; margin-bottom: 20px;">
                <h1 style="font-size: 3em; margin: 0; text-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                    🎮 Connect 4 AI
                </h1>
                <p style="font-size: 1.3em; margin: 10px 0;">
                    Click directly on the board to play!
                </p>
            </div>
        """)

        # Game board - clickable image
        board_image = gr.Image(
            value=create_beautiful_board(create_initial_state()),
            label="",
            type="pil",
            interactive=True,
            elem_id="game-board",
            show_label=False,
            show_download_button=False,
            show_share_button=False,
            container=False
        )

        # Status display
        with gr.Column(elem_class="status-box"):
            status_text = gr.Markdown(
                value=get_game_status(create_initial_state()),
                elem_classes=["status-text"]
            )
            score_text = gr.Markdown(
                value=get_score_display(create_initial_state()),
                elem_classes=["score-text"]
            )

        # Controls
        with gr.Column(elem_class="controls-box"):
            with gr.Row():
                difficulty = gr.Radio(
                    choices=[
                        "Easy (2 moves)",
                        "Medium (4 moves)",
                        "Hard (6 moves)",
                        "Expert (8 moves)",
                    ],
                    value="Medium (4 moves)",
                    label="🎯 AI Difficulty",
                    scale=2
                )

                reset_button = gr.Button(
                    "🔄 New Game",
                    variant="primary",
                    size="lg",
                    scale=1
                )

        # Instructions
        gr.HTML("""
            <div class="instructions">
                <h3>📖 How to Play</h3>
                <p><strong>• Click directly on any column</strong> on the board to drop your red piece</p>
                <p><strong>• Connect 4 pieces</strong> horizontally, vertically, or diagonally to win!</p>
                <p><strong>• AI responds automatically</strong> after your move</p>
                <br>
                <h3>🎯 Difficulty Levels</h3>
                <p>• <strong>Easy:</strong> Thinks 2 moves ahead</p>
                <p>• <strong>Medium:</strong> Thinks 4 moves ahead ⭐</p>
                <p>• <strong>Hard:</strong> Thinks 6 moves ahead</p>
                <p>• <strong>Expert:</strong> Thinks 8 moves ahead (slower but very smart!)</p>
            </div>
        """)

    # Event handlers
    board_image.select(
        fn=handle_click,
        inputs=[game_state, difficulty],
        outputs=[game_state, board_image, status_text, score_text]
    )

    reset_button.click(
        fn=reset_game,
        inputs=[difficulty, game_state],
        outputs=[game_state, board_image, status_text, score_text]
    )

if __name__ == "__main__":
    demo.launch()
