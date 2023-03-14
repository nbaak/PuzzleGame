
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from sb3.environment import Environment as Env
import sb3.config as config
from sb3.config import Algorithm

# Config
env = Env()
env.reset()

config.set_model(f"{config.get_algorithm_name()}_{env.game.level}_{env.game.width}_{env.game.height}")

model = Algorithm("MlpPolicy", env, verbose=1, tensorboard_log=config.logdir)

print(config.model_name)
print(config.models_dir)

for iteration in range(2):
    model.learn(total_timesteps=config.TIMESTEPS, reset_num_timesteps=False, tb_log_name=config.model_name)
    model.save(f"{config.models_dir}/{config.TIMESTEPS*iteration}")
