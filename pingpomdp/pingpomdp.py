import os
import logging
from pathlib import Path
import numpy as np
import pickle
from datetime import datetime
from zoneinfo import ZoneInfo
import random

from gridlink.gridlink import Gridlink
from pong.pong_back import Pong
from agent.agent import ActiveInferenceAgent
from data.database import ExperimentDB

logging.basicConfig(level=logging.INFO)

class PongGridlink(Gridlink):
    def _is_env_state_undesirable(self, env_state):
        # return False
        return env_state.status < 0
        
    def _is_env_state_desirable(self, env_state):
        # return False
        return env_state.status >= 1


    def _active_cell_index(self, env_state):
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
    def observe(self, _): #receives observation but does nothing
        pass
    def act(self):
        return np.random.randint(0,2) 

class PingPOMDP:
    def __init__(self, pong_config, agent_config, gridlink_config):
        np.random.seed(gridlink_config['agent_seed'])
        random.seed(gridlink_config['env_seed'])

        self.db = ExperimentDB()
        self.config_id = self.db.get_config_id(
                                               env_config=pong_config,
                                               agent_config=agent_config,
                                               gridlink_config=gridlink_config)
    
        env = Pong(**(pong_config or {}))
        agent = self.load_agent(agent_config) 
        self.grid = PongGridlink(agent=agent, env=env, **gridlink_config)

    def run(self, num_steps=10):
        start_time = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y-%m-%d %H:%M:%S')
        experiment_id = self.db.start_experiment(start_time=start_time,
                                                 config_id=self.config_id,
                                                 notes= "")
        metrics = {"hits":0, "misses":0, "average_rally_length":0, "aces":0, "long_rallies":0, "logest_rally_length":0}
        results = {}
        try:
            for i in range(num_steps):
                self.grid.step()
                self.update_metrics(self.grid.env_state, metrics)

                logging.info(f"Step {i + 1}; Agent's action: {self.grid.agent_action};({metrics['hits'],metrics['long_rallies'],metrics['misses']});{self.grid.env_state}")
                
                self.db.insert_step(experiment_id=experiment_id,
                                    step_num=(i+1),
                                    environment_state=self.grid.env_state,
                                    agent_action=str(self.grid.agent_action))
                
                if  int(num_steps * 0.25) == (i + 1):
                    results['t1'] = metrics
                    metrics = {"hits":0, "misses":0, "average_rally_length":0, "aces":0, "long_rallies":0, "logest_rally_length":0}

        except Exception as e:
            print(e)
        finally:
            end_time = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y-%m-%d %H:%M:%S')

            self.db.finalize_experiment(experiment_id=experiment_id,
                                        end_time=end_time,
                                        steps_taken=(i+1),
                                        results=metrics)
            
            # self.append_run_to_metadata(start_time=start_time,
            #                                   end_time=end_time,
            #                                   steps_taken=(i+1),
            #                                   metrics=metrics)
            self.db.close()
            self.save_agent()
            results['t2'] = metrics
            print(results['t1'])
            print(results["t2"])
            return {'agent':f'{self.agent_id}_{self.agent_version}',
                    'results':results,
                    'time':f'{start_time}{end_time}'}
                    


    def update_metrics(self, env_state, metrics):
        if env_state.status == 1:
            metrics["hits"] += 1
            if metrics["hits"] > metrics["logest_rally_length"]:
                metrics["logest_rally_length"] = metrics["hits"]
            if env_state.rally == 3:
                metrics["long_rallies"] += 1
        elif self.grid.env_state.status == -1:
            metrics["misses"] += 1
            if env_state.rally == 0:
                metrics["aces"] += 1
        try: 
            metrics["average_rally_length"] = metrics["hits"] / metrics["misses"]
        except ZeroDivisionError:
             metrics["average_rally_length"] 

        
    def save_agent(self):
        if not hasattr(self, 'agent_version'):
            self.agent_version = 0

        filename = f"agent/archive/new/{self.agent_id}_{int(self.agent_version) + 1}.pkl"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        
        with open(filename, "wb") as file:
            pickle.dump(self.grid.agent, file)
        logging.info(f"Agent saved to {filename}")


    def save_ppdp(self):
        filename = f"data/ppdp/{self.agent_id}-{self.agent_version}.pkl"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "wb") as file:
            pickle.dump(self, file)
        logging.info(f"Agent saved to {filename}")


    def load_agent(self, agent_config):
        agent_id = agent_config.get('agent_id')
        if agent_id:
            if agent_id.lower() == "random":
                self.agent_id = "agent_random"
                return RandomAgent()
            else:
                self.agent_id = agent_id
                return self._get_agent_from_file(agent_id)
        else:
            timestamp = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%Y%m%d_%H%M%S')
            self.agent_id = f"agent_{timestamp}"
            return ActiveInferenceAgent(n_obs=agent_config['n_obs'],
                                n_states=agent_config['n_states'], 
                                matrices_mode=agent_config['matrices_mode'])
                      
        

    def _get_agent_from_file(self, agent_id):
        agent_dir = Path("agent/archive")
        agent_files = sorted(agent_dir.glob(f"{agent_id}_*.pkl"), reverse=True)
        if agent_files:
            latest_agent_file = agent_files[0]
            with latest_agent_file.open("rb") as file:
                logging.info(f"Agent loaded from {latest_agent_file}")
                self.agent_version = str(latest_agent_file).split('_')[-1].split(".")[0]
                return pickle.load(file)
        else:
            logging.error(f"No agent files found for ID {agent_id}!")

    def append_run_to_metadata(self, start_time, end_time, steps_taken, metrics):
        if not hasattr(self.grid.agent, 'metadata'):
                self.grid.agent.metadata = {"run_history":[]}

        self.grid.agent.metadata["run_history"].append({
            'started': start_time,
            'finished': end_time,
            'steps_taken': steps_taken,
            'results': metrics
            })


def test_run():
    pong_config = {
        "screen_width": 320,
        "screen_height": 480,
        "ball_base_speed": 5,
        "ball_radius": 20,
        "launch_ball_mode": "random",
        "paddle_speed": 30,
        "paddle_width": 15,
        "paddle_x": 10,
        "paddle_over_screen_proportion": 0.10
        }
    
    agent_config = {
        "n_obs": 2**3,
        "n_states": 2**3,
        "agent_id": None, 
        "matrices_mode": 'random'
    }

    gridlink_config = {
        "grid_shape": (2, 3),
        "sensory_cells": (0, 1, 2),
        # "motor_cells": (3,5),
        "observation_mode": "sensory_cells",
        "n_predictable_cycles": 10,
        "n_unpredictable_cycles": 20,
        'agent_seed': 1,
        'env_seed': 1
    }

    p = PingPOMDP(
        pong_config=pong_config,
        agent_config=agent_config,
        gridlink_config=gridlink_config,
        )  
    p.run(num_steps=40_000)


if __name__ == "__main__":
    test_run()
