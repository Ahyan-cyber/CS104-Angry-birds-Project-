import pygame
import math
from params import *

class Bird:
    def __init__(self, color, x, y, side):
        self.color = color
        self.side = side
        self.original_image = pygame.image.load(f'resources/images/{color}.png').convert_alpha()
        if side == "right":     #flip image
            self.original_image = pygame.transform.flip(self.original_image, True, False)
        scale = BIRD_SCALES[color]
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale)))
        self.start_pos = pygame.Vector2(x, y)
        self.pull_vector = pygame.Vector2(0, 0)
        self.dragging = False
        self.on_ground = False
    
        self.rect = self.image.get_rect(center = (x,y))
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.launched = False

    def launch(self, start_pos, end_pos):
        pull_vector = start_pos - end_pos
        if pull_vector.length() > MAX_PULL_DISTANCE:
            pull_vector.scale_to_length(MAX_PULL_DISTANCE)
        self.vel = pull_vector * LAUNCH_POWER
        self.launched = True
    
    def update_drag(self, mouse_pos):
        if self.dragging:
            self.pull_vector = self.start_pos - mouse_pos
            if self.pull_vector.length() > MAX_PULL_DISTANCE:
                self.pull_vector.scale_to_length(MAX_PULL_DISTANCE)
            self.pos = self.start_pos - self.pull_vector
        if self.pos.y > GROUND_Y-1:
            self.pos.y = GROUND_Y-1
    
    def draw_trajectory(self, screen):
        if self.dragging:
            pygame.draw.line(screen, PULL_BACK_COLOR, self.start_pos, self.pos, 3)

    def update(self, ground_y):
        if self.launched:
            self.vel.y += GRAVITY
            self.pos += self.vel
            self._handle_screen_collision(ground_y)
            angle = math.degrees(math.atan2(-self.vel.y, self.vel.x))
            self.rotated_image = pygame.transform.rotate(self.image, angle)
            self.rect = self.rotated_image.get_rect(center=self.pos)

    def _handle_screen_collision(self, ground_y):
        if self.pos.x < 0 or self.pos.x > SCREEN_WIDTH:
            self.vel.x *= -BOUNCE_DAMPENING
            self.pos.x = max(0, min(self.pos.x, SCREEN_WIDTH))
        if self.pos.y > ground_y - self.rect.height/2:
            self.vel.y *= -BOUNCE_DAMPENING
            self.pos.y = min(self.pos.y, ground_y - self.rect.height/2)
        if self.vel.magnitude() < MIN_VELOCITY:
            self.vel = pygame.Vector2(0, 0)

    def draw(self, screen):
        if self.launched:
            screen.blit(self.rotated_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

    def check_collision(self, blocks):
        collisions = []
        screen_center = SCREEN_WIDTH // 2
        for block in blocks:
            if (self.side == "left" and block.rect.centerx < screen_center) or (self.side == "right" and block.rect.centerx > screen_center):
                continue
            if self.rect.colliderect(block.rect):
                dx = (self.rect.centerx - block.rect.centerx) / (BLOCK_WIDTH/2)
                dy = (self.rect.centery - block.rect.centery) / (BLOCK_HEIGHT/2)
                if abs(dx) > abs(dy):
                    self.vel.x *= -BOUNCE_DAMPENING
                else:
                    self.vel.y *= -BOUNCE_DAMPENING
                damage = BIRD_DAMAGE[self.color][block.block_type]
                block.hitpoints -= damage
                collisions.append(block)
                if self.vel.length() > 0:
                    self.pos += self.vel.normalize() * 2
        return collisions