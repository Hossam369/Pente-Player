import time
from game_state import GameState

class HeuristicEvaluator:
    @staticmethod
    def evaluate(game_state, player):
        score = 0
        score += game_state.captures[player] * 10
        score += HeuristicEvaluator._evaluate_rows(game_state, player)
        score += HeuristicEvaluator._evaluate_center_control(game_state, player)
        score += HeuristicEvaluator._evaluate_potential_captures(game_state, player)
        
        opponent = GameState.BLACK if player == GameState.WHITE else GameState.WHITE
        score -= HeuristicEvaluator._evaluate_rows(game_state, opponent) * 0.8
        score -= HeuristicEvaluator._evaluate_potential_captures(game_state, opponent) * 0.8
        
        return score
    
    @staticmethod
    def _evaluate_rows(game_state, player):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
        score = 0
        
        for i in range(game_state.BOARD_SIZE):
            for j in range(game_state.BOARD_SIZE):
                if game_state.board[i][j] == player:
                    for dr, dc in directions:
                        length = 1
                        open_ends = 0
                        r, c = i + dr, j + dc
                        while 0 <= r < game_state.BOARD_SIZE and 0 <= c < game_state.BOARD_SIZE:
                            if game_state.board[r][c] == player:
                                length += 1
                            elif game_state.board[r][c] == game_state.EMPTY:
                                open_ends += 1
                                break
                            else:
                                break
                            r += dr
                            c += dc
                        r, c = i - dr, j - dc
                        while 0 <= r < game_state.BOARD_SIZE and 0 <= c < game_state.BOARD_SIZE:
                            if game_state.board[r][c] == player:
                                length += 1
                            elif game_state.board[r][c] == game_state.EMPTY:
                                open_ends += 1
                                break
                            else:
                                break
                            r -= dr
                            c -= dc
                        if length >= 5:
                            score += 10000
                        elif length == 4:
                            score += 1000 if open_ends == 2 else 100 if open_ends == 1 else 0
                        elif length == 3:
                            score += 50 if open_ends == 2 else 10 if open_ends == 1 else 0
                        elif length == 2:
                            score += 5 if open_ends == 2 else 2 if open_ends == 1 else 0
        return score
    
    @staticmethod
    def _evaluate_center_control(game_state, player):
        score = 0
        center = game_state.BOARD_SIZE // 2
        for i in range(center-2, center+3):
            for j in range(center-2, center+3):
                if 0 <= i < game_state.BOARD_SIZE and 0 <= j < game_state.BOARD_SIZE:
                    if game_state.board[i][j] == player:
                        distance = max(abs(i - center), abs(j - center))
                        score += 3 - distance * 0.5
        return score
    
    @staticmethod
    def _evaluate_potential_captures(game_state, player):
        score = 0
        opponent = GameState.BLACK if player == GameState.WHITE else GameState.WHITE
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        
        for i in range(game_state.BOARD_SIZE):
            for j in range(game_state.BOARD_SIZE):
                if game_state.board[i][j] == player:
                    for dr, dc in directions:
                        r1, c1 = i + dr, j + dc
                        r2, c2 = i + 2*dr, j + 2*dc
                        r3, c3 = i + 3*dr, j + 3*dc
                        if (0 <= r1 < game_state.BOARD_SIZE and 0 <= c1 < game_state.BOARD_SIZE and
                            0 <= r2 < game_state.BOARD_SIZE and 0 <= c2 < game_state.BOARD_SIZE and
                            0 <= r3 < game_state.BOARD_SIZE and 0 <= c3 < game_state.BOARD_SIZE):
                            if (game_state.board[r1][c1] == opponent and 
                                game_state.board[r2][c2] == opponent and 
                                game_state.board[r3][c3] == game_state.EMPTY):
                                score += 5
        return score


class MinimaxAI:
    def __init__(self, player, max_depth=2, time_limit=2.0):
        self.player = player
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.nodes_evaluated = 0
        self.start_time = None
    
    def get_best_move(self, game_state):
        self.nodes_evaluated = 0
        self.start_time = time.time()
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        valid_moves = game_state.get_valid_moves()
        center = game_state.BOARD_SIZE // 2
        
        if len(game_state.move_history) == 0:
            return (center, center)
        
        # Sort moves based on heuristic evaluation
        move_scores = []
        for move in valid_moves:
            row, col = move
            new_state = game_state.clone()
            new_state.make_move(row, col)
            score = (HeuristicEvaluator._evaluate_rows(new_state, self.player) * 2 +
                     HeuristicEvaluator._evaluate_potential_captures(new_state, self.player) * 3 -
                     max(abs(row - center), abs(col - center)))
            move_scores.append((score, move))
        move_scores.sort(reverse=True)
        valid_moves = [move for _, move in move_scores]
        
        for move in valid_moves[:50]:
            row, col = move
            new_state = game_state.clone()
            new_state.make_move(row, col)
            
            score = self._minimax(new_state, self.max_depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
            
            if time.time() - self.start_time > self.time_limit:
                break
        
        return best_move or valid_moves[0]
    
    def _minimax(self, game_state, depth, alpha, beta, maximizing):
        self.nodes_evaluated += 1
        
        if game_state.game_over or depth == 0 or (time.time() - self.start_time > self.time_limit):
            return self._evaluate_state(game_state)
        
        if maximizing:
            max_eval = float('-inf')
            valid_moves = game_state.get_valid_moves()
            
            for move in valid_moves[:50]:
                row, col = move
                new_state = game_state.clone()
                new_state.make_move(row, col)
                
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            
            return max_eval
        
        else:
            min_eval = float('inf')
            valid_moves = game_state.get_valid_moves()
            
            for move in valid_moves[:50]:
                row, col = move
                new_state = game_state.clone()
                new_state.make_move(row, col)
                
                eval_score = self._minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            
            return min_eval
    
    def _evaluate_state(self, game_state):
        winner = game_state.get_winner()
        if winner == self.player:
            return 100000
        elif winner is not None:
            return -100000
        elif game_state.game_over:
            return 0
        return HeuristicEvaluator.evaluate(game_state, self.player)