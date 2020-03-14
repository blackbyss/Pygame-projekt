import pygame
import random
from settings import *
from sprites import *
from os import path
class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)
        self.load_data()
    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.p_spritesheet = P_Spritesheet(path.join(img_dir, P_SPRITESHEET))
        self.background_img = pygame.image.load(path.join(img_dir, 'triangle.png'))
        self.background_img2 = pygame.image.load(path.join(img_dir, 'lagi.png'))
        self.snd_dir = path.join(self.dir, 'sound')
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'jump4.wav'))
        self.death_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'death.wav'))
        
                
        
    def new(self):
         # game reset
        self.score = 0
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat) # *plat = explode list into all of its components
        Background(self)
        Background2(self)
        self.mob_timer = 0
        pygame.mixer.music.load(path.join(self.snd_dir, 'platformer_level04.ogg'))
        self.run()
    def run(self):
        # game loop
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(5)
            
    def update(self):
        # game loop - update
        self.all_sprites.update()
        now = pygame.time.get_ticks()
        # Enemy spawn frequency - increases every 250 points until 3000 points reached
        if self.score < 3000:
            if now - self.mob_timer > MOB_FREQ - (self.score // 250)*500 + random.choice([- 1500, - 1000, -500, 0, 1500, 1000, 500]):
                self.mob_timer = now
                Mob(self)
        else:
            if now - self.mob_timer > MOB_FREQ - 6000 + random.choice([- 1500, - 1000, -500, 0, 1500, 1000, 500]):
                self.mob_timer = now
                Mob(self)
        # Collision checks        
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask)
        if mob_hits:
            self.death_sound.play()
            self.playing = False
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                        
                #if self.player.pos.x <lowest.rect.right and self.player.pos.x > lowest.rect.left:
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 2
                    self.player.vel.y = 0
                    self.player.jumping = False
        # Player movement on screen and sprite movements in relation to player            
        if self.player.rect.left >= WIDTH / 2:
            self.player.pos.x -= abs(self.player.vel.x)
            self.background.x = self.player.pos.x
            for mob in self.mobs:
                mob.rect.x -= abs(self.player.vel.x)
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)
                if plat.rect.left <= 0:
                    plat.rect.x -= 0.7*abs(self.player.vel.x)
                    if plat.rect.right <= 0:
                        plat.kill()
                        self.score += 5
                        
        # Spawns new platforms when less than 8 on screen            
        while len(self.platforms) < 8:
            width = random.randrange(50, 200)
            Platform(self, random.randrange(WIDTH, WIDTH + width + 100), random.randrange(100, 440))

        # Death
        if self.player.rect.bottom  > HEIGHT:
            self.death_sound.play()
            self.playing = False

                
    def events(self):
        # game loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    self.player.super_jump()
                    self.score -= 50
            
    def draw(self):
        # game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pygame.mixer.music.load(path.join(self.snd_dir, 'platformer_level04.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.draw_text("Kassi õudusunenägu", 48, WHITE, WIDTH/2, HEIGHT / 4)
        self.draw_text("Nooltega saab liikuda, tühikuga saab hüpata", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Tühikut erineva pikkusega all hoides saab hüppe kaugust kontrollida", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
        self.draw_text("Left Control võimaldab super hüpet, aga kaotad 50 punkti seda kasutades", 22, WHITE, WIDTH/2, HEIGHT/2 + 80)
        self.draw_text("Vajutage suvalist nuppu, et mängida", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(5)
    def show_go_screen(self):
        # game over/continue
        pygame.mixer.music.load(path.join(self.snd_dir, 'platformer_level04.ogg'))
        pygame.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH/2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Vajutage suvalist nuppu, et uuesti mängida", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New High Score!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'r+') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
                      
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(5)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    waiting = False
                
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pygame.quit()