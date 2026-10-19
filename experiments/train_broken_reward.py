
import gymnasium as gym
from stable_baselines3 import PPO


class BrokenRewardWrapper(gym.Wrapper):
    def step(self, action):
        observation, original_reward, terminated, truncated, info = (
            self.env.step(action)
        )

        # Observation: x, y, vx, vy, angle, angular velocity,
        # left leg contact, right leg contact
        x, y, vx, vy, angle, angular_velocity, left_leg, right_leg = observation

        # THE BAIT: reward the lander for staying upright and slow.
        hover_bonus = 0.0

        if (
            abs(angle) < 0.1
            and abs(vx) < 0.1
            and abs(vy) < 0.1
        ):
            hover_bonus = 1.0

        # Add our custom reward to LunarLander's original reward.
        shaped_reward = original_reward + hover_bonus

        info["original_reward"] = original_reward
        info["hover_bonus"] = hover_bonus

        return (
            observation,
            shaped_reward,
            terminated,
            truncated,
            info,
        )


# Train a NEW model using the flawed reward.
env = BrokenRewardWrapper(gym.make("LunarLander-v3"))

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
model.save("models/ppo_broken_reward")

env.close()

print("\nTraining complete! Broken-reward model saved.")


# Evaluate it in the ORIGINAL environment reward.
print("\nEvaluating in the original environment...")

eval_env = gym.make("LunarLander-v3", render_mode="human")
model = PPO.load("models/ppo_broken_reward")

for episode in range(5):
    observation, info = eval_env.reset()
    terminated = False
    truncated = False

    original_total = 0.0
    hover_frames = 0
    steps = 0

    while not (terminated or truncated):
        action, _ = model.predict(observation, deterministic=True)

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
            hover_frames += 1

    print(
        f"Episode {episode + 1}: "
        f"original reward = {original_total:.2f}, "
        f"upright/slow frames = {hover_frames}/{steps}"
    )

eval_env.close()
