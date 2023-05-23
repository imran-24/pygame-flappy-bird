import pygame 
from setting import *
import sys, time
from sprites import BG, Ground, Bird, Obstacle

class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_LENGTH))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()


        # background 
        background_surface = pygame.image.load('Game Objects/background-day.png').convert_alpha()
        self.scale_fector = WINDOW_LENGTH/background_surface.get_height()
        self.all_sprite = pygame.sprite.Group()
        self.collision_sprite = pygame.sprite.Group()
        self.obsticle_timer = pygame.USEREVENT + 1
        BG(self.all_sprite, self.scale_fector)
        Ground([self.all_sprite, self.collision_sprite], self.scale_fector) 
        self.bird = Bird( self.all_sprite, self.scale_fector)

        # font 
        self.font = pygame.font.Font('font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        
        self.start_time = pygame.time.get_ticks()
        
        # menu 
        self.active = True
        self.gameover_surface = pygame.image.load('UI/gameover.png')
        self.gameover_rect = self.gameover_surface.get_rect(center= (WINDOW_WIDTH/2, 200))
        self.menu_surface = pygame.image.load('UI/message.png')
        self.menu_rect = self.menu_surface.get_rect(center= (WINDOW_WIDTH/2, WINDOW_LENGTH/2))
        pygame.time.set_timer(self.obsticle_timer, 1500)
        
        # music
        # self.backgroud_music = pygame.mixer.Sound("audio/music.wav")
        # self.backgroud_music.set_volume(.1)
        self.jump_music = pygame.mixer.Sound("Sound Efects/wing.wav")
        self.jump_music.set_volume(.1)
        self.hit_music = pygame.mixer.Sound("Sound Efects/hit.wav")
        self.hit_music.set_volume(.3)
        self.die_music = pygame.mixer.Sound("Sound Efects/die.wav")
        self.die_music.set_volume(.3)
        

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprite, False, pygame.sprite.collide_mask)\
        or self.bird.rect.top <= 0 or self.bird.rect.bottom >= 800:
            self.hit_music.play()
            for sprite in self.collision_sprite.sprites():
                if sprite.type == 'obstacle':
                    sprite.kill()
            # self.die_music.play()
            self.active = False
            self.bird.kill()
            self.bird.rect.x = WINDOW_WIDTH / 2

    def show_score(self):
        current_time = pygame.time.get_ticks() - self.start_time
        score = int(current_time/100)
        score_surface = self.font.render(f'{score}', False, "White")
        score_rect = score_surface.get_rect(center= (WINDOW_WIDTH/2 , 100))
        self.display_surface.blit(score_surface, score_rect)
        return score

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.active:
                        self.bird.jump()
                        self.jump_music.play()
                    elif event.key == pygame.K_SPACE and self.active == False:
                        self.start_time = pygame.time.get_ticks()
                        self.active = True
                        self.bird = Bird( self.all_sprite, self.scale_fector)

                    


                if event.type == self.obsticle_timer and self.active:
                    Obstacle([self.all_sprite, self.collision_sprite], self.scale_fector, 'up')
                    Obstacle([self.all_sprite, self.collision_sprite], self.scale_fector, 'down')
                    Ground([self.all_sprite, self.collision_sprite], self.scale_fector) 


            # draw sprite
            if self.active:
                self.all_sprite.draw(self.display_surface)
                self.all_sprite.update(dt)
                self.collisions()
                self.collision_sprite.draw(self.display_surface)
                self.score = self.show_score()
                self.collision_sprite.update(dt)
                # self.backgroud_music.play(-1)
            else:
                
                self.display_surface.blit(self.gameover_surface, self.gameover_rect)
                self.display_surface.blit(self.menu_surface, self.menu_rect)

                
                

            

            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == '__main__':
    game = Game();
    game.run()