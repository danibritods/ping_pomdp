import logging
from pathlib import Path
import numpy as np
import pickle
from datetime import datetime
from zoneinfo import ZoneInfo


from gridlink.gridlink import Gridlink
from pong.pong_back import Pong
from agent.agent import ActiveInferenceAgent
from data.database import ExperimentDB

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
    
class RandomAgent():
    def observe(self, observation):
        pass
    def act(self):
        return np.random.randint(0,1) 

class PingPOMDP:
    def __init__(self, seed=None, pong_config=None, agent_config=None, gridlink_config={}):
        self.db = ExperimentDB()
        self.config_id = self.db.get_config_id(random_seed=seed,
                                               pong_config=pong_config,
                                               agent_config=agent_config,
                                               gridlink_config=gridlink_config)

        # Set random seeds for reproducibility
        if seed:
            np.random.seed(seed)

        env = Pong(**(pong_config or {}))
        agent_id = agent_config.get('agent_id')
        agent = self.load_agent(agent_id) if agent_id else ActiveInferenceAgent(n_obs=agent_config['n_obs'],
                                                                               n_states=agent_config['n_states'])
        self.grid = PongGridlink(agent=agent, env=env, **gridlink_config)


    def run(self, num_steps=10):

        start_time = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y-%m-%d %H:%M:%S')
        experiment_id = self.db.start_experiment(start_time=start_time,
                                                 config_id=self.config_id,
                                                 notes= "")
        hits, misses, three_plus_rallies = 0, 0, 0
        try:
            for i in range(num_steps):
                self.grid.step()
                env_state = self.grid.env_state

                if env_state.status == 1:
                    hits += 1
                    if env_state.rally == 3:
                        three_plus_rallies += 1
                elif self.grid.env_state.status == -1:
                    misses += 1

                logging.info(f"Step {i + 1}; Agent's action: {self.grid.agent_action};({hits},{three_plus_rallies},{misses});{self.grid.env_state}")
                
                self.db.insert_step(experiment_id=experiment_id,
                                    step_num=(i+1),
                                    environment_state=self.grid.env_state,
                                    agent_action=self.grid.agent_action)

        except KeyboardInterrupt:
            pass
        finally:
            end_time = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y-%m-%d %H:%M:%S')

            self.db.finalize_experiment(experiment_id=experiment_id,
                                        end_time=end_time,
                                        steps_taken=(i+1))
            self.db.close()
            self.save_agent()

    def save_agent(self):
        timestamp = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y%m%d_%H%M%S')
        filename = f"agent/archive/agent_{timestamp}.pkl"
        
        with open(filename, "wb") as file:
            pickle.dump(self.grid.agent, file)
        logging.info(f"Agent saved to {filename}")

    def load_agent(self, agent_id):
        agent_dir = Path("agent/archive")
        agent_files = sorted(agent_dir.glob(f"{agent_id}_*.pkl"), reverse=True)
        if agent_files:
            latest_agent_file = agent_files[0]
            with latest_agent_file.open("rb") as file:
                logging.info(f"Agent loaded from {latest_agent_file}")
                return pickle.load(file)
        else:
            logging.error(f"No agent files found for ID {agent_id}!")

if __name__ == "__main__":
    random_seed = 2
    pong_config = {
        "screen_width": 320,
        "screen_height": 480,
        "ball_base_speed": 5,
        "ball_radius": 20,
        "launch_ball_mode": "fix",
        "paddle_speed": 30,
        "paddle_width": 15,
        "paddle_x": 10,
        "paddle_over_screen_proportion": 0.3
        }
    
    agent_config = {
        "n_obs": 5,
        "n_states": 3,
        "agent_id": "agent_20231101_122848" 
    }

    gridlink_config = {
        "grid_shape": (2, 5),
        "sensory_cells": (0, 1, 2, 3, 4),
        "observation_mode": "sensory_cells" 
    }

    p = PingPOMDP(seed=random_seed,
                  pong_config=pong_config,
                  agent_config=agent_config,
                  gridlink_config=gridlink_config)  
    p.run(num_steps=30_000)