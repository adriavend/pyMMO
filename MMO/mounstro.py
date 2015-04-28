__author__ = 'Adrian'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config
import threading
import time
import random

from datetime import datetime              #Para monitorear los movimientos del monstruo
import sys
import exceptions

#archivo = open("c:/Facultad/Arquitectura de Software/monstruo.txt","w")     #Para monitorear los movimientos del monstruo
#log = open("c:/Facultad/Arquitectura de Software/log"+str(datetime.now().microsecond)+".txt","w")


class Mounstro(pygame.sprite.Sprite,threading.Thread):
    def __init__(self, x, y):
        #threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        threading.Thread.__init__(self)

        #Como hereda de Sprite hay que asignar estos atributos y el metodo update
        self.image_player = pygame.image.load(config.PATH_SPRITES+"monsters.png").convert_alpha()
        self.rect = self.image_player.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.stop_flag = False    

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick):
                return True
        return False

    #Hereda de Sprite
    def update(self, vx, vy):
        self.rect.move_ip(-vx, -vy)

        #now = datetime.now()                                                         #Para monitorear los movimientos del monstruo
        #archivo.write(str(now.microsecond) +"- "+ str(-vx) +','+str(-vy) + "\n")     #Para monitorear los movimientos del monstruo

    def draw(self, screen):
        screen.blit(self.image_player, self.rect)

    #Como hereda de Thread hay que sobreescribir este metodo
    def run(self):
        count = 0
        v = config.SPEED_GAME
        t = -1

        while self.stop_flag == False:
            # Adrian: Propuesta de movimiento aleatorio
            count += 1

            if count < 15:
                self.update(0, v*t)
                time.sleep(0.2)
            else:
                count = 0
                t = t*-1
                #archivo.close()    #Para monitorear los movimientos del monstruo
           
                


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

    def serverUpdate(self,x,y):
        #try:
            self.rect.move_ip(int(x),int(y))

        #except Exception as excp:
        #    #log.write("ARGUMENTOS: \n")
        #    #for arg in excp.args:
        #    #    log.write(arg +"\n")

        #    log = open("c:/Facultad/Arquitectura de Software/log"+str(datetime.now().microsecond)+".txt","w")
        #    log.write("MENSAJE: \n")
        #    log.write(excp.message)
        #    log.close()
      
    def stop(self):
        self.stop_flag = True