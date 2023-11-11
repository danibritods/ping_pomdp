from pingpomdp.pingpomdp import PingPOMDP
import json

def json_append(filename,entry):
    with open(filename, mode='a', encoding='utf-8') as f:
        json.dump(entry, f)
        f.write('\n') 

def run_experiment(config):
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
        "n_obs": config["n_obs"],
        "n_states": config["n_states"],
        "agent_id": config['agent_id'],
        "matrices_mode": config['matrices_mode']
    }
    gridlink_config = {
        "grid_shape": (2, 3),
        "sensory_cells": (0, 1, 2),
        # "motor_cells": (3,5),
        "observation_mode": "sensory_cells",
        "n_predictable_cycles": 10,
        "n_unpredictable_cycles": 20,
        'agent_seed': config['agent_seed'],
        'env_seed': config['env_seed']
    }

    p = PingPOMDP(
        pong_config=pong_config,
        agent_config=agent_config,
        gridlink_config=gridlink_config,
        )  
    p.run(num_steps=config['num_steps'])
    print()


for i in range(5):

    env_seed = [1,2,3,4,5,6]
    n = 3
    xp_config = {
        "n_obs": 2**n,
        "n_states": 2**n,
        "grid_shape": (2, n),
        "sensory_cells": n, #tuple(range(n)),
        "agent_id": None, #agents_ids[i],
        "matrices_mode": 'uniform',
        "agent_seed":1,
        "env_seed":env_seed[i],
        "num_steps":40_000
        }
    batch_name = "uniformS1P1-6_40ksteps_3obs.json"

    results = run_experiment(xp_config)
    json_append(batch_name, results)