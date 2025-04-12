class Connect4Board:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0

    def height(self, column):
        for row in range(6):
            if not (self.player1 & (1 << (row * 7 + column)) or self.player2 & (1 << (row * 7 + column))):
                return row
        return 6

    def reset(self):
        self.player1 = 0
        self.player2 = 0

    def valid_moves(self):
        return [i for i in range(7) if self.height(i) < 6]

    def move(self, column, player):
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
        if column<0 or column>6:
            raise ValueError("Invalid column")

        ht = self.height(column)

        if ht == 0:
            raise ValueError("Column is empty")

        if player == 1:
            self.player1 = self.player1 & ~(1 << ((ht-1) * 7 + column))
        else:
            self.player2 = self.player2 & ~(1 << ((ht-1) * 7 + column))

    def connect_4s(self,player):
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

        # Vertical Connect4s
        for col in range(7):
            curr = 0
            for row in range(6):
                if player & (1 << (row * 7 + col)):
                    curr += 1
                else:
                    curr = 0
                if curr >= 4:
                    count += 11

        # Diagonal Connect4s Positive Slope
        for row in range(3, 6):
            for col in range(4):
                if (player & (1 << (row * 7 + col)) and
                    player & (1 << ((row - 1) * 7 + col + 1)) and
                    player & (1 << ((row - 2) * 7 + col + 2)) and
                    player & (1 << ((row - 3) * 7 + col + 3))):
                    count += 1

        # Diagonal Connect4s Negative Slope
        for row in range(3):
            for col in range(4):
                if (player & (1 << (row * 7 + col)) and
                    player & (1 << ((row + 1) * 7 + col + 1)) and
                    player & (1 << ((row + 2) * 7 + col + 2)) and
                    player & (1 << ((row + 3) * 7 + col + 3))):
                    count += 1

        return count