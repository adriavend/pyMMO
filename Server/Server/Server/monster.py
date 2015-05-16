#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import threading
import time
import random

class Monster():
    def __init__(self):
        self.stop_flag = False
        self.x = 40
        self.y = 50

        self.count = 0
        self.t = -1
        self.v = config.SPEED_GAME

    def step(self):
       self.count += 1
       mov = 0
       if self.count < 15:
           mov = (self.v*self.t)
       else:
           self.count = 0
           self.t= self.t*-1

       if mov == 0:
           return "00,00"
       else:
           return "00" +',' + str(mov)


    def stop(self):
        self.stop_flag = True

    def caminar(self,num):
        self.y + num;

    def getPosition(self):
        rnd = random.randint(1,4)
        if rnd < 3:
            return "40,50"
        if rnd > 2:
            return "50,50"
        



       

