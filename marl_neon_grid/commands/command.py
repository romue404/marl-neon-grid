from abc import ABC
from marl_neon_grid.entitites import GameState


class Event(object):
    def __init__(self, name, **payload):
        super().__init__()
        self.name = name
        for k, v in payload.items():
            setattr(self, k, v)

    def __repr__(self):
        stuff = ','.join([f'{k}={v}' for k, v in self.__dict__.items() if k != 'name'])
        return f'{self.name}({stuff})'


class EmptyEvent(Event):
    def __init__(self):
        super().__init__('empty')


class Command(ABC):
    def __init__(self, game_state: GameState, *args, **kwargs):
        self.game_state = game_state

    def run(self) -> Event:
        pass