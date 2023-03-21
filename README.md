# 🦩🌴 MARL-Neon-Grid

A collection of MARL gridworlds to study coordination and cooperation that follows the 
[Gymnasium](https://github.com/Farama-Foundation/Gymnasium) interface.

## Setup
Simply run:
```pip install marl-neon-grid```

## Example
```py
from marl_neon_grid import FoodNAgents

n_agents = 2
gw = FoodNAgents(n_agents=n_agents, n_food=8, max_steps=128, agents_must_coordinate=False)

for t in range(100):  # simulate 100 episodes
    observations = gw.reset()
    dones = [False] * n_agents
    while not all(dones):
        gw.render()  # render with pygame
        observations, rewards, dones, info = gw.step([gw.action_space.sample(), 
                                                      gw.action_space.sample()])  # perform random actions
        # observations, rewards, dones are lists where each entry i belongs to agent i.


```

### 🚧 Under construction ...