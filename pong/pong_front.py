import pygame


class PongFront:
    def __init__(self, game):
        pygame.init()

        self.screen = pygame.display.set_mode((game.screen_width, game.screen_height))

        self.ball = pygame.Rect(0, 0, game.ball_radius, game.ball_radius)
        self.player_paddle = pygame.Rect(game.paddle_x, game.paddle_y, game.paddle_width, game.paddle_height)

        pygame.display.set_caption("Pong")

        # Colors
        self.white = (255, 255, 255)
        self.paddle_color = (169, 56, 84)  # Color #a93854
        self.ball_color = (255, 173, 64)   # Color #ffad40

        # Fonts and FPS
        self.font = pygame.font.Font(None, 36)
        self.font_big = pygame.font.Font(None, 72)
        self.fps = 60
        self.clock = pygame.time.Clock()

        # Game
        self.game = game




    def run(self):
        done = False

        while not done:
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
            rally_text = self.font_big.render(f"{self.game.score}", True, self.paddle_color)

            self.screen.fill(self.white)  # Background color set to white
            self.screen.blit(rally_text, (self.game.screen_width / 2, 10))

            # Drawing rounded paddle
            pygame.draw.rect(self.screen, self.paddle_color, self.player_paddle, border_radius=10)

            # Drawing the ball
            pygame.draw.ellipse(self.screen, self.ball_color, self.ball)
            pygame.display.flip()

            self.clock.tick(self.fps)


if __name__ == "__main__":
    from pong_back import Pong
    game = Pong()
    interface = PongFront(game)
    interface.run()