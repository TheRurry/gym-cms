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
        while len(mshards) < 20:
	    new_pos = [rnd.randint(0,63), rnd.randint(0,63)]
            if new_pos not in mshards:
                mshards.append(new_pos)
        marines = np.random.rand(64, size = (20, 2))
        step = 0
        return (self.marines, self.mshards)
    
    def step(self, action):
        reward = 0
      
        for marine in marines:
            if marine in mshard:
                mshard.remove(marine)
                reward += 1
          
        action = [-1,-1]
        actions[0] = action / 4
        actions[1] = action % 4
      
        for x in range(0,2):
            if actions[x] == 0: # UP
                marines[x][1] -= 1
            elif actions[x] == 1: # DOWN
                marines[x][1] += 1
            elif actions[x] == 2: # LEFT
                marines[x][0] -= 1
            elif actions[x] == 3: # RIGHT
                marines[x][0] += 1
          
        step += 1
        done = False
        if step == 240:
            done = True
      
        state = (self.marines, self.mshards)
        return state, reward, done, {} 
