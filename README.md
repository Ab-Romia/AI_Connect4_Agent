# 🎮 Connect 4 Platform - AI miniMAX

An **advanced, beautiful, and intelligent** Connect 4 game platform featuring multiple game modes, adjustable AI difficulty, stunning UI themes, and real-time visualization of AI decision-making.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com)

---

## ✨ Features

### 🎯 **Multiple Game Modes**
- **Human vs AI** - Challenge yourself against an intelligent AI opponent
- **Human vs Human** - Classic two-player local multiplayer
- **AI vs AI** - Watch two AI agents battle with real-time visualization
- **CLI Mode** - Traditional command-line interface for purists

### 🤖 **Advanced AI Engine**
- **Minimax Algorithm** with alpha-beta pruning for optimal play
- **5 Difficulty Levels**: Easy, Medium, Hard, Expert, and Insane
- **Intelligent Position Evaluation** with center-column prioritization
- **Threat Detection** - AI recognizes and blocks opponent winning moves
- **Decision Tree Visualization** - Watch the AI think in real-time!

### 🎨 **Beautiful User Interface**
- **4 Gorgeous Themes**: Classic, Dark, Ocean, and Forest
- **Smooth Animations** - Satisfying piece drop effects
- **Hover Previews** - See where your piece will land
- **Responsive Design** - Clean and intuitive layout
- **Real-time Statistics** - Track moves, time, and scores

### 📊 **Game Features**
- **Undo Functionality** - Take back moves to experiment
- **Move History** - Complete game replay capability
- **Real-time Scoring** - Connect-4 pattern tracking
- **Game Statistics** - Time tracking and move counting
- **Settings Persistence** - Your preferences are saved automatically

### ⚡ **Technical Highlights**
- **Efficient Bitboard Representation** - Lightning-fast board operations
- **Optimized Minimax** - Move ordering for efficient tree pruning
- **Pure Python** - No external dependencies except Tkinter (included in Python)
- **Cross-platform** - Runs on Windows, macOS, and Linux

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.7 or higher**
- **Tkinter** (usually comes pre-installed with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI_Connect4_miniMAX.git
   cd AI_Connect4_miniMAX
   ```

2. **Verify Python installation**
   ```bash
   python --version  # Should show Python 3.7+
   ```

3. **Run the game!**
   ```bash
   python Connect4Platform.py
   ```

That's it! No pip installs, no dependencies to manage. Just pure Python fun! 🎉

---

## 🎮 How to Play

### Launching the Game
```bash
# Main platform with all features
python Connect4Platform.py

# Legacy GUI (Human vs AI only)
python GUI.py

# Command-line interface
python CLI.py
```

### Game Rules
1. **Objective**: Connect 4 pieces of your color in a row (horizontal, vertical, or diagonal)
2. **Players**: Take turns dropping pieces into columns
3. **Gravity**: Pieces fall to the lowest available position
4. **Win Conditions**: First player to get 4-in-a-row wins!
5. **Draw**: If the board fills up with no winner, it's a draw

### Controls
- **Mouse Click**: Drop piece in selected column
- **Hover**: Preview where your piece will land
- **Undo Button**: Take back the last move
- **Restart Button**: Start a new game
- **Pause Button** (AI vs AI mode): Pause/resume the game

---

## 🎨 Themes

### Classic Theme
- **Board**: Bright blue (#0074D9)
- **Player 1**: Red (#FF4136)
- **Player 2**: Yellow (#FFDC00)
- **Perfect for**: Traditional Connect 4 feel

### Dark Theme
- **Board**: Dark slate (#2C3E50)
- **Player 1**: Crimson (#E74C3C)
- **Player 2**: Orange (#F39C12)
- **Perfect for**: Night gaming sessions

### Ocean Theme
- **Board**: Deep sea blue (#006994)
- **Player 1**: Coral (#FF6B6B)
- **Player 2**: Teal (#4ECDC4)
- **Perfect for**: Relaxing, peaceful gameplay

### Forest Theme
- **Board**: Forest green (#2D5016)
- **Player 1**: Dark red (#8B0000)
- **Player 2**: Gold (#FFD700)
- **Perfect for**: Nature lovers

---

## 🤖 AI Difficulty Levels

| Difficulty | Search Depth | Strength | Best For |
|------------|--------------|----------|----------|
| **Easy** | 2 | ⭐ | Beginners learning the game |
| **Medium** | 4 | ⭐⭐⭐ | Casual players |
| **Hard** | 6 | ⭐⭐⭐⭐ | Experienced players |
| **Expert** | 8 | ⭐⭐⭐⭐⭐ | Advanced players seeking challenge |
| **Insane** | 10 | ⭐⭐⭐⭐⭐⭐ | Ultimate challenge! |

**Note**: Higher difficulties require more thinking time but play much stronger!

---

## 🏗️ Project Structure

```
AI_Connect4_miniMAX/
├── Connect4Platform.py    # Main launcher with all features ⭐
├── GUI.py                 # Legacy GUI (Human vs AI)
├── CLI.py                 # Command-line interface
├── Board.py               # Bitboard game logic
├── MiniMax.py             # AI engine with alpha-beta pruning
├── config.json            # Auto-generated settings (created on first run)
├── requirements.txt       # Python dependencies (none!)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🧠 How the AI Works

### Minimax Algorithm
The AI uses the **minimax algorithm** with **alpha-beta pruning** to search through possible future game states and choose the optimal move.

```python
def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Recursively evaluate game tree:
    - depth: How many moves to look ahead
    - alpha/beta: Pruning bounds for optimization
    - maximizing_player: AI (maximize) or Human (minimize)
    """
```

### Evaluation Function
The AI scores positions based on:

1. **Positional Weights** (0-200 points)
   - Center columns valued highest
   - Strategic positioning bonus

2. **Tactical Patterns**
   - 4-in-a-row: +100,000 (win!)
   - 3-in-a-row with empty: +1,000
   - 2-in-a-row with empty: +100
   - Opponent 3-in-a-row: -800 (block!)

3. **Threat Detection**
   - Recognizes imminent threats
   - Forces defensive moves when necessary

### Performance
- **Depth 4 (Medium)**: ~0.01-0.1 seconds per move
- **Depth 6 (Hard)**: ~0.1-1 second per move
- **Depth 8 (Expert)**: ~1-5 seconds per move
- **Depth 10 (Insane)**: ~5-30 seconds per move

*Times vary based on board complexity and system performance*

---

## ⚙️ Configuration

Settings are automatically saved to `config.json` in the game directory:

```json
{
  "difficulty": "Medium",
  "theme": "Classic",
  "show_tree": true,
  "animation_speed": 15,
  "sound_enabled": false,
  "last_mode": "Human vs AI"
}
```

You can manually edit this file or use the in-game settings menu.

---

## 🎓 Educational Value

This project is excellent for learning:

- **Game AI**: Minimax algorithm, alpha-beta pruning, heuristic evaluation
- **Data Structures**: Bitboards for efficient state representation
- **GUI Programming**: Tkinter for desktop applications
- **Game Development**: Animation, user interaction, state management
- **Algorithm Optimization**: Move ordering, pruning strategies

Perfect for:
- Computer Science students studying AI
- Game development enthusiasts
- Python learners wanting a complete project
- Interview preparation (game AI is a common topic!)

---

## 🔧 Advanced Usage

### Running Specific Modes Directly

```bash
# Play against AI immediately (legacy)
python GUI.py

# CLI mode for terminal enthusiasts
python CLI.py

# Import and use in your own code
from Board import Connect4Board
from MiniMax import minimax

board = Connect4Board()
best_move, score = minimax(board, depth=6, alpha=float('-inf'),
                           beta=float('inf'), maximizing_player=True)
```

### Customizing AI Behavior

Edit `MiniMax.py` to adjust:
- **Positional weights**: Favor different columns
- **Tactical scoring**: Change threat priorities
- **Search depth**: Balance speed vs strength

### Creating New Themes

Edit `Connect4Platform.py` and add to the `THEMES` dictionary:

```python
"MyTheme": {
    "board": "#HEX_COLOR",
    "empty": "#HEX_COLOR",
    "player1": "#HEX_COLOR",
    "player2": "#HEX_COLOR",
    "player1_hover": "#HEX_COLOR",
    "player2_hover": "#HEX_COLOR",
    "bg": "#HEX_COLOR",
    "text": "#HEX_COLOR"
}
```

---

## 🐛 Troubleshooting

### Tkinter Not Found
**Problem**: `ImportError: No module named 'tkinter'`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (should be pre-installed)
brew install python-tk

# Windows (usually included with Python)
# Reinstall Python from python.org with "tcl/tk" option checked
```

### Slow Performance
**Problem**: AI takes too long to move

**Solution**:
- Lower the difficulty setting
- Close other resource-intensive applications
- The AI is working correctly - higher difficulties need time to think!

### Game Crashes
**Problem**: Unexpected errors or crashes

**Solution**:
1. Delete `config.json` to reset settings
2. Update to Python 3.7+
3. Check for file permissions

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add sound effects and music
- [ ] Implement network multiplayer
- [ ] Add tournament mode with brackets
- [ ] Create mobile version
- [ ] Add replay/save game functionality
- [ ] Implement opening book for AI
- [ ] Add achievements and statistics tracking

**How to contribute**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👏 Credits

**Algorithm**: Minimax with alpha-beta pruning (classic game AI)
**Data Structure**: Bitboard representation for efficient board state
**Framework**: Python + Tkinter for cross-platform GUI
**Inspiration**: Classic Connect 4 game by Milton Bradley

---

## 🎯 Roadmap

### Version 2.0 (Current)
- ✅ Multiple game modes
- ✅ Adjustable difficulty
- ✅ Multiple themes
- ✅ AI decision tree visualization
- ✅ Settings persistence

### Version 3.0 (Planned)
- ⏳ Sound effects
- ⏳ Network multiplayer
- ⏳ Game replay system
- ⏳ Mobile version
- ⏳ Achievement system

---

## 💖 Acknowledgments

Special thanks to:
- The Python community for excellent documentation
- Game AI researchers for minimax algorithm insights
- All contributors and players who make this project better!

---

<div align="center">

**Enjoy playing Connect 4! May the best strategist win! 🏆**

Made with ❤️ and Python 🐍

</div>
