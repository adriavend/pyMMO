#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import pygame

from client import director


def main():

    dir = director.SingletonDirector()
    dir.loop()

if __name__ == '__main__':
    pygame.init()
    main()