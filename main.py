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
        self.is_mbu = False # IS Mouse Button Up
        self.buttonpressed = 0#-1
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
        if False: raise Exception("Error: False == True")
        elif state == "default": return assets.GUI.drawer.default
        elif state == "hover": return assets.GUI.drawer.hover
        elif state == "clicking": return assets.GUI.drawer.pushing
        elif state == "pushed": return assets.GUI.drawer.push
        else: raise TypeError("state is invalid.")
    
    def redrawGUI(self):
        changed = False
        defState = self.getImgDrawerFromStr("default")
        mp = pygame.mouse.get_pressed()[0]
        for i in range(len(self.data.drawer)):
            pos = (0, i * defState.get_height() * self.scale)
            coll = pygame.Rect(*pos, defState.get_width()*self.scale, defState.get_height()*self.scale).collidepoint(pygame.mouse.get_pos())
            if coll:
                changed = True
            if mp and coll:
                img = self.getImgDrawerFromStr("clicking")
            elif coll and self.buttonpressed != i:
                img = self.getImgDrawerFromStr("hover")
            else:
                img = self.getImgDrawerFromStr(["default", "pushed"][self.buttonpressed == i])
            if self.is_mbu and coll:
                #if self.buttonpressed == i:
                #    self.buttonpressed = -1
                #else:
                self.buttonpressed = i
                self.is_mbu = False
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

            img = self.data.drawer[i]["img"]
            self.GUISurface.blit(
                pygame.transform.scale(
                    img,
                    (
                        img.get_width() * self.scale,
                        img.get_height() * self.scale
                    )
                ),
                (
                    self.scale * 3,
                    (i * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2)
                )
            )
        self.hasUpdated = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if changed else pygame.SYSTEM_CURSOR_ARROW)

    def tick(self):
        for event in pygame.event.get():
            #print("Event of type " + str(event.type))
            if event.type == pygame.QUIT:
                self.DONE = True
            if event.type == pygame.MOUSEMOTION:
                GUI.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                GUI.is_mbu = True
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