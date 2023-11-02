import random
from collections import namedtuple

class Pong():
    def __init__(self, screen_width=320, screen_height=480, 
                 ball_base_speed=5, ball_radius=30, launch_ball_mode="fix",
                 paddle_speed=30, paddle_width=15, paddle_x=10, paddle_over_screen_proportion=0.3):
        
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.ball_base_speed = ball_base_speed
        self.ball_radius = ball_radius
        self.launch_ball_mode = launch_ball_mode

        self.paddle_speed = paddle_speed
        self.paddle_width = paddle_width
        self.paddle_height = self.screen_height * paddle_over_screen_proportion
        self.paddle_x = paddle_x

        self.reset()

    def reset(self):
        # Initialize game state
        self.ball_x, self.ball_y, self.ball_speed = self._launch_ball()

        self.paddle_y = (self.screen_height - self.paddle_height) / 2

        self.rally = 0

    def step(self, action):
        """action: (-1,0,1)"""
        #update ball position
        self.ball_x += self.ball_speed[0]
        self.ball_y += self.ball_speed[1]

        #update paddle movement within screen limits
        if self.paddle_y <= 0 and action == -1:
            pass
        elif self.paddle_y >= self.screen_height - self.paddle_height and action == 1:
            pass
        else:
            self.paddle_y += (action * self.paddle_speed)
        
        #status: hit(1),miss(-1),None(0)
        status = self._check_collision()
        if status == -1:
            self.reset()
        else:
            self.rally += status

        # print(self._sensory_feedback())

        
        ball_x_center = self.ball_x + self.ball_radius / 2 
        ball_y_center = self.ball_y + self.ball_radius / 2
        paddle_y_center = self.paddle_y + self.paddle_height / 2
        GameState = namedtuple('GameState', ['status', 'rally', 'ball_x', 'ball_y', 'paddle_y'])
        return GameState(status, self.rally, ball_x_center, ball_y_center , paddle_y_center)


    def _check_collision(self):
        paddle_top = self.paddle_y
        paddle_bottom = self.paddle_y + self.paddle_height
        paddle_right = self.paddle_x + self.paddle_width

        ball_top = self.ball_y
        ball_bottom = self.ball_y + self.ball_radius
        ball_left = self.ball_x
        ball_right = self.ball_x + self.ball_radius
        ball_x_speed = self.ball_speed[0]

        #paddle_right + ball_x_speed establishes a collision area appropriate to the horizontal speed
        #remember the ball_x_speed is negative
        if (paddle_right + ball_x_speed <= ball_left  <= paddle_right) and (
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
        
    def _launch_ball(self):

        if self.launch_ball_mode == "fix":
            ball_x = self.screen_width * 0.8
            ball_y = self.screen_height * 0.2
            ball_speed = [-self.ball_base_speed, self.ball_base_speed]
        
            return ball_x, ball_y, ball_speed
        
        if self.launch_ball_mode == "rand":
            #random mode
            #same x coordinate, random y 
            #same x speed, random y 
            ball_x = self.screen_width * 0.8
            ball_y = random.randint(self.screen_height * 0.2, self.screen_height * 0.8)
            ball_speed = [-self.ball_base_speed, random.randint(-(2*self.ball_base_speed), (2*self.ball_base_speed))]
            
            return ball_x, ball_y, ball_speed
        raise ValueError("Invalid launch_ball_mode.")