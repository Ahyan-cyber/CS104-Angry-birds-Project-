import pygame
import random
from params import *

class Block:
    def __init__(self, color, x, y, hitpoints):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        self.color = color
        self.hitpoints = hitpoints
        self.max_hitpoints = hitpoints
        self.block_type = self._get_type()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.hitpoints < self.max_hitpoints:
            self._draw_health_bar(screen)

    def _draw_health_bar(self, screen):
        health_bar_height = 5
        health_bar_y = self.rect.y - health_bar_height - 2
        health_ratio = self.hitpoints / self.max_hitpoints
        health_width = int(self.rect.width * health_ratio)

        pygame.draw.rect(screen, (50,50,50), (self.rect.x, health_bar_y, health_width, health_bar_height))
        health_color = (int(255 * (1-health_ratio)), int(255 * health_ratio), 0)
        pygame.draw.rect(screen, health_color, (self.rect.x, health_bar_y, health_width, health_bar_height))

    def _get_type(self):
        if self.color == BROWN:
            return "brown"
        elif self.color == BLACK:
            return "black"
        elif self.color == LIGHT_BLUE:
            return "light_blue"
        return "unknown"

def create_blocks():
    colors = COLOR_DISTRIBUTION.copy()
    random.shuffle(colors)

    left_blocks = []
    color_index = 0
    rows = len(BLOCK_STRUCTURE)
    cols = len(BLOCK_STRUCTURE[0])
    for row in range(rows):
        for col in range(cols):
            if BLOCK_STRUCTURE[row][col] == 1:
                x = STRUCTURE_START_X + col * (BLOCK_WIDTH + HORIZONTAL_SPACING)
                y = STRUCTURE_START_Y + row * (BLOCK_HEIGHT + VERTICAL_SPACING)

                color = colors[color_index]
                color_index = (color_index + 1) % len(colors)

                left_blocks.append(Block(color, x, y, BLOCK_HITPOINTS))
    right_blocks = []
    screen_center = SCREEN_WIDTH // 2

    for block in left_blocks:
        mirrored_x = SCREEN_WIDTH - block.rect.x - BLOCK_WIDTH
        right_blocks.append(Block(block.color, mirrored_x, block.rect.y, BLOCK_HITPOINTS))
    return left_blocks + right_blocks