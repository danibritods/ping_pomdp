import random
import pygame
import threading
import time

class PongUI:
    def __init__(self, game):
        pygame.init()

        self.screen = pygame.display.set_mode((game.screen_width, game.screen_height))

        self.ball = pygame.Rect(0,0,game.ball_radius, game.ball_radius)
        self.player_paddle = pygame.Rect(game.paddle_x, game.paddle_y, game.paddle_width, game.paddle_height)

        pygame.display.set_caption("Pong")

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.game = game

    def get_player_input(self):
        # Handle player input here
        pass

    def run(self):
        done = False
        # self.game.reset()

        while not done:
            # action = self.get_player_input()
            # self.game.step(action)

            self.ball.x = self.game.ball_x
            self.ball.y = self.game.ball_y
            self.player_paddle.y = self.game.paddle_y

            # Update display
            self.screen.fill(self.black)
            pygame.draw.rect(self.screen, self.white, self.player_paddle)
            pygame.draw.ellipse(self.screen, self.white, self.ball)
            pygame.display.flip()

class PongGame():
    def __init__(self):
        self.ball_speed = (5,5)
        self.ball_radius = 15

        self.paddle_speed = 10
        self.paddle_width = 15
        self.paddle_height = 140
        self.paddle_x = 0

        self.screen_width = 640
        self.screen_height = 480

        self.reset()

    def reset(self):
        # Initialize game state
        self.ball_x = 0
        self.ball_y = 0

        self.paddle_y = 240

        self.rally = 0

    def step(self, action):
        """action: (-1,0,1)"""
        self.ball_x += self.ball_speed[0]
        self.ball_y += self.ball_speed[1]

        self.paddle_y += (action * self.paddle_speed)
        print(self.paddle_y)
        
        #status(hit(1),miss(-1),None(0))
        status = self.check_collision()
        if status == -1:
            self.reset()
        else:
            self.rally += status

        return status, self.rally, self.paddle_y, self.ball_x, self.ball_y

    def check_collision(self):
        return 0

if __name__ == "__main__":
    print("test")
    game = PongGame()
    ui = PongUI(game)
    x = threading.Timer(1,ui.run)
    x.start()
    # ui.run()
    time.sleep(10)
    print("testing2")
    
    for i in range(50):
        action = int(input("action: "))
        game.step(1)



    
