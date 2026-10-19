
# Lunar Lander AI — Experiment Log

## Project objective
Train a PPO agent to land a spacecraft using Gymnasium LunarLander-v3.
Investigate reward shaping, reward hacking, and reward design.

## Experiment 1 — Baseline PPO (100,000 steps)

- Algorithm: PPO
- Environment: LunarLander-v3
- Network: 2 hidden layers, 64 units each
- Learning rate: 0.0003
- Training steps: 100,000
- Mean training reward at end: Not recorded yet

### Evaluation
- Evaluation episodes: 5
- Episode rewards: -160.91, -63.99, -34.92, -121.66, -118.14
- Average evaluation reward: -99.92
- Successful landings: 0/5
- Observations: No successful landings in the five test episodes.

## Experiment 2 — Baseline PPO (500,000 steps)

- Algorithm: PPO
- Environment: LunarLander-v3
- Network: 2 hidden layers, 64 units each
- Learning rate: 0.0003
- Training steps: 500,000
- Mean training reward at end: Pending

### Evaluation

- Evaluation episodes: 5
- Episode rewards: -111.29, 62.24, -57.83, 112.10, 57.82
- Average evaluation reward: 12.61
- Successful landings: Not verified
- Observations: Performance improved compared with the
  100,000-step model, but results remain inconsistent.


