#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo para implementar el manejo de gráficos y superficies"""
 
# Módulos
import pygame
 
# Carga una imagen transparencia y color tranasparente opcionales.
def load_image(filename, transparent=False, pixel=(0,0)):
	"Carga una imagen al formato interno de pygame"
	try: image = pygame.image.load(filename)
	except pygame.error, message:
		raise SystemExit, message
	image = image.convert()
	
	if transparent:
		color = image.get_at(pixel)
		image.set_colorkey(color, pygame.RLEACCEL)
	return image
	
def text(texto, posx, posy, color=(0, 0, 0), tam=25):
	"Crea una imagen con su texto pasado y su rect"
	fuente = pygame.font.Font("../images/DroidSans.ttf", tam)
	salida = pygame.font.Font.render(fuente, texto, 1, color)
	salida_rect = salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect
