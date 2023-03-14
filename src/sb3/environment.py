import numpy as np
import gym
from gym import spaces

from Game import Game


class Environment(gym.Env):

    def __init__(self, width=5, height=4, level=0) -> None:
        super().__init__()

        self.game = Game(width, height, level)
        self.done = False

        self.action_space = spaces.MultiDiscrete(np.array([self.game.width, self.game.height]))

        n_channels = len(self.observe())
        self.observation_space = spaces.Box(-1, 100, shape=(n_channels,), dtype=np.int64)
        
        self.history = None # maybe a queue to observe the last n games, maaaaybe even the last moves + last obs

    def step(self, action:np.array) -> tuple[np.array, int, bool, dict]:
        action = tuple(action)
        reward = 0

        value = self.game.queue[0]
        placed = self.game.place_at(value, action, do_step=True)

        if placed == value:
            pts, gameover = self.game.check_rules(action, value)
            reward += pts

            while pts > 0:
                pts, gameover = self.game.check_rules(action, value)
                reward += pts

            if gameover:
                self.done = True

        observation = self.observe()
        info = {}

        return observation, reward, self.done, info

    def observe(self) -> np.array:
        flat_field = list(np.array(self.game.field).flatten())
        queue = self.game.queue

        observation = flat_field + queue

        return np.array(observation).flatten()

    def reset(self) -> np.array:
        self.game.reset()
        self.done = False

        return self.observe()


if __name__ == "__main__":
    env = Environment()

