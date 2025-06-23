import pygame
import sys
import time
from game_state import GameState
from ai_logic import MinimaxAI

# Initialize pygame
pygame.init()

# Constants
BOARD_SIZE = 19
CELL_SIZE = 40
BOARD_PADDING = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (219, 178, 94)
LINE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 0, 0)
INFO_PANEL_WIDTH = 300
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING + INFO_PANEL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * BOARD_PADDING
STONE_RADIUS = CELL_SIZE // 2 - 2
FONT_SIZE = 24

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pente Game")
font = pygame.font.SysFont("Arial", FONT_SIZE)