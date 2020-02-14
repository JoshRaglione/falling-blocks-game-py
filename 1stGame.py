import pygame
import random
import sys

pygame.init()

Width = 800
Height = 600

screen = pygame.display.set_mode((Width, Height))

player_size = 50
enemy_size = 50

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
background_color = (0, 0, 0)

player_pos = [Width/2, Height - 2 * player_size]
enemy_pos = [random.randint(0, Width-enemy_size), 0]

highscore = 0

falling_speed = 15

enemy_list = [enemy_pos]


game_over = False

clock = pygame.time.Clock()

scoreFont = pygame.font.SysFont("monospace", 35)

def set_level(highscore, falling_speed):
    # if highscore < 20:
    #     falling_speed = 5
    # elif highscore < 40:
    #     falling_speed = 8
    # elif highscore < 60:
    #     falling_speed = 12
    # else:
    #     falling_speed = 20
    falling_speed = highscore / 2 + 1
    return falling_speed

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, Width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
   for enemy_pos in enemy_list:
    pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_pos(enemy_list, highscore):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < Height:
            enemy_pos[1] += falling_speed
        else:
            enemy_list.pop(idx)
            highscore += 1
    return highscore

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

while not game_over:

    for event in pygame.event.get():
        print(event)

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_RIGHT:
                x += player_size

            elif event.key == pygame.K_LEFT:
                x -= player_size

            player_pos = [x, y]

    screen.fill((background_color))

    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    highscore = update_enemy_pos(enemy_list, highscore)
    falling_speed = set_level(highscore, falling_speed)
    
    text = "Score:" + str(highscore)
    label = scoreFont.render(text, 1, white)
    screen.blit(label, (Width - 200, Height - 40))


    if collision_check(enemy_list, player_pos):
       game_over = True
       break

    draw_enemies(enemy_list)

    pygame.draw.rect(screen, green, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()


