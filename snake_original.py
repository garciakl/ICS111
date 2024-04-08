import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont(None, 40)

again_rect = Rect(screen_width // 2-80, screen_height // 2, 160, 50)

#define snake variables
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([300,310])
snake_pos.append([300,320])
snake_pos.append([300,330])
direction = 1

#define game variables
cell_size = 10
update_snake = 0
food = [0,0]
new_food = True
new_piece = [0,0]
game_over = False
clicked = False
score = 0

#define colors
pink = (247, 108, 123)
green = (93, 210, 162)
yellow = (247, 196, 134)
purple = (106, 100, 127)
bg = purple
body_inner = pink
body_outer = yellow
food_col = green

def draw_screen():
        screen.fill(bg)

def draw_score():
    score_txt = "Score: " + str(score)
    score_img = font.render(score_txt, True, pink)
    screen.blit(score_img, (0,0))

def check_game_over(game_over):
    #first check, snake eaten itself
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            game_over = True
        head_count += 1

    #second check, out of bounds
        if snake_pos[0][0] < 0 or snake_pos[0][0] >= screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] >= screen_height:
            game_over = True

    return game_over

def draw_game_over():
    over_text = "Game Over!"
    over_img = font.render(over_text, True, pink)
    pygame.draw.rect(screen,yellow,(screen_width // 2 - 80, screen_height // 2 - 60,160,50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = "Play Again?"
    again_img = font.render(again_text, True, green)
    pygame.draw.rect(screen, yellow, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            elif event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            elif event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            elif event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    draw_screen()
    draw_score()

    #create food
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width // cell_size) - 1)
        food[1] = cell_size * random.randint(0, (screen_height // cell_size) - 1)

    #draw food
    pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))

    #check if food was eaten
    if snake_pos[0] == food:
        new_food = True
        #create new piece at end of snake tail
        new_piece = list(snake_pos[-1])
        #add extra piece to snake
        if direction == 1:
            new_piece[1] += cell_size
        #down
        if direction == 3:
            new_piece[1] -= cell_size
        #right
        if direction == 2:
            new_piece[0] -= cell_size
        #left
        if direction == 4:
            new_piece[0] += cell_size

        #attach new piece to end of snake
        snake_pos.append(new_piece)

        #increase score
        score += 1

    if game_over == False:
        #update snake
        if update_snake > 250:
            update_snake = 0
            new_head = list(snake_pos[0])
            #first shift the position of snake back
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            #now update the position of head based on direction
            #head up
            if direction == 1:
                new_head[1] -= cell_size
            #head down
            elif direction == 3:
                new_head[1] += cell_size
            #head right
            elif direction == 2:
                new_head[0] += cell_size
            #head left
            elif direction == 4:
                new_head[0] -= cell_size

            snake_pos.insert(0, new_head)

            game_over = check_game_over(game_over)

            if snake_pos[0] != food:
                snake_pos.pop()

    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            #reset variables
            game_over = False
            update_snake = 0
            food = [0,0]
            new_food = True
            new_piece = [0,0]
            #define snake variables
            snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
            snake_pos.append([300,310])
            snake_pos.append([300, 320])
            snake_pos.append([300, 330])
            direction = 1 #1 is up, 2 is down, 3 is down, 4 is left
            score = 0

    head = 1
    for x in snake_pos:

        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1] + 1, cell_size, cell_size))
            pygame.draw.rect(screen, body_outer, (x[0] +1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1] + 1, cell_size, cell_size))
            pygame.draw.rect(screen, (255,0,0), (x[0] +1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_snake += 1

pygame.quit()
