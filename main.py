import pygame
import sys
import random
from params import *
from block import Block, create_blocks
from bird import Bird

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angry Birds Dual')
BACKGROUND_1 = pygame.image.load('resources/images/Background_initial.png')
BACKGROUND_1 = pygame.transform.scale(BACKGROUND_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_2 = pygame.image.load('resources/images/Background_initial_(2).png')
BACKGROUND_2 = pygame.transform.scale(BACKGROUND_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pygame.image.load('resources/images/Background.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#Welcome screen
initial_start_time = pygame.time.get_ticks()
welcome = True
while welcome:
    current_time = pygame.time.get_ticks()
    if current_time - initial_start_time >= 2000:
        welcome = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(BACKGROUND_1, (0,0))
    pygame.display.flip()
    clock.tick(60)

#start screen elements
font = pygame.font.Font(None, 32)
input_box_width = 300
input_box_height = 40
input_box_left = pygame.Rect(SCREEN_WIDTH//4 - input_box_width//2, 300, input_box_width, input_box_height)
input_box_right = pygame.Rect(3*SCREEN_WIDTH//4 - input_box_width//2, 300, input_box_width, input_box_height)
start_button_img = pygame.image.load('resources/images/start_button.png').convert_alpha()
start_button_img = pygame.transform.scale(start_button_img, (200, 100))
start_button_rect = start_button_img.get_rect(center=(SCREEN_WIDTH//2, 500))
left_player_name = ""
right_player_name = ""
active_input = None

start_screen = True
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box_left.collidepoint(event.pos):
                active_input = 'left'
            elif input_box_right.collidepoint(event.pos):
                active_input = 'right'
            elif start_button_rect.collidepoint(event.pos):
                if left_player_name and right_player_name:
                    start_screen = False
            else:
                active_input = None
        
        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == 'right':
                        left_player_name = left_player_name[:-1]
                    else:
                        right_player_name = right_player_name[:-1]
                else:
                    if event.unicode.isalnum or event.unicode in (' ', '-'):
                        if active_input == 'left' and len(left_player_name) < 15:
                            left_player_name += event.unicode
                        elif active_input == 'right' and len(right_player_name) < 15:
                            right_player_name += event.unicode
    
    screen.blit(BACKGROUND_2, (0, 0))
    color_active = (100,200,255)
    color_inactive = (0,0,0)
    pygame.draw.rect(screen, color_active if active_input == 'left' else color_inactive, input_box_left, 2)
    pygame.draw.rect(screen, color_active if active_input == 'right' else color_inactive, input_box_right, 2)

    txt_surface = font.render(left_player_name, True, (0,0,200))
    screen.blit(txt_surface, (input_box_left.x + 5, input_box_right.y + 5))
    txt_surface = font.render(right_player_name, True, (0,0,200))
    screen.blit(txt_surface, (input_box_right.x + 5, input_box_right.y + 5))

    label = font.render("LEFT PLAYER NAME:", True, (0,0,0))
    screen.blit(label, (input_box_left.x, input_box_left.y - 30))
    label = font.render("RIGHT PLAYER NAME:", True, (0,0,0))
    screen.blit(label, (input_box_right.x, input_box_right.y - 30))

    screen.blit(start_button_img, start_button_rect)

    pygame.display.flip()
    clock.tick(60)

#Catapult img scaling
catapult_img = pygame.image.load('resources/images/Catapult.png')
original_size = catapult_img.get_size()
scaled_size = (
    int(original_size[0] * CATAPULT_SCALE),
    int(original_size[1] * CATAPULT_SCALE)
)
catapult = pygame.transform.scale(catapult_img, scaled_size)
CATAPULT_Y = GROUND_Y - scaled_size[1]
LEFT_CATAPULT_X = 400
RIGHT_CATAPULT_X = SCREEN_WIDTH - scaled_size[0] - 400

current_bird = None
current_bird_index = 0
active_side = "left"
birds = []
def load_bird(side):
    global current_bird, current_bird_index
    if not blocks or current_bird_index >= len(BIRD_QUEUE):
        return
    color = BIRD_QUEUE[current_bird_index]
    if side == "left":
        x = LEFT_CATAPULT_X + catapult.get_width()//2
        
    else:
        x = RIGHT_CATAPULT_X + catapult.get_width()//2
    
    y = CATAPULT_Y + 15
    current_bird = Bird(color, x, y, side)

blocks = create_blocks()

current_bird_index = 0
load_bird("left")
left_bird = current_bird
load_bird("right")
right_bird = current_bird
current_bird = left_bird #start from left side

left_score = 0
right_score = 0
score_font = pygame.font.Font(None, 36)

#Check the winner
def check_winner(blocks):
    screen_center = SCREEN_WIDTH // 2
    left_blocks_exist = any(block.rect.centerx < screen_center for block in blocks)
    right_blocks_exist = any(block.rect.centerx > screen_center for block in blocks)
    
    if not left_blocks_exist:
        return "right"
    if not right_blocks_exist:
        return "left"
    return None

def show_result_screen(winner):
    result_bg = pygame.image.load(WINNER_BG).convert_alpha()
    result_bg = pygame.transform.scale(result_bg, (3*SCREEN_WIDTH//4, 3*SCREEN_HEIGHT//4))
    
    result_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 48)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(result_bg, (SCREEN_WIDTH//8, SCREEN_HEIGHT//8))
        
        # Draw winner text
        winner_name = left_player_name if winner == "left" else right_player_name
        text = result_font.render(f"{winner_name} Wins!", True, (255, 0, 0))
        score = left_score if winner == "left" else right_score
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 580))
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 460))
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

winner = None
dragging = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if active_side == "left" and left_bird.rect.collidepoint(event.pos):
                current_bird = left_bird
                current_bird.dragging = True
            elif active_side == "right" and right_bird.rect.collidepoint(event.pos):
                current_bird = right_bird
                current_bird.dragging = True
        
        if event.type == pygame.MOUSEMOTION:
            if active_side == "left" and current_bird.dragging:
                current_bird = left_bird
                current_bird.update_drag(pygame.Vector2(event.pos))
            elif active_side == "right" and current_bird.dragging:
                current_bird = right_bird
                current_bird.update_drag(pygame.Vector2(event.pos))

        if event.type == pygame.MOUSEBUTTONUP:
            if current_bird.dragging:
                current_bird.dragging = False
                current_bird.launch(current_bird.start_pos, pygame.Vector2(event.pos))
                birds.append(current_bird)

                current_bird_index += 1

                load_bird("left")
                new_left_bird = current_bird
                load_bird("right")
                new_right_bird = current_bird

                left_bird = new_left_bird
                right_bird = new_right_bird

                active_side = "left" if active_side == "right" else "right"
                current_bird = left_bird if active_side == "left" else right_bird

    for bird in birds:
        bird.update(GROUND_Y)
        damaged_blocks = bird.check_collision(blocks)
        if damaged_blocks:
            blocks_removed = 0
            for block in damaged_blocks:
                if block.hitpoints <= 0:
                    blocks_removed += 1
            if bird.side == "left":
                left_score += blocks_removed * 100
            else:
                right_score += blocks_removed * 100
            
            birds.remove(bird)
            continue
        for block in damaged_blocks:
            if block.hitpoints <= 0:
                blocks.remove(block)
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button clicked
        mouse_pos = pygame.mouse.get_pos()
        for block in blocks:
            if block.rect.collidepoint(mouse_pos):
                block.hitpoints -= 300
    
    birds = [bird for bird in birds if bird.rect.y < SCREEN_HEIGHT + 100]
    blocks = [block for block in blocks if block.hitpoints > 0]
    
    screen.blit(BACKGROUND, (0,0))
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, SCREEN_WIDTH, GROUND_HEIGHT))

    screen.blit(catapult, (LEFT_CATAPULT_X, CATAPULT_Y))
    screen.blit(catapult, (RIGHT_CATAPULT_X, CATAPULT_Y))
    if active_side == "left":
        pygame.draw.circle(screen, (255,0,0), (LEFT_CATAPULT_X + 50, CATAPULT_Y - 20), 10)
    else:
        pygame.draw.circle(screen, (255,0,0), (RIGHT_CATAPULT_X + catapult.get_width() - 50, CATAPULT_Y - 20), 10)

    if current_bird and not current_bird.launched:
        current_bird.image
        current_bird.draw_trajectory(screen)
        screen.blit(current_bird.image, current_bird.rect)
    
    for bird in birds:
        screen.blit(bird.image, bird.rect)

    for block in blocks:
        block.draw(screen)
    
    #Score display
    left_score_text = score_font.render(f"{left_player_name}: {left_score}", True, (255,255,255))
    right_score_text = score_font.render(f"{right_player_name}: {right_score}", True, (255,255,255))

    screen.blit(left_score_text, (20,20))
    screen.blit(right_score_text, (SCREEN_WIDTH - right_score_text.get_width() - 20, 20))

    #Check for winner
    winner = check_winner(blocks)
    if winner:
        break

    pygame.display.flip()
    clock.tick(60)

if winner:
    result_action = show_result_screen(winner)

pygame.quit()
sys.exit()