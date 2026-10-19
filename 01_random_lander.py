
import gymnasium as gym

env = gym.make("LunarLander-v3", render_mode="human")

observation, info = env.reset()

print("Initial observation:", observation)
print("Observation shape:", observation.shape)
print("Available actions:", env.action_space)

print("Action meanings:")
for action in range(env.action_space.n):
    print("0 -> Do nothing")
print("1 -> Fire left engine")
print("2 -> Fire main engine")
print("3 -> Fire right engine")

for step in range(1000):
    action = env.action_space.sample()

    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        print("Episode ended. Restarting...")
        observation, info = env.reset()

env.close()
