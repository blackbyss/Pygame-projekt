import pygame
from settings import *
vec = pygame.math.Vector2
import random
class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def load_images(self):
        self.standing_frames_og =[self.game.spritesheet.get_image(1737, 155, 52, 44)]

        self.standing_frames = []
        for frame in self.standing_frames_og:
            self.standing_frames.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey(BLACK)
        self.walk_frames_l = [self.game.spritesheet.get_image(777, 217, 63, 30),
                              self.game.spritesheet.get_image(1537, 211, 48, 35),
                              self.game.spritesheet.get_image(1477, 211, 58, 35)]

        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            self.walk_frames_r.append(pygame.transform.flip(frame, True, False))
        self.jump_frames_l = [self.game.spritesheet.get_image(1026, 213, 85, 33)]
                              
        self.jump_frames_r = []
        for frame in self.jump_frames_l:
            frame.set_colorkey(BLACK)
            self.jump_frames_r.append(pygame.transform.flip(frame, True, False))
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def super_jump(self):
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = - 1.5 * PLAYER_JUMP
            
            
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = - PLAYER_JUMP
        
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.2:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # keep character in the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos
        
    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0 and self.vel.y == 0:
            self.walking = True
            self.jumping = False
        elif self.vel.x != 0 and self.vel.y != 0:
            self.walking = False
            self.jumping = True
        elif self.vel.y != 0 and self.vel.x == 0:
            self.jumping = True
            self.walking = False
        elif self.vel.y == 0 and self.vel.x == 0:
            self.jumping = False
            self.walking = False
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if self.jumping:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_r)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jump_frames_r[self.current_frame]
                else:
                    self.image = self.jump_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)
        
class Background(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = BACKGROUND_LAYER
        self.groups = game.all_sprites, game.background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.background_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 0
        self.rect.y = 0
        
class Background2(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = BACKGROUND_LAYER
        self.groups = game.all_sprites, game.background
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.background_img2
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = 0
        self.rect.y = 480


            
class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.p_spritesheet.get_image(7, 7, 161, 42),
                  self.game.p_spritesheet.get_image(452, 7, 224, 41),
                  self.game.p_spritesheet.get_image(690, 7, 192, 41),
                  self.game.p_spritesheet.get_image(896, 7, 128, 41),
                  self.game.p_spritesheet.get_image(182, 7, 256, 41),
                  self.game.p_spritesheet.get_image(7, 7, 161, 42),
                  self.game.p_spritesheet.get_image(452, 7, 224, 41),
                  self.game.p_spritesheet.get_image(690, 7, 192, 41),
                  self.game.p_spritesheet.get_image(896, 7, 128, 41)]
        
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
class Mob(pygame.sprite.Sprite):
    
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_image()
        self.image_up_r = self.f_frames_r[0]
        self.image_up_r.set_colorkey(BLACK)
        self.image_down_r = self.f_frames_r[1]
        self.image_down_r.set_colorkey(BLACK)
        self.image_up_l = self.f_frames_l[0]
        self.image_up_l.set_colorkey(BLACK)
        self.image_down_l = self.f_frames_l[1]
        self.image_down_l.set_colorkey(BLACK)
        self.image = self.f_frames_r[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.vx = random.randrange(6, 10)
        if self.rect.centerx > WIDTH:
            self.vx *= (-0.1 * random.randrange(3, 6))
        self.rect.y = random.randrange(100, 520)
        self.vy = 0
        self.dy = 0.5
        
    def load_image(self):
        self.f_frames_og = [self.game.spritesheet.get_image(1866, 206, 26, 41),
                            self.game.spritesheet.get_image(1830, 213, 25, 33)]
        self.f_frames_r = []
        for frame in self.f_frames_og:
            self.f_frames_r.append(pygame.transform.rotate(frame, 90))
            frame.set_colorkey(BLACK)
        self.f_frames_l = []
        for frame in self.f_frames_r:
            self.f_frames_l.append(pygame.transform.flip(frame, True, False))
            frame.set_colorkey(BLACK)    
        
        
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 2 or self.vy < -2:
            self.dy *= -1
        center = self.rect.center
        if self.vx > 0:
            if self.dy < 0:
                self.image = self.image_up_r
            else:
                self.image = self.image_down_r
        else:
            if self.dy < 0:
                self.image = self.image_up_l
            else:
                self.image = self.image_down_l
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left  > WIDTH + 100 or self.rect.right < -100:
            self.kill()
            
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #image = pygame.transform.scale(image, (width//2, height//2))
        return image
class P_Spritesheet:
    def __init__(self, filename):
        self.p_spritesheet = pygame.image.load(filename).convert()
        
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.p_spritesheet, (0, 0), (x, y, width, height))
        #image = pygame.transform.scale(image, (width//2, height//2))
        return image


        
        
        
        