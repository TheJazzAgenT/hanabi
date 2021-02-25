import tensorflow as tf
import tf_agents as tfa
import numpy as np
import game as H


class HanabiEnv:
    def __init__(self, num_players, num_suits):
        # current state of the board
        self.state = None
        # reward value for the PREVIOUS ACTION ONLY - not total
        self.reward = None
        # previous action taken
        self.action = None
        # Make the game - default is 5 suits, change if needed. ALSO CHANGE IN self.reset IF NEEDED
        self.game = H.game(num_players,deck_type = 'deck50')
        self.current_player = 0
        self.NUM_SUITS = num_suits
        self.NUM_PLAYERS = num_players
        self.ACTION_SPEC = self.HanabiActionSpec(num_players,num_suits).action
        self.TIME_STEP_SPEC = self.HanabiStateSpec(num_players,num_suits)
        return

    def step(self,action):
        # convert to action for game, update the game, return the new state

        # convert vector representation of action into framework action
        self.action = self._vector_to_action(action)
        # update the game, calculate reward function
        b4score = self.game.get_current_score()
        self.game.run_turn(self.game.players[self.current_player], self.action)
        self.reward = self.game.get_current_score() - b4score
        self.state = self._get_state_from_game()
        # update player
        self.current_player = (self.current_player + 1) % self.NUM_PLAYERS
        return self.state,self.reward

    def get_current_time_step(self):
        return self.state, self.reward

    def action_spec(self):
        return self.ACTION_SPEC

    def time_step_spec(self):
        # return an object with BoundedArraySpec attributes: describe state and reward
        return self.TIME_STEP_SPEC

    def reset(self):
        self.game = H.game(self.NUM_PLAYERS, deck_type='deck50')
        return

    def _get_state_from_game(self):
        # use the internals of the framework to generate state vector
        return self.game.board

    def _vector_to_action(self, action_vec):
        # whatever our representation for an action is, convert to game framework
        action = action_vec
        return action


    # Specs are in their own classes based on this link which indicates attributes
    # https://www.tensorflow.org/agents/tutorials/1_dqn_tutorial
    class HanabiTimeStepSpec:
        def __init__(self, num_players = 4, num_suits = 4):
            # change as needed
            shape = (32,1)
            self.state = tfa.specs.BoundedArraySpec((shape), dtype = np.int, minimum = [], maximum = [] )
            self.reward = tfa.specs.BoundedArraySpec((shape), dtype = np.int, minimum = [], maximum = [] )

    class HanabiActionSpec:
        def __init__(self, num_players = 4, num_suits = 4):
            # change shape as needed
            shape = (num_players,num_suits,5)
            self.action = tfa.specs.BoundedArraySpec((shape), dtype = np.int, minimum = [], maximum = [] )





