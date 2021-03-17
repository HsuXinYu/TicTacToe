import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class TicTacToeEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.MultiDiscrete([3]*9)
        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    
    def step(self, action):
        reward =0
        done = False
        observation = self.state

        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        count = np.sum(self.state==2)
        turn = int(1-count%2)
        if self.state[action] != 2:
            reward = -1
        else:
            self.state[action] = turn
            winner_id, done= TicTacToeEnv.who_won(self.state)
            if done:
                if winner_id == 1:
                    reward = 1
                else:
                    reward = -1
            else:
                reward = 0
        observation = self.state
        
        return observation, reward, done, {}
    
    @staticmethod
    def who_won(state):
        if state[0] != 2:
            if state[0] == state[1] and state[0] == state[2]:
                return state[0], True
            elif state[0] == state[3] and state[0] == state[6]:
                return state[0], True
            elif state[0] == state[4] and state[0] == state[8]:
                return state[0], True
        if state[1] != 2:
            if state[1] == state[4] and state[1] == state[7]:
                return state[1], True
        if state[2] != 2:
            if state[2] == state[4] and state[2] == state[6]:
                return state[2], True
            elif state[2] == state[5] and state[2] == state[8]:
                return state[2], True
        if state[3] != 2:
            if state[3] == state[4] and state[3] == state[5]:
                return state[3], True
        if state[6] != 2:
            if state[6] == state[7] and state[6] == state[8]:
                return state[6], True
        if all(state != 2):
            return 2, True
        return 2, False
    
    def reset(self):
        self.close()
        self.state = self.observation_space.nvec-1
        self.steps_beyond_done = None
        return self.state

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400
        size = 50
        
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            self.boxes = []
            for i,val in enumerate(self.state):
                # if val == 2:
                #     continue
                xoffset = (i%3-1)*size*1.1 + screen_width//2
                yoffset = (i//3-1)*size*1.1 + screen_height//2
                
                l, r, t, b = xoffset-size / 2, xoffset+size / 2, yoffset+size / 2, yoffset-size / 2
                
                player = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
                playertrans = rendering.Transform()
                player.add_attr(playertrans)
                self.boxes.append(player)
                self.viewer.add_geom(player)
            
            for i in range(2):
                x = screen_width//2 - (size//2)*1.05 + i*size*1.05
                y = screen_height//2 - (size//2)*1.05 + i*size*1.05
                track = rendering.Line((x, 0), (x, screen_height))
                track.set_color(0, 0, 0)
                self.viewer.add_geom(track)
                track = rendering.Line((0, y), (screen_width, y))
                track.set_color(0, 0, 0)
                self.viewer.add_geom(track)
        if self.state is None:
            return None

        for i,val in enumerate(self.state):
            if val == 2:
                continue
            elif val == 0:
                self.boxes[i].set_color(1.0,0,0)
            else:
                self.boxes[i].set_color(0,1.0,0)

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

