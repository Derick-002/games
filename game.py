import pygame
import sys
import random
import serial

# Initialize Pygame
pygame.init()

# Display
WIDTH, HEIGHT = 500, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Driving Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

# Load assets
car = pygame.image.load("car.png")
car = pygame.transform.scale(car, (90, 150))
car_rect = car.get_rect(center=(WIDTH // 2, HEIGHT - 100))

obstacle_img = pygame.image.load("obstacle1.png")
obstacle_img = pygame.transform.scale(obstacle_img, (100, 80))

road = pygame.image.load("road.png")
road = pygame.transform.scale(road, (WIDTH, HEIGHT))
road_y = 0

# Sounds
collision_sound = pygame.mixer.Sound("collision_sound.wav")
collect_sound = pygame.mixer.Sound("collect_sound.wav")

# Game variables
obstacle_speed = 10
obstacles = []
score = 0
font = pygame.font.Font(None, 36)
spawn_delay = 1500  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# Display functions
def display_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def display_message(text, x, y, color):
    msg = font.render(text, True, color)
    screen.blit(msg, (x, y))

def spawn_obstacle():
    x = random.randint(50, WIDTH - 150)
    y = -80
    return obstacle_img.get_rect(topleft=(x, y))

# Serial setup
try:
    ser = serial.Serial("COM5", 9600)  # Adjust your COM port
except serial.SerialException as se:
    print(f"Error: {se}. Could not connect to Arduino.")
    sys.exit()

# Game loop
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        # Read joystick from Arduino
        joystick_data = ser.readline().decode().strip().split(",")
        if len(joystick_data) == 2:
            joyX = int(joystick_data[0])
            joyY = int(joystick_data[1])

            if not game_over:
                # Move car
                car_rect.move_ip((joyX - 512) / 20, (joyY - 512) / 20)
                car_rect.left = max(0, car_rect.left)
                car_rect.right = min(WIDTH, car_rect.right)
                car_rect.top = max(0, car_rect.top)
                car_rect.bottom = min(HEIGHT, car_rect.bottom)

                # Spawn obstacles
                current_time = pygame.time.get_ticks()
                if current_time - last_spawn_time > spawn_delay:
                    obstacles.append(spawn_obstacle())
                    last_spawn_time = current_time

                # Move obstacles
                for obs in obstacles[:]:
                    obs.move_ip(0, obstacle_speed)
                    if obs.top > HEIGHT:
                        obstacles.remove(obs)
                        score += 1

                # Check collisions
                for obs in obstacles:
                    if car_rect.colliderect(obs):
                        game_over = True
                        collision_sound.play()

            # Draw everything
            road_y = (road_y + 5) % HEIGHT
            screen.blit(road, (0, road_y - HEIGHT))
            screen.blit(road, (0, road_y))
            screen.blit(car, car_rect)
            for obs in obstacles:
                screen.blit(obstacle_img, obs)

            display_score(score)

            if game_over:
                display_message("Game Over! Press 'R' to Restart", 50, 100, RED)

            pygame.display.flip()

        # Restart game
        keys = pygame.key.get_pressed()
        if game_over and keys[pygame.K_r]:
            game_over = False
            car_rect.center = (WIDTH // 2, HEIGHT - 100)
            obstacles.clear()
            score = 0

    except ValueError:
        print("Invalid joystick data received.")
    except Exception as e:
        print(f"Error: {e}")

pygame.quit()
sys.exit()