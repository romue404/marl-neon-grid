import random
from marl_neon_grid.entitites import Food, Floor, GameState


class FoodNAgentsGameState(GameState):
    def __init__(self, *args, n_food, agents_must_coordinate, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_food = n_food
        self.agents_must_coordinate = agents_must_coordinate

        for food in self.get_food():
            self.entities.append(food)

    def get_food(self):
        floor_tiles = self.entities[Floor.SYMBOL]
        random.shuffle(floor_tiles)
        food = [Food(pos=ft.pos, capacity=len(self.agents) if self.agents_must_coordinate else 1)
                for ft in floor_tiles[:self.n_food]]
        return food

    def is_game_over(self):
        no_more_food = len(self.entities.symbol_dict[Food.SYMBOL]) == 0
        return super().is_game_over() or no_more_food

    def tick(self):
        super().tick()
        for food in self.entities.symbol_dict[Food.SYMBOL]:
            food.restock()  # if not completely consumed, restock