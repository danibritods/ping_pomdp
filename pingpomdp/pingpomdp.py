from gridlink.gridlink import Gridlink
from pong.pong_back import Pong
# import model

class Model:
    def observe(self, observation):
        print("model observing")

    def act(self):
        print("model action!")

class PongGridlink(Gridlink):
    def _is_env_state_undesirable(self, env_state):
        if env_state.status < 0:
            return True
        else:
            return False
        
    def _is_env_state_desirable(self, env_state):
        if env_state.status >= 1:
            return True
        else:
            return False

    def _active_cell_index(self, env_state):
        """
        - Kaggan (2020) encodes game state using paddle relative position to the ball
        - This function emulates their place coding:    
          - Calculates the distance from paddle center to ball center
          - Normalize this distance by the screen height
          - Translate the normalized distance to the number of sensorial cells
          - Caps the value to be between the possible indexes of n (zero to n - 1)
        """
        # TODO: also use proximity
        ball_x = env_state.ball_x
        ball_y = env_state.ball_y
        paddle_Y = env_state.paddle_y
        n = self.n_sensory_cells

        relative_position = (paddle_Y - ball_y) 
        normalized_rel_pos = round(relative_position / self.env.screen_height * n + n/2)
        capped_norm_rel_pos = max(0, min(normalized_rel_pos, n - 1))
        
        return capped_norm_rel_pos

    def _map_agent_action_to_env(self, agent_action):
        return super()._map_agent_action_to_env(agent_action)
    
class PingPOMDP:
    def __init__(self):
        env = Pong()
        model = None
        self.grid = PongGridlink(model,env)

    def run(self):
        for i in range(10):
            self.grid.step()

if __name__ == "__main__":
    p = PingPOMDP()
    p.run()