import scene_game

__author__ = 'Bachi'

import pygame
import scene
import config
import cursor
import boton
import fondo


class SceneMenu(scene.Scene):
     def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.dir = director
        self.caption = "Menu"
        self.fondo = fondo.Fondo(config.BACK_SCENE_MENU)
        self.btn_start = boton.Boton(config.BOTON_START_NORMAL,config.BOTON_START_SELECT,x=240, y=120)
        self.rect = self.btn_start.rect

        self.cursor = cursor.Cursor()

     def on_update(self):
		self.cursor.update()

     def on_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cursor.colliderect(self.btn_start.rect):
                    scene_next = scene_game.SceneGame(self.dir)
                    self.dir.change_scene(scene_next)
                    self.dir.loop

     def on_draw(self, screen):
         self.fondo.draw(screen)
         self.btn_start.update(screen, self.cursor)




