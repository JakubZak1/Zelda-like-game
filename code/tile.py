import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group_list, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(group_list)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -25)
