import pymdp
from pymdp import utils
from pymdp.agent import Agent

class ActiveInferenceAgent:
    def __init__(self):
        # Define observation and action spaces
        self.num_obs = [2**8]  # 8 binary elements representing the sensory electrodes
        self.num_states = [2**8]  # 8 binary elements representing possible states
        self.num_controls = [2]  # 0 or 1

        # Create the generative model
        self.A_array = utils.random_A_matrix(self.num_obs, self.num_states)  # Sensory likelihood
        self.B_array = utils.random_B_matrix(self.num_states, self.num_controls)  # Transition likelihood
        self.C_vector = utils.obj_array_uniform(self.num_obs)  # Uniform preferences

        # Instantiate the agent
        self.agent = Agent(A=self.A_array, B=self.B_array, C=self.C_vector)

    def observe(self, observation):
        """
        Update beliefs based on the received observation.
        """
        # Convert observation (binary array) to index
        obs_idx = [int("".join(map(str, observation)), 2)]
        
        # Update beliefs
        self.agent.infer_states(obs_idx)

    def act(self):
        """
        Select an action based on current beliefs.
        """
        # Infer the optimal policy based on current beliefs
        self.agent.infer_policies()
        
        # Sample an action from the inferred policy
        action = self.agent.sample_action()
        return action
