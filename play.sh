#!/bin/bash
# Connect 4 Platform Launcher

echo "🎮 Connect 4 Platform - Starting..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION detected"

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Error: tkinter is not installed."
    echo ""
    echo "Install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  macOS: brew install python-tk"
    echo "  Windows: Reinstall Python with tcl/tk enabled"
    exit 1
fi

echo "✓ Tkinter available"
echo ""
echo "🚀 Launching Connect 4 Platform..."
echo ""

# Run the platform
python3 Connect4Platform.py
