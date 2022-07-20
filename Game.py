import os
import random
import sys
import pygame
import time

pygame.init()

s_width = 500
f_width = 100
s_height = 600
f_height = 50
txt_X = 95
txt_Y = 42.5
scr_X = 440
scr_Y = 42.5
regular_font = 'freesansbold.ttf'
window = pygame.display.set_mode((s_width, s_height))
bg = pygame.image.load('Images/bg2.jpg')
closing_bg = pygame.image.load('Images/bg.jpg')
window.blit(bg, (0, 0))
pygame.display.set_caption("Map Game")
char = pygame.image.load('Images/hab.png')
clock = pygame.time.Clock()
all_flags = os.listdir("Flags")
start_time = time.time()
fs = []
char_x = 200
char_y = 510
baseX = 60
baseY = 110
xOffset = [0, 150, 300]
locations = []
flag_vel = 2.5
hab_vel = 5
ttl = 30
left = False
right = False
run = True
text = None
textRect = None
scoreRect = None
scoreText = None
counting_text = None
counting_Rect = None
random_flag = ''
score = 0
rnd = 0
expert = False


class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 90
        self.height = 90
        self.vel = hab_vel
        self.left = False
        self.right = False
        self.hitbox = (self.x + 23, self.y + 8, 45, 70)

    def draw(self, win):
        if self.right:
            win.blit(char, (self.x, self.y))
        else:
            win.blit(char, (self.x, self.y))


# In order to display the correct country
def gen_text():
    global text, textRect, rnd, random_flag
    font = pygame.font.Font(regular_font, 16)
    rnd = random.randint(0, 2)
    random_flag = str(fs[rnd]).replace('.gif', '')
    text = font.render(random_flag, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (txt_X, txt_Y)


# In order to display the score throughout the game
def gen_score():
    global score, scoreText, scoreRect
    font = pygame.font.Font(regular_font, 24)
    scoreText = font.render(str(score), True, (255, 255, 255))
    scoreRect = scoreText.get_rect()
    scoreRect.center = (scr_X, scr_Y)


# In order to display the running clock
def genClock():
    global counting_text, counting_Rect
    font = pygame.font.Font(regular_font, 20)
    counting_minutes = str(00).zfill(2)
    counting_seconds = str(counting_time).zfill(2)
    counting_string = "{}:{}".format(counting_minutes, counting_seconds)
    counting_text = font.render(str(counting_string), True, (255, 255, 255))
    counting_Rect = counting_text.get_rect()
    counting_Rect.center = (285, scr_Y)


# Chooses 3 random flags for each instance
def list_flags():
    global fs
    fs.clear()
    for _ in range(3):
        f = random.choice(all_flags)
        if f:
            if f not in fs:
                fs.append(f)
    gen_text()
    return [pygame.image.load('Flags/' + i) for i in fs]


# Makes the flags appear on screen
def upload_flags():
    global baseX, baseY, locations
    locations.clear()
    baseY = 110
    for flag, x in zip(flags, xOffset):
        locations.append((baseX + x - f_width // 2, baseX + x + f_width // 2))
        window.blit(flag, (baseX + x, baseY))
    pygame.display.update()


# Reloads the list of 3 flags going up on the screen
def reload_flags():
    global flags
    flags.clear()
    flags = list_flags()
    upload_flags()


# In charge of updating the screen every tick for the game
def redraw_game():
    window.blit(bg, (0, 0))
    gen_score()
    genClock()
    if len(random_flag) > 12:
        pygame.draw.rect(window, (120, 120, 120), (20, 20, 200, 40))
        textRect.center = (txt_X + len(random_flag) * 1.2, txt_Y)
    else:
        pygame.draw.rect(window, (120, 120, 120), (20, 20, 150, 40))
    pygame.draw.rect(window, (120, 120, 120), (420, 20, 40, 40))
    pygame.draw.rect(window, (120, 120, 120), (235, 20, 100, 40))
    window.blit(text, textRect)
    window.blit(scoreText, scoreRect)
    window.blit(counting_text, counting_Rect)
    hab.draw(window)
    for flag, x in zip(flags, xOffset):
        window.blit(flag, (baseX + x, baseY))
    pygame.display.update()


# In charge of the closing screen
def game_over():
    font = pygame.font.Font(regular_font, 30)
    game_over_txt = font.render("Game Over", True, (200, 200, 200))
    if score < 10:
        score_display = font.render(f"You knew only {score // 5} flag!", True, (200, 200, 200))
    else:
        score_display = font.render(f"You knew {score // 5} flags!", True, (200, 200, 200))
    window.fill((11, 11, 69))
    window.blit(game_over_txt,
                (s_width / 2 - (game_over_txt.get_width() / 2), s_height / 3 - (game_over_txt.get_height() / 2)))
    window.blit(score_display,
                (s_width / 2 - (score_display.get_width() / 2), s_height / 3 - (score_display.get_height() / 2) + 80))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()
    sys.exit()


hab = player(char_x, char_y)
flags = list_flags()
upload_flags()

# The loop that's in charge of the game
while run:
    clock.tick(45)
    counting_time = ttl - int(time.time() - start_time)     # The time that runs throughout the game
    if not expert and score % 15 == 0 and score != 0:
        expert = True
        flag_vel *= 1.2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Gives you the opportunity to get out of the game
            run = False
    KEYS = pygame.key.get_pressed()

    if KEYS[pygame.K_LEFT] and hab.x > hab.vel:     # When you go left
        hab.x -= hab.vel
        hab.left = True
        hab.right = False
    elif KEYS[pygame.K_RIGHT] and hab.x < s_width - baseX - hab.vel:    # When you go right
        hab.x += hab.vel
        hab.right = True
        hab.left = False
    else:   # When you stay put
        hab.left = False
        hab.right = False
    if baseY < hab.y - hab.height + 54:     # As long as the flag is not near you
        baseY += flag_vel
    else:   # When the flag is on you
        low, high = locations[rnd]
        if hab.x in range(low, high):
            score += 5
        reload_flags()
    if counting_time == 0:      # Time's up!
        run = False
        game_over()
    redraw_game()
