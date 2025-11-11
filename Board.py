class Connect4Board:
    """
    Connect 4 Board using efficient bitboard representation.

    The board state is stored using two integers (player1 and player2) where each bit
    represents a position on the 6x7 board. This allows for very fast operations.

    Attributes:
        player1 (int): Bitboard for player 1's pieces
        player2 (int): Bitboard for player 2's pieces
    """

    def __init__(self):
        """Initialize an empty board."""
        self.player1 = 0
        self.player2 = 0

    def height(self, column):
        """
        Get the next available row in a column.

        Args:
            column (int): Column index (0-6)

        Returns:
            int: Row index (0-5) where the next piece will land, or 6 if column is full
        """
        for row in range(6):
            if not (self.player1 & (1 << (row * 7 + column)) or self.player2 & (1 << (row * 7 + column))):
                return row
        return 6

    def reset(self):
        """Reset the board to empty state."""
        self.player1 = 0
        self.player2 = 0

    def valid_moves(self):
        """
        Get list of valid column moves.

        Returns:
            list: List of column indices (0-6) that are not full
        """
        return [i for i in range(7) if self.height(i) < 6]

    def move(self, column, player):
        """
        Make a move by dropping a piece in a column.

        Args:
            column (int): Column index (0-6)
            player (int): Player number (1 or 2)

        Raises:
            ValueError: If column is invalid or full
        """
        if column<0 or column>6:
            raise ValueError("Invalid column")

        ht = self.height(column)

        if ht == 6:
            raise ValueError("Column is full")

        if player == 1:
            self.player1 = self.player1 | (1 << (ht * 7 + column))
        else:
            self.player2 = self.player2 | (1 << (ht * 7 + column))

    def undo(self, column, player):
        """
        Undo a move by removing the top piece from a column.

        Args:
            column (int): Column index (0-6)
            player (int): Player number (1 or 2)

        Raises:
            ValueError: If column is invalid or empty
        """
        if column<0 or column>6:
            raise ValueError("Invalid column")

        ht = self.height(column)

        if ht == 0:
            raise ValueError("Column is empty")

        if player == 1:
            self.player1 = self.player1 & ~(1 << ((ht-1) * 7 + column))
        else:
            self.player2 = self.player2 & ~(1 << ((ht-1) * 7 + column))

    def connect_4s(self, player):
        """
        Count the number of Connect-4 patterns for a player.

        This counts all instances of 4-in-a-row (horizontal, vertical, and diagonal)
        for scoring purposes. Vertical connections are weighted higher (×11).

        Args:
            player (int): Player number (1 or 2)

        Returns:
            int: Count of Connect-4 patterns (vertical patterns weighted ×11)
        """
        if player == 1:
            player = self.player1
        else:
            player = self.player2

        # Horizontal Connect4s
        count = 0
        for row in range(6):
            curr = 0
            for col in range(7):
                if player & (1 << (row * 7 + col)):
                    curr += 1
                else:
                    curr = 0
                if curr >= 4:
                    count += 1

        # Vertical Connect4s (weighted higher)
        for col in range(7):
            curr = 0
            for row in range(6):
                if player & (1 << (row * 7 + col)):
                    curr += 1
                else:
                    curr = 0
                if curr >= 4:
                    count += 11

        # Diagonal Connect4s Positive Slope (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if (player & (1 << (row * 7 + col)) and
                    player & (1 << ((row - 1) * 7 + col + 1)) and
                    player & (1 << ((row - 2) * 7 + col + 2)) and
                    player & (1 << ((row - 3) * 7 + col + 3))):
                    count += 1

        # Diagonal Connect4s Negative Slope (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if (player & (1 << (row * 7 + col)) and
                    player & (1 << ((row + 1) * 7 + col + 1)) and
                    player & (1 << ((row + 2) * 7 + col + 2)) and
                    player & (1 << ((row + 3) * 7 + col + 3))):
                    count += 1

        return count