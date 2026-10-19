
import os
import gymnasium as gym
from stable_baselines3 import PPO


class FixedRewardWrapper(gym.Wrapper):
    def step(self, action):
        observation, original_reward, terminated, truncated, info = (
            self.env.step(action)
        )

        # Small penalty for spending another frame in the episode.
        time_penalty = 0.01
        shaped_reward = original_reward - time_penalty

        info["original_reward"] = original_reward
        info["time_penalty"] = time_penalty

        return (
            observation,
            shaped_reward,
            terminated,
            truncated,
            info,
        )


os.makedirs("models", exist_ok=True)

env = FixedRewardWrapper(gym.make("LunarLander-v3"))

model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    learning_rate=0.0003,
    n_steps=1024,
    batch_size=64,
    policy_kwargs=dict(net_arch=[64, 64]),
)

model.learn(total_timesteps=500_000)
model.save("models/ppo_fixed_reward")
env.close()

print("\nTraining complete! Fixed-reward model saved.")

# Evaluate using the ORIGINAL environment and reward.
eval_env = gym.make("LunarLander-v3", render_mode="human")
model = PPO.load("models/ppo_fixed_reward")

for episode in range(5):
    observation, info = eval_env.reset()
    terminated = False
    truncated = False
    original_total = 0.0
    upright_slow_frames = 0
    steps = 0

    while not (terminated or truncated):
        action, _ = model.predict(
            observation, deterministic=True
        )

        observation, reward, terminated, truncated, info = (
            eval_env.step(action)
        )

        original_total += reward
        steps += 1

        _, _, vx, vy, angle, _, _, _ = observation

        if (
            abs(angle) < 0.1
            and abs(vx) < 0.1
            and abs(vy) < 0.1
        ):
            upright_slow_frames += 1

    left_leg = observation[6] > 0.5
    right_leg = observation[7] > 0.5

    print(f"Leg contact: left={left_leg}, right={right_leg}")

    print(
        f"Episode {episode + 1}: "
        f"original reward = {original_total:.2f}, "
        f"upright/slow frames = "
        f"{upright_slow_frames}/{steps}, "
        f"terminated = {terminated}, "
        f"truncated = {truncated}"
    )

eval_env.close()
