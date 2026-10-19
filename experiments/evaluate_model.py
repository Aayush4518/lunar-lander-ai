
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
timeouts = 0

for episode in range(args.episodes):
    obs, info = env.reset()
    terminated = False
    truncated = False
    total_reward = 0.0

    while not (terminated or truncated):
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward

    # Approximate safe landing check using final state.
    vx, vy, angle = obs[2], obs[3], obs[4]
    left_leg = obs[6] > 0.5
    right_leg = obs[7] > 0.5

    landed_safely = (
        terminated
        and left_leg
        and right_leg
        and abs(vx) < 0.2
        and abs(vy) < 0.2
        and abs(angle) < 0.2
    )

    successful_landings += int(landed_safely)
    timeouts += int(truncated)
    rewards.append(total_reward)

    print(
        f"Episode {episode + 1}: "
        f"reward={total_reward:.2f}, "
        f"safe_landing={landed_safely}, "
        f"timeout={truncated}"
    )

print("\n--- Evaluation Summary ---")
print(f"Average reward: {np.mean(rewards):.2f}")
print(f"Best reward: {np.max(rewards):.2f}")
print(f"Worst reward: {np.min(rewards):.2f}")
print(f"Likely safe landings: {successful_landings}/{args.episodes}")
print(f"Timeouts: {timeouts}/{args.episodes}")

env.close()
