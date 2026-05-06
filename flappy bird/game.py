import pygame
import random

pygame.init()


bird_idle = "flappy bird\\birdie.png"
bird_flying = "flappy bird\\birdie_flying.png"
sky = "flappy bird\\flappy_bird_sky.png"
bar = "flappy bird\\flappy_bird_bar_slimmer.png"


def random_middlepoint():
    return random.randint(100, 500)

class Game:
    def __init__(self):
        self.screen_width, self.screen_height = 600, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.gravity = 1.2


        self.scale_factor = 0.15
        self.bird_img = pygame.image.load(bird_idle)
        self.bird_idle = pygame.transform.smoothscale_by(self.bird_img, self.scale_factor)
        self.bird_pos = self.bird_idle.get_rect(x=100, y=100)
        self.bird_speed = 0
        
        self.bird_flying_img = pygame.image.load(bird_flying)
        self.bird_flying = pygame.transform.smoothscale_by(self.bird_flying_img, self.scale_factor)

        self.sky = pygame.image.load(sky)
        self.sky_pos = self.sky.get_rect()
        self.sky_speed = 1.5


        self.bar = pygame.image.load(bar)
        self.bar_pos = self.bar.get_rect(x=self.screen_width-10, y=400)
        self.bar_speed = 2.5
 
        self.bar_middlepoint = random_middlepoint()
        self.bar_2_middlepoint = random_middlepoint()
        self.bar_halfdist = 100


        self.clock = pygame.time.Clock()


    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get(): # Event loop
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.jump()

            self.screen.fill("#FFFFFF")
            self.draw_sky()
            self.bird_movement()
            self.draw_bird()
            self.draw_bars()
            self.bar_movement()

            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()
        return
    
    def draw_bird(self):
        if self.bird_speed > 0:
            self.screen.blit(self.bird_idle, self.bird_pos)
        else:
            self.screen.blit(self.bird_flying, self.bird_pos)

    def bird_movement(self):
        self.bird_speed += self.gravity
        self.bird_pos.y += self.bird_speed
    

    def jump(self):
        self.bird_speed = -15

    def draw_sky(self):
        if self.sky_pos.x < -(self.screen_width):
            self.sky_pos.x = 0
        self.screen.blit(self.sky, self.sky_pos)
        self.screen.blit(self.sky, (self.sky_pos.x + self.screen_width, self.sky_pos.y))
        self.sky_pos.x -= self.sky_speed
        
    def draw_bars(self):
        # if self.bar_pos.x < -self.bar_pos.width:
        #     self.bar_pos.x = self.screen_width + self.bar_pos.width
        #     self.bar_middlepoint = random_middlepoint()

        self.top_bar_pos = (self.bar_pos.x, self.bar_middlepoint - (self.bar_halfdist + self.bar_pos.height))
        self.bottom_bar_pos = (self.bar_pos.x, self.bar_middlepoint + self.bar_halfdist)

        self.top_bar_2_pos = (self.bar_pos.x+400, self.bar_2_middlepoint-(self.bar_halfdist+self.bar_pos.height))
        self.bottom_bar_2_pos = (self.bar_pos.x+400, self.bar_2_middlepoint+self.bar_halfdist)

        self.screen.blit(self.bar, self.top_bar_pos) # top bar
        self.screen.blit(self.bar, self.bottom_bar_pos) # bottom bar
        self.screen.blit(self.bar, self.top_bar_2_pos) # top bar
        self.screen.blit(self.bar, self.bottom_bar_2_pos)     


    def bar_movement(self):
        self.bar_pos.x -= self.bar_speed


game = Game()
game.run()