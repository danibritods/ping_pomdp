import gridlink
from pong.pong_back import Pong
# import model

class Model:
    def observe(self, observation):
        print("model observing")

    def act(self):
        print("model action!")

class PongGridlink(gridlink.Gridlink):
    def _env_state_is_undesirable(self, env_state):
        if env_state.status < 0:
            return True
        else:
            return False
        
    def _env_state_is_desirable(self, env_state):
        if env_state.status >= 1:
            return True
        else:
            return False


class PingPOMDP:
    def __init__(self):
        self.env = Pong()
        self.grid = PongGridlink(Model())
        #my_agent = Agent( A = A_array, B = B_array, C = C_vector)

    def step(self):
        env_action = self.grid.act()
        env_state = self.env.step(env_action)

        self.grid.observe(env_state)

if __name__ == "__main__":
    p = PingPOMDP()
    p.step()