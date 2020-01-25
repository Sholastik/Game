from BaseClasses.Screen import Screen
from BaseClasses.Sprite import Sprite


class StartButtonSprite(Sprite):
    def __init__(self, parent: Screen) -> None:
        super(StartButtonSprite, self).__init__("StartScreen/start_button.png", parent, left=640, top=480, center=True)

    def on_click(self) -> None:
        from StartScreen.StartScreen import StartScreen
        self.parent: StartScreen
        self.parent.load_game()
