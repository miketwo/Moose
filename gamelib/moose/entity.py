#! /usr/bin/env python
import os
import sys
import pygame
import pygame.locals as pl
import random

import events
import controllers

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'


def create_all(evManager):
    human = Man(evManager, (650, 690))
    dog = Dog(evManager, (750, 690))
    tree = Tree(evManager, (750, 790))

    # Associate entities with foreground
    # evManager.Post(events.AddToForeground(human))
    # evManager.Post(events.AddToBackground(ground))
    # evManager.Post(events.AddToForeground(dog))
    # evManager.Post(events.AddToForeground(tree))

    return human, dog, tree


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


def sprite_sheet_load(colorKey, spriteLocX, spriteLocY, spriteSizeX, spriteSizeY, fileName):
    '''Purpose: to extract a sprite from a sprite sheet at the chosen location'''
    '''credit to Stackover flow user hammyThePig for original code'''
    sheet = pygame.image.load(fileName).convert() #loads up the sprite sheet. convert makes sure the pixel format is coherent
    sheet.set_colorkey(colorKey) #sets the color key
    sprite = sheet.subsurface(pygame.Rect(spriteLocX, spriteLocY, spriteSizeX, spriteSizeY)) #grabs the sprite at this location
    return sprite


def create_transparent_surface(width, height):
    image = pygame.Surface([width,height], pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    return image


class InstaSprite(pygame.sprite.Sprite):
    '''
    Create an instant sprite by initializing with a surface.
    '''
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = surface.get_rect()


class Entity(pygame.sprite.Sprite):
    '''
    An entity is any object in the game. So this includes all sorts of stuff:
        - the dog, the walker, trees, birds, bushes, people, cars, etc...

    An entitity can receive events that request certain actions, and responds
    to those events by performing the action (moving, changing sprite, etc..).

    The entity can also generate events when it changes state.
    '''
    DOWN = "D"
    UP = "U"
    LEFT = "L"
    RIGHT = "R"

    def __init__(self, evManager, map_pos=gw2.Vec2d(0.0, 0.0)):
        super(Entity, self).__init__(map_pos)
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.rect = pygame.Rect(map_pos.x, map_pos.y, 1, 1)
        self.hitbox = self.rect
        # An entitiy's position is with respect to the underlying map.
        # 0,0 is the top left
        self.position = map_pos
        self.velocity = gw2.Vec2d(0.0, 0.0)
        self.acceleration = gw2.Vec2d(0.0, 0.0)

        ev = events.EntityCreated(self)
        self.evManager.Post(ev)


    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        # float pos
        self._position[:] = val
        x, y = val
        # my rect
        r = self.rect
        r.centerx = int(round(x))
        r.centery = int(round(y))
        # my hitbox
        r2 = self.hitbox
        r2.x = r.x
        r2.bottom = r.bottom

    def update(self, *args):
        print "{} not implemented update".format(self)

    def notify(self, event):
        pass


class Dog(Entity):
    def __init__(self, *args):
        super(Dog, self).__init__(*args)
        self.direction = self.DOWN
        self.image = sprite_sheet_load(
            (0, 0, 0),  # sets alpha color
            spriteLocX=0, spriteLocY=0, spriteSizeX=46, spriteSizeY=27,
            fileName="data/images/dog_brown_0.png")
        self.rect = pygame.Rect(240, 240, 46, 27)
        # number of pixels to move each time
        self.x_vel = 0
        self.y_vel = 0
        self.vmax = 5

    def notify(self, event):
        if event.type == events.TICK_EVENT_TYPE:
            print "Tick in Dog"
            self.move()

    def get_sprite(self):
        return self.image

    def stop(self):
        self.x_vel = 0
        self.y_vel = 0

    def change_direction(self, direction):
        if (direction == self.RIGHT):
            self.x_vel = self.vmax
            self.direction = self.RIGHT
        elif (direction == self.LEFT):
            self.x_vel = -self.vmax
            self.direction = self.LEFT
        elif (direction == self.UP):
            self.y_vel = -self.vmax
            self.direction = self.UP
        elif (direction == self.DOWN):
            self.y_vel = self.vmax
            self.direction = self.DOWN
        elif (direction is None):
            self.stop()
        self.image = self.get_sprite()

    def move(self):
        # Check if we are actually moving
        if self.x_vel == 0 and self.y_vel == 0:
            return
        old_pos = self.rect
        self.rect.move_ip(self.x_vel, self.y_vel)
        # self.evManager.Post(events.EntityMoved({
        #     "entity": self,
        #     "old_position": old_pos,
        #     "new_position": self.rect}))

    def update(self, *args):
        pass


class Man(Entity):
    def __init__(self, *args):
        super(Man, self).__init__(*args)
        self.sprite_sheet, _ = load_image("man.png")
        self.direction = self.DOWN
        self.image = self.get_sprite()
        self.rect = pygame.Rect(120, 200, *self.image.get_size())
        self.vmax = 80

        ## Tell renderer to use anti-interpolation on this object. If we don't
        ## do this, then the avatar will jitter when scrolling. This is usually
        ## necessary when avatar is used as the camera target.
        self.anti_interp = True

    def update(self, *args):
        self.image = self.get_sprite()

    def get_sprite(self):
        # Each sprite is 16x16, arranged in 2 colums and 2 rows
        # There are 4 sprites per direction
        # UP DOWN
        # LEFT RIGHT
        # Start coordinates: (0,0), (3*16,0), (0, 3*16), (3*16, 3*16)
        start = {
            self.UP: (0, 0),
            self.DOWN: (4*16, 0),
            self.LEFT: (0, 16),
            self.RIGHT: (4*16, 16),
        }
        x = start[self.direction][0]
        y = start[self.direction][1]
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, 16, 16))

    def max_velocity(self, key):
        '''
        Make the dude walk
        '''
        v = self.velocity
        if (key == pl.K_RIGHT):
            self.velocity = gw2.Vec2d(self.vmax, v.y)
            self.direction = self.RIGHT
        elif (key == pl.K_LEFT):
            self.velocity = gw2.Vec2d(-self.vmax, v.y)
            self.direction = self.LEFT
        elif (key == pl.K_UP):
            self.velocity = gw2.Vec2d(v.x, -self.vmax)
            self.direction = self.UP
        elif (key == pl.K_DOWN):
            self.velocity = gw2.Vec2d(v.x, self.vmax)
            self.direction = self.DOWN

    def move(self):
        t = controllers.TICK_DELTA_MS/1000.0
        p = self.position
        v = self.velocity
        a = self.acceleration
        print p,v,a
        self.position += v*t + 0.5*a*t*t
        self.velocity += a*t
        print p,v,a
        # print self.rect
        self.rect = pygame.Rect(self.position.x, self.position.y, self.rect[2], self.rect[3])
        # print self.rect
        ev = events.RequestViewChangeTarget(self.position)
        print "Man posting {}".format(self.position)
        self.evManager.Post(ev)

    def notify(self, event):
        if event.type == events.TICK_EVENT_TYPE:
            print "Tick in Man"
            self.move()

    def stop_velocity(self, key):
        '''
        Stop walking
        '''
        if (key == pl.K_RIGHT and self.velocity.x > 0):
            self.velocity.x = 0
        elif (key == pl.K_LEFT and self.velocity.x < 0):
            self.velocity.x = 0
        elif (key == pl.K_UP and self.velocity.y < 0):
            self.velocity.y = 0
        elif (key == pl.K_DOWN and self.velocity.y > 0):
            self.velocity.y = 0


class Tree(Entity):
    def __init__(self, *args):
        super(Tree, self).__init__(*args)
        self.marked = False
        self.sprite_sheet, self.rect = load_image("trees_tilee_celianna.png")
        self.image = self.get_sprite()
        self.rect = pygame.Rect(240, 320, 64, 128)

    def get_sprite(self):
        if self.marked:
            return self.sprite_sheet.subsurface(pygame.Rect(448, 0, 64, 128))
        else:
            return self.sprite_sheet.subsurface(pygame.Rect(320, 0, 64, 128))

    def notify(self, event):
        if event.type == pl.KEYDOWN:
            if (event.key == pl.K_m):
                self.marked = not self.marked

    def update(self, *args):
        pass


class ClockOverlay(Entity):
    def __init__(self, *args):
        super(ClockOverlay, self).__init__(*args)
        self.location = (10, 10)

    def notify(self, event):
        if events.isUserEvent(event, "Tick"):
            self.image, self.rect = self.render_debug(event.userData)
            self.rect.move_ip(self.location)
        if events.isUserEvent(event, "FlipDebugDisplay"):
            if self.alive():
                self.kill()
            else:
                self.evManager.Post(events.AddToForeground(self))

    def render_debug(self, clock_data):
        ''' Creates a framerate and time display

        ARGS:
            clock_data  A dictionary containing a pygame clock and the current
                        seconds counter, in the following format:
                        {
4                            "clock": pygame clock,
                            "seconds": number
                        }

        RETRUNS:
            A transparent surface and its containing rect
        '''
        clock = clock_data["clock"]
        seconds = clock_data["seconds"]
        BLUE = (0, 0, 255)
        font = pygame.font.Font(None, 36)
        time_display = font.render("Time: " + str(clock.get_time()), 1, BLUE)
        rawtime_display = font.render("Raw Time: " + str(clock.get_rawtime()), 1, BLUE)
        fps_display = font.render("FPS: " + str(clock.get_fps()), 1, BLUE)
        pygame_total_ticks_display = font.render("Pygame Ticks (total): " + str(pygame.time.get_ticks()), 1, BLUE)
        seconds_display = font.render("Seconds: " + str(seconds), 1, BLUE)
        lines = [time_display ,rawtime_display ,fps_display ,
                 pygame_total_ticks_display ,seconds_display]
        max_width = max([x.get_width() for x in lines])
        max_height = max([x.get_height() for x in lines])
        sz = (max_width, 110 + max_height)
        trans = create_transparent_surface(*sz)
        trans.blit(time_display, (0, 0))
        trans.blit(rawtime_display, (0, 25))
        trans.blit(fps_display, (0, 50))
        trans.blit(pygame_total_ticks_display, (0, 75))
        trans.blit(seconds_display, (0, 100))
        return trans, trans.get_rect()


class Background(Entity):
    def __init__(self, *args):
        super(Background, self).__init__(*args)
        self.image, self.rect = load_image("level1pic.png")

    def update(self, *args):
        pass

