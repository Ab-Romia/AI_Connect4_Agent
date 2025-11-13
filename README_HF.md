---
title: Connect 4 AI - Minimax Algorithm
emoji: 🎮
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🎮 Connect 4 AI - Powered by Minimax Algorithm

Play Connect 4 against an intelligent AI opponent! This application features a sophisticated AI that uses the minimax algorithm with alpha-beta pruning to make optimal moves.

## ✨ Features

### 🤖 **Intelligent AI Engine**
- **Minimax Algorithm** with alpha-beta pruning for optimal gameplay
- **5 Difficulty Levels**: From Easy (2-ply) to Insane (10-ply)
- **Smart Position Evaluation** - AI favors center positions and recognizes threats
- **Move Ordering** - Efficient tree pruning for faster computation

### 🎯 **Game Features**
- **Interactive Web Interface** - Easy-to-use Gradio interface
- **Visual Board** - Clear, colorful display of game state
- **Real-time Scoring** - Tracks Connect-4 patterns for both players
- **Undo Functionality** - Take back moves to experiment with strategies
- **Adjustable Difficulty** - Choose your challenge level

### ⚡ **Technical Highlights**
- **Bitboard Representation** - Efficient board state storage
- **Alpha-Beta Pruning** - Optimal minimax tree exploration
- **Pure Python** - Built with Python, Gradio, and Pillow
- **Fast Computation** - Optimized for responsive gameplay

## 🚀 How to Play

1. **Choose Your Difficulty** - Select from Easy to Insane
2. **Enter Column Number** - Type 1-7 to select which column to drop your piece
3. **Click "Play Move"** - Make your move and watch the AI respond
4. **Connect 4 to Win!** - Get 4 pieces in a row (horizontal, vertical, or diagonal)

### Game Rules
- You play as **Red (Player 1)**
- AI plays as **Yellow (Player 2)**
- Players alternate dropping pieces into columns
- Pieces fall to the lowest available position
- First to connect 4 pieces wins!
- If the board fills up, the player with the most Connect-4 patterns wins

## 🤖 AI Difficulty Levels

| Difficulty | Search Depth | Response Time | Skill Level |
|------------|--------------|---------------|-------------|
| **Easy** | 2 moves ahead | < 0.1s | ⭐ Beginner-friendly |
| **Medium** | 4 moves ahead | 0.1-0.5s | ⭐⭐⭐ Balanced |
| **Hard** | 6 moves ahead | 0.5-2s | ⭐⭐⭐⭐ Challenging |
| **Expert** | 8 moves ahead | 2-10s | ⭐⭐⭐⭐⭐ Very Strong |
| **Insane** | 10 moves ahead | 10-60s | ⭐⭐⭐⭐⭐⭐ Near-Optimal |

**Note**: Higher difficulties take longer to compute but play much stronger!

## 🧠 How the AI Works

### Minimax Algorithm
The AI uses the **minimax algorithm**, a decision-making algorithm for turn-based games. It works by:

1. **Exploring Future Moves** - Simulates possible game states several moves ahead
2. **Evaluating Positions** - Scores each position based on tactical and positional factors
3. **Choosing Optimal Move** - Selects the move that leads to the best outcome
4. **Alpha-Beta Pruning** - Skips branches that can't improve the result (optimization)

### Evaluation Function
The AI scores positions based on:

- **Tactical Patterns** (most important)
  - 4-in-a-row: +100,000 points (win!)
  - 3-in-a-row with empty space: +1,000 points
  - 2-in-a-row with empty spaces: +100 points
  - Opponent threats: Negative scores (forces defensive play)

- **Positional Strategy**
  - Center columns valued highly (more connection opportunities)
  - Middle rows preferred (more flexible positioning)
  - Edge positions less valuable

### Performance
- **Bitboard Representation**: Uses integer bitmasks for lightning-fast board operations
- **Move Ordering**: Evaluates promising moves first for better pruning
- **Efficient Recursion**: Minimal memory overhead with depth-limited search

## 🏗️ Project Structure

```
AI_Connect4_Agent/
├── app.py                 # Gradio web interface (main entry point)
├── Board.py               # Bitboard game logic
├── MiniMax.py             # AI engine with minimax algorithm
├── requirements.txt       # Python dependencies
└── README_HF.md          # This file (Hugging Face documentation)
```

## 🚀 Local Deployment

To run this application locally:

```bash
# Clone the repository
git clone <your-repo-url>
cd AI_Connect4_Agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app will launch at `http://localhost:7860`

## 🎓 Educational Value

This project demonstrates:
- **Game AI**: Minimax algorithm implementation
- **Algorithm Optimization**: Alpha-beta pruning technique
- **Data Structures**: Bitboard representation
- **Web Development**: Gradio interface creation
- **Python Programming**: Clean, modular code structure

Perfect for:
- Computer Science students learning AI
- Game development enthusiasts
- Interview preparation (game AI is a common topic!)
- Anyone interested in game algorithms

## 🔧 Customization

### Adjust AI Behavior
Edit `MiniMax.py` to customize:
- Positional weights (favor different columns)
- Tactical scoring (change threat priorities)
- Search depth (balance speed vs strength)

### Modify Interface
Edit `app.py` to customize:
- Color scheme
- Board size
- UI layout
- Additional features

## 📝 Algorithm Complexity

- **Time Complexity**: O(b^d) where b ≈ 7 (branching factor) and d = depth
  - Without pruning: ~7^10 ≈ 282 billion nodes at depth 10
  - With alpha-beta pruning: Reduces to ~7^5 ≈ 16,800 nodes (typical case)
- **Space Complexity**: O(d) for recursion stack
- **Board Operations**: O(1) for most operations thanks to bitboards

## 🤝 Contributing

Contributions are welcome! Some ideas:
- Add opening book for early game
- Implement iterative deepening
- Add game statistics and analytics
- Create tournament mode
- Add sound effects

## 📄 License

This project is open source and available under the MIT License.

## 👏 Credits

- **Algorithm**: Minimax with alpha-beta pruning (classic game AI)
- **Data Structure**: Bitboard representation
- **Framework**: Gradio for web interface
- **Inspiration**: Classic Connect 4 by Milton Bradley

---

<div align="center">

**Enjoy playing Connect 4! May the best strategist win! 🏆**

Made with ❤️ using Python 🐍, Gradio, and AI algorithms

</div>
