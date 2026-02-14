import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ocean Scene with Boat Control")

clock = pygame.time.Clock()

# Colors
SKY_TOP = (180, 225, 255)
SKY_BOTTOM = (135, 206, 250)
DEEP_WATER = (0, 70, 130)
SUN_COLOR = (255, 220, 0)
BOAT_COLOR = (139, 69, 19)

# Boat settings
boat_x = 150
boat_speed = 5
boat_wave_offset = 0

# Player fish
player_x = WIDTH // 2
player_y = HEIGHT // 2 + 80
player_speed = 5

# Other fishes
fish_list = []
for i in range(8):
    fish_list.append([
        random.randint(0, WIDTH),
        random.randint(HEIGHT//2 + 40, HEIGHT - 40),
        random.choice([-2, -1, 1, 2]),
        random.choice([(255,150,0), (255,255,0),
                       (0,255,255), (255,0,150)])
    ])

wave_offset = 0

running = True
while running:
    clock.tick(60)

    # -------------------------
    # SKY GRADIENT
    # -------------------------
    for y in range(HEIGHT//2):
        ratio = y / (HEIGHT//2)
        r = SKY_TOP[0] * (1 - ratio) + SKY_BOTTOM[0] * ratio
        g = SKY_TOP[1] * (1 - ratio) + SKY_BOTTOM[1] * ratio
        b = SKY_TOP[2] * (1 - ratio) + SKY_BOTTOM[2] * ratio
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

    pygame.draw.circle(screen, SUN_COLOR, (850, 100), 50)

    # -------------------------
    # WATER BASE
    # -------------------------
    pygame.draw.rect(screen, DEEP_WATER, (0, HEIGHT//2, WIDTH, HEIGHT//2))

    # -------------------------
    # WAVES
    # -------------------------
    wave_offset += 0.05

    for layer in range(3):
        wave_points = []

        for x in range(0, WIDTH, 8):
            y = HEIGHT//2 + math.sin(x * 0.02 + wave_offset + layer) * (10 + layer*4)
            wave_points.append((x, y))

        wave_points.append((WIDTH, HEIGHT))
        wave_points.append((0, HEIGHT))

        wave_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        color = (0, 120 + layer*20, 190 + layer*10, 120)
        pygame.draw.polygon(wave_surface, color, wave_points)
        screen.blit(wave_surface, (0, 0))

    # -------------------------
    # BOAT CONTROL
    # -------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        boat_x -= boat_speed
    if keys[pygame.K_RIGHT]:
        boat_x += boat_speed

    boat_x = max(0, min(WIDTH - 200, boat_x))

    boat_wave_offset += 0.05
    boat_y = HEIGHT//2 - 20 + math.sin(boat_wave_offset) * 5

    # Boat body
    pygame.draw.polygon(screen, BOAT_COLOR,
                        [(boat_x, boat_y),
                         (boat_x + 150, boat_y),
                         (boat_x + 120, boat_y + 40),
                         (boat_x + 30, boat_y + 40)])

    # Mast
    pygame.draw.line(screen, (0, 0, 0),
                     (boat_x + 65, boat_y),
                     (boat_x + 65, boat_y - 80), 3)

    # Sail
    pygame.draw.polygon(screen, (255, 255, 255),
                        [(boat_x + 65, boat_y - 80),
                         (boat_x + 65, boat_y),
                         (boat_x + 120, boat_y - 20)])

    # -------------------------
    # Other Fishes
    # -------------------------
    for fish in fish_list:
        fish[0] += fish[2]

        if fish[0] > WIDTH + 20:
            fish[0] = -20
        if fish[0] < -20:
            fish[0] = WIDTH + 20

        pygame.draw.ellipse(screen, fish[3], (fish[0], fish[1], 40, 20))

        if fish[2] > 0:
            tail = [(fish[0], fish[1] + 10),
                    (fish[0] - 15, fish[1]),
                    (fish[0] - 15, fish[1] + 20)]
        else:
            tail = [(fish[0] + 40, fish[1] + 10),
                    (fish[0] + 55, fish[1]),
                    (fish[0] + 55, fish[1] + 20)]

        pygame.draw.polygon(screen, fish[3], tail)
        pygame.draw.circle(screen, (0,0,0),
                           (fish[0] + 30, fish[1] + 8), 3)

    # -------------------------
    # Player Fish Control
    # -------------------------
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    player_x = max(0, min(WIDTH - 50, player_x))

    pygame.draw.ellipse(screen, (255,100,100),
                        (player_x, player_y, 50, 25))
    pygame.draw.polygon(screen, (255,100,100),
                        [(player_x, player_y + 12),
                         (player_x - 20, player_y),
                         (player_x - 20, player_y + 25)])
    pygame.draw.circle(screen, (0,0,0),
                       (player_x + 35, player_y + 10), 4)

    # Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
