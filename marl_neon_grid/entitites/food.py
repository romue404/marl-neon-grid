from marl_neon_grid.entitites.entity import DynamicEntity


class Food(DynamicEntity):
    SYMBOL = '*'

    def __init__(self, *args, capacity=1, **kwargs):
        super().__init__(*args, **kwargs)
        self._capacity = capacity
        self.current_capacity = capacity

    def consume(self):
        self._capacity -= 1

    def restock(self):
        self.current_capacity = self._capacity

    def tick(self):
        if self.current_capacity <= 0:
            self.kill()

