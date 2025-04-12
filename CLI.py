import os
from Board import Connect4Board

def display_board(board):
    """Displays the current state of the board."""
    grid = [["." for _ in range(7)] for _ in range(6)]
    for col in range(7):
        print(board.height(col), end=" ")
    print()
    for row in range(6):
        for col in range(7):
            if board.player1 & (1 << (row * 7 + col)):
                grid[row][col] = "X"
            elif board.player2 & (1 << (row * 7 + col)):
                grid[row][col] = "O"
    for row in reversed(grid):
        print(" ".join(row))
    print("0 1 2 3 4 5 6")  # Column indices

def main():
    """Main function to run the Connect 4 game."""
    board = Connect4Board()
    current_player = 1

    print("Welcome to Connect 4!")
    print("Player 1: X, Player 2: O")
    display_board(board)

    while True:
        try:
            print(f"Player {current_player}'s turn.")

            column = int(input("Enter the column (0-6) to drop your piece: "))
            while column not in board.valid_moves():
                column = int(input("Invalid move. Enter a valid column (0-6): "))

            # Make the move
            board.move(column, current_player)

            # Display the updated board
            display_board(board)

            # Check for a win
            if board.connect_4s(current_player) > 0:
                print(f"Player {current_player} wins!")
                break

            # Check for a draw
            if not board.valid_moves():
                print("The game is a draw!")
                break

            # Switch players
            current_player = 2 if current_player == 1 else 1

        except ValueError as e:
            print(f"Invalid move: {e}. Try again.")
        except Exception as e:
            print(f"An error occurred: {e}. Exiting game.")
            break

if __name__ == "__main__":
    main()