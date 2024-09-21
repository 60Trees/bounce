import pygame

pygame.init()

clock = pygame.time.Clock()

# Window size, change as you wish
winSize = (1000, 600)
WIN = pygame.display.set_mode(winSize)

# Assets class...
class Assets():
    def __init__(self) -> None:
        class Gui():
            def __init__(self) -> None:
                class Drawer():
                    def __init__(self) -> None:
                        self.default = pygame.image.load("textures/gui/other/_drawerTile.png")
                        self.hover = pygame.image.load("textures/gui/other/_drawerTileHover.png")
                        self.pushing = pygame.image.load("textures/gui/other/_drawerTilePushedBeing.png")
                        self.push = pygame.image.load("textures/gui/other/_drawerTilePushed.png")
                self.drawer = Drawer()
        self.GUI = Gui()

        class Blocks():
            def __init__(self) -> None:
                self.pumpkin = pygame.image.load("textures/pumpkin_side.png")
        self.BLOCKS = Blocks()

    def refreshAssets(self):
        self.__init__()
assets = Assets()
# Input class...
class Input():
    def __init__(self) -> None:
        class Keyboard():
            def __init__(self) -> None:
                self.keysPressed = pygame.key.get_pressed()
        self.keyboard = Keyboard()

        class Mouse():
            def __init__(self) -> None:
                self.mousePos = pygame.mouse.get_pos()
                self.mousePosX, self.mousePosY = self.mousePos
                self.mousePos = pygame.mouse.get_pos()
        self.mouse = Mouse()

    def update(self):
        self.keyboard.keysPressed = pygame.key.get_pressed()
        self.mouse.mousePos = pygame.mouse.get_pos()
        self.mouse.keysPressed = pygame.key.get_pressed()
        self.mouse.mousePosX, self.mouse.mousePosY = self.mouse.mousePos
inp = Input()

# GUI class...
class Gui():
    def __init__(self) -> None:
        self.GUISurface = pygame.display.set_mode(winSize)
        self.hasUpdated = False
        self.scale = 4
        class Data():
            def __init__(self) -> None:
                self.drawer = [
                    {
                        "state": "default",
                        "text": "Hello!",
                        "img": assets.BLOCKS.pumpkin,
                    },
                    {
                        "state": "default",
                        "text": "Goodbye!",
                        "img": assets.BLOCKS.pumpkin,
                    },
                    {
                        "state": "default",
                        "text": "Bonjour!",
                        "img": assets.BLOCKS.pumpkin,
                    },
                    {
                        "state": "default",
                        "text": "Au revoir!",
                        "img": assets.BLOCKS.pumpkin,
                    },
                    {
                        "state": "default",
                        "text": "Comment vas-tu?",
                        "img": assets.BLOCKS.pumpkin,
                    },
                ]
        self.data = Data()

    def update(self):
        self.hasUpdated = True

    def getImgDrawerFromStr(self, state):
        if False: raise Exception("Why is False == True?")
        elif state == "default": return assets.GUI.drawer.default
        elif state == "hover": return assets.GUI.drawer.hover
        elif state == "pushing": return assets.GUI.drawer.pushing
        elif state == "push": return assets.GUI.drawer.push
        else: raise TypeError("state is invalid.")
    
    def redrawGUI(self):
        for i in range(len(self.data.drawer)):
            img = self.getImgDrawerFromStr(self.data.drawer[i]["state"]) # For simplicity.

            if self.data.drawer[i]["state"] == "hover": self.data.drawer[i]["state"] = "default"

            if inp.mouse.mousePosX < img.get_width() * self.scale:
                print(f"MX ({inp.mouse.mousePosX}) < {img.get_width() * self.scale}, b1")

                if inp.mouse.mousePosY > img.get_height() * self.scale * i:
                    print(f"MY ({inp.mouse.mousePosY}) < {img.get_height() * self.scale * i}, b2")

                    if inp.mouse.mousePosY < img.get_height() * (i + 1) * self.scale:
                        print(f"MY ({inp.mouse.mousePosY}) < {img.get_height() * (i + 1) * self.scale}, b3. Done")

                        self.data.drawer[i]["state"] = "hover"
            
            img = self.getImgDrawerFromStr(self.data.drawer[i]["state"]) # For simplicity.

            self.GUISurface.blit(
                pygame.transform.scale(
                    img,
                    (
                        img.get_width() * self.scale,
                        img.get_height() * self.scale
                    )
                ),
                    (
                        0,
                        i * img.get_height() * self.scale
                    )
            )
        self.hasUpdated = False

    def tick(self):
        for event in pygame.event.get():
            #print("Event of type " + str(event.type))
            if event.type == pygame.QUIT:
                self.DONE = True
            if event.type == pygame.MOUSEMOTION:
                GUI.update()
GUI = Gui()

# Game class...
class Game():
    def __init__(self) -> None:
        # Target FPS
        self.TargetFPS = 60
        self.DONE = False
        
    def tick(self):
        # Loop code here...
        pass
game = Game()

GUI.redrawGUI()
while not game.DONE:
    WIN.fill((0, 0, 0))

    inp.update()
    game.tick()
    GUI.tick()

    GUI.redrawGUI()
    WIN.blit(GUI.GUISurface, (0, 0))

    pygame.display.flip()

    clock.tick(game.TargetFPS)

pygame.quit()