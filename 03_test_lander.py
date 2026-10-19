
import gymnasium as gym
from stable_baselines3 import PPO
import numpy as np

env = gym.make("LunarLander-v3", render_mode="human")
model = PPO.load("ppo_lander")

rewards = []
successful_landings = 0
episodes = 20

for episode in range(episodes):
    observation, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0

    while not (terminated or truncated):
        action, _ = model.predict(observation, deterministic=True)

        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    rewards.append(total_reward)

    # LunarLander awards a positive terminal reward for a safe landing.
    # We'll use the episode score as a preliminary indicator here.
    if total_reward >= 200:
        successful_landings += 1

    print(f"Episode {episode + 1}: reward = {total_reward:.2f}")

print("\n--- Evaluation Summary ---")
print(f"Average reward: {np.mean(rewards):.2f}")
print(f"Best reward: {np.max(rewards):.2f}")
print(f"Worst reward: {np.min(rewards):.2f}")
print(f"Episodes scoring 200+: {successful_landings}/{episodes}")

env.close()
