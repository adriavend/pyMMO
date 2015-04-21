#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import director
import scene_menu

def main():
    dir = director.Director()
    scene_init = scene_menu.SceneMenu(dir)
    dir.change_scene(scene_init)
    dir.loop()

if __name__ == '__main__':
    pygame.init()
    main()
