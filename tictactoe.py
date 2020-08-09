import os
import numpy as np
import cv2
import copy
import pickle

class TicTacAgent:
    def __init__(self):
        super().__init__()
        self.STATES = dict()
        self.ACTIONS = np.arange(9)
        self.step = 0
        self.MODEL_FILE_NAME = "tictactoe_model.pkl"
        self.load_model()
    
    REWARD_WIN_1 = 100
    REWARD_WIN_0 = -100
    REWARD_DRAW = 5
    REWARD_PLAY = 1
    GAMMA = 0.9
    
    @staticmethod
    def avg_action_policy(state):
        a = (state==-1).astype(np.float)
        total = np.sum(a)
        return a/total
    
    @staticmethod
    def calc_reward(prev_state, action, next_state):
        if all(next_state == prev_state):
            return 0
        result = TicTac.who_won(next_state)
        if result == 0:
            return TicTacAgent.REWARD_WIN_0
        if result == 1:
            return TicTacAgent.REWARD_WIN_1
        if result == -2:
            return TicTacAgent.REWARD_DRAW
        return TicTacAgent.REWARD_PLAY

    def calc_action(self, state):
        action_policy = TicTacAgent.avg_action_policy(state) 
        action = np.random.choice(np.arange(9),1,p=action_policy.reshape(-1))[0]
        return action

    def update_return(self, prev_state, action, next_state):
        prev_state_str = TicTac.string_state(prev_state)
        next_state_str = TicTac.string_state(next_state)
        reward = TicTacAgent.calc_reward(prev_state, action, next_state)
            
        # initialize if needed
        if prev_state_str not in self.STATES:
            self.STATES[prev_state_str] = [{"return":-1000, "step":-100, "count":0} for k in range(9)]
            for k in range(9):
                if prev_state[k] == -1: 
                    self.STATES[prev_state_str][k]["return"] = 1
        
        # update time reference
        self.STATES[prev_state_str][action]["step"] = self.step

        # update all states
        for state_str in self.STATES:
            state = TicTac.state_from_str(state_str)
            dt = (self.step - self.STATES[state_str][action]["step"])
            if dt >= 0 and dt < 10:
                if self.STATES[state_str][action]["step"] % 2 == 1 and reward in [TicTacAgent.REWARD_WIN_0, TicTacAgent.REWARD_WIN_1]:
                    reward_sign = -1    
                else:
                    reward_sign = 1
                self.STATES[state_str][action]["return"] = (self.STATES[state_str][action]["return"]*self.STATES[prev_state_str][action]["count"] +
                                        reward_sign*pow(TicTacAgent.GAMMA, dt)*reward)/(self.STATES[prev_state_str][action]["count"] + 1)
                self.STATES[prev_state_str][action]["count"] += 1
                

    def calc_return(self, state):
        return_val = -np.ones(9)
        state_str = TicTac.string_state(state)
        if state_str in self.STATES:
            for i,k in enumerate(self.STATES[state_str]):
                return_val[i] = k["return"]
        return return_val

    def action_policy(self, state):
        return_val = self.calc_return(state)
        exp_return_val = pow(2, return_val)
        total = np.sum(exp_return_val)
        return exp_return_val/(total + 0.000001)

    def save_model(self):
        with open(self.MODEL_FILE_NAME, "wb") as fid:
            pickle.dump(self.STATES, fid)
    
    def load_model(self):
        if os.path.isfile(self.MODEL_FILE_NAME):
            with open(self.MODEL_FILE_NAME, "rb") as fid:
                self.STATES = pickle.load(fid)
        else:
            self.STATES = dict()
            
    def explore(self):
        self.win_count = np.zeros(2,dtype=np.int)
        self.step = 0
        ticTac = TicTac()
        for step in range(10000):
            action = self.calc_action(ticTac.state)
            prev_state = copy.deepcopy(ticTac.state)
            ticTac.perform(action)
            reward = self.calc_reward(prev_state, action, ticTac.state)
            self.update_return(prev_state, action, ticTac.state)
            # print("{2}:{0}:{1},".format(action, reward, TicTac.string_state(ticTac.state)),end='')
            if reward in [TicTacAgent.REWARD_WIN_1, TicTacAgent.REWARD_WIN_0, TicTacAgent.REWARD_DRAW]:
                self.step = 0
                ticTac = TicTac()
                if reward == TicTacAgent.REWARD_WIN_1:
                    self.win_count[1] += 1
                elif  reward == TicTacAgent.REWARD_WIN_0:
                    self.win_count[0] += 1
                print("win count:", self.win_count)    
                # print("")
            else:
                self.step += 1
        self.save_model()

    def monitor(self):
        self.win_count = np.zeros(2,dtype=np.int)
        self.step = 0
        ticTac = TicTac()
        for step in range(20):
            # action_probability = np.round(100*self.action_policy(ticTac.state))
            # return_val = np.round(self.calc_return(ticTac.state))
            # print(ticTac.state.reshape((3,3)))
            # print(action_probability.reshape((3,3)))
            # print(return_val.reshape((3,3)))
            
            action = self.calc_action(ticTac.state)
            prev_state = copy.deepcopy(ticTac.state)
            ticTac.perform(action)
            reward = self.calc_reward(prev_state, action, ticTac.state)
            # self.update_return(prev_state, action, ticTac.state)
            if reward in [TicTacAgent.REWARD_WIN_0, TicTacAgent.REWARD_WIN_1, TicTacAgent.REWARD_DRAW]:
                self.step = 0
            else:
                self.step += 1
            # print("step:{0}, action:{1}, reward:{2}, state:{3},".format(self.step, action, reward, TicTac.string_state(ticTac.state)))
            if reward in [TicTacAgent.REWARD_WIN_0, TicTacAgent.REWARD_WIN_1, TicTacAgent.REWARD_DRAW]:
                action_probability = np.round(100*self.action_policy(prev_state))
                return_val = np.round(self.calc_return(prev_state))
                print(prev_state.reshape((3,3)))
                print(action_probability.reshape((3,3)))
                print(return_val.reshape((3,3)))
                
                if reward == TicTacAgent.REWARD_WIN_1:
                    self.win_count[1] += 1
                elif  reward == TicTacAgent.REWARD_WIN_0:
                    self.win_count[0] += 1
                print("win count:", self.win_count)    
                
                print("New Game")
                ticTac = TicTac()
            
        
    @staticmethod
    def find_symmatric_states(state):
        states = set()
        state_mat = state.reshape((3,3))
        states.addstate_mat.reshape(-1)
        states.add(state_mat[2::-1,:].reshape(-1))
        states.add(state_mat[:,2::-1].reshape(-1))
        states.add(state_mat[2::-1,2::-1].reshape(-1))
        states.add(state_mat.T.reshape(-1))
        states.add(state_mat[2::-1,:].T.reshape(-1))
        states.add(state_mat[:,2::-1].T.reshape(-1))
        states.add(state_mat[2::-1,2::-1].T.reshape(-1))
        return states

    
class TicTac:
    def __init__(self):
        self.state = -np.ones((9), dtype=np.int)
        self.action = -1
        self.turn = True
    
    @staticmethod
    def calc_all_states():
        count = 0
        state = -np.ones((9), dtype=np.int)
        for action in range(9):
            if state[action] != -1:
                continue
            count += 1
            state[action] = 1
            for action in range(9):
                if state[action] != -1:
                    continue
                count += 1
                state[action] = 0
                
    def is_action_valid(self, action):
        return self.state[action] == -1
    
    def perform(self, action):
        if self.is_action_valid(action):
            self.state[action] = int(self.turn)
            self.turn = not self.turn
        else:
            print("not allowed")

    def print_state(self):
        print(self.state.reshape((3,3)))

    @staticmethod
    def string_state(state):
        str_val = ""
        for i,k in enumerate(state):
            if k == 1:
                str_val += 'B'
            elif k == 0:
                str_val += 'A'
            else:
                str_val += 'Z'
        return str_val

    @staticmethod
    def state_from_str(str_val):
        state = -np.ones(9, dtype=int)
        for k in range(9):
            if str_val[k]=='A':
                state[k] = 0
            elif str_val[k] == 'B':
                state[k] = 1
        return state
    @staticmethod
    def who_won(state):
        if state[0] != -1:
            if state[0] == state[1] and state[0] == state[2]:
                if state[0] == 0:
                    return 0
                else:
                    return 1
            elif state[0] == state[3] and state[0] == state[6]:
                if state[0] == 0:
                    return 0
                else:
                    return 1
            elif state[0] == state[4] and state[0] == state[8]:
                if state[0] == 0:
                    return 0
                else:
                    return 1
        if state[1] != -1:
            if state[1] == state[4] and state[1] == state[7]:
                if state[1] == 0:
                    return 0
                else:
                    return 1
        if state[2] != -1:
            if state[2] == state[4] and state[2] == state[6]:
                if state[2] == 0:
                    return 0
                else:
                    return 1
            elif state[2] == state[5] and state[2] == state[8]:
                if state[2] == 0:
                    return 0
                else:
                    return 1
        if state[3] != -1:
            if state[3] == state[4] and state[3] == state[5]:
                if state[3] == 0:
                    return 0
                else:
                    return 1
        if state[6] != -1:
            if state[6] == state[7] and state[6] == state[8]:
                if state[6] == 0:
                    return 0
                else:
                    return 1
        if all(state != -1):
            return -2
        return -1

    def play(self):
        self.__init__()
        while(1):
            self.print_state()
            action = input("input player {0}:".format(int(self.turn) + 1))
            action = ord(action[0]) - ord('0')
            if action < 0 or action > 8:
                print("not allowed")
            self.perform(action)
            result = self.who_won()

            if result == 0 or result == 1:
                print("player {0} won".format(result))
                break
            if result == -1:
                self.print_state()
                print("Draw")
                break
            if result == -2:
                print("not finished")


if __name__ == "__main__":
    # ticTac = TicTac()
    # ticTac.play()
    tictacAgent = TicTacAgent()
    # tictacAgent.explore()
    tictacAgent.monitor()
    