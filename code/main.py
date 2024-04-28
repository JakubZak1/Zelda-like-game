import pygame
from settings import *
from sys import exit
from debug import debug
from level import Level
from random import choice


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption(choice(['Maciej Łerbers', 'Antoni Moszko', 'Szczepan Sawina', 'Wiktoria Mięsko',
                                           'Ewelina Paznokcie', 'Martina Preszek', 'Piotr Żak', 'Ernest Kozieł',
                                           'Anart Lenart', 'Koticzek']))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill('black')
            self.level.run()
            # debug(pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
