#Importing Libaries
import pygame
import os
import random

screen_width = 850
screen_height = 700

pygame.init()
pygame.mixer.init()
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shoot Them Up')

FPS = 60
clock = pygame.time.Clock()

#Music
def background_music():
    pygame.mixer.music.load(os.path.join('Songs', 'background_music_2.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

player_laser_music = pygame.mixer.Sound(os.path.join('Songs', 'player_laser.wav'))
enemy_laser_music = pygame.mixer.Sound(os.path.join('Songs', 'enemy_laser.wav'))
player_spaceship_destroyed_music = pygame.mixer.Sound(os.path.join('Songs', 'Blast.wav'))

#Score
font = pygame.font.SysFont('Helvatica', 40, True, True)
title_font = pygame.font.SysFont("Helvatica", 70)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y, player_img, laser_img, sprite_list, laser_list, level):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = player_img
        self.rect = self.image.get_rect()
        self.laser_img = laser_img
        self.sprites = sprite_list
        self.player_lasers = laser_list
        self.radius = 25
        self.rect.centerx = screen_width //2
        self.rect.bottom = screen_height - 50
        self.velocity = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100
        self.shield = False
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.visible = True
        self.invisible_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.protection_time = pygame.time.get_ticks()
        self.level = level

    def update(self):
        time = pygame.time.get_ticks()
        if self.visible == False and time - self.invisible_timer > 1000:    
            self.visible = True
            self.rect.centerx = screen_width // 2 
            self.rect.bottom = screen_height - 10
        if self.visible == True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.rect.x += self.velocity
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.rect.x -= self.velocity
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.rect.y -= self.velocity
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.rect.y += self.velocity
            if keys[pygame.K_SPACE]:
                self.shoot()

            if self.rect.right > screen_width - 20:
                self.rect.right = screen_width - 20
            if self.rect.left < 10:
                self.rect.left = 10
            if self.rect.top < 250:
                self.rect.top = 250
            if self.rect.bottom > screen_height - 50:
                self.rect.bottom = screen_height - 50

    def shoot(self):
        player_laser_music.play()

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                    laser_beam = Laser(self.rect.centerx, self.rect.top + 10, -10, self.laser_img)
                    self.sprites.add(laser_beam)
                    self.player_lasers.add(laser_beam)
            if self.power == 2:
                    laser_beam1 = Laser(self.rect.left + 10, self.rect.top + 25, -10, self.laser_img)
                    laser_beam2 = Laser(self.rect.right - 10, self.rect.top + 25, -10, self.laser_img)
                    self.sprites.add(laser_beam1)
                    self.sprites.add(laser_beam2)
                    self.player_lasers.add(laser_beam1)
                    self.player_lasers.add(laser_beam2)
            if self.power == 3:
                    laser_beam1 = Laser(self.rect.left + 10, self.rect.top + 25, -20, self.laser_img)
                    laser_beam2 = Laser(self.rect.right - 10, self.rect.top + 25, -20, self.laser_img)
                    self.sprites.add(laser_beam1)
                    self.sprites.add(laser_beam2)
                    self.player_lasers.add(laser_beam1)
                    self.player_lasers.add(laser_beam2)
            if self.power >= 4:
                    laser_beam = Laser(self.rect.centerx, self.rect.top + 10, -20, self.laser_img)
                    laser_beam1 = Laser(self.rect.left + 10, self.rect.top + 25, -20, self.laser_img)
                    laser_beam2 = Laser(self.rect.right - 10, self.rect.top + 25, -20, self.laser_img)
                    self.sprites.add(laser_beam)
                    self.sprites.add(laser_beam1)
                    self.sprites.add(laser_beam2)
                    self.player_lasers.add(laser_beam)
                    self.player_lasers.add(laser_beam1)
                    self.player_lasers.add(laser_beam2)
    def hide(self):
        self.visible = False
        self.invisible_timer = pygame.time.get_ticks()
        self.rect.center = (screen_width + 200, screen_height + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
         
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, laser_img,sprite_list,enemy_laser_list,enemy_type, villian_entry):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = enemy_img
        self.image_original.set_colorkey((0,0,0))
        self.image = self.image_original.copy()
        self.sprites = sprite_list
        self.enemy_lasers = enemy_laser_list
        self.entry = villian_entry
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.laser_img = laser_img
        self.radius = 34
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-1500,-100)
        self.velocity = random.randrange(1,6)
        self.velocity = 2
        self.rotate = 0
        self.rotation_velocity = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.type = enemy_type

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y < screen_height and self.rect.y > -25:
            self.shoot()
        if self.entry == True:
            if self.rect.y > screen_height + 50:
                self.rect.x = random.randrange(10,screen_width)
                self.rect.y = random.randrange(-500,-100)
        
    def shoot(self):
        enemy_laser_music.play()
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            if self.type == 1:
                laser_beam = Laser(self.rect.centerx, self.rect.top + 105, 10, self.laser_img)
                self.sprites.add(laser_beam)
                self.enemy_lasers.add(laser_beam)

            elif self.type == 2:
                laser_beam1 = Laser(self.rect.centerx + 5, self.rect.top + 135,8,self.laser_img)
                laser_beam2 = Laser(self.rect.centerx -5 , self.rect.top + 135,8,self.laser_img)
                self.sprites.add(laser_beam1)
                self.sprites.add(laser_beam2)
                self.enemy_lasers.add(laser_beam1)
                self.enemy_lasers.add(laser_beam2)

            elif self.type == 3:
                laser_beam1 = Laser(self.rect.left + 10, self.rect.bottom + 40,7,self.laser_img)
                laser_beam2 = Laser(self.rect.right - 10, self.rect.bottom + 40,7,self.laser_img)
                self.sprites.add(laser_beam1)
                self.sprites.add(laser_beam2)
                self.enemy_lasers.add(laser_beam1)
                self.enemy_lasers.add(laser_beam2)

            elif self.type == 4:
                vel = random.randint(6,10)
                laser_beam1 = Laser(self.rect.centerx , self.rect.top + 135,7,self.laser_img)
                laser_beam2 = Laser(self.rect.left + 10 , self.rect.top + 135,7,self.laser_img)
                laser_beam3 = Laser(self.rect.right - 10 , self.rect.top + 135,7,self.laser_img)

                self.sprites.add(laser_beam1)
                self.sprites.add(laser_beam2)
                self.sprites.add(laser_beam3)
                self.enemy_lasers.add(laser_beam1)
                self.enemy_lasers.add(laser_beam2)
                self.enemy_lasers.add(laser_beam3)

            elif self.type == 5:
                laser_beam = Laser(self.rect.centerx, self.rect.top + 135, 10, self.laser_img)
                self.sprites.add(laser_beam)
                self.enemy_lasers.add(laser_beam)
            
            elif self.type == 6:
                laser_beam1 = Laser(self.rect.left + 10, self.rect.bottom + 50,10,self.laser_img)
                laser_beam2 = Laser(self.rect.right - 10, self.rect.bottom + 50,10,self.laser_img)
                self.sprites.add(laser_beam1)
                self.sprites.add(laser_beam2)
                self.enemy_lasers.add(laser_beam1)
                self.enemy_lasers.add(laser_beam2)

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, laser_img,sprite_list,enemy_laser_list,enemy_type, villian_entry, laser_blast,level):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey((255,255,255))
        self.sprites = sprite_list
        self.enemy_lasers = enemy_laser_list
        self.entry = villian_entry
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.laser_img = laser_img
        self.laser_blast = laser_blast
        self.level = level
        self.radius = 34
        self.rect.centerx = screen_width//2
        self.rect.y = -500
        self.velocity = random.randrange(2,5)
        self.speed = 5
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.laser_shot = pygame.time.get_ticks()
        self.laser_shot_timer = pygame.time.get_ticks()
        self.type = enemy_type
        self.health = 100
        self.shoot_now = False
        self.timer = pygame.time.get_ticks()
        self.position_change = False
        self.final_timer = pygame.time.get_ticks()
        self.done = False

    def update(self):
        if self.rect.y <= 80:
            self.rect.y += self.velocity
        if self.rect.y < screen_height and self.rect.y > -25:
            self.shoot()

        if self.type == 1:
            initial_timer = pygame.time.get_ticks()
            if initial_timer - self.timer > 5000:
                self.timer = initial_timer
                self.position_change = True
            if self.position_change == True:
                if self.rect.y >= 82:
                    if self.rect.left <= 10:
                        self.velocity = -4
                    elif self.rect.right >= screen_width - 10:
                        self.velocity = 4
                    self.rect.x -= self.velocity
                    if self.rect.left <= 10 or self.rect.right >= screen_width - 10 or self.rect.x == 325:
                        self.position_change = False
        
        if self.type == 2:
            initial_timer = pygame.time.get_ticks()
            if initial_timer - self.timer > 5000:
                self.timer = initial_timer
                self.position_change = True
            if self.position_change == True:
                if self.rect.y >= 82:
                    if self.rect.left <= 10:
                        self.velocity = 4
                    elif self.rect.right >= screen_width - 10:
                        self.velocity = -4
                    self.rect.x += self.velocity
                    if self.rect.left <= 10 or self.rect.right >= screen_width - 10 or self.rect.x == 325:
                        self.position_change = False

        if self.type == 3:
            one_last_coundown = pygame.time.get_ticks()
            if one_last_coundown - self.final_timer > 5000:
                self.done = True
            if self.done == True:
                if self.rect.x == 300:
                    if self.rect.bottom > screen_height + 10:
                        self.velocity = -10
                    if self.rect.top < 80:
                        self.velocity = 10 
                    self.rect.y += self.velocity                    

    def shoot(self):
        enemy_laser_music.play()
        now = pygame.time.get_ticks()
        timer_now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            
            laser_beam = Laser(self.rect.centerx, self.rect.bottom , 10, self.laser_img)
            self.sprites.add(laser_beam)
            self.enemy_lasers.add(laser_beam)

            if timer_now - self.laser_shot_timer > 2000:
                self.shoot_now = True
                self.laser_shot_timer = timer_now

                if self.shoot_now == True:
                    right_now = pygame.time.get_ticks()
                    self.last_shot = right_now
                    laser_beam1 = Laser(self.rect.left + 50, self.rect.bottom + 60,10,self.laser_blast)
                    laser_beam2 = Laser(self.rect.right - 50, self.rect.bottom + 60,10,self.laser_blast)
                    laser_beam3 = Laser(self.rect.left + 50, self.rect.bottom + 40,10,self.laser_blast)
                    laser_beam4 = Laser(self.rect.right - 50, self.rect.bottom + 40,10,self.laser_blast)
                    laser_beam5 = Laser(self.rect.left + 50, self.rect.bottom + 20,10,self.laser_blast)
                    laser_beam6 = Laser(self.rect.right - 50, self.rect.bottom + 20,10,self.laser_blast)
                    self.sprites.add(laser_beam1)
                    self.sprites.add(laser_beam2)
                    self.sprites.add(laser_beam3)
                    self.sprites.add(laser_beam4)
                    self.sprites.add(laser_beam5)
                    self.sprites.add(laser_beam6)
                    self.enemy_lasers.add(laser_beam1)
                    self.enemy_lasers.add(laser_beam2)
                    self.enemy_lasers.add(laser_beam3)
                    self.enemy_lasers.add(laser_beam4)
                    self.enemy_lasers.add(laser_beam5)
                    self.enemy_lasers.add(laser_beam6)
                    self.shoot_now = False

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, img,level):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(img)
        self.image_original.set_colorkey((0,0,0))
        self.image = self.image_original.copy()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.radius = 34
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-1500,-100)
        self.speed_x = random.randrange(-1,1)
        self.velocity = random.randrange(4,8)
        self.velocity = 5
        self.rotate = 0
        self.level = level
        self.rotation_velocity = random.randrange(-10,10)
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def rotation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotate = (self.rotate + self.rotation_velocity) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rotate)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
              
    def update(self):
        if self.level < 5:
            self.rotation()
            self.rect.x += self.speed_x
        self.rect.y += self.velocity

        if self.rect.y > screen_height + 50:
            self.rect.y = random.randrange(-1500,-100)
            self.rect.x = random.randrange(0,screen_width)
                 
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, laser_img):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.bottom = self.y
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size,explosion_animation):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.animation_img = explosion_animation
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.animation_img[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.animation_img[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center, powerup_imgs):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.images = powerup_imgs
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.velocity = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top > screen_height:
            self.kill()

class HealthBooster(pygame.sprite.Sprite):
    def __init__(self, center, health_booster_image):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'health_booster'
        self.image = health_booster_image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.velocity = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top > screen_height:
            self.kill()

def draw_lives(x,y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        game_window.blit(img, img_rect)

def draw_shield_bar(x,y,health):
    if health <= 0:
        pygame.draw.rect(game_window, (255,0,0),(10,10,x,y))
    else:
        pygame.draw.rect(game_window, (255,0,0),(10,10,x,y))
        pygame.draw.rect(game_window, (0,255,0),(10,10,(health/100) * (x) ,y))
    
def draw_enemy_shield_bar(health):
    if health > 0:
        pygame.draw.rect(game_window,(0,255,0),(screen_width - (screen_width//4) - 20,10,screen_width//4 + 10  ,35))
        pygame.draw.rect(game_window,(255,0,0),(screen_width - (screen_width//4) - 20,10,(screen_width//4 + 10) - ((health/100)*(screen_width//4 + 10)) ,35))

def draw_enemy_health_bar(health,bigenemy):
    if health > 0:
        pygame.draw.rect(game_window,(0,255,0),(bigenemy.rect.x, bigenemy.rect.top - 15, 200 - ((200/100)*(100-health)), 15))
    
def level_bar(level,number_of_obstacles,hit):
    if level == 0:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 1:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 2:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 3:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 4:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 5:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

    if level == 6:
        x = screen_width//4 + 50
        if hit <= number_of_obstacles + 20:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,40,(hit/(number_of_obstacles+20)) * x  ,30))
        else:
            pygame.draw.rect(game_window,(0,255,255),(screen_width//2 - 100,30,x  ,30))

def main_screen(win='Begin'):
    if win == False:
        background_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'main.png')),(screen_width,screen_height))
        title_label = title_font.render("Press Enter to begin...", 1, (0,255,0))

    elif win == True:
        background_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'win.png')),(screen_width,screen_height))
        title_label = title_font.render(".", 1, (0,0,0))
    else:
        background_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'lose.png')),(screen_width,screen_height))
        title_label = title_font.render(".", 1, (0,0,0))

    background_img_rect = background_img.get_rect()

    game_window.blit(background_img, background_img_rect)
    game_window.blit(title_label, (screen_width/2 - title_label.get_width()/2, 350))
    
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
                waiting = False
                background_music()

# Game loop
def game_loop():
    timer = pygame.time.get_ticks()

    #Image
    background_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.jpg')),(screen_width,screen_height))
    background_img_rect = background_img.get_rect()

    win_img = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'win.png')),(screen_width,screen_height))
    win_img_rect = win_img.get_rect()

    player_img = pygame.image.load(os.path.join('Assets','space_shuttle.png'))
    shielded_img = pygame.image.load(os.path.join('Assets','shielded.png'))

    enemy_spaceship_img1 = []
    enemy_spaceship_img1a = pygame.image.load(os.path.join('Assets','enemy1a.png'))
    enemy_spaceship_img1b = pygame.image.load(os.path.join('Assets','enemy1b.png'))
    enemy_spaceship_img1c = pygame.image.load(os.path.join('Assets','enemy1c.png'))
    enemy_spaceship_img1d = pygame.image.load(os.path.join('Assets','enemy1d.png'))
    enemy_spaceship_img1.append(enemy_spaceship_img1a)
    enemy_spaceship_img1.append(enemy_spaceship_img1b)
    enemy_spaceship_img1.append(enemy_spaceship_img1c)
    enemy_spaceship_img1.append(enemy_spaceship_img1d)

    enemy_spaceship_img2 = pygame.image.load(os.path.join('Assets','enemy4.png'))
    enemy_spaceship_img3 = pygame.image.load(os.path.join('Assets','spaceship.png'))

    miniature_enemy_spaceship_img = []
    miniature_enemy_spaceship_img1 = pygame.image.load(os.path.join('Assets','enemy3.png'))
    miniature_enemy_spaceship_img2 = pygame.image.load(os.path.join('Assets','enemy6.png'))
    miniature_enemy_spaceship_img.append(miniature_enemy_spaceship_img1)
    miniature_enemy_spaceship_img.append(miniature_enemy_spaceship_img2)

    enemy_bigspaceship_img1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','bigenemy1.png')),(200,200))
    enemy_bigspaceship_img2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets','bigenemy2.png')),(250,250))

    laser_red = pygame.image.load(os.path.join('Assets','laser_red.png'))
    
    enemy_laser_red = pygame.image.load(os.path.join('Assets','pixel_laser_red.png'))
    enemy_laser_blue = pygame.image.load(os.path.join('Assets','laser_blue.png'))
    enemy_laser_blue1 = pygame.image.load(os.path.join('Assets','laserBlue01.png'))
    enemy_laser_green = pygame.image.load(os.path.join('Assets','laser_green.png'))
    enemy_laser_powerful = pygame.image.load(os.path.join('Assets','pixel_laser_blue.png'))
    
    big_enemy1_laser = pygame.transform.scale(pygame.image.load(os.path.join('Assets','laser_purple.png')),(80,100))
    big_enemy1_laser_blast = pygame.image.load(os.path.join('Assets','bigenemy1_laser.png'))
    big_enemy2_laser_blast = pygame.image.load(os.path.join('Assets','bigenemy2_laser.png'))
    
    explosion_animation = {}
    explosion_animation['large'] = []
    explosion_animation['small'] = []
    explosion_animation['ship'] = []
    explosion_animation['stone'] = []
    
    player_mini_img = pygame.transform.scale(player_img,(50,50))

    asteroid_images = []
    meteor_images = []

    for i in range(1,7):
        filename = 'meteor{}.png'.format(i)
        img = pygame.image.load(os.path.join('Assets', filename)).convert()
        asteroid_images.append(img)

    for i in range(1,5):
        filename = 'asteroid{}.png'.format(i)
        img = pygame.image.load(os.path.join('Assets', filename)).convert()
        meteor_images.append(img)

    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(os.path.join('Assets', filename)).convert_alpha()
        image_lg = pygame.transform.scale(img, (75, 75))
        explosion_animation['large'].append(image_lg)
        image_sm = pygame.transform.scale(img, (45, 45))
        explosion_animation['small'].append(image_sm)
        
    for i in range(10):
        filename = 'ship_explosion0{}.png'.format(i)
        img = pygame.image.load(os.path.join('Assets', filename))
        image_ship = pygame.transform.scale(img, (100,100))
        explosion_animation['ship'].append(img)


    for i in range(4):
        filename = 'explosion0{}.png'.format(i)
        img = pygame.image.load(os.path.join('Assets', filename))
        image_ship = pygame.transform.scale(img, (15,15))
        explosion_animation['stone'].append(img)
          
    powerup_imgs = {}
    powerup_imgs['shield'] = pygame.image.load(os.path.join('Assets','shield_gold.png'))
    powerup_imgs['gun'] = pygame.image.load(os.path.join('Assets','bolt_gold.png'))

    health_booster_image = pygame.image.load(os.path.join('Assets','shield_silver.png'))

    run = True
    game_over = True

    level = 0

    asteriod_hit = 0
    villian_hit = 0

    villian_entry = True

    range_of_asteriods = 25
    range_of_enemies = 0
               
    asteriod_flag = True

    level0_entry_asteriod = True
    level1_entry_enemy = True
    level2_entry_enemy = True
    level3_entry_enemy = True
    level4_entry_asteriod = True
    level5_entry_asteriod = True
    level5_entry_enemy = True
    level6_entry_enemy = True
    level6_entry_bigenemy = True

    number_of_obstacles = 25
    obstacle_hit = 0
    hit_flag = True

    score = 0
    while run:
        
        if game_over:
            main_screen(False)
            game_over = False
            all_sprites = pygame.sprite.Group()
            asteriods = pygame.sprite.Group()
            villians = pygame.sprite.Group()
            big_enemy = pygame.sprite.Group()
            big_enemy1 = pygame.sprite.Group()
            big_enemy2 = pygame.sprite.Group()
            player_lasers = pygame.sprite.Group()
            villian_lasers = pygame.sprite.Group()
            player_explosions = pygame.sprite.Group()
            health = pygame.sprite.Group()
            powerups = pygame.sprite.Group()

            player = Player(screen_width // 2, screen_height - 50, player_img, laser_red, all_sprites, player_lasers,level)
            all_sprites.add(player)
    
            
            score = 0
            level = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        all_sprites.update()

        if villian_entry == False:
            for villian in villians:
                    if villian.rect.y > screen_height:
                        villians.remove(villian)
                        all_sprites.remove(villian)

        hits = pygame.sprite.groupcollide(player_lasers,villians,True, True, pygame.sprite.collide_mask)
        for hit in hits:
            score += 1
            villian_hit += 1
            obstacle_hit += 1
            explosion = Explosion(hit.rect.center, 'large', explosion_animation)
            all_sprites.add(explosion)
            if level > 1:
                if random.random() > 0.7:
                    pow = Powerup(hit.rect.center, powerup_imgs)
                    all_sprites.add(pow)
                    powerups.add(pow)
            if random.random() > 0.5:
                health_booster = HealthBooster(hit.rect.center,health_booster_image)
                all_sprites.add(health_booster)
                powerups.add(health_booster)

        hits = pygame.sprite.groupcollide(player_lasers,asteriods,True, True, pygame.sprite.collide_mask)
        for hit in hits:
            score += 1
            asteriod_hit += 1
            if asteriod_hit <= range_of_asteriods:
                obstacle_hit += 1
            if level == 4:
                explosion = Explosion(hit.rect.center, 'stone', explosion_animation)
            else:
                explosion = Explosion(hit.rect.center, 'large', explosion_animation)
            all_sprites.add(explosion)
            if asteriod_flag == True:
                if level == 3 or level == 4:
                    asteriod = Asteroids(meteor_images,level)
                elif level <3: 
                    asteriod = Asteroids(asteroid_images,level)
                elif level == 5:
                    asteriod = Asteroids(miniature_enemy_spaceship_img,level)

                all_sprites.add(asteriod)
                asteriods.add(asteriod)
            if level > 0:
                if random.random() > 0.7:
                    pow = Powerup(hit.rect.center, powerup_imgs)
                    all_sprites.add(pow)
                    powerups.add(pow)
            if random.random() > 0.5:
                health_booster = HealthBooster(hit.rect.center,health_booster_image)
                all_sprites.add(health_booster)
                powerups.add(health_booster)

        hits = pygame.sprite.spritecollide(player,powerups,True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield = True
            if hit.type == 'gun':
                player.powerup()
            if hit.type == 'health_booster':
                player.health += 20
                if player.health >= 100:
                    player.health = 100

        if player.shield == True:
            time_now = pygame.time.get_ticks()
            player.image = shielded_img
            
            if time_now - player.protection_time  > 5000:
                player.protection_time = time_now
                player.shield = False
        
        if player.shield == False:
            player.image = player_img

        hits = pygame.sprite.spritecollide(player,villian_lasers,True,pygame.sprite.collide_mask)
        for hit in hits:
            if player.shield == False:
                player.health -= 20
                explosion = Explosion(hit.rect.center, 'large', explosion_animation)
                all_sprites.add(explosion)
                if player.health <= 0:
                    player_spaceship_destroyed_music.play()
    
                    death_explosion = Explosion(player.rect.center, 'ship', explosion_animation)
                    player_explosions.add(death_explosion)
                    all_sprites.add(death_explosion)
                    player.hide()
                    if player.lives > 0 :
                        player.lives -= 1
                        player.power = 1

                    player.health = 100

        hits = pygame.sprite.spritecollide(player,villians,True,pygame.sprite.collide_mask)
        for hit in hits:
            death_explosion = Explosion(player.rect.center, 'ship', explosion_animation)
            player_explosions.add(death_explosion)
            all_sprites.add(death_explosion)
            if player.shield == False:
                player.health = 0
                player_spaceship_destroyed_music.play()
                
                if player.lives > 0:
                    player.hide()
                    player.lives -= 1
                    player.health = 100
                    player.power = 1    

        hits = pygame.sprite.spritecollide(player,asteriods,True,pygame.sprite.collide_mask)
        for hit in hits:
            score += 1
            if player.shield == False:
                exp = Explosion(hit.rect.center, 'small', explosion_animation)
                all_sprites.add(exp)
                player.health -= 20
                if asteriod_flag == True:
                    if level == 3 or level == 4:
                        asteriod = Asteroids(meteor_images,level)
                    elif level < 3:
                        asteriod = Asteroids(asteroid_images,level)
                    elif level == 5:
                        asteriod = Asteroids(miniature_enemy_spaceship_img,level)

                    all_sprites.add(asteriod)
                    asteriods.add(asteriod)

            if player.health == 0:
                player_spaceship_destroyed_music.play()
               
                death_explosion = Explosion(player.rect.center, 'ship', explosion_animation)
                player_explosions.add(death_explosion)
                all_sprites.add(death_explosion)
                if player.lives > 0:
                    player.hide()
                    player.lives -= 1
                    player.health = 100
                    player.power = 1
    
        hits = pygame.sprite.groupcollide(big_enemy1,player_lasers,False, True, pygame.sprite.collide_mask)
        for hit in hits:
            score += 1
            if bigenemy1.health > 0:
                bigenemy1.health -= 2
                explosion = Explosion(bigenemy1.rect.center, 'large', explosion_animation)
                all_sprites.add(explosion)
            else:    
                explosion = Explosion(bigenemy1.rect.center, 'ship', explosion_animation)
                all_sprites.add(explosion)
                
                big_enemy1.remove(bigenemy1)
                all_sprites.remove(bigenemy1)
                for enemy in big_enemy1:
                    big_enemy1.remove(enemy)

        hits = pygame.sprite.groupcollide(big_enemy2,player_lasers,False, True, pygame.sprite.collide_mask)
        for hit in hits:
            score += 1

            if bigenemy2.health > 0:
                bigenemy2.health -= 4
                explosion = Explosion(bigenemy2.rect.center, 'large', explosion_animation)
                all_sprites.add(explosion)
            else:    
                explosion = Explosion(bigenemy2.rect.center, 'ship', explosion_animation)
                all_sprites.add(explosion)
        
                big_enemy.remove(bigenemy2)
                all_sprites.remove(bigenemy2)
                for enemy in big_enemy2:
                    big_enemy2.remove(enemy)

        hits = pygame.sprite.groupcollide(big_enemy,player_lasers,False, True, pygame.sprite.collide_mask)
        for hit in hits:
            score += 1
            if bigenemy.health > 0:
                bigenemy.health -= 2
                explosion = Explosion(bigenemy.rect.center, 'large', explosion_animation)
                all_sprites.add(explosion)
                
            else :
                explosion = Explosion(bigenemy.rect.center, 'ship', explosion_animation)
                all_sprites.add(explosion)

                big_enemy.remove(bigenemy)
                all_sprites.remove(bigenemy)
    
        if player.lives == 0 :
            player.kill()
            player.health = 0
            if len(player_explosions) == 0:
                player_spaceship_destroyed_music.play()
                main_screen()
            
        if level == 0:
            range_of_asteriods = 25
            number_of_obstacles = range_of_asteriods

            if level0_entry_asteriod == True:
                for asteriod in range(range_of_asteriods):
                    asteriod = Asteroids(asteroid_images,level)
                    asteriods.add(asteriod)
                    all_sprites.add(asteriod)
                asteriod_flag = True
                level0_entry_asteriod = False

            if asteriod_hit > range_of_asteriods:
                if asteriod.rect.y > screen_height:
                        asteriods.remove(asteriod)
                        all_sprites.remove(asteriod)
                asteriod_flag = False
                if len(asteriods) == 0:
                    level = 1
                    asteriod_hit = 0
                    villian_hit = 0
                    obstacle_hit = 0

        if level == 1:
            range_of_enemies = 20
            number_of_obstacles = range_of_enemies

            if level1_entry_enemy == True:
                for villian in range(range_of_enemies):
                    villian = Enemy(enemy_spaceship_img2, enemy_laser_blue1, all_sprites, villian_lasers,1,villian_entry)
                    villians.add(villian)
                    all_sprites.add(villian)
                level1_entry_enemy = False

            if villian_hit > range_of_enemies:
                villian_entry = False
                hit_flag = False
            
            if len(villians) == 0:
                level = 2
                asteriod_hit = 0
                villian_hit = 0
                obstacle_hit = 0

        if level == 2:
            range_of_enemies = 20
            number_of_obstacles = range_of_enemies

            if level2_entry_enemy == True:
                for villian in range(range_of_enemies):
                    img = random.choice(enemy_spaceship_img1)
                    if img == enemy_spaceship_img1a or img == enemy_spaceship_img1b:
                        villian = Enemy(img, enemy_laser_blue, all_sprites, villian_lasers,2,villian_entry)
                    else:
                        villian = Enemy(img, enemy_laser_green, all_sprites, villian_lasers,2,villian_entry)
                                
                    villians.add(villian)
                    all_sprites.add(villian)
                level2_entry_enemy= False

            if villian_hit > 30:
                villian_entry = False
                hit_flag = False
            if len(villians) == 0:
                level = 3
                asteriod_hit = 0
                villian_hit = 0
                obstacle_hit = 0

        if level == 3:
            range_of_enemies = 30
            number_of_obstacles = range_of_enemies

            if level3_entry_enemy == True:
                for villian in range(range_of_enemies):
                    enemy_type = random.choice([5,6])
                    villian = Enemy(enemy_spaceship_img3, enemy_laser_red, all_sprites, villian_lasers,enemy_type,villian_entry)                                    
                    villians.add(villian)
                    all_sprites.add(villian)
                level3_entry_enemy = False

            if villian_hit > range_of_enemies:
                villian_entry = False
                hit_flag = False
            
            if len(villians) == 0:
                level = 4
                asteriod_hit = 0
                villian_hit = 0
                obstacle_hit = 0

        if level == 4:
            range_of_asteriods = 50
            number_of_obstacles = range_of_asteriods

            if level4_entry_asteriod == True:
                for asteriod in range(range_of_asteriods):
                    asteriod = Asteroids(meteor_images,level)
                    asteriods.add(asteriod)
                    all_sprites.add(asteriod)
                level4_entry_asteriod = False

            if asteriod_hit > range_of_asteriods:
                if asteriod.rect.y > screen_height:
                    asteriods.remove(asteriod)
                    all_sprites.remove(asteriod)
                asteriod_flag = False
            if len(asteriods) == 0:
                level = 5
                for enemy in villians:
                    villians.remove(enemy)
                    all_sprites.remove(enemy)
                for laser in villian_lasers:
                    villian_lasers.remove(laser)
                    all_sprites.remove(laser)
            
                asteriod_hit = 0
                villian_hit = 0
                obstacle_hit = 0

        if level == 5:
            range_of_asteriods = 50
            number_of_obstacles = range_of_asteriods

            if level5_entry_asteriod == True:
                for asteriod in range(range_of_asteriods):
                    asteriod = Asteroids(miniature_enemy_spaceship_img,level)
                    asteriods.add(asteriod)
                    all_sprites.add(asteriod)
                level5_entry_asteriod = False

            if asteriod_hit > range_of_asteriods:
                if asteriod.rect.y > screen_height:
                    asteriods.remove(asteriod)
                    all_sprites.remove(asteriod)
                asteriod_flag = False
            if len(asteriods) == 0:

                if level5_entry_enemy == True:
                    bigenemy = BigEnemy(enemy_bigspaceship_img1, big_enemy1_laser, all_sprites, villian_lasers,0,villian_entry,big_enemy1_laser_blast,level)
                    big_enemy.add(bigenemy)
                    all_sprites.add(bigenemy)
                    level5_entry_enemy = False   
                if level5_entry_enemy == False:
                    if bigenemy.health == 0:
                        level = 6
                        asteriod_hit = 0
                        villian_hit = 0
                        obstacle_hit = 0

        if level == 6:
            if level6_entry_enemy == True:
                
                bigenemy1 = BigEnemy(enemy_bigspaceship_img1, big_enemy1_laser, all_sprites, villian_lasers,1,villian_entry,big_enemy1_laser_blast,level)
                bigenemy2 = BigEnemy(enemy_bigspaceship_img1, big_enemy1_laser, all_sprites, villian_lasers,2,villian_entry,big_enemy1_laser_blast,level)
                big_enemy1.add(bigenemy1)
                big_enemy2.add(bigenemy2)
                all_sprites.add(bigenemy1)
                all_sprites.add(bigenemy2)
                level6_entry_enemy = False 
            if level6_entry_enemy == False:
                # if hit > 20:
                if len(big_enemy1) == 0 and len(big_enemy2) == 0:
                    if level6_entry_bigenemy == True:
                        bigenemy = BigEnemy(enemy_bigspaceship_img2, big_enemy1_laser, all_sprites, villian_lasers,3,villian_entry,big_enemy2_laser_blast,level)
                        big_enemy.add(bigenemy)
                        all_sprites.add(bigenemy)
                        level6_entry_bigenemy = False   
                    if level6_entry_bigenemy == False:
                        if bigenemy.health == 0:
                            asteriod_hit = 0
                            villian_hit = 0
                            obstacle_hit = 0
                            main_screen(True)

        game_window.blit(background_img,background_img_rect)
        all_sprites.draw(game_window)
        text = font.render('Score: ' + str(score),1, (255,255,255) )
        game_window.blit(text, (370,8))

        draw_shield_bar(screen_width//4, 35, player.health)
        if level >= 5:
            if level == 5 and level5_entry_enemy == False:
                draw_enemy_shield_bar(bigenemy.health)
            if level == 6 and level6_entry_bigenemy == False:
                draw_enemy_shield_bar(bigenemy.health)
            if level == 6 and level6_entry_enemy == False:
                draw_enemy_health_bar(bigenemy1.health,bigenemy1)
                draw_enemy_health_bar(bigenemy2.health,bigenemy2)

        draw_lives( 10, 60, player.lives, player_mini_img)
        # if level == 0 or level == 4:
            # level_bar(level,number_of_obstacles,asteriod_hit)
        # if level == 1 or level == 2 or level == 3:
            # level_bar(level,number_of_obstacles,villian_hit)

        clock.tick(FPS)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_loop()


