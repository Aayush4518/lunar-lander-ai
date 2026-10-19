# LunarLander AI 

I wanted to understand how reinforcement learning actually works, beyond just training a model and watching it do something cool.

So I built an AI that learns to land a lunar lander using PPO, and then experimented with its reward function to see what happens when you accidentally reward the wrong behavior.

Turns out, the AI doesn't necessarily do what you *want*. It does what gets it the most reward.

## What I built

The project uses Gymnasium's `LunarLander-v3` environment and Stable-Baselines3 to train an agent using Proximal Policy Optimization (PPO).

I ran three experiments:

- **Baseline:** Train the agent using the environment's original reward.
- **Broken reward:** Give it an extra reward for staying upright and moving slowly.
- **Fixed reward:** Remove that bonus and add a small penalty for every frame spent in the episode.

The idea behind the second experiment was simple: if hovering keeps earning points, will the agent figure out that hovering is easier than landing?

## The results

I evaluated each model over 20 episodes, using the original environment reward for comparison.

| Metric | Baseline | Broken reward | Fixed reward |
|---|---:|---:|---:|
| Average reward | 155.24 | -29.80 | 145.60 |
| Successful landings | 17/20 | 1/20 | 14/20 |
| Crashes | 3/20 | 2/20 | 6/20 |
| Timeouts | 0/20 | 17/20 | 0/20 |

The broken-reward model was the most interesting part. It timed out in 17 out of 20 episodes, which fits the idea that the hovering bonus encouraged it to stay around instead of finishing the task.

Removing that bonus made a big difference. The fixed-reward model landed in 14 episodes and didn't time out in any of them.

Interestingly, though, it still didn't beat the baseline. So the lesson wasn't that my new reward function was better. It was that a seemingly reasonable reward can make an agent behave in a way you never intended.

*These are results from one 20-episode evaluation per model, so there's still room for more testing.*

## Tech stack

- Python
- Gymnasium
- Stable-Baselines3
- PPO
- PyTorch
- Box2D

## Running it locally

Clone the repository and install the dependencies:

```bash
git clone <your-repository-url>
cd lunar-lander-ai

python -m venv .venv
```

Activate the virtual environment, then install the packages:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Train the baseline:

```bash
python 02_train_lander.py
```

Evaluate a saved model:

```bash
python -m experiments.evaluate_model --model ppo_lander --episodes 20
```

Train the reward-hacking experiment:

```bash
python -m experiments.train_broken_reward
```

Train the fixed-reward version:

```bash
python -m experiments.train_fixed_reward
```

The experimental training scripts save their models under `models/`. Generated models and training outputs are excluded from Git, so you'll need to train them before evaluating them locally.

## What I learned

The biggest takeaway was that reward design matters a lot more than I initially expected.

Adding a reward that sounds sensible doesn't guarantee better behavior. The agent can find a strategy that maximizes the reward without actually solving the problem.

I also learned to evaluate models using the original environment reward instead of judging them only by the custom reward they were trained on.

## What's next?

- Run more evaluation episodes and compare multiple training runs.
- Plot reward curves to see how learning progresses.
- Improve the reward design and test whether it can outperform the baseline.
- Record a few successful landings and examples of the hovering behavior.

This is a learning project, so the results aren't perfect. That's kind of the point I wanted to see what happens, understand why it happens and improve the experiment from there.
