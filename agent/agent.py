import pymdp
from pymdp import utils
from pymdp.agent import Agent

class ActiveInferenceAgent(Agent):
    def __init__(self, n_obs, n_states, matrices_mode):
        # Define observation and action spaces
        self.num_obs = [n_obs]  # n binary elements representing the sensory electrodes
        self.num_states = [n_states]  # n binary elements representing possible states
        self.num_controls = [2]  # 0 or 1

        # Create the generative model
        if matrices_mode == 'random':
            A = utils.random_A_matrix(self.num_obs, self.num_states)  # Sensory likelihood
            B = utils.random_B_matrix(self.num_states, self.num_controls)  # Transition likelihood
            C = utils.obj_array_uniform(self.num_obs)  # Uniform preferences
        elif matrices_mode == 'uniform':
            # Initialize A matrix (observation likelihood) with uniform values
            A_m_shapes = [[o_dim] + self.num_states for o_dim in self.num_obs]
            A = utils.obj_array_uniform(A_m_shapes)

            # Initialize B (transition likelihood) with uniform values
            B_f_shapes = [[ns, ns, self.num_controls[f]] for f, ns in enumerate(self.num_states)]
            B = utils.obj_array_uniform(B_f_shapes)

            C = utils.obj_array_uniform(self.num_obs)

        # Initialize the agent
        super().__init__(A=A, B=B, C=C)

    def observe(self, observation):
        """
        Update beliefs based on the received observation.
        """
        # Convert observation (binary array) to index
        obs_idx = [int("".join(map(str, observation.astype(int))), 2)]

        # Update beliefs
        self.infer_states(obs_idx)

    def act(self):
        """
        Select an action based on current beliefs.
        """
        # Infer the optimal policy based on current beliefs
        self.infer_policies()
        
        # Sample an action from the inferred policy
        action = self.sample_action()
        return action

        # Instantiate the agent
        # self.agent = Agent(A=self.A_array, B=self.B_array, C=self.C_vector)

    # def __init__(self, n_obs=8, n_states=4):
    #     self.num_obs = [2**n_obs] 
    #     self.num_states = [n_states]  
    #     self.num_controls = [2]  
    #           #     # Create the generative model
    #     A = utils.random_A_matrix(self.num_obs, self.num_states)  # Sensory likelihood
    #     B = utils.random_B_matrix(self.num_states, self.num_controls)  # Transition likelihood
    #     C = utils.obj_array_uniform(self.num_obs)  # Uniform preference   s




        # # Set preference for [0,0,1,0,0] to a high value
        # C[0][4] = 10.0

        # # Set aversion (negative preference) for [1,0,0,0,0] and [0,0,0,0,1]
        # C[0][16] = -100.0
        # C[0][1] = -100.0

        # # Normalize the C matrix
        # C[0] = utils.norm_dist(C[0])
