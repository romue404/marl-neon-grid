from marl_neon_grid.entitites import GameState, Agent, Wall, Door, Food,  EntityStates
from marl_neon_grid.commands.open_door_command import OpenDoorCommand


class EatFoodCommand(OpenDoorCommand):
    def __init__(self, game_state: GameState, agent: Agent, **kwargs):
        super().__init__(game_state, agent, **kwargs)

    def run(self):
        food = [e for e in self.check_around(self.agent) if isinstance(e, Food)]
        if len(food) > 0:
            consumed_food = food[0]
            consumed_food.consume()
            self.agent.state = EntityStates.VALID
        else:
            self.agent.state = EntityStates.INVALID
