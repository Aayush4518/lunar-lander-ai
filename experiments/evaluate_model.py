
import argparse
import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO


parser = argparse.ArgumentParser()
parser.add_argument("--model", required=True)
parser.add_argument("--episodes", type=int, default=20)
parser.add_argument("--render", action="store_true")
args = parser.parse_args()

env = gym.make(
    "LunarLander-v3",
    render_mode="human" if args.render else None,
)

model = PPO.load(args.model, device="cpu")

rewards = []
successful_landings = 0
crashes = 0
timeouts = 0

for episode in range(args.episodes):
    obs, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0.0
    outcome = "unknown"

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)

        # Accumulate EVERY step's reward.
        total_reward += reward

        # Classify the terminal event separately.
        if terminated:
            if reward >= 100:
                outcome = "landed"
            elif reward <= -100:
                outcome = "crashed"
            else:
                outcome = "other"
        elif truncated:
            outcome = "timeout"

    rewards.append(total_reward)
    successful_landings += int(outcome == "landed")
    crashes += int(outcome == "crashed")
    timeouts += int(truncated)

    print(
        f"Episode {episode + 1}: "
        f"total reward={total_reward:.2f}, "
        f"outcome={outcome}"
    )

print("\n--- Evaluation Summary ---")
print(f"Average reward: {np.mean(rewards):.2f}")
print(f"Best reward: {np.max(rewards):.2f}")
print(f"Worst reward: {np.min(rewards):.2f}")
print(f"Successful landings: {successful_landings}/{args.episodes}")
print(f"Crashes: {crashes}/{args.episodes}")
print(f"Timeouts: {timeouts}/{args.episodes}")

env.close()
