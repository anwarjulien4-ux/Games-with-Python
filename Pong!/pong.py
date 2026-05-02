import pygame
import math
import random

pygame.init()



bg_color = "#1C2842"
pad_color = "#e7eaff"
ball_color = "#ff2121"

class PongPad(pygame.Rect):
    def __init__(self, x, y, width=15, height=120):
        super().__init__(x, y, width, height)
        self.speed = 15

        self.moving_up = False
        self.moving_down = False

    def moveable_up(self, keys: pygame.key, key):
        if keys[key]:
            self.moving_up = True
            self.y -= self.speed
    
    def moveable_down(self, keys: pygame.key, key):
        if keys[key]:
            self.moving_down = True
            self.y += self.speed

        

class Ball(pygame.Rect):
    def __init__(self, x, y, width=20, height=20):
        super().__init__(x, y, width, height)
        self.speed_y = 7
        self.speed_x = 8
        self.moveable = False

    def default_pos(self, screen_width, screen_height): 
        self.center = (screen_width*0.5, screen_height*0.5)

        


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = 800, 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.score_font = pygame.font.Font("04B_30__.ttf", 30)
        self.start_page_title_font = pygame.font.Font("04B_30__.ttf", 60)

        self.padding = 10
        self.left_pad = PongPad(self.padding, 100)

        self.right_pad = PongPad(0, 150)
        self.right_pad.x = (self.screen_width - (self.padding+self.right_pad.width))

        self.ball = Ball(400, 250)
        self.ball.default_pos(self.screen_width, self.screen_height)

        self.left_score = 0
        self.right_score = 0

        self.angle = 0


        self.clock = pygame.time.Clock() # To control FPS


    def run(self):
        self.running = True
        self.running_start_page = True
        self.running_gameplay = False

        while self.running:
            self.screen.fill(bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.running_start_page:
                        self.running_start_page = False
                        self.running_gameplay = True
                    elif self.running_gameplay:
                        self.ball.moveable = True


            if self.running_start_page:
                self.run_start_page()
            if self.running_gameplay:
                self.run_gameplay()

            self.clock.tick(60)
            pygame.display.flip()
        
        pygame.quit()
        return



    def run_start_page(self): # Start page logic goes here
        self.draw_start_page_text()


    def run_gameplay(self):  # Game stuff goes here

            # For the middle line
            self.draw_middle_line()

            # For the pong pads
            self.draw_pads()
            self.pad_movement()

            # For the ball
            self.draw_ball()
            self.ball_movement()

            # main game logic
            self.core_logic()

            # For the scores
            self.draw_scores()


    def draw_start_page_text(self):
        text_speed = (10 * math.sin(1.5*(self.angle))) + self.screen_height*0.5 - 30

        self.start_page_title = self.start_page_title_font.render("PONG GAME!", True, "#FFFFFF")
        self.start_page_title_pos = self.start_page_title.get_rect(center=(self.screen_width*0.5, text_speed)) 

        self.screen.blit(self.start_page_title, self.start_page_title_pos)

        self.angle += 0.05

        self.start_page_text_font = pygame.font.Font("ari-w9500-bold.ttf", 20)
        self.start_page_text = self.start_page_text_font.render("Press Enter to start!", True, "#FFFFFF")
        self.start_page_text_pos = self.start_page_text.get_rect(center=(self.screen_width*0.5, self.screen_height*0.5 + 50))
        
        self.screen.blit(self.start_page_text, self.start_page_text_pos)

    

    def draw_middle_line(self):
        space_increment = 15
        
        middle_blocks = []
        for _ in range(10):
            middle_blocks.append(pygame.Rect(0.5*self.screen_width-0.5*15, -15+space_increment, 10, 40))
            space_increment += 65
        
        for block in middle_blocks:
            pygame.draw.rect(self.screen, "#1A243A", block)

    
    def draw_pads(self):
        pygame.draw.rect(self.screen, pad_color, self.left_pad)
        pygame.draw.rect(self.screen, pad_color, self.right_pad)


    def pad_movement(self):
        pressed_keys = pygame.key.get_pressed()
        floor = self.screen_height-(self.padding+self.left_pad.height)

        # Left pad movement
        if self.padding < self.left_pad.y < floor:
            self.left_pad.moveable_up(pressed_keys, pygame.K_w)
            self.left_pad.moveable_down(pressed_keys, pygame.K_s)

        elif self.left_pad.y <= self.padding:
            self.left_pad.y = self.padding
            self.left_pad.moveable_down(pressed_keys, pygame.K_s)

        elif self.left_pad.y >= floor:
            self.left_pad.y = floor
            self.left_pad.moveable_up(pressed_keys, pygame.K_w)

        # Right pad movement
        if self.padding < self.right_pad.y < floor:
            self.right_pad.moveable_up(pressed_keys, pygame.K_UP)
            self.right_pad.moveable_down(pressed_keys, pygame.K_DOWN)

        elif self.right_pad.y <= self.padding:
            self.right_pad.y = self.padding
            self.right_pad.moveable_down(pressed_keys, pygame.K_DOWN)

        elif self.right_pad.y >= floor:
            self.right_pad.y = floor
            self.right_pad.moveable_up(pressed_keys, pygame.K_UP)      


         
    def draw_ball(self):
        pygame.draw.rect(self.screen, ball_color, self.ball)

    def ball_movement(self):
        floor = self.screen_height-(self.padding+self.ball.height)

        if self.ball.moveable:
            self.ball.x += self.ball.speed_x
            self.ball.y += self.ball.speed_y

        if self.ball.colliderect(self.left_pad) and self.ball.speed_x < 0:
            self.ball.speed_x *= -1   

        if self.ball.colliderect(self.right_pad) and self.ball.speed_x > 0:
            self.ball.speed_x *= -1   

        if self.ball.y > floor or self.ball.y < (self.padding):
            if self.ball.y > floor:
                self.ball.y = floor
            else:
                self.ball.y = self.padding
            self.ball.speed_y *= -1

    
    def core_logic(self):
        if self.ball.x > self.screen_width:
            self.left_score += 1
            self.ball.default_pos(self.screen_width, self.screen_height)
            self.ball.moveable = False

        
        if self.ball.x < 0:
            self.right_score += 1
            self.ball.default_pos(self.screen_width, self.screen_height)
            self.ball.moveable = False


    
    def draw_scores(self):

        # For left score
        self.left_score_text = self.score_font.render(str(self.left_score), True, "#EBBE1E")
        self.left_score_pos = self.left_score_text.get_rect(center=(self.screen_width*0.5 - 60, 40))

        # For right score
        self.right_score_text = self.score_font.render(str(self.right_score), True, "#EBBE1E")
        self.right_score_pos = self.right_score_text.get_rect(center=(self.screen_width*0.5 + 60, 40))

        self.screen.blit(self.left_score_text, self.left_score_pos)
        self.screen.blit(self.right_score_text, self.right_score_pos)








game = Game()
game.run()
