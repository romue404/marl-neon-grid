class RenderGroup(object):
    def __init__(self, ui, group):
        super().__init__()
        self.ui = ui
        self.group = group

    def asset_name(self, entity):
        return f'{entity.__class__.__name__.lower()}_{entity.state}'.rstrip('_')

    def get_xy(self, entity):
        offset_r, offset_c = (self.ui.lvl_padded_shape[0] - self.ui.grid_h) // 2, \
                             (self.ui.lvl_padded_shape[1] - self.ui.grid_w) // 2

        r, c = entity.pos
        r, c = r - offset_r, c - offset_c

        o = self.ui.cell_size // 2
        r_, c_ = r * self.ui.cell_size + o, c * self.ui.cell_size + o
        return r_, c_

    def blit_params(self, entity):
        img = self.ui.assets[self.asset_name(entity)]
        rect = img.get_rect()
        rect.centerx, rect.centery = self.get_xy(entity)
        return [dict(source=img, dest=rect)]

    def blits(self):
        return sum([self.blit_params(e) for e in self.group], [])


class WallRenderGroup(RenderGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = {e.pos: e for e in self.group}

    def asset_name(self, entity):
        x, y = entity.pos
        name = f'{entity.__class__.__name__.lower()}'

        north, west, south, east = (
            (x+i, y+j) in self.group for i, j in [(0, 1), (-1, 0), (0, -1), (1, 0)]
        )
        if north and east:
            name = f'{name}_upper_left_corner'
        elif north and west:
            name = f'{name}_upper_right_corner'
        elif south and east:
            name = f'{name}_lower_left_corner'
        elif south and west:
            name = f'{name}_lower_right_corner'
        elif north or south:
            name = f'{name}_vertical'
        elif east or west:
            name = f'{name}_horizontal'
        else:
            name = f'{name}_horizontal'

        return name

    def blits(self):
        return sum([self.blit_params(e) for e in self.group.values()], [])


class AgentRenderGroup(RenderGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def blit_params(self, entity):
        blit = super().blit_params(entity)[0]
        textsurface = self.ui.font.render(str(entity.id), False, (0, 0, 0))
        rect = blit['dest']
        text_blit = dict(source=textsurface, dest=(rect.center[0] - .07 * self.ui.cell_size, rect.center[1]))
        return [blit, text_blit]
