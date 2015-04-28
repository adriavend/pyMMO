#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import threading
import time
import random

class Monster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_flag = False
        self.x = 40
        self.y = 50

        self.count = 0
        self.t = -1
        self.v = config.SPEED_GAME

    #Como hereda de Thread hay que sobreescribir este metodo
    def run(self):
        count = 0
        v = config.SPEED_GAME
        t = -1

        while self.stop_flag == False:
            # Adrian: Propuesta de movimiento aleatorio
            count += 1

            if count < 15:
                self.y = (v*t)
                time.sleep(0.1)
            else:
                count = 0
                t = t*-1

            # Bachi: probando movimiento aleatorio
            # rnd = random.randint(1,4)
            # if rnd == 1:
            #    self.update(-1,0)   #izquierda
            # if rnd == 2:
            #    self.update(1,0)    #derecha
            # if rnd == 1:
            #    self.update(0,1)    #arriba
            # if rnd == 1:
            #    self.update(0,-1)   #abajo

    def stop(self):
        self.stop_flag = True

    def caminar(self,num):
        self.y + num;

    def posicion(self):
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

       

