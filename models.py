import pickle
import numpy as np
import copy

class TicTacAgent:
    def __init__(self):
        super().__init__()
        self.STATES = dict()
        self.ACTIONS = np.arange(9)
        self.step = 0
        self.MODEL_FILE_NAME = "tictactoe_model_1.pkl"
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

    def update_value_function(self, prev_state, action, next_state):
        prev_state_str = TicTac.string_state(prev_state)
        next_state_str = TicTac.string_state(next_state)
        reward = TicTacAgent.calc_reward(prev_state, action, next_state)
            
        # initialize if needed
        if prev_state_str not in self.STATES:
            self.STATES[prev_state_str] = {"return": 0, "by_actions":[{"reward":0} for k in range(9)]}
        if "next_state_str" not in self.STATES[prev_state_str]["by_actions"][action]:
            self.STATES[prev_state_str]["by_actions"][action]["next_state_str"] = next_state_str
            self.STATES[prev_state_str]["by_actions"][action]["reward"] = reward
        
        # update all states
        for state_str in self.STATES:
            state = TicTac.state_from_str(state_str)
            action_probability = self.avg_action_policy(state)
            return_val = 0
            for ia,action_probability in enumerate(action_probability):
                try:
                    try:
                        next_state_str = self.STATES[state_str]["by_actions"][ia]["next_state_str"]
                        next_state_return = self.STATES[next_state_str]["return"]
                    except:
                        next_state_return = 0
                    return_per_action = (self.STATES[state_str]["by_actions"][ia]["reward"] + self.GAMMA*next_state_return)
                except:
                    return_per_action = 0
                return_val += action_probability*return_per_action
            self.STATES[state_str]["return"] = return_val
                 

    def calc_return(self, state):
        state_str = TicTac.string_state(state)
        return self.STATES[state_str]["return"] if state_str in self.STATES else 0

    def action_policy(self, state):
        state_str = TicTac.string_state(state)
        prob = np.zeros(9)
        action_probability = self.avg_action_policy(state)
        for action,action_probability in enumerate(action_probability):
            try:
                try:
                    next_state_str = self.STATES[state_str]["by_actions"][action]["next_state_str"]
                    next_state_return = self.STATES[next_state_str]["return"]
                except:
                    next_state_return = 0
                return_per_action = (self.STATES[state_str]["by_actions"][action]["reward"] + self.GAMMA*next_state_return)
            except:
                return_per_action = 0
            prob[action] = pow(2,return_per_action)
        total = np.sum(prob)
        return prob/(total + 0.000001)

    def save_model(self):
        with open(self.MODEL_FILE_NAME, "wb") as fid:
            pickle.dump(self.STATES, fid)
    
    def load_model(self):
        if os.path.isfile(self.MODEL_FILE_NAME):
            with open(self.MODEL_FILE_NAME, "rb") as fid:
                self.STATES = pickle.load(fid)
        else:
            self.STATES = dict()
            
    def explore(self, TOTAL_STEPS=10000):
        self.win_count = np.zeros(2,dtype=np.int)
        self.step = 0
        ticTac = TicTac()
        for step in range(TOTAL_STEPS):
            action = self.calc_action(ticTac.state)
            prev_state = copy.deepcopy(ticTac.state)
            ticTac.perform(action)
            reward = self.calc_reward(prev_state, action, ticTac.state)
            self.update_value_function(prev_state, action, ticTac.state)
            # print("{2}:{0}:{1},".format(action, reward, TicTac.string_state(ticTac.state)),end='')
            if reward in [TicTacAgent.REWARD_WIN_1, TicTacAgent.REWARD_WIN_0, TicTacAgent.REWARD_DRAW]:
                self.step = 0
                ticTac = TicTac()
                if reward == TicTacAgent.REWARD_WIN_1:
                    self.win_count[1] += 1
                elif  reward == TicTacAgent.REWARD_WIN_0:
                    self.win_count[0] += 1
                print("win count:", self.win_count)
                print("state count:", len(self.STATES))
                # print("")
            else:
                self.step += 1
        self.save_model()

    def monitor(self):
        self.win_count = np.zeros(2,dtype=np.int)
        self.step = 0
        ticTac = TicTac()
        for step in range(20):
            action_probability = np.round(100*self.action_policy(ticTac.state))
            return_val = self.calc_return(ticTac.state)
            print('--'*10, step, self.step)
            ticTac.print_state()
            print("action:", action_probability.reshape((3,3)))
            print("return:", return_val)
            
            action = self.calc_action(ticTac.state)
            print("action:", action)
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
                # action_probability = np.round(100*self.action_policy(prev_state))
                # return_val = np.round(self.calc_return(prev_state))
                # print(prev_state.reshape((3,3)))
                # print(action_probability.reshape((3,3)))
                # print(return_val)
                
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

class TicTac(object):
    def __init__(self):
        self.state = -np.ones((9), dtype=np.int)
        self.action = -1
        self.turn = True
    
    STATES = set()
    @staticmethod
    def calc_all_states(prev_state, turn=1):
        count = 1
        prev_state_str = TicTac.string_state(prev_state)
        TicTac.STATES.add(prev_state_str)
        for action in range(9):
            if prev_state[action] != -1:
                continue
            state = copy.deepcopy(prev_state)
            state[action] = turn
            count += TicTac.calc_all_states(state,  1-turn)
        return count

    @staticmethod
    def calc_all_states():
        counts = np.zeros(10)
        counts[0] = 1                   # 0c0
        counts[1] = 9                   # 9c1 = 9
        counts[2] = 9*8                 # 9c1* 8c1 = 9*8
        counts[3] = 9*8*7/2             # 9c2* 7c1 = 36*7
        counts[4] = 9*8*7*6/2/2         # 9c2* 7c2 = 36*21
        counts[5] = 9*8*7*6*5/(3*2)/2   # 9c3* 6c2 = 84*15
        counts[6] = 9*8*7*6*5*4/(3*2)/(3*2)                 # 9c3* 6c3 = 84*20
        counts[7] = 9*8*7*6*5*4*3/(4*3*2*1)/(3*2*1)         # 9c4* 5c3 = 126*10
        counts[8] = 9*8*7*6*5*4*3*2/(4*3*2*1)/(4*3*2*1)     # 9c4* 5c4 = 126*5
        counts[9] = 9*8*7*6*5*4*3*2*1/(5*4*3*2*1)/(4*3*2*1) # 9c5* 4c4 = 126
        return np.sum(counts)

    @staticmethod
    def get_finishing_states_win_count():
        win_count = np.zeros(3,dtype=np.int)
        for i0 in range(9):
            for i1 in range(i0+1,9):
                for i2 in range(i1+1,9):
                    for i3 in range(i2+1,9):
                        # ind = np.array([i0,i1,i2,i3],dtype=np.int)
                        # if any(ind == 0):
                        #     continue
                        state = np.ones(9, dtype=np.int)
                        state[[i0,i1,i2,i3]] = 0
                        result = TicTac.who_won(state)
                        # print(state, result)
                        
                        if result == 1:
                            win_count[1] += 1
                        elif result == 0:
                            win_count[0] += 1
                        elif result == -2:
                            win_count[2] += 1
        print(win_count)
        return win_count


    def is_action_valid(self, action):
        return self.state[action] == -1
    
    def perform(self, action):
        if self.is_action_valid(action):
            self.state[action] = int(self.turn)
            self.turn = not self.turn
        else:
            print("not allowed")

    def print_state(self):
        print(TicTac.render(self.state))

    @staticmethod
    def render(state):
        str_val = ""
        for r in range(3):
            for c in range(3):
                id = r*3+c
                if state[id] == 1:
                    str_val += '|x|'
                elif state[id] == 0:
                    str_val += '|o|'
                elif state[id] == -1:
                    str_val += '| |'
            str_val += '\n' + '-'*10 + '\n'
        return str_val
                
                
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
