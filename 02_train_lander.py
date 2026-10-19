import gymnasium as gym
from stable_baselines3 import PPO

#lunar lander environemnt

env= gym.make("LunarLander-v3")

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate= 0.0003,
    n_steps= 1024,
    batch_size= 64,
    policy_kwargs= dict(net_arch=[64,64]),

)

model.learn(total_timesteps= 100000)

model.save("ppo_lander")

env.close()
