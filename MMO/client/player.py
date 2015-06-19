#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame

import config


class Player(pygame.sprite.Sprite):
    def __init__(self, id, nickname):
        pygame.sprite.Sprite.__init__(self)

        self.image_player_stop_right = pygame.image.load(config.PATH_SPRITES + "player_stop_right.png").convert_alpha()
        self.image_player_go_right = pygame.image.load(config.PATH_SPRITES + "player_go_right.png").convert_alpha()
        self.image_player_stop_left = pygame.image.load(config.PATH_SPRITES + "player_stop_left.png").convert_alpha()
        self.image_player_go_left = pygame.image.load(config.PATH_SPRITES + "player_go_left.png").convert_alpha()

        self.image_player_stop_top = pygame.image.load(config.PATH_SPRITES + "player_stop_top.png").convert_alpha()
        self.image_player_go_top = pygame.image.load(config.PATH_SPRITES + "player_go_top.png").convert_alpha()
        self.image_player_stop_bottom = pygame.image.load(
            config.PATH_SPRITES + "player_stop_bottom.png").convert_alpha()
        self.image_player_go_bottom = pygame.image.load(config.PATH_SPRITES + "player_go_bottom.png").convert_alpha()
        self.image_player_explosion = pygame.image.load(config.PATH_SPRITES + "explosion.png").convert_alpha()

        self.images = [
            [self.image_player_stop_right, self.image_player_go_right],
            [self.image_player_stop_left, self.image_player_go_left],
            [self.image_player_stop_bottom, self.image_player_go_bottom],
            [self.image_player_stop_top, self.image_player_go_top]
        ]

        self.image_current = 0
        self.image = self.images[self.image_current][0]

        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = (config.SCREEN_HEIGHT / 2, config.SCREEN_WIDTH / 2)

        self.is_moving = False
        self.orientation = 0

        self.posX = self.rect.x
        self.posY = self.rect.y

        self.id = id
        self.nickname = nickname

        self.rect_nickname = None
        self.rect_border_nickname = None
        
        self.font_object = pygame.font.Font(None, 16)

        self.heart = 5

    def is_collision_brick(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick.rect):
                return True
        return False

    def is_collision_monsters(self, monsters):
        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                return True
        return False

    def is_collision_port(self, port):
        if None == port:
            return False

        if self.rect.colliderect(port.rect):
            return True
        return False

    def is_collision_players(self, players):
        for p in players:
            if self.rect.colliderect(p.rect):
                return True
        return False

    def is_collision_treasure(self, treasure):
        if None == treasure:
            return False

        if self.rect.colliderect(treasure.rect):
            return True
        return False

    def update(self, vx, vy, t):
        if (vx, vy) == (0, 0):
            self.is_moving = False
        else:
            self.is_moving = True

        if vx > 0 and vy == 0:
            self.orientation = 0
        elif vx < 0 and vy == 0:
            self.orientation = 1
        elif vx == 0 and vy > 0:
            self.orientation = 2
        elif vx == 0 and vy < 0:
            self.orientation = 3

        if t == 1 and self.is_moving:
            self.next_image()

        self.image = self.images[self.orientation][self.image_current]

        self.rect.move_ip(vx, vy)

        if not self.rect_nickname == None:
            self.rect_nickname.move_ip(vx, vy)

        if not self.rect_border_nickname == None:
            self.rect_border_nickname.move_ip(vx, vy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.heart == 5 or self.heart == 4:
            color_heart = config.COLOR_GREEN
        elif self.heart == 3 or self.heart == 2:
            color_heart = config.COLOR_YELLOW
        elif self.heart == 6: #Se trata de otro player.
            color_heart = config.COLOR_LIGHTBLUE
        else:
            color_heart = config.COLOR_RED

        if self.heart == 6 or self.heart == 5:
            porc = 1.0
        else:
            porc = float(self.heart) / 5

        self.rect_nickname = pygame.draw.rect(screen, color_heart, (self.rect.left - 4, self.rect.top - 10, 40*porc, 10), 0)
        self.rect_border_nickname = pygame.draw.rect(screen, config.COLOR_BLACK, (self.rect.left - 4, self.rect.top - 10, 40, 10), 1)
        screen.blit(self.font_object.render(self.nickname, 1, config.COLOR_BLACK),
                        (self.rect.left - 4, self.rect.top - 10))

    def next_image(self):
        self.image_current += 1

        if self.image_current > len(self.images[self.orientation]) - 1:
            self.image_current = 0

    def change_image_explosion(self):
        self.image = self.image_player_explosion

    """
        Part for Server.
        ----------------
        Metodo que actuliza la posicion segun le indique el server. Este metodo es para actulizar los players que estan
         en el mapa.
    """
    def server_update(self, x, y, o, c):
        self.image = self.images[o][c]
        self.rect.left = x
        self.rect.top = y

    def collision_flecha(self, flechas):
        for f in flechas:
            if self.rect.colliderect(f.rect):
                self.heart -= 1