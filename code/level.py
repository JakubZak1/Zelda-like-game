import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder, point_on_circle, calculate_angle
from random import choice
from weapons import Weapon
from math import atan2


class Level:
    def __init__(self):
        # display surface
        self.display_surf = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCamera()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

        # player
        self.player = Player((1280, 1260), [self.visible_sprites], self.obstacle_sprites)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
            'object': import_folder('../graphics/objects')
        }

        for layout_type, layout in layouts.items():
            for row in range(len(layout)):
                for col in range(len(layout[0])):
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE

                    if layout_type == 'boundary' and layout[row][col] != '-1':
                        Tile((x, y), self.obstacle_sprites, 'invisible')

                    elif layout_type == 'grass' and layout[row][col] != '-1':
                        grass_choice = choice(graphics['grass'])
                        Tile((x, y), [self.obstacle_sprites, self.visible_sprites], 'grass', grass_choice)

                    elif layout_type == 'object' and layout[row][col] != '-1':
                        object_type = graphics['object'][int(layout[row][col])]
                        Tile((x, y - TILE_SIZE), [self.obstacle_sprites, self.visible_sprites], 'object', object_type)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(pygame.mouse.get_pos())


class YSortCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.background_surf = pygame.image.load('../graphics/tilemap/background.png').convert()
        self.background_rect = self.background_surf.get_rect(topleft=(-500, -500))
        self.ground_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        background_offset_pos = self.background_rect.topleft - self.offset
        ground_offset_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.background_surf, background_offset_pos)
        self.display_surface.blit(self.ground_surf, ground_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # drawing weapon
        rotated_weapon_image, rotated_weapon_rect = player.rotate_weapon()
        self.display_surface.blit(rotated_weapon_image, rotated_weapon_rect)
