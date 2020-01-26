import pygame

from BaseClasses.Screen import Screen
from Screens.GameScreen.BackgroundSprite import BackgroundSprite
from Screens.GameScreen.Character import Character
from Screens.GameScreen.World import World
from Tools.Constants import size
from Tools.Tools import play_music


class GameScreen(Screen):
    def __init__(self, screen: pygame.display, parent):
        sprites = pygame.sprite.Group()
        self.sprites_dict = dict()

        bg = BackgroundSprite(self)
        sprites.add(bg)
        self.sprites_dict["background"] = bg

        self.char = Character(self)

        super().__init__(screen, parent, sprites)
        self.state = {"horizontalMovement": None, "falling": False, "jump": 0, "attack": 0}
        self.world = World()
        self.locked = False

        play_music("GameScreen/music.wav", loop=True)

    def notify(self, event: pygame.event):
        if self.locked:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state["horizontalMovement"] = self.char.right = event.key == pygame.K_RIGHT
                self.char.item = "Run"
                self.char.frame = -1
            elif event.key == pygame.K_UP and self.state["jump"] == 0 and not self.state["falling"]:
                self.state["jump"] = 20
                self.char.item = "Run"
                self.char.frame = -1
            elif event.key == pygame.K_SPACE:
                self.state["attack"] = 15
                self.char.item = "Attack"
                self.char.frame = -1
                self.state["horizontalMovement"] = None
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.state["horizontalMovement"] = None

    def pending_updates(self):
        if not self.locked:
            self.state["falling"] = self.world.should_fall(self.char)
            if self.state["horizontalMovement"] is not None:
                delta = 7
                if self.state["horizontalMovement"]:
                    delta = -delta
                if self.world.can_go_there(self.char, delta):
                    self.sprites_dict["background"].update(delta)
                    self.world.update(delta)
            if self.state["jump"] > 0:
                self.state["jump"] -= 1
                self.char.update_pos(-self.state["jump"] * 3 // 2)
            elif self.state["falling"]:
                self.char.update_pos(10)
            elif self.state["horizontalMovement"] is None and self.state["attack"] == 0:
                self.char.item = "Idle"
            self.check_char()
            if self.state["attack"] > 0:
                self.state["attack"] -= 1
        self.char.update_image()

    def check_char(self):
        if self.world.in_water(self.char):
            self.locked = True
            self.char.item = "Died"
            self.char.frame = -1

    def create_surface(self) -> pygame.Surface:
        surface = pygame.Surface(size)

        self.sprites.draw(surface)
        self.world.draw(surface)
        self.char.draw(surface)

        return surface
