import random as rnd
import numpy as np
import gym
from gym import spaces

class CmsEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(16)
        self.marines = []
        self.mshards = []
        self.step = 0
        self.reset()

    def reset(self):
        while len(self.mshards) < 20:
	    new_pos = [rnd.randint(0,63), rnd.randint(0,63)]
            if new_pos not in self.mshards:
                self.mshards.append(new_pos)
        self.marines = np.random.rand(64, size = (20, 2))
        self.step = 0
        return (self.marines, self.mshards)

    def step(self, action):
        reward = 0

        for marine in self.marines:
            if marine in self.mshard:
                self.mshard.remove(marine)
                reward += 1

        action = [-1,-1]
        actions[0] = action // 4
        actions[1] = action % 4

        # Apply action
        for x in range(0,2):
            if actions[x] == 0: # UP
                self.marines[x][1] -= 1
            elif actions[x] == 1: # DOWN
                self.marines[x][1] += 1
            elif actions[x] == 2: # LEFT
                self.marines[x][0] -= 1
            elif actions[x] == 3: # RIGHT
                self.marines[x][0] += 1

        # Check to see if marine has gone out of the map. Assume map is square
        for x in range(0,2):
            for y in range(0,2):
                if self.marines[x][y] >= 64:
                    self.marines[x][y] = 63
                elif self.marines[x][y] < 0:
                    self.marines[x][y] = 0

        self.step += 1
        done = False
        if self.step == 240:
            done = True

        state = (self.marines, self.mshards)
        return state, reward, done, {}
