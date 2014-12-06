#!/usr/bin/env python


import sys
import os
import cProfile
import pstats

import pygame

import pygame.locals as pl

# Add directories to python path
base = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(base, 'gamelib')))
sys.path.append(os.path.abspath(os.path.join(base, 'gamelib', 'pgu')))

import gummworld2 as gw2
from moose import entity
from moose import events
from moose import maps


class App(gw2.Engine):

    def __init__(self, resolution=(1024, 768)):

        self.evManager = events.EventManager()

        # Load Tiled TMX map.
        # tiled_map = gw2.TiledMap(gw2.data.filepath('maps', 'level1.tmx'))
        self.tiled_map = maps.Map(self.evManager, 'level1.tmx')

        # Save special layers for easy access.
        self.avatar_group = self.tiled_map.entity_group
        self.collision_group = self.tiled_map.collision_group

        # The avatar. Note: this is also the camera target.
        self.avatar = entity.Avatar((650, 690))

        resolution = gw2.Vec2d(resolution)
        caption = ('Moose on the Move')

        # The big cahoona.  This initializes the pgame screen, creates
        # the map and world, initializes the camera and game controllers,
        # and saves global state.
        gw2.Engine.__init__(
            self,
            caption=caption,
            resolution=resolution,
            camera_target=self.avatar,
            map=self.tiled_map,
            frame_speed=0)

        # Conserve CPU.
        gw2.State.clock.use_wait = True

        # Insert avatar into the Fringe layer.
        self.avatar_group.add(self.avatar)

        # A dummy to try moving before updating the avatar.
        self.collision_dummy = entity.Avatar((0, 0))

        # The renderer.
        self.renderer = gw2.BasicMapRenderer(
            self.tiled_map, max_scroll_speed=gw2.State.speed)
        # New requirement. When renderer draws dynamic layers (e.g. Fringe)
        # we need to tell it to redraw the changed tiles. This also is done
        # in the draw cycle; see self.draw_renderer().
        self.dirty_rect = pl.Rect(self.avatar.rect)
        self.renderer.set_dirty(self.dirty_rect)

        # I like huds.
        gw2.toolkit.make_hud()
        gw2.State.hud.add(
            'Max FPS', gw2.Statf(
                gw2.State.hud.next_pos(),
                'Max FPS %d', callback=lambda: gw2.State.clock.max_fps,
                interval=1.0))
        gw2.State.hud.add(
            'Use Wait', gw2.Statf(
                gw2.State.hud.next_pos(),
                'Use Wait %s', callback=lambda: gw2.State.clock.use_wait,
                interval=1.0))
        gw2.State.hud.add(
            'Tile Size', gw2.Statf(
                gw2.State.hud.next_pos(),
                'Tile Size %s', callback=lambda: '{0} pixels (key={1})'.format(
                    self.renderer.tile_size,
                    gw2.State.camera.rect.w // self.renderer.tile_size),
                    interval=1.0))

        # Create a speed box for converting mouse position to destination
        # and scroll speed.
        self.speed_box = gw2.geometry.Diamond(0, 0, 4, 2)
        self.speed_box.center = gw2.Vec2d(gw2.State.camera.rect.size) // 2
        self.max_speed_box = float(self.speed_box.width) / 3.33

        # Mouse and movement state. move_to is in world coordinates.
        self.move_to = None
        self.speed = None
        self.target_moved = (0, 0)
        self.mouse_down = False

        gw2.State.speed = 3.33

    def update(self, dt):
        """overrides Engine.update"""
        # If mouse button is held down update for continuous walking.
        if self.mouse_down:
            self.update_mouse_movement(pygame.mouse.get_pos())
        self.update_camera_position()
        gw2.State.camera.update()
        gw2.State.hud.update(dt)

    def update_mouse_movement(self, pos):
        # Angle of movement.
        # angle = geometry.angle_of(self.speed_box.center, pos)
        # Final destination.
        self.move_to = None
        for edge in self.speed_box.edges:
            # line_intersects_line() returns False or (True,(x,y)).
            cross = gw2.geometry.line_intersects_line(edge, (
                self.speed_box.center, pos))
            if cross:
                x, y = cross[0]
                self.move_to = gw2.State.camera.screen_to_world(pos)
                self.speed = gw2.geometry.distance(
                    self.speed_box.center, (x, y)) / self.max_speed_box
                break

    def update_camera_position(self):
        """update the camera's position if any movement keys are held down
        """
        if self.move_to is not None:
            camera = gw2.State.camera
            wx, wy = camera.position
            # Speed formula.
            speed = self.speed * gw2.State.speed
            # If we're within spitting distance, then taking a full step would
            # overshoot the desired destination. Therefore, we'll jump there.
            dist = gw2.geometry.distance((wx, wy), self.move_to)
            if dist < speed:
                wx, wy = self.move_to
                self.move_to = None
            else:
                # Otherwise, calculate the full step.
                angle = gw2.geometry.angle_of((wx, wy), self.move_to)
                wx, wy = gw2.geometry.point_on_circumference(
                    (wx, wy), speed, angle)
            # Check collision with environment.
            avatar = self.avatar
            dummy = self.collision_dummy
            dummy.position = wx, wy
            get_objects = self.collision_group.objects.intersect_objects
            # Collision handling.
            hits = get_objects(dummy.hitbox)
            if not hits:
                pass
            else:
                # Try move x
                dummy.position = wx, avatar.position.y
                hits = get_objects(dummy.hitbox)
                if not hits:
                    wy = avatar.position.y
                else:
                    # Try move y
                    dummy.position = avatar.position.x, wy
                    hits = get_objects(dummy.hitbox)
                    if not hits:
                        wx = avatar.position.x
                    else:
                        # Can't move
                        self.move_to = None
                        return
            # Keep avatar inside map bounds.
            rect = gw2.State.world.rect
            wx = max(min(wx, rect.right), rect.left)
            wy = max(min(wy, rect.bottom), rect.top)
            camera.position = wx, wy
            self.avatar_group.add(avatar)

    def toggle_layer(self, i):
        """toggle visibility of layer i"""
        try:
            layer = gw2.State.map.layers[i]
            layer.visible = not layer.visible
            self.renderer.clear()
        except:
            pass

    def draw(self, interp):
        """overrides Engine.draw"""
        # Draw stuff.
        gw2.State.screen.clear()
        self.draw_renderer()
        if False:
            self.draw_debug()
        gw2.State.hud.draw()
        gw2.State.screen.flip()

    def draw_renderer(self):
        """renderer draws map layers"""

        renderer = self.renderer

        # If panning, mark the renderer's tiles dirty where avatar is.
        panning = False
        camera = gw2.State.camera
        camera_rect = camera.rect
        dirty_rect = self.dirty_rect
        camera_center = camera_rect.center
        if camera.target.rect.center != camera_center:
            dirty_rect.center = camera_center
            renderer.set_dirty(dirty_rect)
            panning = True

        # Set render's rect and draw the screen.
        renderer.set_rect(center=camera_center)
        renderer.draw_tiles()

        # Must mark dirty rect before next call to draw(), otherwise avatar
        # leaves little artifacts behind.
        if panning:
            renderer.set_dirty(dirty_rect)

    def draw_debug(self):
        # draw the hitbox and speed box
        camera = gw2.State.camera
        cx, cy = camera.rect.topleft
        rect = self.avatar.hitbox
        pygame.draw.rect(camera.surface, pl.Color('red'), rect.move(-cx, -cy))
        pygame.draw.polygon(
            camera.surface, pl.Color('white'), self.speed_box.corners, 1)

    def on_mouse_button_down(self, pos, button):
        self.mouse_down = True

    def on_mouse_button_up(self, pos, button):
        self.mouse_down = False

    def on_key_down(self, unicode, key, mod):
        if key == pl.K_ESCAPE:
            gw2.context.pop()
        elif key >= pl.K_1 and key <= pl.K_9:
            if mod & pl.KMOD_SHIFT:
                num_tiles = key - pl.K_0
                self.renderer.tile_size = gw2.State.camera.rect.w // num_tiles
            else:
                self.toggle_layer(key - pl.K_0)
        elif key == pl.K_w:
            gw2.State.clock.use_wait = not State.clock.use_wait
        elif key == pl.K_SPACE:
            clock = gw2.State.clock
            if clock.max_fps <= 540:
                if clock.fps > clock.max_fps - 60:
                    clock.max_fps += 60
                else:
                    clock.max_fps = 0
            else:
                clock.max_fps = 0

    def on_quit(self):
        gw2.context.pop()


def main():
    app = App()
    gw2.run(app)


if __name__ == '__main__':
    if False:
        cProfile.run('main()', 'prof.dat')
        p = pstats.Stats('prof.dat')
        p.sort_stats('time').print_stats()
    else:
        main()
