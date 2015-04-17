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
        self.caption = "Menu"
        self.botonClickeado = False

        self.fondo = fondo.Fondo(config.BACK_SCENE_MENU)
        self.botonStart = boton.Boton(config.SPRITE_BOTON_START,config.SPRITE_BOTON_START,x =240, y= 200)
        self.rect = self.botonStart.rect

        self.cursor = cursor.Cursor()


     def on_update(self):
        return

     def on_event(self, events):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cursor.colliderect(self.botonStart.rect):
                   self.botonClickeado = True

        self.cursor.update()


     def on_draw(self, screen):
        self.botonStart.draw(screen)

     def isBotonClickeado(self):
         return self.botonClickeado




