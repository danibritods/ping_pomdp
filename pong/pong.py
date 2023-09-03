import random
import pygame

class PongUI:
    def __init__(self, game):
        pygame.init()

        self.screen = pygame.display.set_mode((game.screen_width, game.screen_height))

        self.ball = pygame.Rect(0,0,game.ball_radius, game.ball_radius)
        self.player_paddle = pygame.Rect(game.paddle_x, game.paddle_y, game.paddle_width, game.paddle_height)

        pygame.display.set_caption("Pong")

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        self.font_big = pygame.font.Font(None,72)
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.game = game

    def run(self):
        frame_count = 0
        done = False
        # self.game.reset()

        while not done:
            frame_count += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.game.step(1)
                    if event.key == pygame.K_UP:
                        self.game.step(-1)   
            self.game.step(0)

            self.ball.x = self.game.ball_x
            self.ball.y = self.game.ball_y
            self.player_paddle.y = self.game.paddle_y

            # Update display
            # elapsed_frames_text = self.font.render(f"Elapsed Frames: {frame_count}", True, self.white)
            rally_text = self.font_big.render(f"{self.game.rally}", True, self.white)


            self.screen.fill(self.black)
            # self.screen.blit(elapsed_frames_text, (10, 10))
            self.screen.blit(rally_text, (self.game.screen_width/2, 10))

            pygame.draw.rect(self.screen, self.white, self.player_paddle)
            pygame.draw.ellipse(self.screen, self.white, self.ball)
            pygame.display.flip()

            self.clock.tick(self.fps)

class PongGame():
    def __init__(self):
        self.ball_speed = [5,5]
        self.ball_radius = 30

        self.paddle_speed = 30
        self.paddle_width = 15
        self.paddle_height = 200
        self.paddle_x = 10

        self.screen_width = 640
        self.screen_height = 480

        self.reset()

    def reset(self):
        # Initialize game state
        self.ball_x = self.screen_width * 0.8
        self.ball_y = self.screen_height * 0.2

        self.paddle_y = self.screen_height/2 - self.paddle_height/2

        self.rally = 0

    def step(self, action):
        """action: (-1,0,1)"""
        self.ball_x += self.ball_speed[0]
        self.ball_y += self.ball_speed[1]

        self.paddle_y += (action * self.paddle_speed)
        
        #status(hit(1),miss(-1),None(0))
        status = self.check_collision()
        if status == -1:
            self.reset()
        else:
            self.rally += status

        return status, self.rally, self.paddle_y, self.ball_x, self.ball_y

    def check_collision(self):
        paddle_top = self.paddle_y
        paddle_bottom = self.paddle_y + self.paddle_height
        paddle_right = self.paddle_x + self.paddle_width

        ball_top = self.ball_y
        ball_bottom = self.ball_y + self.ball_radius
        ball_left = self.ball_x
        ball_right = self.ball_x + self.ball_radius
        ball_x_speed = self.ball_speed[0]

        #paddle_right - ball_x_speed establishes a collision area appropriate to the horizontal speed
        if (paddle_right - ball_x_speed  <= ball_left  <= paddle_right) and (
            ball_bottom >= paddle_top and ball_top <= paddle_bottom):  
            self.ball_speed[0] *= -1

            return 1
        else:
            if self.ball_x < 0:
                return -1
            
            if ball_right >= self.screen_width:
                self.ball_speed[0] *= -1

            if ball_bottom >= self.screen_height or ball_top <= 0:
                self.ball_speed[1] *= -1
            
            return 0

if __name__ == "__main__":
    game = PongGame()
    ui = PongUI(game)
    ui.run()



    
