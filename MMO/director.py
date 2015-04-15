#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import config


class Director:
    """Representa el objeto Principal del Juego.
	
	El objeto Director mantiene en funcionamiento el juego, se
    encarga de actualizar, dibuja y propagar eventos.
 
    Tiene que utilizar este objeto en conjunto con objetos
    derivados de Scene."""

    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.name)
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
        self.vx = 0
        self.vy = 0
        self.left_sigue_apretada, self.right_sigueapretada, self.up_sigueapretada, self.down_sigueapretada = False, False, False, False

    def loop(self):
        "Pone en Funcionamiento el Juego"

        while not self.quit_flag:
            self.screen.fill(config.COLOR_WHITE)
            self.time = self.clock.tick(20)

            #Eventos de Salida
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_flag = True

            # Detecta Eventos
            self.scene.on_event(events)

            # Actualiza la Escena
            self.scene.on_update()

            # Dibuja la Pantalla
            self.scene.on_draw(self.screen)

            pygame.display.update()
            # pygame.display.flip() #Actualizar la superficie de visualización por completo sobre la pantalla.

        pygame.quit()

    def change_scene(self, scene):
        "Altera la escena actual."
        self.scene = scene

    def quit(self):
        self.quit_flag = True
