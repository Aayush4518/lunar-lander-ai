
import gymnasium as gym
from stable_baselines3 import PPO

env = gym.make("LunarLander-v3", render_mode="human")
model = PPO.load("ppo_lander")

for episode in range(5):
    observation, info = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, _ = model.predict(observation, deterministic=True)

        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated

    print(f"Episode {episode + 1}: reward = {total_reward:.2f}")

env.close()
