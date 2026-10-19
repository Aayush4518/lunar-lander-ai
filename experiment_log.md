
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


## Experiment 5: Final Model Comparison

**Evaluation episodes:** 20 per model  
**Evaluation reward:** Original LunarLander-v3 reward  
**Landing detection:** Approximate heuristic using leg contact, velocity, and angle

| Metric | Baseline | Broken Reward | Fixed Reward |
|---|---:|---:|---:|
| Average reward | 97.41 | -12.27 | 160.84 |
| Likely safe landings | 9/20 | 1/20 | 9/20 |
| Timeouts | 1/20 | 18/20 | 1/20 |

### Findings

- The broken-reward model spent most of its time satisfying the upright-and-slow condition and timed out in 18 of 20 episodes.
- The fixed-reward model achieved the highest average original reward and timed out in only one episode.
- Both the baseline and fixed-reward models achieved 9 likely safe landings under the approximate landing detector.
- The broken reward appears to have encouraged behavior inconsistent with the intended landing objective.

### Conclusion

The experiment demonstrates how a poorly chosen reward incentive can lead to undesirable behavior. Removing the hovering bonus and introducing a small time penalty was associated with substantially better performance under the original environment reward.

### Limitations

- Only 20 evaluation episodes were tested per model.
- The landing detector is approximate and may misclassify some outcomes.
- Each model was trained separately, so training randomness may affect the comparison.
- More evaluation episodes and repeated training runs are needed for stronger conclusions.