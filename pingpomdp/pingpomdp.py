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
        pass

    def env_state_is_desirable(self, env_state):
        pass

    def _sensory_feedback(env_state):
        pass

class PingPOMDP:
    def __init__(self):
        self.env = Pong()
        self.grid = PongGridlink()
        self.model = Model()
        #my_agent = Agent( A = A_array, B = B_array, C = C_vector)

    def step(self):
        env_state = self.env.state()
        observation = self.grid.observe(env_state)
        self.model.observe(observation)

        model_action = self.model.act()
        env_action = self.grid.act(model_action)
        self.env.step(env_action)
        

        self._apply_protocols(env_state)




if __name__ == "__main__":
    p = PingPOMDP()

    p.step()


























    # def agent_observe_and_act(self, observation): #-> action:
    #     qs = my_agent.infer_states(observation) # get posterior over hidden states (a multi-factor belief)
    #     # Do active inference
    #     q_pi, neg_efe = my_agent.infer_policies() # return the policy posterior and return (negative) expected free energies of each policy as well
    #     action = my_agent.sample_action()
    #     return action

        # if self.pong.event == "hit!":
        #     self.predictable_feedback()
        # elif self.pong.event == "miss":
        #     self.unpredictable_feedback()
        # else:
        #     observation = grid.observe(pong.state)
        #     action = agent_observe_and_act(observation)
        #     pong.step(grid.act(action))