import pygame
from csv import reader
from os import walk
import math


def import_csv_layout(path):
    map_list = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            map_list.append(list(row))
    return map_list


def import_folder(path):
    surfaces = []
    for data in walk(path):
        for file in data[2]:
            full_path = path + '/' + file
            image_surf = pygame.image.load(full_path).convert_alpha()
            surfaces.append(image_surf)
    return surfaces


def point_on_circle(point1, point2=pygame.mouse.get_pos(), radius=50):
    if point1[0] == point2[0] and point1[1] == point2[1]:
        return point1

    point_a = pygame.math.Vector2(point1)
    point_b = pygame.math.Vector2(point2)

    vector = point_b - point_a
    vector.scale_to_length(radius)

    result = point_a + vector
    return result


def calculate_angle(vector1, vector2):
    vector = pygame.math.Vector2(vector1[0] - vector2[0], vector1[1] - vector2[1])
    angle = vector.angle_to(pygame.Vector2(0, 1))
    # angle = math.atan2(vector1[0] - vector2[0], vector1[1] - vector2[1])
    return angle
