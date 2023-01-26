import random
from marl_neon_grid.entitites import Food, Floor, GameState


class FoodNAgentsGameState(GameState):
    def __init__(self, *args, n_food, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_food = n_food

        for food in self.get_food():
            print(food)
            self.entities.append(food)


    def get_food(self):
        floor_tiles = self.entities[Floor.SYMBOL]
        random.shuffle(floor_tiles)
        food = [Food(pos=ft.pos) for ft in floor_tiles[:self.n_food]]
        return food
