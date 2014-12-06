#! /usr/bin/env python
import sys

# Disable .pyc during development.  We can remove this later.
sys.dont_write_bytecode = True

import pygame
import pygame.locals as pl
import kezmenu

# Add directories to python path
import os
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(base, 'gamelib')))

from moose import game


def load_image(name, colorkey=None):
    '''
    Loads an image using pygame's functions.
    Must have video mode set before calling
    '''
    fullname = os.path.join('data', 'images')
    fullname = os.path.join(fullname, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pl.RLEACCEL)
    return image, image.get_rect()


class Menu(object):
    running = True

    def main(self, screen):
        clock = pygame.time.Clock()
        background, _ = load_image('menu_background.png')
        menu = kezmenu.KezMenu(
            ['Play!', lambda: game.Game().main(screen)],
            ['Quit', lambda: setattr(self, 'running', False)],
        )
        menu.x = 500
        menu.y = 100
        menu.color = (255, 255, 255, 100)
        menu.enableEffect('enlarge-font-on-focus',
            font=None, size=18, enlarge_factor=3., enlarge_time=0.200)
        # menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        while self.running:
            menu.update(pygame.event.get(), clock.tick(30)/1000.)
            screen.blit(background, (0, 0))
            menu.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Menu().main(screen)

