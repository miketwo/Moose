#! /usr/bin/env python

import sys
sys.path.append('../moose')
import unittest
from mock import Mock
from mock import patch
from moose import tmx


class TestMaps(unittest.TestCase):

    def setUp(self):
        # Patch stdout to suppress output.
        # Reset for a specific test by using:
        #    reload(sys)
        patcher = patch('sys.stdout')
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_map_loading(self):
        screen_mock = (300, 300)
        tmx.load('testdata/maps/level1.tmx', screen_mock)

    @patch("pygame.image.load")
    def test_map_loading_2(self, mock_load):
        screen = (300, 300)
        tmx.load('testdata/maps/level2.tmx', screen)
        assert mock_load.called


if __name__ == '__main__':
    unittest.main()
