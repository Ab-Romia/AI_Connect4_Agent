"""
Connect 4 Platform - Main Launcher
An amazing Connect 4 game platform with AI, multiple modes, and beautiful UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import os
from Board import Connect4Board
from MiniMax import minimax


class Config:
    """Configuration manager for game settings"""
    CONFIG_FILE = "config.json"

    DEFAULT_CONFIG = {
        "difficulty": "Medium",
        "theme": "Classic",
        "show_tree": True,
        "animation_speed": 15,
        "sound_enabled": False,
        "last_mode": "Human vs AI"
    }

    @classmethod
    def load(cls):
        """Load configuration from file"""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    return {**cls.DEFAULT_CONFIG, **config}
            except:
                pass
        return cls.DEFAULT_CONFIG.copy()

    @classmethod
    def save(cls, config):
        """Save configuration to file"""
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass


class Theme:
    """Theme configurations for the UI"""

    THEMES = {
        "Classic": {
            "board": "#0074D9",
            "empty": "#FFFFFF",
            "player1": "#FF4136",
            "player2": "#FFDC00",
            "player1_hover": "#FF8080",
            "player2_hover": "#FFFF80",
            "bg": "#F0F0F0",
            "text": "#333333"
        },
        "Dark": {
            "board": "#2C3E50",
            "empty": "#34495E",
            "player1": "#E74C3C",
            "player2": "#F39C12",
            "player1_hover": "#C0392B",
            "player2_hover": "#D68910",
            "bg": "#1A1A1A",
            "text": "#FFFFFF"
        },
        "Ocean": {
            "board": "#006994",
            "empty": "#87CEEB",
            "player1": "#FF6B6B",
            "player2": "#4ECDC4",
            "player1_hover": "#FF8E8E",
            "player2_hover": "#6FE0D8",
            "bg": "#E8F4F8",
            "text": "#003F5C"
        },
        "Forest": {
            "board": "#2D5016",
            "empty": "#90EE90",
            "player1": "#8B0000",
            "player2": "#FFD700",
            "player1_hover": "#CD5C5C",
            "player2_hover": "#FFEC8B",
            "bg": "#F0FFF0",
            "text": "#1B4D0E"
        }
    }

    @classmethod
    def get(cls, theme_name):
        """Get theme colors"""
        return cls.THEMES.get(theme_name, cls.THEMES["Classic"])


class MainMenu:
    """Main launcher menu for Connect 4 Platform"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 Platform")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.config = Config.load()
        self.setup_ui()

    def setup_ui(self):
        """Setup the main menu UI"""
        # Configure root background
        theme = Theme.get(self.config["theme"])
        self.root.configure(bg=theme["bg"])

        # Title
        title_frame = tk.Frame(self.root, bg=theme["bg"])
        title_frame.pack(pady=40)

        title_label = tk.Label(
            title_frame,
            text="🎮 Connect 4 Platform",
            font=("Arial", 32, "bold"),
            fg=theme["text"],
            bg=theme["bg"]
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="Powered by miniMAX AI",
            font=("Arial", 14, "italic"),
            fg=theme["text"],
            bg=theme["bg"]
        )
        subtitle_label.pack()

        # Game mode selection
        mode_frame = tk.LabelFrame(
            self.root,
            text="Select Game Mode",
            font=("Arial", 14, "bold"),
            fg=theme["text"],
            bg=theme["bg"],
            padx=20,
            pady=20
        )
        mode_frame.pack(pady=20, padx=40, fill="x")

        modes = [
            ("🎯 Human vs AI", self.launch_human_vs_ai, "Play against the AI"),
            ("👥 Human vs Human", self.launch_human_vs_human, "Two player local game"),
            ("🤖 AI vs AI", self.launch_ai_vs_ai, "Watch two AIs battle"),
            ("⌨️  CLI Mode", self.launch_cli, "Command-line interface")
        ]

        for text, command, desc in modes:
            btn = tk.Button(
                mode_frame,
                text=text,
                font=("Arial", 14, "bold"),
                command=command,
                width=25,
                height=2,
                relief=tk.RAISED,
                borderwidth=3,
                bg="#4CAF50",
                fg="white",
                activebackground="#45a049",
                cursor="hand2"
            )
            btn.pack(pady=5)

            desc_label = tk.Label(
                mode_frame,
                text=desc,
                font=("Arial", 10, "italic"),
                fg=theme["text"],
                bg=theme["bg"]
            )
            desc_label.pack(pady=(0, 10))

        # Settings frame
        settings_frame = tk.LabelFrame(
            self.root,
            text="Settings",
            font=("Arial", 14, "bold"),
            fg=theme["text"],
            bg=theme["bg"],
            padx=20,
            pady=15
        )
        settings_frame.pack(pady=10, padx=40, fill="x")

        # Difficulty
        diff_frame = tk.Frame(settings_frame, bg=theme["bg"])
        diff_frame.pack(fill="x", pady=5)

        tk.Label(
            diff_frame,
            text="AI Difficulty:",
            font=("Arial", 12),
            fg=theme["text"],
            bg=theme["bg"]
        ).pack(side="left")

        self.difficulty_var = tk.StringVar(value=self.config["difficulty"])
        difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard", "Expert", "Insane"],
            state="readonly",
            width=15,
            font=("Arial", 11)
        )
        difficulty_combo.pack(side="right")
        difficulty_combo.bind("<<ComboboxSelected>>", self.save_settings)

        # Theme
        theme_frame = tk.Frame(settings_frame, bg=theme["bg"])
        theme_frame.pack(fill="x", pady=5)

        tk.Label(
            theme_frame,
            text="Theme:",
            font=("Arial", 12),
            fg=theme["text"],
            bg=theme["bg"]
        ).pack(side="left")

        self.theme_var = tk.StringVar(value=self.config["theme"])
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=list(Theme.THEMES.keys()),
            state="readonly",
            width=15,
            font=("Arial", 11)
        )
        theme_combo.pack(side="right")
        theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Show tree checkbox
        self.show_tree_var = tk.BooleanVar(value=self.config["show_tree"])
        tree_check = tk.Checkbutton(
            settings_frame,
            text="Show AI Decision Tree",
            variable=self.show_tree_var,
            font=("Arial", 11),
            fg=theme["text"],
            bg=theme["bg"],
            selectcolor=theme["bg"],
            command=self.save_settings
        )
        tree_check.pack(anchor="w", pady=5)

        # Info and quit buttons
        button_frame = tk.Frame(self.root, bg=theme["bg"])
        button_frame.pack(pady=20)

        info_btn = tk.Button(
            button_frame,
            text="ℹ️ About",
            font=("Arial", 11),
            command=self.show_about,
            width=12,
            relief=tk.RAISED,
            borderwidth=2
        )
        info_btn.pack(side="left", padx=5)

        quit_btn = tk.Button(
            button_frame,
            text="❌ Quit",
            font=("Arial", 11),
            command=self.root.quit,
            width=12,
            relief=tk.RAISED,
            borderwidth=2
        )
        quit_btn.pack(side="left", padx=5)

    def get_ai_depth(self):
        """Get AI depth based on difficulty"""
        depths = {
            "Easy": 2,
            "Medium": 4,
            "Hard": 6,
            "Expert": 8,
            "Insane": 10
        }
        return depths.get(self.difficulty_var.get(), 4)

    def save_settings(self, event=None):
        """Save current settings"""
        self.config["difficulty"] = self.difficulty_var.get()
        self.config["show_tree"] = self.show_tree_var.get()
        Config.save(self.config)

    def change_theme(self, event=None):
        """Change and apply theme"""
        self.config["theme"] = self.theme_var.get()
        Config.save(self.config)
        # Recreate UI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def launch_human_vs_ai(self):
        """Launch Human vs AI game"""
        game_window = tk.Toplevel(self.root)
        Connect4Game(
            game_window,
            mode="human_vs_ai",
            ai_depth=self.get_ai_depth(),
            theme=self.config["theme"],
            show_tree=self.config["show_tree"]
        )

    def launch_human_vs_human(self):
        """Launch Human vs Human game"""
        game_window = tk.Toplevel(self.root)
        Connect4Game(
            game_window,
            mode="human_vs_human",
            theme=self.config["theme"]
        )

    def launch_ai_vs_ai(self):
        """Launch AI vs AI game"""
        game_window = tk.Toplevel(self.root)
        Connect4Game(
            game_window,
            mode="ai_vs_ai",
            ai_depth=self.get_ai_depth(),
            theme=self.config["theme"],
            show_tree=self.config["show_tree"]
        )

    def launch_cli(self):
        """Launch CLI mode"""
        messagebox.showinfo(
            "CLI Mode",
            "To play in CLI mode, run:\n\npython CLI.py\n\nfrom your terminal."
        )

    def show_about(self):
        """Show about dialog"""
        about_text = """Connect 4 Platform v2.0

An advanced Connect 4 game featuring:

🎯 Multiple Game Modes
• Human vs AI with adjustable difficulty
• Human vs Human local multiplayer
• AI vs AI battle simulation

🤖 Intelligent AI
• Minimax algorithm with alpha-beta pruning
• Configurable difficulty (Easy to Insane)
• Position evaluation and threat detection
• Decision tree visualization

🎨 Beautiful UI
• Multiple themes
• Smooth animations
• Hover previews
• Undo functionality

📊 Features
• Real-time scoring
• Move history
• Game statistics
• Settings persistence

Created with ❤️ using Python & Tkinter
Powered by miniMAX AI algorithm"""

        messagebox.showinfo("About Connect 4 Platform", about_text)

    def run(self):
        """Run the main menu"""
        self.root.mainloop()


class Connect4Game:
    """Enhanced Connect 4 game with multiple modes"""

    # Constants
    ROWS = 6
    COLS = 7
    SQUARE_SIZE = 100
    PADDING = 10
    RADIUS = (SQUARE_SIZE - PADDING * 2) // 2
    WIDTH = COLS * SQUARE_SIZE
    HEIGHT = (ROWS + 1) * SQUARE_SIZE

    def __init__(self, root, mode="human_vs_ai", ai_depth=4, theme="Classic", show_tree=True):
        self.root = root
        self.mode = mode
        self.ai_depth = ai_depth
        self.show_tree_enabled = show_tree
        self.theme_colors = Theme.get(theme)

        # Set window title based on mode
        mode_titles = {
            "human_vs_ai": "Human vs AI",
            "human_vs_human": "Human vs Human",
            "ai_vs_ai": "AI vs AI"
        }
        self.root.title(f"Connect 4 - {mode_titles.get(mode, mode)}")

        # Game state
        self.board = Connect4Board()
        self.current_player = 1
        self.game_over = False
        self.is_animating = False
        self.hover_col = None
        self.hover_preview_id = None
        self.move_history = []
        self.move_count = 0
        self.start_time = time.time()

        # Statistics
        self.stats = {
            "moves": 0,
            "p1_time": 0.0,
            "p2_time": 0.0,
            "last_move_time": time.time()
        }

        self.setup_ui()
        self.draw_board()
        self.update_message()
        self.update_stats()

        # Start AI vs AI if needed
        if self.mode == "ai_vs_ai":
            self.root.after(1000, self.ai_move)

    def setup_ui(self):
        """Setup game UI"""
        self.root.configure(bg=self.theme_colors["bg"])
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.theme_colors["bg"],
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        # Message label
        self.message_var = tk.StringVar()
        self.message_label = tk.Label(
            self.root,
            textvariable=self.message_var,
            font=("Arial", 16, "bold"),
            fg=self.theme_colors["text"],
            bg=self.theme_colors["bg"],
            pady=5
        )
        self.message_label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # Score label
        self.score_var = tk.StringVar()
        self.score_label = tk.Label(
            self.root,
            textvariable=self.score_var,
            font=("Arial", 12),
            fg=self.theme_colors["text"],
            bg=self.theme_colors["bg"]
        )
        self.score_label.grid(row=2, column=0, sticky="ew", padx=10)

        # Stats label
        self.stats_var = tk.StringVar()
        self.stats_label = tk.Label(
            self.root,
            textvariable=self.stats_var,
            font=("Arial", 10),
            fg=self.theme_colors["text"],
            bg=self.theme_colors["bg"]
        )
        self.stats_label.grid(row=3, column=0, sticky="ew", padx=10)

        # Buttons
        button_frame = tk.Frame(self.root, bg=self.theme_colors["bg"])
        button_frame.grid(row=4, column=0, pady=10)

        self.undo_button = tk.Button(
            button_frame,
            text="⬅️ Undo",
            font=("Arial", 11),
            command=self.undo_action,
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            width=12
        )
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            button_frame,
            text="🔄 Restart",
            font=("Arial", 11),
            command=self.restart_game,
            relief=tk.RAISED,
            borderwidth=2,
            padx=10,
            width=12
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        if self.mode == "ai_vs_ai":
            self.pause_button = tk.Button(
                button_frame,
                text="⏸️ Pause",
                font=("Arial", 11),
                command=self.toggle_pause,
                relief=tk.RAISED,
                borderwidth=2,
                padx=10,
                width=12
            )
            self.pause_button.pack(side=tk.LEFT, padx=5)
            self.paused = False

        # Bind events
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_mouse_motion)
        self.canvas.bind("<Leave>", self.handle_mouse_leave)

        self.update_button_states()

    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("board")
        board_height = self.ROWS * self.SQUARE_SIZE

        # Draw board background
        self.canvas.create_rectangle(
            0, self.HEIGHT - board_height,
            self.WIDTH, self.HEIGHT,
            fill=self.theme_colors["board"],
            outline=self.theme_colors["board"],
            tags="board"
        )

        # Draw pieces
        for row in range(self.ROWS):
            for col in range(self.COLS):
                center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                center_y = (self.ROWS - 1 - row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.SQUARE_SIZE

                # Check piece state
                bit_position = 1 << (row * self.COLS + col)
                if self.board.player1 & bit_position:
                    fill_color = self.theme_colors["player1"]
                elif self.board.player2 & bit_position:
                    fill_color = self.theme_colors["player2"]
                else:
                    fill_color = self.theme_colors["empty"]

                x0, y0 = center_x - self.RADIUS, center_y - self.RADIUS
                x1, y1 = center_x + self.RADIUS, center_y + self.RADIUS

                self.canvas.create_oval(
                    x0, y0, x1, y1,
                    fill=fill_color,
                    outline=self.theme_colors["board"],
                    width=2,
                    tags="board"
                )

    def update_message(self, message=None):
        """Update status message"""
        if message:
            self.message_var.set(message)
        elif self.game_over:
            pass  # Keep existing message
        else:
            if self.mode == "human_vs_ai":
                player_name = "Your turn" if self.current_player == 1 else "AI thinking..."
            elif self.mode == "ai_vs_ai":
                player_name = f"AI {self.current_player} thinking..."
            else:
                player_name = f"Player {self.current_player}'s turn"
            self.message_var.set(player_name)

    def update_score(self):
        """Update score display"""
        p1_score = self.board.connect_4s(1)
        p2_score = self.board.connect_4s(2)

        p1_name = "You" if self.mode == "human_vs_ai" else "Player 1"
        p2_name = "AI" if self.mode == "human_vs_ai" else "Player 2"

        if self.mode == "ai_vs_ai":
            p1_name, p2_name = "AI 1", "AI 2"

        leader1 = " 🏆" if p1_score > p2_score else ""
        leader2 = " 🏆" if p2_score > p1_score else ""

        self.score_var.set(
            f"{p1_name}: {p1_score}{leader1}  |  {p2_name}: {p2_score}{leader2}"
        )

    def update_stats(self):
        """Update game statistics"""
        elapsed = time.time() - self.start_time
        self.stats_var.set(
            f"Moves: {self.stats['moves']}  |  "
            f"Time: {elapsed:.1f}s  |  "
            f"Difficulty: {['Easy', 'Medium', 'Hard', 'Expert', 'Insane'][min(self.ai_depth // 2, 4)]}"
        )

    def update_button_states(self):
        """Update button states"""
        if not self.move_history or self.game_over or self.is_animating:
            self.undo_button.config(state=tk.DISABLED)
        else:
            self.undo_button.config(state=tk.NORMAL)

    def handle_mouse_motion(self, event):
        """Handle mouse motion for hover preview"""
        if self.game_over or self.is_animating:
            self.clear_hover()
            return

        # Only show hover for human players
        if self.mode == "human_vs_ai" and self.current_player == 2:
            self.clear_hover()
            return

        if self.mode == "ai_vs_ai":
            self.clear_hover()
            return

        col = event.x // self.SQUARE_SIZE
        if 0 <= col < self.COLS and col != self.hover_col:
            self.clear_hover()
            if col in self.board.valid_moves():
                self.hover_col = col
                self.draw_hover_preview(col)
        elif not (0 <= col < self.COLS):
            self.clear_hover()

    def handle_mouse_leave(self, event):
        """Handle mouse leaving canvas"""
        self.clear_hover()

    def clear_hover(self):
        """Clear hover preview"""
        if self.hover_preview_id:
            self.canvas.delete(self.hover_preview_id)
            self.hover_preview_id = None
        self.hover_col = None

    def draw_hover_preview(self, col):
        """Draw hover preview"""
        if self.hover_preview_id:
            self.canvas.delete(self.hover_preview_id)

        color = self.theme_colors["player1_hover"] if self.current_player == 1 else self.theme_colors["player2_hover"]
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        center_y = self.SQUARE_SIZE // 2
        x0, y0 = center_x - self.RADIUS, center_y - self.RADIUS
        x1, y1 = center_x + self.RADIUS, center_y + self.RADIUS

        self.hover_preview_id = self.canvas.create_oval(
            x0, y0, x1, y1,
            fill=color,
            outline="",
            tags="hover",
            stipple="gray50"
        )

    def handle_click(self, event):
        """Handle mouse click"""
        if self.game_over or self.is_animating:
            return

        # Check if it's a human player's turn
        if self.mode == "human_vs_ai" and self.current_player == 2:
            return

        if self.mode == "ai_vs_ai":
            return

        col = event.x // self.SQUARE_SIZE
        if col not in self.board.valid_moves():
            self.update_message("Invalid move! Try another column.")
            self.root.after(1500, self.update_message)
            return

        self.make_move(col)

    def make_move(self, col):
        """Make a move with animation"""
        self.clear_hover()
        self.is_animating = True
        self.update_button_states()

        target_row = self.board.height(col)
        self.animate_drop(col, target_row)

    def animate_drop(self, col, target_row):
        """Animate piece drop"""
        if target_row == self.ROWS:
            self.is_animating = False
            self.update_button_states()
            return

        color = self.theme_colors["player1"] if self.current_player == 1 else self.theme_colors["player2"]
        center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        target_y = (self.ROWS - 1 - target_row) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 + self.SQUARE_SIZE

        current_y = self.SQUARE_SIZE // 2
        x0 = center_x - self.RADIUS
        x1 = center_x + self.RADIUS

        piece_id = self.canvas.create_oval(
            x0, current_y - self.RADIUS,
            x1, current_y + self.RADIUS,
            fill=color,
            outline=self.theme_colors["board"],
            width=2
        )

        def step():
            nonlocal current_y
            current_y += 20

            if current_y >= target_y:
                self.canvas.delete(piece_id)
                self.board.move(col, self.current_player)
                self.move_history.append((col, self.current_player))
                self.stats["moves"] += 1

                self.draw_board()
                self.is_animating = False
                self.check_game_state()
                self.update_button_states()
                self.update_stats()
            else:
                self.canvas.coords(piece_id, x0, current_y - self.RADIUS, x1, current_y + self.RADIUS)
                self.root.after(15, step)

        step()

    def check_game_state(self):
        """Check game state and handle turn switching"""
        self.update_score()

        # Check for game over
        if not self.board.valid_moves():
            self.game_over = True
            p1_score = self.board.connect_4s(1)
            p2_score = self.board.connect_4s(2)

            if p1_score > p2_score:
                winner = "You win! 🎉" if self.mode == "human_vs_ai" else "Player 1 wins! 🎉"
            elif p2_score > p1_score:
                winner = "AI wins! 🤖" if self.mode == "human_vs_ai" else "Player 2 wins! 🎉"
            else:
                winner = "It's a draw! 🤝"

            if self.mode == "ai_vs_ai":
                winner = f"AI {1 if p1_score > p2_score else 2} wins! 🏆" if p1_score != p2_score else "Draw! 🤝"

            self.update_message(f"Game Over! {winner}")
            self.update_button_states()
            return

        # Switch players
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_message()

        # Handle AI turns
        if self.mode == "human_vs_ai" and self.current_player == 2:
            self.root.after(500, self.ai_move)
        elif self.mode == "ai_vs_ai" and not self.game_over:
            if not hasattr(self, 'paused') or not self.paused:
                self.root.after(800, self.ai_move)

    def ai_move(self):
        """Make AI move"""
        if self.game_over:
            return

        if hasattr(self, 'paused') and self.paused:
            return

        start_time = time.time()

        # Get AI move
        best_col, _, tree_root = minimax(
            self.board,
            depth=self.ai_depth,
            alpha=float('-inf'),
            beta=float('inf'),
            maximizing_player=(self.current_player == 2),
            return_tree=True
        )

        time_taken = time.time() - start_time

        if best_col is not None:
            self.make_move(best_col)

            # Show tree if enabled
            if self.show_tree_enabled and self.mode != "ai_vs_ai":
                self.show_tree(tree_root, time_taken)

    def show_tree(self, root_node, time_taken):
        """Show minimax decision tree"""
        tree_window = tk.Toplevel(self.root)
        tree_window.title("AI Decision Tree")
        tree_window.geometry("900x700")

        frame = tk.Frame(tree_window)
        frame.pack(fill="both", expand=True)

        # Time label
        time_label = tk.Label(
            frame,
            text=f"⏱️  Calculation Time: {time_taken:.4f}s  |  Depth: {self.ai_depth}  |  Nodes Explored: {self.count_nodes(root_node)}",
            font=("Arial", 12, "bold"),
            bg="#F0F0F0",
            pady=10
        )
        time_label.pack(side="top", fill="x")

        canvas = tk.Canvas(frame, bg="white", scrollregion=(0, 0, 5000, 5000))
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbars
        hbar = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        hbar.pack(side="bottom", fill="x")
        vbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        vbar.pack(side="right", fill="y")

        canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        # Zoom functionality
        scale = [1.0]

        def zoom(event):
            if event.state & 0x0004:
                delta = event.delta if event.delta != 0 else (1 if event.num == 4 else -1)
                factor = 1.1 if delta > 0 else 0.9
                scale[0] *= factor
                canvas.scale("all", canvas.canvasx(event.x), canvas.canvasy(event.y), factor, factor)
                canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<MouseWheel>", zoom)
        canvas.bind("<Button-4>", zoom)
        canvas.bind("<Button-5>", zoom)

        # Pan functionality
        canvas.bind("<ButtonPress-2>", lambda e: canvas.scan_mark(e.x, e.y))
        canvas.bind("<B2-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))
        canvas.bind("<Shift-ButtonPress-1>", lambda e: canvas.scan_mark(e.x, e.y))
        canvas.bind("<Shift-B1-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))

        # Draw tree
        self.draw_tree_node(canvas, root_node, 1000, 50, 0)

    def count_nodes(self, node):
        """Count nodes in tree"""
        if not node:
            return 0
        count = 1
        for child in node.children:
            count += self.count_nodes(child)
        return count

    def draw_tree_node(self, canvas, node, x, y, depth):
        """Draw tree node recursively"""
        radius = 30

        # Choose color based on score
        if node.score > 1000:
            color = "#4CAF50"  # Good move
        elif node.score < -1000:
            color = "#F44336"  # Bad move
        else:
            color = "#9E9E9E"  # Neutral

        canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            tags="all"
        )

        canvas.create_text(
            x, y,
            text=f"Col: {node.move}\n{node.score}",
            font=("Arial", 8, "bold"),
            fill="white",
            tags="all"
        )

        # Draw children
        child_count = len(node.children)
        if child_count > 0:
            spacing = 120
            start_x = x - (child_count - 1) * spacing // 2
            child_y = y + 100

            for i, child in enumerate(node.children):
                child_x = start_x + i * spacing
                canvas.create_line(x, y + radius, child_x, child_y - radius, tags="all", fill="#666")
                self.draw_tree_node(canvas, child, child_x, child_y, depth + 1)

    def toggle_pause(self):
        """Toggle pause for AI vs AI"""
        self.paused = not self.paused
        self.pause_button.config(text="▶️ Resume" if self.paused else "⏸️ Pause")

        if not self.paused and not self.game_over and not self.is_animating:
            self.ai_move()

    def undo_action(self):
        """Undo last move"""
        if not self.move_history or self.game_over or self.is_animating:
            return

        last_col, last_player = self.move_history.pop()
        self.board.undo(last_col, last_player)

        self.current_player = last_player
        self.game_over = False
        self.stats["moves"] -= 1

        self.draw_board()
        self.update_message()
        self.update_score()
        self.update_stats()
        self.update_button_states()
        self.clear_hover()

    def restart_game(self):
        """Restart the game"""
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.is_animating = False
        self.move_history.clear()
        self.stats = {"moves": 0, "p1_time": 0.0, "p2_time": 0.0, "last_move_time": time.time()}
        self.start_time = time.time()

        if hasattr(self, 'paused'):
            self.paused = False
            self.pause_button.config(text="⏸️ Pause")

        self.clear_hover()
        self.canvas.delete("hover")
        self.draw_board()
        self.update_message()
        self.update_score()
        self.update_stats()
        self.update_button_states()

        # Start AI vs AI if needed
        if self.mode == "ai_vs_ai":
            self.root.after(1000, self.ai_move)


def main():
    """Main entry point"""
    menu = MainMenu()
    menu.run()


if __name__ == "__main__":
    main()
