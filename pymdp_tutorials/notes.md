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