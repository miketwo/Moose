#! /usr/bin/env python

import pygame
import pygame.locals as pl

import events
import entity

from pymunk import Vec2d


class Viewer(object):
    '''
    The main display for the game
    '''
    def __init__(self, event_manager):
        self.evManager = event_manager
        self.evManager.RegisterListener(self)
        pygame.display.set_caption("Moose on the Move")
        self.width = 640
        self.height = 480
        # Create screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Create background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((20, 20, 20))

        # Setup groups for sprite rendering
        self.backgroundSprites = pygame.sprite.RenderUpdates()
        self.foregroundSprites = pygame.sprite.RenderUpdates()

        # Annouce self
        ev = events.ViewCreated(self)
        self.evManager.Post(ev)

    def show_entity(self, entity):
        self.foregroundSprites.add(entity)

    def redraw(self, complete_redraw=True):
        ''' Redraws the screen. Intended to be called on every frame. '''
        # Clear
        self.foregroundSprites.clear(self.screen, self.background)
        self.backgroundSprites.clear(self.screen, self.background)

        # Draw Everything
        self.foregroundSprites.update()
        self.backgroundSprites.update()

        self.backgroundSprites.draw(self.screen)
        self.foregroundSprites.draw(self.screen)
        pygame.display.flip()

    def notify(self, event):
        if events.isUserEvent(event, "PlayerCreated"):
            player = event.userData
            if player.name == "Player1":
                self.foregroundSprites.add(player.entity)
            if player.name == "CPU":
                self.backgroundSprites.add(player.entity)
        elif events.isUserEvent(event, "Tick"):
            self.redraw()
        elif events.isUserEvent(event, "AddToBackground"):
            self.backgroundSprites.add(event.userData)
        elif events.isUserEvent(event, "AddToForeground"):
            self.foregroundSprites.add(event.userData)


class ScrollingView(object):
    '''
    A view that maintains a target location and it's own location.  On every
    change to the target, the view updates the positions of all sprites, to simulate
    a scrolling effect.

    The view also has limits of minimum and maximum x and y. The scrolling stops
    if the edge of the view would exceed these limits
    '''
    def __init__(self, event_manager):
        self.evManager = event_manager
        self.evManager.RegisterListener(self)
        pygame.display.set_caption("Scrolling view")
        self.width = 640
        self.height = 480
        self.target = Vec2d(self.width/2, self.height/2)

        # Create viewport
        self.viewport = pygame.display.set_mode((self.width, self.height))

        # Setup sprite group
        self.allSprites = pygame.sprite.LayeredUpdates()

        # Annouce self
        ev = events.ViewCreated(self)
        self.evManager.Post(ev)

    def redraw(self):
        ''' Redraws the screen. Intended to be called on every frame. '''

        # Update any animations
        self.allSprites.update()
        self.allSprites.draw(self.viewport)
        pygame.display.flip()

    def change_target(self, new_target):
        old = self.target
        diff = new_target - old
        print "Current: {}  New: {} Diff: {}".format(self.target, new_target, diff)
        self.target = new_target
        for sprite in self.allSprites.sprites():
            # print sprite, sprite.position, diff,
            sprite.position = sprite.position - diff
            # print sprite.position

    def notify(self, event):
        if events.isUserEvent(event, "RequestViewChangeTarget"):
            print "Got change event"
            self.change_target(event.userData)
        elif events.isUserEvent(event, "Tick"):
            self.redraw()
        elif events.isUserEvent(event, "AddToBackground"):
            self.allSprites.add(event.userData, layer=0)
        elif events.isUserEvent(event, "AddToForeground"):
            self.allSprites.add(event.userData, layer=1)
