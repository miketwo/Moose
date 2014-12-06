#! /usr/bin/env python

import sys
import pygame
import pygame.locals as pl

import events

TICK_DELTA_MS = 5000


class ClockTicker(object):
    ''' A controller that handles the clock.  Generates ticks and keeps
    track of seconds.

    EMITS:
        USEREVENT containing a dictionary of a pygame clock and the current
        seconds counter.
    '''
    def __init__(self, event_manager, max_fps=60):
        self.em = event_manager
        self.em.RegisterListener(self)
        self.fps = max_fps
        self.seconds = 0.0
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(events.TICK_EVENT_TYPE, TICK_DELTA_MS)

    def tick(self):
        # We expect to call this method on every frame
        self.clock.tick(self.fps)
        self.em.Post(events.Tick(userData={
            "clock": self.clock,
            "seconds": self.seconds
        }))

    def notify(self, event):
        if event.type == events.TICK_EVENT_TYPE:
            print "Tick in Clock"
            self.seconds += TICK_DELTA_MS/1000.0


class KeyboardController(object):
    '''
    The purpose of this controller is to map keyboard input events to:
        - model/entity/view events
        - immediate actions (like quitting)

    We keep this as an extra layer so that the keyboard layout can be altered
    later.

    EMITS
        TBD
    '''
    def __init__(self, event_manager):
        self.em = event_manager
        self.em.RegisterListener(self)

        # tell pygame to keep sending up keystrokes when they are held down
        # pygame.key.set_repeat(500, 30)

    def notify(self, event):
        if event.type == pl.KEYDOWN:
            if ((event.key == pl.K_RIGHT)
                or (event.key == pl.K_LEFT)
                or (event.key == pl.K_UP)
                    or (event.key == pl.K_DOWN)):
                # Here is where we would emit action requests to the Player's
                # Sprites, but for now we'll just handle the keypresses
                # directly there.
                pass
            elif event.key == pl.K_d:
                self.em.Post(events.FlipDebugDisplay())
            elif event.key == pl.K_q:
                sys.exit()
