import pygame
from pong_back import PongGame

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

if __name__ == "__main__":
    game = PongGame()
    ui = PongUI(game)
    ui.run()
    



    
