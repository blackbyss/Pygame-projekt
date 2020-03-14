WIDTH = 960
HEIGHT = 540
FPS = 60
FONT = 'arial'
TITLE = "Platformer"
HS_FILE = "highscore.txt"
SPRITESHEET = "koos leekidega.png"
P_SPRITESHEET = "p_spritesheet.png"
# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5
PLAYER_JUMP = 17
MOB_FREQ = 8000
PLAYER_LAYER = 3
PLATFORM_LAYER = 2
MOB_LAYER = 3
BACKGROUND_LAYER = 1

# starting platforms (x, y, width, height)
PLATFORM_LIST = [(900, 350),
                 (WIDTH / 2 - 50, HEIGHT * 3/4),
                 (125, HEIGHT - 250),
                 (350, 200),
                 (175, 100),
                 (650, 200),
                 (850, 80),
                 (1000, 200)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
