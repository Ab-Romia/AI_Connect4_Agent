import tkinter as tk
import time
from MiniMax import minimax
# --- Import the actual Connect4Board class ---
# Make sure Board.py is in the same directory or accessible
try:
    from Board import Connect4Board
except ImportError:
    print("Error: Could not find Board.py. Make sure it's in the same directory.")
    print("Using a dummy class for now - Undo/Win checks might not work correctly.")
    # Define a dummy class if import fails, so the GUI can still load partially
    class Connect4Board:
        def __init__(self): self.player1=0; self.player2=0
        def height(self, column): return 0
        def valid_moves(self): return list(range(7))
        def move(self, column, player): pass
        def undo(self, column, player): print("WARN: Using dummy undo!")
        def connect_4s(self, player): return 0
        def reset(self): self.player1=0; self.player2=0

# --- End Import ---


class Connect4GUI:
    # Constants
    ROWS = 6
    COLS = 7
    SQUARE_SIZE = 100
    PADDING = 10
    RADIUS = (SQUARE_SIZE - PADDING * 2) // 2
    WIDTH = COLS * SQUARE_SIZE
    HEIGHT = (ROWS + 1) * SQUARE_SIZE

    BOARD_COLOR = "#0000FF" # Blue
    EMPTY_COLOR = "#FFFFFF" # White (for empty slots)
    PLAYER1_COLOR = "#FF0000" # Red
    PLAYER2_COLOR = "#FFFF00" # Yellow
    PLAYER1_HOVER_COLOR = "#FF8080" # Lighter Red
    PLAYER2_HOVER_COLOR = "#FFFF80" # Lighter Yellow
    WIN_COLOR = "#00FF00" # Green for win message background

    ANIMATION_SPEED = 15
    ANIMATION_STEP = 20

    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4 - Improved")
        # Use the imported Connect4Board class
        self.board = Connect4Board()
        self.current_player = 1
        self.game_over = False
        self.is_animating = False
        self.hover_col = None
        self.hover_preview_id = None
        # --- Add move history for undo ---
        self.move_history = []

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=0)

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg=self.EMPTY_COLOR)
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,0))

        self.message_label_var = tk.StringVar()
        self.message_label = tk.Label(root, textvariable=self.message_label_var, font=("Arial", 16, "bold"), pady=5)
        self.message_label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.score_label_var = tk.StringVar()
        self.score_label = tk.Label(root, textvariable=self.score_label_var, font=("Arial", 14))
        self.score_label.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,5))

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, pady=(0, 10))

        # --- Add Undo Button ---
        self.undo_button = tk.Button(self.button_frame, text="Undo Move", font=("Arial", 12), command=self.undo_action, relief=tk.RAISED, borderwidth=2, padx=10)
        self.undo_button.pack(side=tk.LEFT, padx=5) # Pack next to restart

        self.restart_button = tk.Button(self.button_frame, text="Restart Game", font=("Arial", 12), command=self.restart_game, relief=tk.RAISED, borderwidth=2, padx=10)
        self.restart_button.pack(side=tk.LEFT, padx=5) # Pack next to undo

        self.draw_board()
        self.update_message()
        self._update_button_states() # Initial button state

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_mouse_motion)
        self.canvas.bind("<Leave>", self.handle_mouse_leave)

    def update_score_display(self):
        p1_score = self.board.connect_4s(1)
        p2_score = self.board.connect_4s(2)

        if p1_score > p2_score:
            winner = " ⬅ Leader"
        elif p2_score > p1_score:
            winner = " ⬅ Leader"
        else:
            winner = ""

        self.score_label_var.set(
            f"Player 1 (Red): {p1_score}{' ⬅ Leader' if p1_score > p2_score else ''}  |  "
            f"Player 2 (Yellow): {p2_score}{' ⬅ Leader' if p2_score > p1_score else ''}"
        )

    def draw_board(self):
        """Draw the Connect 4 board graphically based on bitboards."""
        self.canvas.delete("board")
        board_height = self.ROWS * self.SQUARE_SIZE
        self.canvas.create_rectangle(0, self.HEIGHT - board_height, self.WIDTH, self.HEIGHT, fill=self.BOARD_COLOR, outline=self.BOARD_COLOR, tags="board")

        for row in range(self.ROWS):
            for col in range(self.COLS):
                center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                center_y = (self.ROWS - 1 - row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.SQUARE_SIZE

                # --- Determine fill color based on bitboard state ---
                bit_position = 1 << (row * self.COLS + col)
                if self.board.player1 & bit_position:
                    fill_color = self.PLAYER1_COLOR
                elif self.board.player2 & bit_position:
                    fill_color = self.PLAYER2_COLOR
                else:
                    fill_color = self.EMPTY_COLOR # "Hole" color
                # --- End bitboard check ---

                x0 = center_x - self.RADIUS
                y0 = center_y - self.RADIUS
                x1 = center_x + self.RADIUS
                y1 = center_y + self.RADIUS
                self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline=self.BOARD_COLOR, width=2, tags="board")

    def update_message(self, message=None):
         if self.game_over:
             if message:
                 self.message_label_var.set(message)
         else:
             self.message_label_var.set(message or f"Player {self.current_player}'s turn")

    def _update_button_states(self):
        """Enable/disable Undo button based on game state."""
        if not self.move_history or self.game_over or self.is_animating:
            self.undo_button.config(state=tk.DISABLED)
        else:
            self.undo_button.config(state=tk.NORMAL)

    def handle_mouse_motion(self, event):
        if self.game_over or self.is_animating:
            self.clear_hover()
            return
        col = event.x // self.SQUARE_SIZE
        if 0 <= col < self.COLS and col != self.hover_col:
            self.clear_hover()
            # Use valid_moves() from the actual board class
            if col in self.board.valid_moves():
                self.hover_col = col
                self.draw_hover_preview(col)
        elif not (0 <= col < self.COLS):
             self.clear_hover()

    def handle_mouse_leave(self, event):
        self.clear_hover()

    def clear_hover(self):
        if self.hover_preview_id:
            self.canvas.delete(self.hover_preview_id)
            self.hover_preview_id = None
        self.hover_col = None

    def draw_hover_preview(self, col):
        if self.hover_preview_id:
            self.canvas.delete(self.hover_preview_id)
        color = self.PLAYER1_HOVER_COLOR if self.current_player == 1 else self.PLAYER2_HOVER_COLOR
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        center_y = self.SQUARE_SIZE // 2
        x0 = center_x - self.RADIUS
        y0 = center_y - self.RADIUS
        x1 = center_x + self.RADIUS
        y1 = center_y + self.RADIUS
        self.hover_preview_id = self.canvas.create_oval(x0, y0, x1, y1, fill=color, outline="", tags="hover", stipple="gray50")

    def handle_click(self, event):
        """Handle user clicks and make a move if it's the user's turn."""
        if self.game_over or self.is_animating or self.current_player == 2:  # Block clicks during AI's turn
            return
        col = event.x // self.SQUARE_SIZE
        if col not in self.board.valid_moves():
            self.update_message("Invalid move. Try again.")
            self.root.after(1500, self.update_message)
            return
        self.clear_hover()
        self.is_animating = True
        self._update_button_states()
        target_row = self.board.height(col)
        self.animate_drop(col, target_row, is_ai=False)

    def animate_drop(self, col, target_row, is_ai):
        """Animate the piece dropping into the column."""
        if target_row == self.ROWS:
            self.is_animating = False
            self._update_button_states()
            return

        color = self.PLAYER1_COLOR if self.current_player == 1 else self.PLAYER2_COLOR
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        target_center_y = (self.ROWS - 1 - target_row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.SQUARE_SIZE

        current_y = self.SQUARE_SIZE // 2
        x0 = center_x - self.RADIUS
        x1 = center_x + self.RADIUS
        piece_id = self.canvas.create_oval(x0, current_y - self.RADIUS, x1, current_y + self.RADIUS, fill=color,
                                           outline=self.BOARD_COLOR, width=2)

        def step_animation():
            nonlocal current_y
            current_y += self.ANIMATION_STEP
            if current_y >= target_center_y:
                self.canvas.delete(piece_id)
                try:
                    self.board.move(col, self.current_player)
                    self.move_history.append((col, self.current_player))
                except ValueError as e:
                    self.is_animating = False
                    self._update_button_states()
                    self.update_message("An error occurred. Please restart.")
                    return

                self.draw_board()
                self.is_animating = False
                self.check_game_state(is_ai)
                self._update_button_states()
            else:
                self.canvas.coords(piece_id, x0, current_y - self.RADIUS, x1, current_y + self.RADIUS)
                self.root.after(self.ANIMATION_SPEED, step_animation)

        step_animation()

    def show_tree(self, root_node, time_taken=None):
        import tkinter as tk

        tree_window = tk.Toplevel(self.root)
        tree_window.title("Minimax Tree")

        # Create a Frame to hold canvas and scrollbars
        frame = tk.Frame(tree_window)
        frame.pack(fill="both", expand=True)

        # Add time information at the top if available
        if time_taken is not None:
            time_label = tk.Label(
                frame,
                text=f"Time taken for minimax: {time_taken:.4f} seconds",
                font=("Arial", 12, "bold")
            )
            time_label.pack(side="top", pady=5)

        canvas = tk.Canvas(frame, width=800, height=600, bg="white", scrollregion=(0, 0, 5000, 5000))
        canvas.pack(side="left", fill="both", expand=True)

        # Add scrollbars
        hbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        hbar.pack(side="bottom", fill="x")
        vbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        vbar.pack(side="right", fill="y")

        canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        # Zoom and pan support
        scale = [1.0]

        def zoom(event):
            if event.state & 0x0004:  # Ctrl is held
                # Normalize event.delta for consistent behavior across platforms
                delta = event.delta if event.delta != 0 else (1 if event.num == 4 else -1)
                factor = 1.1 if delta > 0 else 0.9  # Zoom in for positive delta, out for negative
                scale[0] *= factor
                canvas.scale("all", canvas.canvasx(event.x), canvas.canvasy(event.y), factor, factor)
                # Adjust scroll region dynamically
                canvas.configure(scrollregion=canvas.bbox("all"))

        # Bindings for different platforms
        canvas.bind("<MouseWheel>", zoom)  # Windows and macOS
        canvas.bind("<Button-4>", lambda e: zoom(e))  # Linux scroll up
        canvas.bind("<Button-5>", lambda e: zoom(e))  # Linux scroll down

        # Drag to move view (panning)
        def start_pan(event):
            canvas.scan_mark(event.x, event.y)

        def do_pan(event):
            canvas.scan_dragto(event.x, event.y, gain=1)

        canvas.bind("<ButtonPress-2>", start_pan)  # Middle mouse button press
        canvas.bind("<B2-Motion>", do_pan)

        # Also allow dragging with Shift + Left Click
        canvas.bind("<Shift-ButtonPress-1>", start_pan)
        canvas.bind("<Shift-B1-Motion>", do_pan)

        # Recursive function to draw nodes
        def draw_node(node, x, y, depth=0):
            radius = 30
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#D3D3D3", tags="all")
            canvas.create_text(x, y, text=f"Score: {node.score}\nCol: {node.move}", font=("Arial", 8), tags="all")

            child_x = x - 100 + depth * 20
            child_y = y + 100
            for child in node.children:
                canvas.create_line(x, y + radius, child_x, child_y - radius, tags="all")
                draw_node(child, child_x, child_y, depth + 1)
                child_x += 120

        draw_node(root_node, 1000, 50)

    def check_game_state(self, is_ai):
        """Check the game state and switch turns."""
        self.update_score_display()

        if not self.board.valid_moves():
            self.game_over = True
            p1_score = self.board.connect_4s(1)
            p2_score = self.board.connect_4s(2)
            if p1_score > p2_score:
                self.update_message("Game Over! Player 1 wins by score!")
            elif p2_score > p1_score:
                self.update_message("Game Over! Player 2 wins by score!")
            else:
                self.update_message("Game Over! It's a draw!")
            self._update_button_states()
            return

        self.current_player = 2 if self.current_player == 1 else 1
        if self.current_player == 2 and not self.game_over:
            self.root.after(500, self.ai_move)
        else:
            self.update_message()
            self._update_button_states()

    def ai_move(self):
        """Make a move for the AI using the enhanced minimax algorithm with alpha-beta pruning and save the decision tree."""
        if self.game_over:
            return

        # Start timing the minimax calculation
        start_time = time.time()

        # AI is Player 2, so maximizing_player = False
        best_col, _, self.minimax_tree_root = minimax(
            self.board,
            depth=5,
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=False,
            return_tree=True
        )

        # Calculate time taken
        time_taken = time.time() - start_time

        if best_col is not None:
            target_row = self.board.height(best_col)
            self.animate_drop(best_col, target_row, is_ai=True)

            # Pass the time taken to show_tree
            self.show_tree(self.minimax_tree_root, time_taken)

    # --- Undo Action Implementation ---
    def undo_action(self):
        """Undoes the last move made."""
        if not self.move_history or self.game_over or self.is_animating:
            return # Cannot undo

        # Get the last move
        last_col, last_player = self.move_history.pop()

        # Perform undo on the board logic
        try:
            self.board.undo(last_col, last_player)
        except ValueError as e:
            print(f"Error during board undo: {e}")
            # If undo fails, put move back in history (optional, depends on desired behavior)
            self.move_history.append((last_col, last_player))
            return
        except Exception as e:
            print(f"Unexpected error during board undo: {e}")
            return


        # Update GUI state
        self.current_player = last_player # It's this player's turn again
        self.game_over = False # Game cannot be over after an undo
        self.draw_board() # Redraw the board to show the removed piece
        self.update_message() # Update message to show correct player turn
        self._update_button_states() # Update button enabled state
        self.clear_hover() # Clear any lingering hover effect

    def restart_game(self):
        """Restart the game."""
        # --- Use reset() from the actual board class ---
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.is_animating = False
        # --- Clear move history on restart ---
        self.move_history.clear()
        self.clear_hover()
        self.canvas.delete("hover")
        self.draw_board()
        self.update_message()
        self._update_button_states() # Reset button states
        self.update_score_display()


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(Connect4GUI.WIDTH + 20, Connect4GUI.HEIGHT + 100)
    # Ensure the Board.py file exists and is importable
    game = Connect4GUI(root)
    root.mainloop()