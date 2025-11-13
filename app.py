"""
Connect 4 AI - Beautiful Interactive Gradio Interface
An intelligent Connect 4 game with stunning animations and intuitive gameplay
"""

import gradio as gr
from Board import Connect4Board
from MiniMax import minimax
import json
import copy

# Color scheme
COLORS = {
    'player1': '#FF4757',  # Vibrant Red
    'player2': '#FFA502',  # Vibrant Orange/Yellow
    'empty': '#2C3E50',    # Dark blue-gray
    'board': '#34495E',    # Slightly lighter blue-gray
    'win': '#00D2FF'       # Cyan for winning pieces
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
        'winning_cells': []
    }

def get_board_state_json(state):
    """Convert board state to JSON for JavaScript"""
    board_array = []
    for row in range(6):
        row_data = []
        for col in range(7):
            bit_position = 1 << (row * 7 + col)
            if state['board'].player1 & bit_position:
                row_data.append(1)
            elif state['board'].player2 & bit_position:
                row_data.append(2)
            else:
                row_data.append(0)
        board_array.append(row_data)

    return {
        'board': board_array,
        'currentPlayer': state['current_player'],
        'gameOver': state['game_over'],
        'winner': state['winner'],
        'winningCells': state['winning_cells'],
        'player1Score': state['board'].connect_4s(1),
        'player2Score': state['board'].connect_4s(2)
    }

def check_winner(state):
    """Check for winner and get winning cells"""
    # Simple check - if one player has more connect-4s and board is full or no valid moves
    p1_score = state['board'].connect_4s(1)
    p2_score = state['board'].connect_4s(2)

    if not state['board'].valid_moves():
        state['game_over'] = True
        if p1_score > p2_score:
            state['winner'] = 1
        elif p2_score > p1_score:
            state['winner'] = 2
        else:
            state['winner'] = 0  # Draw

    return state

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
            check_winner(state)
            if not state['game_over']:
                state['current_player'] = 1
    except Exception as e:
        print(f"AI Error: {e}")
        import random
        col = random.choice(valid_moves)
        state['board'].move(col, 2)
        state['move_history'].append((col, 2))
        check_winner(state)
        if not state['game_over']:
            state['current_player'] = 1

    return state

def play_move(col_idx, state, difficulty):
    """Handle a player's move"""
    state = copy.deepcopy(state)

    try:
        if state['game_over']:
            return state, json.dumps(get_board_state_json(state))

        if state['current_player'] != 1:
            return state, json.dumps(get_board_state_json(state))

        valid_moves = state['board'].valid_moves()
        if col_idx not in valid_moves:
            return state, json.dumps(get_board_state_json(state))

        # Player move
        state['board'].move(col_idx, 1)
        state['move_history'].append((col_idx, 1))
        check_winner(state)

        if not state['game_over']:
            state['current_player'] = 2
            # AI move
            state = make_ai_move(state)

        return state, json.dumps(get_board_state_json(state))

    except Exception as e:
        print(f"Error: {e}")
        return state, json.dumps(get_board_state_json(state))

def reset_game(difficulty, state):
    """Reset the game"""
    state = create_initial_state()

    difficulty_map = {
        "Easy (2 moves)": 2,
        "Medium (4 moves)": 4,
        "Hard (6 moves)": 6,
        "Expert (8 moves)": 8,
    }
    state['ai_depth'] = difficulty_map.get(difficulty, 4)

    return state, json.dumps(get_board_state_json(state))

# Custom CSS for beautiful styling
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    #game-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }

    #game-board-canvas {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        display: block;
        margin: 0 auto;
        transition: transform 0.3s ease;
    }

    #game-board-canvas:hover {
        transform: translateY(-5px);
    }

    .game-header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .game-header h1 {
        font-size: 3em;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(45deg, #fff, #a8edea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .status-panel {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        color: white;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }

    .score-display {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        font-size: 1.2em;
        font-weight: 600;
    }

    .player-score {
        padding: 15px 30px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }

    .status-message {
        font-size: 1.5em;
        font-weight: 600;
        margin: 10px 0;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    .controls {
        text-align: center;
        margin: 20px 0;
    }

    .control-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        margin: 5px;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }

    .control-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    #particle-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
</style>
"""

# Custom JavaScript for interactive gameplay
custom_js = """
<script>
class Connect4Game {
    constructor() {
        this.canvas = document.getElementById('game-board-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.rows = 6;
        this.cols = 7;
        this.cellSize = 80;
        this.padding = 10;
        this.radius = (this.cellSize - this.padding * 2) / 2;

        this.canvas.width = this.cols * this.cellSize;
        this.canvas.height = (this.rows + 1) * this.cellSize;

        this.boardState = null;
        this.hoverCol = -1;
        this.animatingPiece = null;
        this.particles = [];

        this.colors = {
            player1: '#FF4757',
            player2: '#FFA502',
            empty: '#2C3E50',
            board: '#34495E',
            hover1: 'rgba(255, 71, 87, 0.5)',
            hover2: 'rgba(255, 165, 2, 0.5)',
            win: '#00D2FF'
        };

        this.setupEventListeners();
        this.animate();
    }

    setupEventListeners() {
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('mouseleave', () => this.handleMouseLeave());
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const col = Math.floor(x / this.cellSize);

        if (col >= 0 && col < this.cols) {
            this.hoverCol = col;
        } else {
            this.hoverCol = -1;
        }
    }

    handleMouseLeave() {
        this.hoverCol = -1;
    }

    handleClick(e) {
        if (!this.boardState || this.boardState.gameOver || this.animatingPiece) return;
        if (this.boardState.currentPlayer !== 1) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const col = Math.floor(x / this.cellSize);

        if (col >= 0 && col < this.cols) {
            // Find the row where piece will land
            let targetRow = -1;
            for (let row = this.rows - 1; row >= 0; row--) {
                if (this.boardState.board[row][col] === 0) {
                    targetRow = row;
                    break;
                }
            }

            if (targetRow !== -1) {
                this.startAnimation(col, targetRow, 1);
                // Call Python backend
                window.playMove(col);
            }
        }
    }

    startAnimation(col, targetRow, player) {
        this.animatingPiece = {
            col: col,
            currentY: 0,
            targetY: (this.rows - targetRow) * this.cellSize + this.cellSize / 2,
            player: player,
            velocity: 0,
            gravity: 0.8
        };
    }

    updateBoard(stateJson) {
        const newState = JSON.parse(stateJson);
        const oldState = this.boardState;
        this.boardState = newState;

        // Check if AI made a move and animate it
        if (oldState && !oldState.gameOver && newState.currentPlayer === 1) {
            // Find the AI's move
            for (let row = 0; row < this.rows; row++) {
                for (let col = 0; col < this.cols; col++) {
                    if (oldState.board[row][col] === 0 && newState.board[row][col] === 2) {
                        this.startAnimation(col, row, 2);
                        return;
                    }
                }
            }
        }

        // Check for win and create particles
        if (newState.gameOver && newState.winner !== 0) {
            this.createWinParticles();
        }
    }

    createWinParticles() {
        for (let i = 0; i < 100; i++) {
            this.particles.push({
                x: this.canvas.width / 2,
                y: this.canvas.height / 2,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 100,
                color: Math.random() > 0.5 ? this.colors.player1 : this.colors.player2
            });
        }
    }

    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#1e3c72';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw board
        this.drawBoard();

        // Draw hover preview
        if (this.hoverCol !== -1 && this.boardState && !this.boardState.gameOver && this.boardState.currentPlayer === 1 && !this.animatingPiece) {
            this.drawHoverPreview();
        }

        // Draw animating piece
        if (this.animatingPiece) {
            this.updateAnimation();
            this.drawAnimatingPiece();
        }

        // Draw particles
        this.updateParticles();
        this.drawParticles();
    }

    drawBoard() {
        if (!this.boardState) return;

        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                const x = col * this.cellSize + this.cellSize / 2;
                const y = (this.rows - row) * this.cellSize + this.cellSize / 2;

                const cellValue = this.boardState.board[row][col];
                let color = this.colors.empty;

                if (cellValue === 1) {
                    color = this.colors.player1;
                } else if (cellValue === 2) {
                    color = this.colors.player2;
                }

                // Draw piece with glow effect
                if (cellValue !== 0) {
                    const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, this.radius);
                    gradient.addColorStop(0, color);
                    gradient.addColorStop(1, this.adjustColor(color, -30));
                    this.ctx.fillStyle = gradient;
                } else {
                    this.ctx.fillStyle = color;
                }

                this.ctx.beginPath();
                this.ctx.arc(x, y, this.radius, 0, Math.PI * 2);
                this.ctx.fill();

                // Add shine effect for placed pieces
                if (cellValue !== 0) {
                    const shineGradient = this.ctx.createRadialGradient(
                        x - this.radius / 3, y - this.radius / 3, 0,
                        x - this.radius / 3, y - this.radius / 3, this.radius / 2
                    );
                    shineGradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
                    shineGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
                    this.ctx.fillStyle = shineGradient;
                    this.ctx.beginPath();
                    this.ctx.arc(x, y, this.radius, 0, Math.PI * 2);
                    this.ctx.fill();
                }
            }
        }
    }

    drawHoverPreview() {
        const x = this.hoverCol * this.cellSize + this.cellSize / 2;
        const y = this.cellSize / 2;

        this.ctx.fillStyle = this.colors.hover1;
        this.ctx.beginPath();
        this.ctx.arc(x, y, this.radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Draw column highlight
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.fillRect(this.hoverCol * this.cellSize, this.cellSize, this.cellSize, this.rows * this.cellSize);
    }

    updateAnimation() {
        if (!this.animatingPiece) return;

        this.animatingPiece.velocity += this.animatingPiece.gravity;
        this.animatingPiece.currentY += this.animatingPiece.velocity;

        if (this.animatingPiece.currentY >= this.animatingPiece.targetY) {
            this.animatingPiece.currentY = this.animatingPiece.targetY;
            this.animatingPiece = null;
        }
    }

    drawAnimatingPiece() {
        if (!this.animatingPiece) return;

        const x = this.animatingPiece.col * this.cellSize + this.cellSize / 2;
        const y = this.animatingPiece.currentY;
        const color = this.animatingPiece.player === 1 ? this.colors.player1 : this.colors.player2;

        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, this.radius);
        gradient.addColorStop(0, color);
        gradient.addColorStop(1, this.adjustColor(color, -30));
        this.ctx.fillStyle = gradient;

        this.ctx.beginPath();
        this.ctx.arc(x, y, this.radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Add motion blur effect
        this.ctx.shadowBlur = Math.min(this.animatingPiece.velocity * 2, 20);
        this.ctx.shadowColor = color;
    }

    updateParticles() {
        this.particles = this.particles.filter(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.2;
            p.life--;
            return p.life > 0;
        });
    }

    drawParticles() {
        this.particles.forEach(p => {
            this.ctx.fillStyle = p.color;
            this.ctx.globalAlpha = p.life / 100;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
            this.ctx.fill();
        });
        this.ctx.globalAlpha = 1;
    }

    adjustColor(color, amount) {
        const num = parseInt(color.slice(1), 16);
        const r = Math.max(0, Math.min(255, (num >> 16) + amount));
        const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amount));
        const b = Math.max(0, Math.min(255, (num & 0x0000FF) + amount));
        return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
    }
}

// Initialize game when page loads
window.addEventListener('load', () => {
    window.game = new Connect4Game();
});
</script>
"""

# Create Gradio interface
with gr.Blocks(title="Connect 4 AI - Beautiful Edition", theme=gr.themes.Soft()) as demo:
    game_state = gr.State(create_initial_state())

    gr.HTML(custom_css)

    with gr.Column(elem_id="game-container"):
        gr.HTML("""
            <div class="game-header">
                <h1>🎮 Connect 4 AI</h1>
                <p style="font-size: 1.2em; margin: 10px 0;">Play against an intelligent AI with beautiful animations!</p>
            </div>
        """)

        # Game board canvas
        gr.HTML('<canvas id="game-board-canvas"></canvas>')

        # Status panel
        with gr.Column():
            status_display = gr.HTML(value="""
                <div class="status-panel">
                    <div class="status-message">🔴 Your Turn - Click a column!</div>
                    <div class="score-display">
                        <div class="player-score">🔴 You: 0</div>
                        <div class="player-score">🟠 AI: 0</div>
                    </div>
                </div>
            """)

        # Controls
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

            with gr.Column(scale=1):
                reset_btn = gr.Button("🔄 New Game", size="lg", variant="primary")

        gr.HTML("""
            <div class="status-panel">
                <h3>📖 How to Play</h3>
                <p>Click directly on any column to drop your red piece. Connect 4 pieces horizontally, vertically, or diagonally to win!</p>
                <p><strong>💡 Tip:</strong> Hover over columns to see where your piece will land.</p>
            </div>
        """)

    # Hidden component to trigger board updates
    board_state_json = gr.Textbox(value=json.dumps(get_board_state_json(create_initial_state())), visible=False)

    # JavaScript communication
    gr.HTML(custom_js)

    # Update status display based on game state
    def update_status(state_json):
        state = json.loads(state_json)
        if state['gameOver']:
            if state['winner'] == 1:
                status_msg = '🎉 You Win! Congratulations!'
            elif state['winner'] == 2:
                status_msg = '🤖 AI Wins! Try again!'
            else:
                status_msg = '🤝 It\'s a Draw!'
        elif state['currentPlayer'] == 1:
            status_msg = '🔴 Your Turn - Click a column!'
        else:
            status_msg = '🟠 AI is thinking...'

        return f"""
            <div class="status-message">{status_msg}</div>
            <div class="score-display">
                <div class="player-score">🔴 You: {state['player1Score']}</div>
                <div class="player-score">🟠 AI: {state['player2Score']}</div>
            </div>
        """

    # Update board when state changes
    board_state_json.change(
        fn=update_status,
        inputs=[board_state_json],
        outputs=[status_display],
        js="""
        (stateJson) => {
            if (window.game) {
                window.game.updateBoard(stateJson);
            }
            return stateJson;
        }
        """
    )

    # Create column buttons (hidden but functional)
    col_buttons = []
    with gr.Row(visible=False):
        for i in range(7):
            btn = gr.Button(f"Col{i}", elem_id=f"col-btn-{i}")
            col_buttons.append(btn)

    # Play move function
    def handle_move(col_idx, state, diff):
        state, board_json = play_move(col_idx, state, diff)
        return state, board_json

    # Connect column buttons to handler
    for idx, btn in enumerate(col_buttons):
        btn.click(
            fn=lambda state, diff, i=idx: handle_move(i, state, diff),
            inputs=[game_state, difficulty],
            outputs=[game_state, board_state_json]
        )

    # Reset game
    def handle_reset(diff, state):
        state, board_json = reset_game(diff, state)
        return state, board_json

    reset_btn.click(
        fn=handle_reset,
        inputs=[difficulty, game_state],
        outputs=[game_state, board_state_json]
    )

    # JavaScript to trigger column buttons
    gr.HTML("""
    <script>
    window.playMove = function(col) {
        const btn = document.getElementById('col-btn-' + col);
        if (btn) {
            btn.click();
        }
    };
    </script>
    """)

if __name__ == "__main__":
    demo.launch()
