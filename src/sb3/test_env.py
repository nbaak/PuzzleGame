
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from sb3.environment import Environment as Env


def test():
    env = Env()

    for _ in range(10):
        sample = env.action_space.sample()
        print(sample, type(sample), sample[0], sample[1])
        print(tuple(sample))

    env.game.show()
    print(env.observe())
    print(len(env.observe()))


if __name__ == "__main__":
    test()

