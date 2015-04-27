#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import config

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image_player_stop_right = pygame.image.load(config.PATH_SPRITES+"player_stop_right.png").convert_alpha()
        self.image_player_go_right = pygame.image.load(config.PATH_SPRITES+"player_go_right.png").convert_alpha()
        self.image_player_stop_left = pygame.image.load(config.PATH_SPRITES+"player_stop_left.png").convert_alpha()
        self.image_player_go_left = pygame.image.load(config.PATH_SPRITES+"player_go_left.png").convert_alpha()
        self.image_player_explosion = pygame.image.load(config.PATH_SPRITES+"explosion.png").convert_alpha()

        self.imagenes = [[self.image_player_stop_right, self.image_player_go_right],[self.image_player_stop_left, self.image_player_go_left]]

        self.image_current = 0
        self.image = self.imagenes[self.image_current][0]

        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = (config.SCREEN_HEIGHT / 2, config.SCREEN_WIDTH / 2)

        self.is_moving = False
        self.orientation = 0

    def is_collision(self, wall):
        for brick in wall:
            if self.rect.colliderect(brick.rect):
                return True
        return False

    def is_collision_monsters(self, monster):
        if self.rect.colliderect(monster.rect):
                return True
        return False

    def update(self, vx, vy, t):
        if (vx, vy) == (0, 0):
            self.is_moving = False
        else:
            self.is_moving = True

        if vx > 0:
            self.orientation = 0
        elif vx < 0:
            self.orientation = 1

        if t == 1 and self.is_moving:
            self.next_image()

        self.image = self.imagenes[self.orientation][self.image_current]
        self.rect.move_ip(vx, vy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def next_image(self):
        self.image_current += 1

        if self.image_current > len(self.imagenes) -1:
            self.image_current = 0

    def change_image_explosion(self):
        self.image = self.image_player_explosion
