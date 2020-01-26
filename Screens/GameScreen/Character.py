from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite
from Tools.Tools import load_image

LEFT = {"Attack": [], "Died": [], "Run": [], "Idle": []}
RIGHT = {"Attack": [], "Died": [], "Run": [], "Idle": []}


class Character(Sprite):
    def __init__(self, parent: Screen):
        super().__init__("GameScreen/Character/Right/Idle.png", parent, left=640, top=360, center=True)
        for i in range(15):
            LEFT["Attack"].append(load_image(f"GameScreen/Character/Left/Attack/{i}.png"))
            RIGHT["Attack"].append(load_image(f"GameScreen/Character/Right/Attack/{i}.png"))
        for i in range(30):
            LEFT["Died"].append(load_image(f"GameScreen/Character/Left/Died/{i}.png"))
            RIGHT["Died"].append(load_image(f"GameScreen/Character/Right/Died/{i}.png"))
        for i in range(15):
            LEFT["Run"].append(load_image(f"GameScreen/Character/Left/Run/{i}.png"))
            RIGHT["Run"].append(load_image(f"GameScreen/Character/Right/Run/{i}.png"))
        LEFT["Idle"].append(load_image(f"GameScreen/Character/Left/Idle.png"))
        RIGHT["Idle"].append(load_image(f"GameScreen/Character/Right/Idle.png"))

        self.item = "Idle"
        self.right = True
        self.frame = -1

    def on_click(self) -> None:
        pass

    def update_image(self):
        if self.right:
            self.frame = (self.frame + 1) % len(RIGHT[self.item])
            self.image = RIGHT[self.item][self.frame]
        else:
            self.frame = (self.frame + 1) % len(LEFT[self.item])
            self.image = LEFT[self.item][self.frame]

    def update_pos(self, delta_y):
        self.rect.top += delta_y
