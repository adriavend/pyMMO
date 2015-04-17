#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame
import director
import scene_game
import scene_menu


def main():
    dir = director.Director()

    #scene = scene_game.SceneGame(dir)
    #scene = scene_menu.SceneMenu(dir)

    #dir.change_scene(scene)

    #dir.loop()
    dir.start()



if __name__ == '__main__':
    pygame.init()
    main()
