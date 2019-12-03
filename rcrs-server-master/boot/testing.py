import gym
import RCRS_gym


import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import time 
import subprocess
from subprocess import *

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
# from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize, VecEnv
# from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import PPO2, DQN
# from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines import DDPG
from stable_baselines.ddpg import AdaptiveParamNoiseSpec


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

best_mean_reward, n_steps = -np.inf, 0
def callback(_locals, _globals):
    global n_steps, best_mean_reward
    # Print stats every 1000 calls
    if (n_steps + 1) % 10 == 0:
# Evaluate policy training performance
        x, y = ts2xy(load_results(log_dir), 'timesteps')
        if len(x) > 0:
            mean_reward = np.mean(y[-100:])
            print(x[-1], 'timesteps')
            print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward))
            best_mean_reward = mean_reward
            print("Saving new best model")
            _locals['self'].save(log_dir + 'best_model.pkl')
            # New best model, you could save the agent here
            # if mean_reward > best_mean_reward:
                # best_mean_reward = mean_reward
                # Example for saving best model
                # print("Saving new best model")
                # _locals['self'].save(log_dir + 'best_model.pkl')
    n_steps += 1
    return True


# Create log dir
log_dir = "/u/animesh9/Documents/RoboCup-gRPC/plots/"
os.makedirs(log_dir, exist_ok=True)
# Create and wrap the environment
env = gym.make('RCRS-v2')
env = Monitor(env, log_dir, allow_early_resets=True)
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: env]) 
# Automatically normalize the input features
env = VecNormalize(env, norm_obs=True, norm_reward=False,
                   clip_obs=10.)

# Add some param noise for exploration
# param_noise = AdaptiveParamNoiseSpec(initial_stddev=0.1, desired_action_stddev=0.1)
# Because we use parameter noise, we should use a MlpPolicy with layer normalization
model = PPO2(MlpPolicy, env, verbose=1, tensorboard_log = "./ppo2_rcrs_tensorboard/", n_steps = 100)
# Train the agent
model.learn(total_timesteps=int(300), callback=callback)

model.save("rcrs_gym")
del model  # delete trained model to demonstrate loading

# Load the trained agent
model = PPO2.load("rcrs_gym")

obs = env.reset()
# print(obs)
# int(input("pause.."))
final_rewards = []
for i in range(1000):
    action, _states = model.predict(obs)
    print(action)
    # int(input("pause.."))
    # action=[2]
    obs, rewards, dones, info = env.step(action)
    # print(obs)
    # print(dones)
    # int(input("pause.."))
    if dones == True:
        final_rewards.append(rewards)
    print(final_rewards)
    print(i)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print(np.mean(final_rewards))
print(stats.sem(final_rewards))
subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/kill.sh", shell=True)