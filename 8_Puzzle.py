import pyxel
import random

class App:
    def __init__(self):
        # Dimensions
        self.N = 3
        self.base_size = 150
        self.tile_size = self.base_size // self.N
        self.panel_width = 70
        self.screen_width = self.base_size + self.panel_width * 2
        self.screen_height = self.base_size

        pyxel.init(self.screen_width, self.screen_height, "8 Puzzle", display_scale=4)
        pyxel.mouse(True)
        self.board = list(range(9))
        self.moves = 0
        self.shuffle_board()
        pyxel.run(self.update, self.draw)

    def shuffle_board(self):
        while True:
            self.board = random.sample(range(9), 9)
            if self.is_solvable() and not self.is_solved():
                break
        self.moves = 0

    # Check if the current board configuration is solvable
    def is_solvable(self):
        inversions = 0
        for i in range(len(self.board)):
            for j in range(i+1, len(self.board)):
                if self.board[i] and self.board[j] and self.board[i] > self.board[j]:
                    inversions += 1
        return inversions % 2 == 0

    def is_solved(self):
        return self.board[:8] == list(range(1,9)) and self.board[8] == 0

    def get_empty_neighbors(self):
        empty_index = self.board.index(0)
        row, col = empty_index // self.N, empty_index % self.N
        neighbors = []
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if 0 <= row+dr < self.N and 0 <= col+dc < self.N:
                neighbors.append((row+dr)*self.N + (col+dc))
        return neighbors

    def swap_tile(self, index):
        empty_index = self.board.index(0)
        self.board[empty_index], self.board[index] = self.board[index], self.board[empty_index]
        self.moves += 1

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # Puzzle area interaction (center square)
            if self.panel_width <= pyxel.mouse_x < self.screen_width - self.panel_width:
                x = (pyxel.mouse_x - self.panel_width) // self.tile_size
                y = pyxel.mouse_y // self.tile_size
                index = y * self.N + x
                if index in self.get_empty_neighbors():
                    self.swap_tile(index)
            
            # Shuffle button (right panel)
            btn_x = self.screen_width - self.panel_width + 10
            btn_y = self.screen_height - 40
            if (btn_x <= pyxel.mouse_x <= btn_x + self.panel_width - 20 and
                btn_y <= pyxel.mouse_y <= btn_y + 30):
                self.shuffle_board()

    def draw(self):
        pyxel.cls(1)
        
        # Draw puzzle tiles (centered square)
        for i, value in enumerate(self.board):
            x = self.panel_width + (i % self.N) * self.tile_size
            y = (i // self.N) * self.tile_size
            if value != 0:
                pyxel.rect(x, y, self.tile_size-1, self.tile_size-1, 6)
                pyxel.text(x + self.tile_size//2 - 4, y + self.tile_size//2 - 4, str(value), 5)
        
        # Left panel - Instructions
        pyxel.rect(0, 0, self.panel_width, self.screen_height, 12)
        pyxel.text(5, 15, "HOW TO PLAY:", 0)
        pyxel.text(5, 35, "Click adjacent", 0)
        pyxel.text(5, 45, "tiles to slide", 0)
        pyxel.text(5, 55, "into empty", 0)
        pyxel.text(5, 65, "space", 0)
        pyxel.text(5, 90, "GOAL:", 0)
        pyxel.text(5, 105, "Arrange 1-8", 0)
        pyxel.text(5, 115, "with empty", 0)
        pyxel.text(5, 125, "at bottom", 0)
        
        # Right panel - Controls
        right_panel_x = self.screen_width - self.panel_width
        pyxel.rect(right_panel_x, 0, self.panel_width, self.screen_height, 12)
        pyxel.text(right_panel_x + 10, 15, "MOVES:", 0)
        pyxel.text(right_panel_x + 10, 35, str(self.moves), 7)
        
        # Shuffle button
        btn_x = right_panel_x + 10
        btn_y = self.screen_height - 40
        pyxel.rect(btn_x, btn_y, self.panel_width - 20, 30, 5)
        pyxel.text(btn_x + 8, btn_y + 10, "SHUFFLE", 7)
        
        # Custom cursor
        pyxel.rect(pyxel.mouse_x, pyxel.mouse_y, 2, 2, 7)
        
        # Victory overlay (centered in puzzle area)
        if self.is_solved():
            overlay_x = self.panel_width + 20
            overlay_y = self.base_size//2 - 20
            pyxel.rect(overlay_x, overlay_y, self.base_size - 40, 40, 0)
            pyxel.text(overlay_x + 15, overlay_y + 15, "PUZZLE SOLVED!", 10)

App()