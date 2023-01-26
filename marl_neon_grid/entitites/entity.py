import numpy as np
from collections import defaultdict


class EntityStates:
    VALID = 'valid'
    INVALID = 'invalid'
    IDLE = ''


class Entity:
    SYMBOL = 'E'
    NORTH = np.array([0, -1])
    SOUTH = np.array([0, 1])
    EAST = np.array([1, 0])
    WEST = np.array([-1, 0])
    NO_OP = np.array([0, 0])
    NORTH_WEST = NORTH + WEST
    SOUTH_WEST = SOUTH + WEST
    NORTH_EAST = NORTH + EAST
    SOUTH_EAST = SOUTH + EAST

    def __init__(self, pos: np.array, view_radius=3):
        super().__init__()
        self._pos_np    = pos if isinstance(pos, np.ndarray) else np.array(pos)
        self.view_radius = view_radius
        self._blocks_ray = False
        self.state = EntityStates.IDLE

    @property
    def blocks_ray(self):
        return self._blocks_ray

    @property
    def pos_np(self):
        return self._pos_np

    @pos_np.setter
    def pos_np(self, new_pos):
        raise NotImplemented('You cannot modify the position of a non-moveable entity!')

    @property
    def pos(self):
        return tuple(self._pos_np)

    @property
    def x(self):
        return self._pos_np[0]

    @property
    def y(self):
        return self._pos_np[1]

    def tick(self):
        self.state = EntityStates.IDLE

    def __repr__(self):
        return f'{self.__class__.__name__}_@_{self._pos_np}'


def notify_pos(func):
    def _notify_pos(self, *args, **kwargs):
        old_pos = self.pos
        fn_out = func(self, *args, **kwargs)
        self.notify(dict(old_pos=old_pos))
        return fn_out
    return _notify_pos


class MoveableEntity(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []

    @Entity.pos_np.setter
    @notify_pos
    def pos_np(self, new_pos):
        self._pos_np = new_pos if isinstance(new_pos, np.ndarray) else np.array(new_pos)

    def notify(self, payload=None):
        payload = {} if payload is None else payload
        for observer in self._observers:
            observer.update(self, payload)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass


class Entities(object):
    def __init__(self, lst=()):
        super().__init__()
        self.pos_dict         = defaultdict(list)
        self.symbol_dict      = defaultdict(list)
        for e in lst:
            self.append(e)

    def append(self, entity: Entity):
        self.pos_dict[entity.pos].append(entity)
        self.symbol_dict[entity.SYMBOL].append(entity)
        if isinstance(entity, MoveableEntity):
            entity.attach(self)

    def values(self):
        return sum(self.symbol_dict.values(), [])

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.symbol_dict[item]
        elif isinstance(item, tuple):
            return self.pos_dict[item]
        return []

    def update(self, entity, payload):
        #print(f'received an update from {entity} with payload {payload}')
        self.pos_dict[payload['old_pos']].remove(entity)
        self.symbol_dict[entity.SYMBOL].remove(entity)
        entity.detach(self)  # todo can this be omitted?
        self.append(entity)