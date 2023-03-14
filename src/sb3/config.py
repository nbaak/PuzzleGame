
import os
from stable_baselines3 import PPO as _Algorithm

Algorithm = _Algorithm

TIMESTEPS = 10_000  # save every n steps

# models fodler
models_fodler_name:str = 'models'

# model name
model_name:str = Algorithm.__name__

# saving
models_dir:str = f"{models_fodler_name}/{model_name}"

# TODO: loading
IN_FILE_NAME = Algorithm.__name__
in_model_file = ""
in_models_dir = f"models/{IN_FILE_NAME}"
in_model_path = f"{in_models_dir}/{in_model_file}"

# logging
logdir = "logs"


def get_algorithm_name():
    return Algorithm.__name__


def set_model(name:str):
    global model_name, models_dir
    model_name = name
    models_dir = f"{models_fodler_name}/{model_name}"


def ensure_dirs():
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    if not os.path.exists(logdir):
        os.makedirs(logdir)

