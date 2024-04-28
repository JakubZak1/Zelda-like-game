import pygame
from support import point_on_circle


class Weapon():
    def __init__(self, player):
        # super().__init__(group_list)

        self.image = pygame.image.load('../graphics/weapons/lance/full.png')
        self.rect = self.image.get_rect(center=player.rect.center)

