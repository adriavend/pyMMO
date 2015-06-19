__author__ = 'Bachi'

import scene, pygame, fondo, config
import sys

class SceneGameover(scene.Scene):

    def __init__(self,id_winner,nickname_winner):
        self.id_winner = id_winner
        self.nickname_winner = nickname_winner

        pygame.mouse.set_visible(False)

        self.fondo = fondo.Fondo(config.PATH_BACKS + "GAMEOVER.png")


    def on_update(self):
        pass

    def on_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

    def on_draw(self, screen):
        self.fondo.draw(screen)
        fontobjectName = pygame.font.Font(None, 50)
        fontobjectNum = pygame.font.Font(None, 50)

        screen.blit(fontobjectName.render("Jugador ganador: "+self.nickname_winner, 1, config.COLOR_WHITE),
                        ((5), 10))

        # screen.blit(fontobjectNum.render("Numero: "+str(self.id_winner), 1, config.COLOR_WHITE),
        #                 ((5), 55))
        pass
