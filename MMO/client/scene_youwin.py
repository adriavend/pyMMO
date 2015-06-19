__author__ = 'Bachi'

import scene,pygame,fondo,config

class SceneYouWin(scene.Scene):

    def __init__(self):
        #self.winner_player = winner_player

        pygame.mouse.set_visible(False)

        self.fondo = fondo.Fondo(config.PATH_BACKS + "YOUWIN.png")


    def on_update(self):
        pass

    def on_event(self, events):
        pass

    def on_draw(self, screen):
        self.fondo.draw(screen)
        #fontobject = pygame.font.Font(None, 90)

        #screen.blit(fontobject.render(self.winner_player, 1, config.COLOR_WHITE),
        #                ((screen.get_width() / 4), 10))
        pass