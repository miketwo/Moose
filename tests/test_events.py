#! /usr/bin/env python

import sys
sys.path.append('../moose')
import unittest
from mock import Mock
from moose import events
import pygame


class TestEvents(unittest.TestCase):

    def setUp(self):
        self.obj = Mock()

    def test_end_to_end(self):
        pygame.init()
        E = events.EventManager()
        E.RegisterListener(self.obj)

        MyEvent = events._makeEvent("MyEvent", 1)
        ev = MyEvent("data")
        E.Post(ev)

        for event in pygame.event.get():
            E.notifyAllListeners(event)

        self.obj.notify.assert_called_with(ev)


if __name__ == '__main__':
    unittest.main()
