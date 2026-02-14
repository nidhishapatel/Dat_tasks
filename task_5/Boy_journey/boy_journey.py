import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boy Journey Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# Colors
GRASS = (34, 139, 34)
ROAD = (90, 90, 90)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

road_y = 220
road_height = 180

# Boy
boy_size = 40
boy_x = 50
boy_y = road_y + 60
boy_speed = 5

# Buildings
home_rect = pygame.Rect(40, road_y - 150, 150, 120)
market_rect = pygame.Rect(WIDTH//2 - 250, road_y - 160, 170, 120)
friend_rect = pygame.Rect(WIDTH//2 + 80, road_y + road_height + 30, 170, 120)
school_rect = pygame.Rect(WIDTH - 220, road_y - 150, 170, 120)

# ---------- CREATE CARS ----------
def create_cars():
    car_list = []
    for _ in range(3):
        x = random.randint(300, WIDTH - 200)
        y = random.randint(road_y + 20, road_y + road_height - 60)
        car_list.append(pygame.Rect(x, y, 70, 35))
    return car_list

# ---------- CREATE OBSTACLES ----------
def create_obstacles():
    obs_list = []
    for _ in range(3):
        x = random.randint(250, WIDTH - 200)
        y = random.randint(road_y + 20, road_y + road_height - 60)
        obs_list.append(pygame.Rect(x, y, 40, 40))
    return obs_list

cars = create_cars()
obstacles = create_obstacles()

# ---------- RESET ----------
def reset_game():
    global boy_x, boy_y, cars, obstacles, game_state
    boy_x = 50
    boy_y = road_y + 60
    cars = create_cars()
    obstacles = create_obstacles()
    game_state = "playing"

game_state = "playing"
location_message = ""
message_timer = 0

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

running = True
while running:
    screen.fill(GRASS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "win":
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_h:
                    game_state = "returning"

            if game_state == "gameover":
                if event.key == pygame.K_r:
                    reset_game()

            if game_state == "finished":
                if event.key == pygame.K_r:
                    reset_game()

    if game_state in ["playing", "returning"]:

        keys = pygame.key.get_pressed()

        new_x = boy_x
        new_y = boy_y

        if keys[pygame.K_RIGHT]:
            new_x += boy_speed
        if keys[pygame.K_LEFT]:
            new_x -= boy_speed
        if keys[pygame.K_UP]:
            new_y -= boy_speed
        if keys[pygame.K_DOWN]:
            new_y += boy_speed

        new_rect = pygame.Rect(new_x, new_y, boy_size, boy_size)
        road_rect = pygame.Rect(0, road_y, WIDTH, road_height)

        # ✅ MARKET ENTERABLE NOW
        if (
            road_rect.colliderect(new_rect)
            or home_rect.colliderect(new_rect)
            or friend_rect.colliderect(new_rect)
            or school_rect.colliderect(new_rect)
            or market_rect.colliderect(new_rect)
        ):
            boy_x = new_x
            boy_y = new_y

        boy_rect = pygame.Rect(boy_x, boy_y, boy_size, boy_size)

        # Cars
        for car in cars:
            car.x -= 1
            if car.x < -70:
                car.x = WIDTH
                car.y = random.randint(road_y + 20, road_y + road_height - 60)

            if boy_rect.colliderect(car):
                game_state = "gameover"

        # Obstacles
        for obs in obstacles:
            if boy_rect.colliderect(obs):
                game_state = "gameover"

        current_time = pygame.time.get_ticks()

        # Reaching places
        if boy_rect.colliderect(home_rect):
            location_message = "You reached Home!"
            message_timer = current_time
            if game_state == "returning":
                game_state = "finished"

        if boy_rect.colliderect(friend_rect):
            location_message = "You reached Friend House!"
            message_timer = current_time

        if boy_rect.colliderect(school_rect):
            location_message = "You reached School!"
            message_timer = current_time
            if game_state == "playing":
                game_state = "win"

        if boy_rect.colliderect(market_rect):
            location_message = "You reached Market!"
            message_timer = current_time

    # Draw Road
    pygame.draw.rect(screen, ROAD, (0, road_y, WIDTH, road_height))

    # Buildings
    pygame.draw.rect(screen, BLUE, home_rect)
    pygame.draw.rect(screen, ORANGE, market_rect)
    pygame.draw.rect(screen, BLUE, friend_rect)
    pygame.draw.rect(screen, BLUE, school_rect)

    # Titles
    draw_text("HOME", home_rect.x + 40, home_rect.y - 30)
    draw_text("MARKET", market_rect.x + 40, market_rect.y - 30)
    draw_text("FRIEND HOUSE", friend_rect.x + 20, friend_rect.y - 30)
    draw_text("SCHOOL", school_rect.x + 50, school_rect.y - 30)

    # Cars
    for car in cars:
        pygame.draw.rect(screen, RED, car)

    # Obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, BROWN, obs)

    # Boy
    pygame.draw.rect(screen, WHITE, (boy_x, boy_y, boy_size, boy_size))
    draw_text("BOY", boy_x + 5, boy_y - 20)

    # Location message
    if pygame.time.get_ticks() - message_timer < 2000:
        draw_text(location_message, WIDTH//2 - 150, 60)

    # Win screen
    if game_state == "win":
        draw_text("You Won!", WIDTH//2 - 50, 100)
        draw_text("Press R to Restart", WIDTH//2 - 120, 140)
        draw_text("Press H to Return Home", WIDTH//2 - 160, 180)

    # Finished
    if game_state == "finished":
        draw_text("Journey Completed!", WIDTH//2 - 120, 100)
        draw_text("Press R to Restart Game", WIDTH//2 - 150, 140)

    # Game Over
    if game_state == "gameover":
        draw_text("Game Over! Press R to Restart", WIDTH//2 - 170, 100)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
