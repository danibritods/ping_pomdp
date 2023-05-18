- Factor dimensions: number of possible factors for each modality of observation and states (hidden and control)
  - `num_obs = [3, 5] # observation modality dimensions`
  - `num_states = [4, 2, 3] # hidden state factor dimensions`
  - `num_controls = [4, 1, 1] # control state factor dimensions`
  - That is, two modalities of observation with 3 and 5 possible sensory outcomes. Three hidden states with 4, 2 and 3 possible values for each latent variable that the agent believes can generate the observations. Three control states with 4, 1 and 1 possible actions. 

- `A matrix`: sensory likelihood matrix 
  - A_array = utils.random_A_matrix(num_obs, num_states)
  - This matrix model the likelihood of observing an observation given a hidden state.  
  - ```python
    def random_A_matrix(num_obs, num_states):
    if type(num_obs) is int:
        num_obs = [num_obs]
    if type(num_states) is int:
        num_states = [num_states]
    num_modalities = len(num_obs)

    A = obj_array(num_modalities)
    for modality, modality_obs in enumerate(num_obs):
        modality_shape = [modality_obs] + num_states
        modality_dist = np.random.rand(*modality_shape)
        A[modality] = norm_dist(modality_dist)
    return A 
    ```

- `B matrix`: transitioning likelihood matrix
  - This matrix model the likelihood of each transition between hidden states  considering the value of each control state.
  - This matrix encondes the agent's beliefs about how its actions affects the states of the world and its own states. 
  - ```python 
    def random_B_matrix(num_states, num_controls):
    if type(num_states) is int:
        num_states = [num_states]
    if type(num_controls) is int:
        num_controls = [num_controls]
    num_factors = len(num_states)
    assert len(num_controls) == len(num_states)

    B = obj_array(num_factors)
    for factor in range(num_factors):
        factor_shape = (num_states[factor], num_states[factor], num_controls[factor])
        factor_dist = np.random.rand(*factor_shape)
        B[factor] = norm_dist(factor_dist)
    return B
    ```

- `C Vector`: vector of preferences
  - Agent's preference for each possible observation. 

- `qs`: hidden states values after observation 
  - The posterior distribution is the agent’s updated belief about the state of the world after receiving new sensory evidence.
  - the infer_states method implements a variational message passing algorithm that approximates the posterior distribution by minimizing the variational free energy.