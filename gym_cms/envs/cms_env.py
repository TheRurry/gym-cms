import random as rnd
import numpy as np
import gym
from gym import spaces

EMPTY = 0
MARINE = 1
MINERAL = 2

HEIGHT = 5
WIDTH = 5

class CmsEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(4)
        # self.observation_space = spaces.Box(low=np.array([0] * WIDTH * HEIGHT), high=np.array([2] * WIDTH * HEIGHT))
        self.observation_space = spaces.Box(low=0, high=2, shape=(HEIGHT, WIDTH))
        self.marines = []
        self.mshards = []
        self.steps = 0
        self.reset()

    def reset(self):
        self.marines = []
        self.mshards = []

        # while len(self.mshards) < 1:
        #     new_pos = [rnd.randint(0,HEIGHT - 1), rnd.randint(0,HEIGHT - 1)]
        #     if new_pos not in self.mshards:
        #         self.mshards.append(new_pos)

        new_pos = [2, 2]
        self.mshards.append(new_pos)
        new_pos = [4, 4]
        self.mshards.append(new_pos)

        self.marines.append([rnd.randint(0,WIDTH - 1), rnd.randint(0,HEIGHT - 1)])
        # self.marines.append([rnd.randint(0,WIDTH - 1), rnd.randint(0,HEIGHT - 1)])
        self.steps = 0
        return self.observation()

    # TODO change this
    def observation(self):
        inside = [EMPTY] * WIDTH
        observation = [inside] * HEIGHT
        for shard in self.mshards:
            observation[shard[1]][shard[0]] = MINERAL
        for marine in self.marines:
            observation[marine[1]][marine[0]] = MARINE
        return np.array(observation)

    def step(self, action):
        # print("-------- NEW STEP --------")

        reward = 0

        zombies = []

        # print("Step:", self.steps)
        # print(self.steps)
        # print(action)
        # print(self.marines)
        # print(self.mshards)

        # See if marine/s collides with a shard/s
        for marine in self.marines:
            if marine in self.mshards:
                zombies.append(marine)
                reward += 1

        #  Remove the shards that have been collided with
        for zombie in zombies:
            if zombie in self.mshards:
                self.mshards.remove(zombie)

        # Apply action
        if action == 0: # UP
            self.marines[0][1] -= 1
        elif action == 1: # DOWN
            self.marines[0][1] += 1
        elif action == 2: # LEFT
            self.marines[0][0] -= 1
        elif action == 3: # RIGHT
            self.marines[0][0] += 1

        # Check to see if marine has gone out of the map. Assume map is square
        boundary = False
        if self.marines[0][1] >= HEIGHT:
            boundary = True
            self.marines[0][1] = HEIGHT - 1
        elif self.marines[0][1] < 0:
            boundary = True
            self.marines[0][1] = 0
        if self.marines[0][0] >= WIDTH:
            boundary = True
            self.marines[0][0] = WIDTH - 1
        elif self.marines[0][0] < 0:
            boundary = True
            self.marines[0][0] = 0

        # if boundary:
        #     reward = -1

        self.steps += 1
        done = False
        if self.steps == 10 or len(self.mshards) == 0:
            done = True
            print("Steps taken:", self.steps)
            print("Rem Shards:", len(self.mshards))

        state = self.observation()
        # print(reward)
        return state, reward, done, {}
