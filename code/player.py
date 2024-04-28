import pygame
from weapons import Weapon
from support import point_on_circle, calculate_angle
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group_list, obstacle_sprites):
        super().__init__(group_list)
        self.image = pygame.image.load('../graphics/player/down_idle/idle_down.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -20)
        

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.is_rolling = False
        self.roll_cooldown = 1000
        self.roll_start_time = None
        self.roll_timer = 300
        self.direction_help = None

        self.obstacle_sprites = obstacle_sprites

        self.weapon = Weapon(self)

    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # roll
        if keys[pygame.K_SPACE] and not self.is_rolling and self.direction != (0, 0):
            self.is_rolling = True
            self.roll_start_time = pygame.time.get_ticks()

        # attack


    def movement(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction_help = self.direction_help.normalize()

        current_time = pygame.time.get_ticks()

        # roll
        if self.is_rolling and current_time - self.roll_start_time <= self.roll_timer:
            self.hitbox.x += self.direction_help.x * 2 * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction_help.y * 2 * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

        # walk
        else:
            self.direction_help = self.direction
            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction_help.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    else:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if self.hitbox.colliderect(sprite.hitbox):
                    if self.direction_help.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    else:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.is_rolling:
            if current_time - self.roll_start_time >= self.roll_cooldown:
                self.is_rolling = False

    def rotate_weapon(self):
        offset = pygame.math.Vector2()
        offset.x = self.rect.centerx - WIDTH // 2
        offset.y = self.rect.centery - HEIGHT // 2
        mouse_pos = pygame.mouse.get_pos()
        self.weapon.rect.center = point_on_circle(self.rect.center - offset, mouse_pos, 50)

        angle = calculate_angle(self.rect.center - offset, mouse_pos)
        rotated_weapon_image = pygame.transform.rotate(self.weapon.image, angle)
        rotated_weapon_rect = rotated_weapon_image.get_rect(center=self.weapon.rect.center)

        return rotated_weapon_image, rotated_weapon_rect

    def update(self):
        self.input()
        self.movement(self.speed)
        self.collision(self.direction)
        self.cooldowns()
