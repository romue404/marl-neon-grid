from marl_neon_grid.entitites.entity import DynamicEntity


class Food(DynamicEntity):
    SYMBOL = '*'

    def __init__(self, *args, capacity=1, **kwargs):
        super().__init__(*args, **kwargs)
        self._capacity = capacity
        self.current_capacity = capacity

    @property
    def value(self):
        return self.current_capacity

    def consume(self):
        if self.current_capacity > 0:
            self.current_capacity -= 1

    def restock(self):
        self.current_capacity = self._capacity

    def tick(self):
        if self.current_capacity <= 0:
            self.kill()

    def __repr__(self):
        return f'{super().__repr__()}_C={self.current_capacity}'
