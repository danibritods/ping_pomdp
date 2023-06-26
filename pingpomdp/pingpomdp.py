import gridlink
import pong
import model


class PongGridlink(gridlink.Gridlink):
    def observe(self):
        pass

    def act(self):
        pass

class PingPOMDP:
    def __init__(self):
        self.pong = pong.Pong()
        self.grid = PongGridlink()
        self.model = model.Model()
        #my_agent = Agent( A = A_array, B = B_array, C = C_vector)

    def predictable_feedback(self):
        pass

    def unpredictable_feedback(self):
        pass

    def agent_observe_and_act(self, observation): #-> action:
        qs = my_agent.infer_states(observation) # get posterior over hidden states (a multi-factor belief)
        # Do active inference
        q_pi, neg_efe = my_agent.infer_policies() # return the policy posterior and return (negative) expected free energies of each policy as well
        action = my_agent.sample_action()
        return action

    def step():
        if self.pong.event == "hit!":
            self.predictable_feedback()
        elif self.pong.event == "miss":
            self.unpredictable_feedback()
        else:
            observation = grid.observe(pong.state)
            action = agent_observe_and_act(observation)
            pong.step(grid.act(action))

