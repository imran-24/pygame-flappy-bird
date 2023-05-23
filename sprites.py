import pygame
from setting import *
from random import choice, randint, randrange

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_fector):
        super().__init__(group)

        background_surface = pygame.image.load('Game Objects/background-day.png').convert_alpha()
        full_height = background_surface.get_height() * scale_fector
        full_width = background_surface.get_width() * scale_fector
        full_image = pygame.transform.scale(background_surface, (full_width, full_height))
        
        self.image = pygame.Surface((full_width * 2, full_height * 2))
        self.image.blit(full_image, (0, 0))
        self.image.blit(full_image, (full_width, 0))
        self.rect = self.image.get_rect(topleft= (0, 0))

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):

        self.pos.x -= 100 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.centerx < 0:
            self.pos.x = 0


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_fector):
        super().__init__(groups)

        self.type = "ground"
        ground_image = pygame.image.load('Game Objects/base.png').convert_alpha()
        full_height = ground_image.get_height() 
        full_width = ground_image.get_width() * scale_fector

        full_image = pygame.transform.scale(ground_image, pygame.math.Vector2(ground_image.get_size()) * scale_fector)
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_image, (0,0))
        self.image.blit(full_image, (full_width, 0))
        self.rect = self.image.get_rect(bottomleft= (0, WINDOW_LENGTH))
        # msk
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.x)

    def update(self, dt):

        self.pos.x -= 220 * dt
        
        if self.rect.centerx < 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_fector):
        super().__init__(groups)

        self.birds = [ pygame.image.load(f'Game Objects/{i}.png').convert_alpha() for i in range(0, 3)]
        self.birds = [ pygame.transform.rotozoom(bird, 0, 1.5).convert_alpha() for bird in self.birds]

        self.bird_index = 0
        self.image = self.birds[self.bird_index]

        self.rect = self.image.get_rect(center= ( WINDOW_WIDTH/ 2, WINDOW_LENGTH/ 2))

        self.direction = 0
        self.gravity = 700
        self. pos = pygame.math.Vector2(self.rect.topleft)
        # msk
        self.mask = pygame.mask.from_surface(self.image)
        
    
    def gravity_method(self, dt):
            self.direction += self.gravity * dt
            self.pos.y += self.direction * dt
            self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -250

    def animate(self, dt):
        self.bird_index += 10 * dt 
        if self.bird_index > len(self.birds):
            self.bird_index = 0
        self.image = self.birds[int(self.bird_index)]
    
    def rotate(self, dt):
        self.image = pygame.transform.rotozoom(self.image, -self.direction * .07, 1)
        # msk
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, dt):
        self.gravity_method(dt)
        self.animate(dt)
        self.rotate(dt)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_fector, type):
        super().__init__(groups)
        
        self.type = 'obstacle'
        obstacle_image = pygame.image.load('Game Objects/pipe-green.png').convert_alpha()
        full_height = obstacle_image.get_height() * scale_fector
        full_width = obstacle_image.get_width() * scale_fector * 1.3
        self.image = pygame.transform.scale(obstacle_image, (full_width, full_height))
        width = WINDOW_WIDTH + randint(20, 50)
        
        if type == 'up':
            height = randrange(-180, -100, 40)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(topright= (width, height))
        else:
            height = randrange(950, 1020, 40)
            self.rect = self.image.get_rect(bottomright= (width, height))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        # msk
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.pos.x -= 100 *dt
        self.rect.x = round(self.pos.x)
        if self.rect.x < -200:
            self.kill()

    