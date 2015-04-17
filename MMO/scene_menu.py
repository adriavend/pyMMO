__author__ = 'Bachi'

import pygame
import scene
import config
import cursor
import boton

class SceneMenu(scene.Scene):
     def __init__(self, director):
        scene.Scene.__init__(self, director)
        self.Cursor = cursor.cursor()
        self.botonStart = boton.Boton(pygame.image.load(config.sprites+"start.png").convert_alpha(), pygame.image.load(config.sprites+"start.png").convert_alpha())

     def on_update(self):
        return

     def on_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cursor.colliderect(self.botonStart.rect):
                    self.btnStartClick()


     def on_draw(self, screen):
        return

     def btnStartClick(self):
         dir.quit_flag = False



