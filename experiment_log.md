
# Lunar Lander AI - Experiment Log

## Project objective
Train a PPO agent to land a spacecraft using Gymnasium LunarLander-v3.
Investigate reward shaping, reward hacking, and reward design.

## Experiment 1 - Baseline PPO (100,000 steps)

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

## Experiment 2 - Baseline PPO (500,000 steps)

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

## Experiment 3 - Baseline PPO (1,000,000 steps)

- Algorithm: PPO
- Environment: LunarLander-v3
- Network: 2 hidden layers, 64 units each
- Learning rate: 0.0003
- Training steps: 1,000,000

### Evaluation
- Evaluation episodes: 5
- Episode rewards: 186.94, 199.98, 171.75, -64.63, 253.69
- Average evaluation reward: 149.55
- Successful landings: Not verified
- Observations: Major improvement over the 100k and
  500k runs, but performance remains inconsistent.
  One episode had a negative reward.



### Extended Evaluation - 20 Episodes

- Training steps: 1,000,000
- Evaluation episodes: 20
- Average evaluation reward: 91.53
- Best reward: 273.06
- Worst reward: -154.82
- Episodes scoring 200+: 7/20 (35%)
- Verified successful landings: Not measured

Observations:
The agent achieves high rewards in several episodes but
has substantial performance variability. The average
over 20 episodes is lower than the initial five-episode
average, showing why larger evaluation samples matter.


## Experiment 4: Broken Reward - Hovering Incentive

**Training steps:** 500,000  
**Evaluation episodes:** 5  
**Evaluation environment:** Original `LunarLander-v3` reward

| Metric | Result |
|---|---:|
| Average original reward | -23.47 |
| Average upright/slow frames | 927 / 1,000 |
| Average upright/slow percentage | 92.7% |

**Observation:** The agent spent most of its episode satisfying the upright-and-slow condition, but its average original reward was negative. This suggests that the custom reward may have encouraged behavior that did not translate into effective landing performance.

**Limitation:** Upright/slow frames are only a proxy for hovering. Successful landings and time-limit truncations were not explicitly counted, so the behavior requires further verification.

**Conclusion:** Reward design matters. An agent can optimize a poorly designed incentive without achieving the intended objective.


## Experiment 5: Final Comparison

**Evaluation:** 20 episodes per model  
**Evaluation environment:** Original `LunarLander-v3`  
**Metric:** Accumulated original environment reward

| Metric | Baseline | Broken Reward | Fixed Reward |
|---|---:|---:|---:|
| Training steps | 1,000,000 | 500,000 | 500,000 |
| Average reward | 155.24 | -29.80 | 145.60 |
| Best reward | 255.32 | 222.90 | 266.20 |
| Worst reward | -72.35 | -174.58 | -77.17 |
| Successful landings | 17/20 | 1/20 | 14/20 |
| Crashes | 3/20 | 2/20 | 6/20 |
| Timeouts | 0/20 | 17/20 | 0/20 |

### Findings

- The broken-reward model timed out in 17 of 20 episodes, suggesting that its upright-and-slow bonus encouraged unproductive behavior.
- The fixed-reward model landed successfully in 14 episodes and had no timeouts.
- The baseline performed best in this evaluation, with 17 successful landings and an average reward of 155.24.
- The fixed model achieved an average reward of 145.60, so the modified reward did not outperform the baseline in this sample.

### Conclusion

The experiment illustrates reward hacking: an agent can optimize an incentive that does not align with the intended goal. Removing the hovering bonus and adding a small time penalty substantially improved behavior compared with the broken-reward model.

However, the fixed reward did not outperform the baseline. Reward modifications should be evaluated empirically rather than assumed to improve performance.

### Limitations

- Each model was evaluated on one sample of 20 episodes.
- Models were trained separately, with potentially different training randomness.
- The baseline received twice as many training steps as either experimental model.
- More evaluation episodes and repeated training runs are needed for robust comparisons.
