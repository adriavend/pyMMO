import scene_game

__author__ = 'Bachi'

import pygame
import scene
import config
import cursor
import boton
import fondo
import sys

class SceneMenu(scene.Scene):
     def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.dir = director
        self.fondo = fondo.Fondo(config.BACK_SCENE_MENU)
        self.btn_start = boton.Boton(config.PATH_ICONS+"start.png" ,config.PATH_ICONS+"start_select.png",x=240, y=120)
        self.btn_exit = boton.Boton(config.PATH_ICONS+"salir.png", config.PATH_ICONS+"salir_select.png", x=280, y=270)
        self.btn_start_rect = self.btn_start.rect
        self.btn_exit_rect = self.btn_exit.rect
        self.cursor = cursor.Cursor()

     def on_update(self):
		self.cursor.update()

     def on_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cursor.colliderect(self.btn_start_rect):
                    scene_next = scene_game.SceneGame(self.dir)
                    self.dir.change_scene(scene_next)
                    self.dir.loop
                if self.cursor.colliderect(self.btn_exit_rect):
                    sys.exit()

     def on_draw(self, screen):
         self.fondo.draw(screen)
         self.btn_start.update(screen, self.cursor)
         self.btn_exit.update(screen, self.cursor)




