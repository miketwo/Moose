#! /usr/bin/env python

import os
import sys
import pygame
import pygame.locals as pl
import random

import events
import entity
from pymunk import Vec2d

if not pygame.font:
    print 'Warning, fonts disabled'
if not pygame.mixer:
    print 'Warning, sound disabled'


def load_all(evManager):
    '''
    Create entities and players
    '''
    player = Human(evManager, "Player1")
    cpu = CPU(evManager, "CPU")

    return [player, cpu]


class Player(object):
    '''
    A player is a controller of an entity, it can receive input events
    such as keyboard and mouse, and translate those into output events that
    request entities to perform actions.  In the case of the CPU as player,
    it can also generate these action requests on its own.
    '''
    def __init__(self, evManager, name, entity):
        self.name = name
        self.entity = entity
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        print "{} is born".format(self)
        ev = events.PlayerCreated(self)
        self.evManager.Post(ev)

    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))


class Human(Player):
    def notify(self, event):
        if event.type == pl.KEYDOWN:
            if ((event.key == pl.K_RIGHT)
                or (event.key == pl.K_LEFT)
                or (event.key == pl.K_UP)
                    or (event.key == pl.K_DOWN)):
                self.entity.max_velocity(event.key)
        if event.type == pl.KEYUP:
            if ((event.key == pl.K_RIGHT)
                or (event.key == pl.K_LEFT)
                or (event.key == pl.K_UP)
                    or (event.key == pl.K_DOWN)):
                self.entity.stop_velocity(event.key)


class CPU(Player):
    '''
    An automatically controlled dog.
    '''
    def __init__(self, *args):
        super(CPU, self).__init__(*args)
        self.target = None

    def move_toward_target(self):
        if self.target is None:
            self.entity.change_direction(None)
            return
        current = Vec2d(*self.entity.rect.center)
        desired = Vec2d(*self.target.rect.center)
        delta = desired - current
        dist = current.get_distance(desired)
        if dist > 50:
            self.entity.change_direction(get_dir(delta))
        else:
            self.entity.change_direction(None)

    def notify(self, event):
        if event.type == events.TICK_EVENT_TYPE:
            print "Tick in CPU"
            self.move_toward_target()


def random_dir():
    R, L, D, U = (entity.Entity.RIGHT, entity.Entity.LEFT,
                  entity.Entity.DOWN, entity.Entity.UP)
    return random.choice([R, L, D, U])


def get_dir(vector):
    a = vector.get_angle_degrees()
    assert a >= -180 and a < 180, '???'
    if a >= -180 and a < -90:
        return entity.Entity.LEFT
    if a >= -90 and a < 0:
        return entity.Entity.RIGHT
    if a >= 0 and a < 90:
        return entity.Entity.DOWN
    if a >= 90 and a < 180:
        return entity.Entity.UP
    raise Exception("Can't get here")


