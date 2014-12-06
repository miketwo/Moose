#! /usr/bin/env python
import os
import pygame

import events
import gummworld2 as gw2


def load_all(evManager):
    '''
    Load all maps
    '''
    map1 = Map(evManager, "level1.tmx")
    return map1


class Map(gw2.TiledMap):
    def __init__(self, event_manager, tmx_mapfile, *args):
        """Looking at the map in Tiled, we see the following layers:
        tiled_map.layers[0] = Ground
        tiled_map.layers[1] = Entities
        tiled_map.layers[2] = Over
        tiled_map.layers[3] = Collision
        tiled_map.layers[4] = Objects

        Dynamic game objects go in Entities.
        """
        self.evManager = event_manager
        self.evManager.RegisterListener(self)

        mypath = os.path.abspath(os.path.dirname(__file__))
        fullname = os.path.join(mypath, '../..', 'data', 'maps')
        fullname = os.path.join(fullname, tmx_mapfile)
        super(Map, self).__init__(map_file_name=fullname)

        # Save special layers for easy access.
        self.entity_group = self.layers[1]
        self.collision_group = self.layers[3]
        # Tell the renderer this layer needs to be sorted, and how to.
        self.entity_group.objects.sort_key = lambda o: o.rect.bottom
        # Hide the busy Collision layer. Player can show it by hitting K_3.
        self.collision_group.visible = False

        ev = events.MapCreated(self)
        self.evManager.Post(ev)

    def mapify(self, size):
        '''
        Creates a surface with the map image tiles blitted onto it.

        size is a tuple of x, y
        '''
        surface = pygame.Surface(size)
        surface = surface.convert()
        surface.fill((255, 0, 0))
        # Loop over the map, blitting tiles onto it
        x = y = 0
        for x in xrange(surface.get_width()/16):
            for y in xrange(surface.get_height()/16):
                tile = self.tmxdata.get_tile_image(x, y, 0)
                surface.blit(tile, pygame.Rect(x*16, y*16, *tile.get_size()))
        return surface

    def notify(self, event):
        pass
