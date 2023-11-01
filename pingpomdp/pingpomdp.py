import logging
import os
import numpy as np
import pickle
from datetime import datetime
from zoneinfo import ZoneInfo


from gridlink.gridlink import Gridlink
from pong.pong_back import Pong
from agent.agent import ActiveInferenceAgent

logging.basicConfig(level=logging.INFO)

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
        # Map the agent's action (0 or 1) to environment's actions (-1 or 1)
        return -1 if agent_action == 0 else 1
    
class PingPOMDP:
    def __init__(self, seed=None):
        # Set random seeds for reproducibility
        if seed:
            np.random.seed(seed)

        grid_shape = (2,8)
        sensory_cells = (0,1,2,3,4,5,6,7)
        observation_mode = "sensory_cells" 
        #agent = ActiveInferenceAgent(8)
        agent = self.load_agent('agent/archive/agent_20231031_234900.pkl')


        self.grid = PongGridlink(agent=agent,
                                 env=Pong(),
                                 grid_shape=grid_shape,
                                 sensory_cells=sensory_cells,
                                 observation_mode=observation_mode)

    def run(self, num_steps=10):
        try:
            for i in range(num_steps):
                self.grid.step()
                logging.info(f"Step {i+1}: Agent's action: {self.grid.agent_action}, Environment state: {self.grid.env_state}")
                
        finally:
            # print("\nCtrl+C pressed. Gracefully stopping...")
            self.save_agent()
            

    def save_agent(self, filename=None):
        if filename == None:
            timestamp = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y%m%d_%H%M%S')
            filename = f"agent/archive/agent_{timestamp}.pkl"
        
        with open(filename, "wb") as file:
            pickle.dump(self.grid.agent, file)
        logging.info(f"Agent saved to {filename}")

    def load_agent(self, filename):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                return pickle.load(file)
            logging.info(f"Agent loaded from {filename}")
        else:
            logging.error(f"File {filename} not found!")

if __name__ == "__main__":
    p = PingPOMDP(seed=1)  
    p.run(num_steps=100_000)