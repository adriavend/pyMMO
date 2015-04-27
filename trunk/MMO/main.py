#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import director
import scene_menu

def main():
    dir = director.Director()
    dir.loop()

if __name__ == '__main__':
    pygame.init()
    main()
