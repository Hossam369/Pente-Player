from main import *
from game_state import GameState
from ai_logic import MinimaxAI

class PenteGUI:
    def __init__(self):
        self.game_state = GameState()
        self.ai = MinimaxAI(GameState.BLACK, max_depth=2, time_limit=2.0)  # AI plays as Black
        self.selected_cell = None
        self.game_over = False
        self.thinking = False
        self.message = ""
        self.ai_thinking_time = 0
        self.ai_nodes_evaluated = 0
        self.player_vs_ai = True
        self.difficulty_level = 2
        self.player_color = GameState.WHITE  # Human plays as White
    
    def draw_board(self):
        screen.fill(WHITE)
        
        # Draw board
        board_width = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
        board_height = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
        board_rect = pygame.Rect(0, 0, board_width, board_height)
        pygame.draw.rect(screen, BOARD_COLOR, board_rect)
        
        # Draw grid lines
        for i in range(BOARD_SIZE):
            start_pos = (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING)
            end_pos = (BOARD_PADDING + i * CELL_SIZE, BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE)
            pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)
            
            start_pos = (BOARD_PADDING, BOARD_PADDING + i * CELL_SIZE)
            end_pos = (BOARD_PADDING + (BOARD_SIZE - 1) * CELL_SIZE, BOARD_PADDING + i * CELL_SIZE)
            pygame.draw.line(screen, LINE_COLOR, start_pos, end_pos, 1)
        
        # Draw stones
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center_x = BOARD_PADDING + col * CELL_SIZE
                center_y = BOARD_PADDING + row * CELL_SIZE
                
                if self.game_state.board[row][col] == GameState.BLACK:
                    pygame.draw.circle(screen, BLACK, (center_x, center_y), STONE_RADIUS)
                elif self.game_state.board[row][col] == GameState.WHITE:
                    pygame.draw.circle(screen, WHITE, (center_x, center_y), STONE_RADIUS)
                    pygame.draw.circle(screen, BLACK, (center_x, center_y), STONE_RADIUS, 1)
        
        # Highlight last move
        if self.game_state.last_move:
            row, col = self.game_state.last_move
            center_x = BOARD_PADDING + col * CELL_SIZE
            center_y = BOARD_PADDING + row * CELL_SIZE
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (center_x, center_y), 5, 2)
        
        self.draw_info_panel()
    
    def draw_info_panel(self):
        # Draw info panel
        panel_rect = pygame.Rect(BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(screen, (240, 240, 240), panel_rect)
        pygame.draw.line(screen, BLACK, (panel_rect.left, 0), (panel_rect.left, WINDOW_HEIGHT), 2)
        
        x = panel_rect.left + 20
        y = 30
        
        # Display game information
        title = font.render("Pente Game", True, BLACK)
        screen.blit(title, (x, y))
        y += 50
        
        current_player = "Black" if self.game_state.current_player == GameState.BLACK else "White"
        player_text = font.render(f"Current Player: {current_player}", True, BLACK)
        screen.blit(player_text, (x, y))
        y += 40
        
        black_captures = font.render(f"Black Captures: {self.game_state.captures[GameState.BLACK]}", True, BLACK)
        screen.blit(black_captures, (x, y))
        y += 30
        
        white_captures = font.render(f"White Captures: {self.game_state.captures[GameState.WHITE]}", True, BLACK)
        screen.blit(white_captures, (x, y))
        y += 50
        
        mode = "Player vs AI" if self.player_vs_ai else "Player vs Player"
        mode_text = font.render(f"Game Mode: {mode}", True, BLACK)
        screen.blit(mode_text, (x, y))
        y += 30
        
        if self.player_vs_ai:
            ai_text = font.render(f"AI Difficulty: {self.difficulty_level} (Depth {self.difficulty_level}, Time ~{self.difficulty_level}s)", True, BLACK)
            screen.blit(ai_text, (x, y))
            y += 30
            
            if self.ai_thinking_time > 0:
                time_text = font.render(f"AI Think Time: {self.ai_thinking_time:.2f}s", True, BLACK)
                screen.blit(time_text, (x, y))
                y += 30
                
                nodes_text = font.render(f"Nodes Evaluated: {self.ai_nodes_evaluated}", True, BLACK)
                screen.blit(nodes_text, (x, y))
                y += 30
        
        y += 20
        
        # Display game status or messages
        if self.game_state.game_over:
            winner = ""
            if self.game_state.winner == GameState.BLACK:
                winner = "Black Wins!"
            elif self.game_state.winner == GameState.WHITE:
                winner = "White Wins!"
            else:
                winner = "Game Draw!"
            
            winner_text = font.render(winner, True, (200, 0, 0))
            screen.blit(winner_text, (x, y))
        elif self.thinking:
            thinking_text = font.render("AI is thinking...", True, (0, 0, 200))
            screen.blit(thinking_text, (x, y))
        elif self.message:
            message_text = font.render(self.message, True, (0, 0, 200))
            screen.blit(message_text, (x, y))
        
        y += 60
        self.draw_button(x, y, 260, 40, "New Game", self.new_game)
        y += 50
        self.draw_button(x, y, 260, 40, "Switch Game Mode", self.switch_game_mode)
        y += 50
        self.draw_button(x, y, 260, 40, "Undo Move", self.undo_move)
        
        if self.player_vs_ai:
            y += 50
            self.draw_button(x, y, 260, 40, "Change Difficulty", self.cycle_difficulty)
        else:
            y += 50
            self.draw_button(x, y, 260, 40, "Switch Color", self.switch_color)
    
    def draw_button(self, x, y, width, height, text, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        button_rect = pygame.Rect(x, y, width, height)
        hover = button_rect.collidepoint(mouse)
        
        color = (200, 200, 200) if hover else (180, 180, 180)
        pygame.draw.rect(screen, color, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        
        if hover and click[0] == 1 and action is not None:
            pygame.time.delay(300)
            action()
    
    def get_board_position(self, mouse_pos):
        x, y = mouse_pos
        if (x < BOARD_PADDING or x >= BOARD_PADDING + BOARD_SIZE * CELL_SIZE or
            y < BOARD_PADDING or y >= BOARD_PADDING + BOARD_SIZE * CELL_SIZE):
            return None
        
        col = round((x - BOARD_PADDING) / CELL_SIZE)
        row = round((y - BOARD_PADDING) / CELL_SIZE)
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return (row, col)
        return None
    
    def handle_click(self, mouse_pos):
        if self.game_state.game_over or self.thinking:
            return
        
        position = self.get_board_position(mouse_pos)
        if not position:
            return
        
        row, col = position
        
        if self.game_state.is_valid_move(row, col):
            self.game_state.make_move(row, col)
            self.message = ""
            
            if self.game_state.game_over:
                return
            
            if self.player_vs_ai and self.game_state.current_player == GameState.BLACK:  # AI's turn (Black)
                self.thinking = True
                self.draw_board()
                pygame.display.flip()
                
                start_time = time.time()
                ai_move = self.ai.get_best_move(self.game_state)
                self.ai_thinking_time = time.time() - start_time
                self.ai_nodes_evaluated = self.ai.nodes_evaluated
                
                if ai_move:
                    self.game_state.make_move(ai_move[0], ai_move[1])
                
                self.thinking = False
        else:
            self.message = "Invalid move!"
    
    def undo_move(self):
        if self.game_state.undo_move():
            self.message = "Move undone!"
            if self.player_vs_ai and self.game_state.current_player == GameState.BLACK:
                self.game_state.undo_move()  # Undo AI move as well
                self.message = "Two moves undone!"
        else:
            self.message = "No moves to undo!"
    
    def new_game(self):
        self.game_state = GameState()
        self.game_over = False
        self.thinking = False
        self.message = "New game started!"
        self.ai_thinking_time = 0
        self.ai_nodes_evaluated = 0
        self.player_color = GameState.WHITE
    
    def switch_game_mode(self):
        self.player_vs_ai = not self.player_vs_ai
        self.new_game()
        self.message = f"Mode: {'Player vs AI' if self.player_vs_ai else 'Player vs Player'}"
    
    def cycle_difficulty(self):
        if self.difficulty_level < 5:
            self.difficulty_level += 1
        else:
            self.difficulty_level = 1
        
        self.ai.max_depth = self.difficulty_level
        self.ai.time_limit = self.difficulty_level * 0.8
        self.message = f"AI Difficulty set to {self.difficulty_level} (Depth {self.difficulty_level}, Time ~{self.difficulty_level*0.8}s)"
    
    def switch_color(self):
        self.player_color = GameState.BLACK if self.player_color == GameState.WHITE else GameState.WHITE
        self.message = f"Your color is now {('Black' if self.player_color == GameState.BLACK else 'White')}"
        self.new_game()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
            
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)