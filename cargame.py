import pygame
from pygame.locals import *
import random
import os
import sys

# For Relative Path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# declaring Size
size = width, height = (800, 900)

road_width = int(width / 1.6)
# Center Yellow Line For Road
roadmark_w = int(width / 80)  # relative co-ordinate

# For Right Lane enemy vehicle
right_lane = width / 2 + road_width / 4
left_lane = width / 2 - road_width / 4

speed = 1

# initialize pygame application with pygame.init()
pygame.init()

# Font settings
font = pygame.font.Font(resource_path('data\\SpeedRush-JRKVB.ttf'), 36)  # You can specify the font file and size here
text_color = (255, 0, 0)  # Red

running = True
paused = False  # Flag to indicate whether the game is paused or not
# set window size
screen = pygame.display.set_mode((size))
# set title
pygame.display.set_caption("Car Dodging Game")
# set background color
screen.fill((60, 220, 0))
# draw graphics


# apply Changes
pygame.display.update()

# Load Images
car = pygame.image.load(resource_path("data\\car.png"))
car_loc = car.get_rect()
# Car Setting on left lane
car_loc.center = left_lane, height * 0.85

# Load Enemy Vehicle
# Load Images
car2 = pygame.image.load(resource_path("data\\car2.png"))
car2_loc = car.get_rect()
# Car Setting on left lane
car2_loc.center = random.choice([right_lane, left_lane]), -200
counter = 0

last_level = 0

# Eventlistener when the user will click the exit button
while running:
    counter += 1
    if not paused and counter % 5000 == 0:
        speed += 0.25
        counter = 0
        print("Current Level:", speed)
    # Locate Enemy Vehicle
    car2_loc[1] += speed

    if car2_loc[1] > height:
        # Randomly Selecting the lane
        car2_loc.center = random.choice([right_lane, left_lane]), -200

    # End Game Logic
    if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 256:  # Check for collision
        game_over_text = font.render(f'GAME OVER! LAST LEVEL: {speed}', True, text_color)
        # print("GAME OVER! YOU LOST!")
        running = False  # End the game loop

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if not paused:  # Only handle events when the game is not paused
            if event.type == KEYDOWN:
                if event.key in [K_a, K_LEFT]:
                    # Check if moving left will keep the car within road boundaries
                    if car_loc.left > width / 2 - road_width / 2 + roadmark_w * 2:
                        car_loc = car_loc.move([-int(road_width / 2), 0])
                if event.key in [K_d, K_RIGHT]:
                    # Check if moving right will keep the car within road boundaries
                    if car_loc.right < width / 2 + road_width / 2 - roadmark_w * 3:
                        car_loc = car_loc.move([int(road_width / 2), 0])
                if event.key == K_SPACE:
                    paused = not paused  # Toggle the pause state

    # road rectangle
    pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_width / 2, 0, road_width, height))
    # center Yellow line
    pygame.draw.rect(screen, (255, 240, 60), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
    # Edge White Lines left
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_width / 2 + roadmark_w * 2, 0, roadmark_w, height))
    # Edge White Lines Right
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_width / 2 - roadmark_w * 3, 0, roadmark_w, height))

    # Blit the text onto the screen
    level_text = font.render('Current Level: {:.2f}'.format(speed), True, text_color)
    screen.blit(level_text, (10, 10))  # Position of Level Up text

    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)
    # If game is paused, display a pause message
    if paused:
        pause_text = font.render('Paused', True, text_color)
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))
        pygame.display.update()  # Update the display after blitting pause text to show it immediately
        while paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    paused = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    paused = False

    # apply Changes
    pygame.display.update()

# Blit the game over text onto the screen
screen.blit(game_over_text, (10, 50))  # Position of Game Over text
pygame.display.update()

# Pause for a moment before quitting
pygame.time.delay(5000)

# for collapsing the pygame window
pygame.quit()
