from marl_neon_grid.entitites.entity import Entity


class DoorStates:
    OPEN = 'open'
    CLOSED = 'closed'


class Door(Entity):
    SYMBOL = 'D'

    def __init__(self, *args, n_ticks_open=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = DoorStates.CLOSED
        self.n_ticks_open = n_ticks_open
        self.open_ticks = 0

    def tick(self):
        if self.state == DoorStates.OPEN:
            self.open_ticks += 1
            if self.open_ticks >= self.n_ticks_open:
                self.open_ticks = 0
                self.state = DoorStates.CLOSED

    @property
    def blocks_ray(self):
        return self.state == DoorStates.CLOSED

    @property
    def open(self):
        return self.state == DoorStates.OPEN