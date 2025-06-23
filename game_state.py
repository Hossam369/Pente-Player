class GameState:
    BOARD_SIZE = 19
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = self.WHITE  # Start with White as the human player
        self.captures = {self.BLACK: 0, self.WHITE: 0}
        self.last_move = None
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def get_valid_moves(self):
        """Return valid moves, prioritizing those near existing stones."""
        valid_moves = []
        if not self.move_history:
            center = self.BOARD_SIZE // 2
            return [(center, center)]  # Start at center for first move
        
        # Filter moves within radius of existing stones
        radius = 3
        occupied = set((r, c) for r, c, _, _ in self.move_history)
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.EMPTY:
                    for hr, hc in occupied:
                        if abs(i - hr) <= radius and abs(j - hc) <= radius:
                            valid_moves.append((i, j))
                            break
        return valid_moves or [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE) if self.board[i][j] == self.EMPTY]
    
    def is_valid_move(self, row, col):
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return False
        return self.board[row][col] == self.EMPTY
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        
        # Check for captures and store captured positions
        captured_positions = self.check_captures(row, col)
        self.captures[self.current_player] += len(captured_positions) // 2
        
        # Store move with captured positions
        self.move_history.append((row, col, self.current_player, captured_positions))
        
        # Check for win conditions
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif self.captures[self.current_player] >= 5:
            self.game_over = True
            self.winner = self.current_player
        elif len(self.get_valid_moves()) == 0:
            self.game_over = True
            self.winner = None
            if self.captures[self.BLACK] > self.captures[self.WHITE]:
                self.winner = self.BLACK
            elif self.captures[self.WHITE] > self.captures[self.BLACK]:
                self.winner = self.WHITE
        
        self.current_player = self.BLACK if self.current_player == self.WHITE else self.WHITE
        return True
    
    def undo_move(self):
        if not self.move_history:
            return False
        
        row, col, player, captured_positions = self.move_history.pop()
        self.board[row][col] = self.EMPTY
        self.current_player = player
        
        # Restore captured stones
        opponent = self.BLACK if player == self.WHITE else self.WHITE
        for r, c in captured_positions:
            self.board[r][c] = opponent
        
        # Restore capture counts
        self.captures = {self.BLACK: 0, self.WHITE: 0}
        for _, _, p, cp in self.move_history:
            self.captures[p] += len(cp) // 2
        
        self.last_move = self.move_history[-1][:2] if self.move_history else None
        self.game_over = False
        self.winner = None
        return True
    
    def check_captures(self, row, col):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        opponent = self.BLACK if self.current_player == self.WHITE else self.WHITE
        captured_positions = set()
        
        for dr, dc in directions:
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2*dr, col + 2*dc
            r3, c3 = row + 3*dr, col + 3*dc
            
            if (0 <= r1 < self.BOARD_SIZE and 0 <= c1 < self.BOARD_SIZE and
                0 <= r2 < self.BOARD_SIZE and 0 <= c2 < self.BOARD_SIZE and
                0 <= r3 < self.BOARD_SIZE and 0 <= c3 < self.BOARD_SIZE):
                if (self.board[r1][c1] == opponent and 
                    self.board[r2][c2] == opponent and 
                    self.board[r3][c3] == self.current_player):
                    captured_positions.add((r1, c1))
                    captured_positions.add((r2, c2))
        
        for r, c in captured_positions:
            self.board[r][c] = self.EMPTY
        
        return list(captured_positions)
    
    def check_win(self, row, col):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == self.current_player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == self.current_player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False
    
    def get_winner(self):
        return self.winner if self.game_over else None
    
    def clone(self):
        clone = GameState()
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                clone.board[i][j] = self.board[i][j]
        clone.current_player = self.current_player
        clone.captures = {player: self.captures[player] for player in self.captures}
        clone.last_move = self.last_move
        clone.game_over = self.game_over
        clone.winner = self.winner
        clone.move_history = self.move_history.copy()
        return clone
    
    