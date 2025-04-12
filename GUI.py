import tkinter as tk
import time
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
        if self.game_over or self.is_animating:
            return
        col = event.x // self.SQUARE_SIZE
        # Use valid_moves() from the actual board class
        if col not in self.board.valid_moves():
            self.update_message("Invalid move. Try again.")
            self.root.after(1500, self.update_message)
            return
        self.clear_hover()
        self.is_animating = True
        self._update_button_states() # Disable undo during animation
        # Use height() from the actual board class
        target_row = self.board.height(col) # Get target row before animating
        self.animate_drop(col, target_row) # Pass target_row

    # --- Modified animate_drop to take target_row ---
    def animate_drop(self, col, target_row):
        if target_row == self.ROWS: # Check if column is full (height returns 6 for full)
             self.is_animating = False
             self._update_button_states()
             print("Error: Tried to animate into a full column.") # Should be caught by handle_click
             return

        color = self.PLAYER1_COLOR if self.current_player == 1 else self.PLAYER2_COLOR
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        target_center_y = (self.ROWS - 1 - target_row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.SQUARE_SIZE

        current_y = self.SQUARE_SIZE // 2
        x0 = center_x - self.RADIUS
        x1 = center_x + self.RADIUS
        piece_id = self.canvas.create_oval(x0, current_y - self.RADIUS, x1, current_y + self.RADIUS, fill=color, outline=self.BOARD_COLOR, width=2)

        def step_animation():
            nonlocal current_y
            current_y += self.ANIMATION_STEP
            if current_y >= target_center_y:
                self.canvas.delete(piece_id)
                # --- Use move() from the actual board class ---
                try:
                    self.board.move(col, self.current_player)
                    # --- Add move to history AFTER successful board move ---
                    self.move_history.append((col, self.current_player))
                except ValueError as e:
                    print(f"Error during board move: {e}") # Should not happen ideally
                    # Handle potential errors if move fails unexpectedly
                    self.is_animating = False
                    self._update_button_states()
                    self.update_message("An error occurred. Please restart.")
                    return

                self.draw_board() # Redraw AFTER board state is updated
                self.is_animating = False # Unlock clicks/buttons AFTER drawing
                self.check_game_state() # Check win/draw/next turn
                self._update_button_states() # Update button state AFTER animation/checks
            else:
                self.canvas.coords(piece_id, x0, current_y - self.RADIUS, x1, current_y + self.RADIUS)
                self.root.after(self.ANIMATION_SPEED, step_animation)

        step_animation()

    def check_game_state(self):
        """Check the game state after a move using the actual board's methods."""
        winner = self.current_player

        # --- Use connect_4s() from the actual board class ---
        if self.board.connect_4s(winner) > 0: # Check if count > 0
            self.game_over = True
            self.update_message(f"Player {winner} wins!")
            self._update_button_states()
            return

        # --- Check draw using valid_moves() ---
        if not self.board.valid_moves():
            self.game_over = True
            self.update_message("It's a draw!")
            self._update_button_states()
            return

        # Switch players if game not over
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_message()
        self._update_button_states() # Update buttons for next turn

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


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(Connect4GUI.WIDTH + 20, Connect4GUI.HEIGHT + 100)
    # Ensure the Board.py file exists and is importable
    game = Connect4GUI(root)
    root.mainloop()