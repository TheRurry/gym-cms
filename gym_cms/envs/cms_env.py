# Two marines on the 32x32 map

import random as rnd
import numpy as np
import gym
from gym import spaces

EMPTY = 0
MARINE = 1
MINERAL = 2

HEIGHT = 16
WIDTH = 16

class CmsEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(16)
        self.observation_space = spaces.Box(low=np.zeros(WIDTH * HEIGHT), high=np.zeros(WIDTH * HEIGHT) + 2)
        # self.observation_space = spaces.Box(low=0, high=2, shape=(1,))
        self.marines = []
        self.mshards = []
        self.steps = 0
        self.reset()

    def reset(self):
        self.marines = []
        self.mshards = []

        while len(self.mshards) < 20:
            new_pos = [rnd.randint(0,HEIGHT - 1), rnd.randint(0,HEIGHT - 1)]
            if new_pos not in self.mshards:
                self.mshards.append(new_pos)
        self.marines.append([rnd.randint(0,WIDTH - 1), rnd.randint(0,HEIGHT - 1)])
        self.marines.append([rnd.randint(0,WIDTH - 1), rnd.randint(0,HEIGHT - 1)])
        self.steps = 0
        return self.observation()

    def observation(self):
        observation = [EMPTY] * WIDTH * HEIGHT
        for shard in self.mshards:
            observation[shard[0] + HEIGHT * shard[1]] = MINERAL
        for marine in self.marines:
            observation[marine[0] + HEIGHT * marine[1]] = MARINE
        return np.array(observation)

    def step(self, action):
        reward = 0

        zombies = []

        for marine in self.marines:
            if marine in self.mshards:
                zombies.append(marine)
                reward += 1

        for zombie in zombies:
            if zombie in self.mshards:
                self.mshards.remove(zombie)

        actions = [-1,-1]
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
                if self.marines[x][y] >= HEIGHT:
                    self.marines[x][y] = HEIGHT - 1
                elif self.marines[x][y] < 0:
                    self.marines[x][y] = 0

        self.steps += 1
        done = False
        if self.steps == 240 or len(self.mshards) == 0:
            done = True
            print("Rem Shards:", len(self.mshards))

        state = self.observation()
        return state, reward, done, {}
