import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.BackgroundSprite import BackgroundSprite


class GameScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        sprites = pygame.sprite.Group()
        self.sprites_dict = dict()

        bg = BackgroundSprite(self)
        sprites.add(bg)
        self.sprites_dict["background"] = bg

        super().__init__(screen, parent, sprites)
        self.state = {"horizontalMovement": None}

    def notify(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state["horizontalMovement"] = event.key == pygame.K_RIGHT
            else:
                print(event)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state["horizontalMovement"] = None
            else:
                print(event)

    def pending_updates(self):
        if self.state["horizontalMovement"] is not None:
            self.sprites_dict["background"].update(self.state["horizontalMovement"])
