import pygame

pygame.init()

clock = pygame.time.Clock()

# Window size, change as you wish
winSize = (1000, 600)
WIN = pygame.display.set_mode(winSize)

# I did not make the "fill(surface, color)" function. Big thanks to Stack Overflow (https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen)
def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

# Assets class...
class Assets():
    def __init__(self) -> None:
        class Gui():
            def __init__(self) -> None:
                class Font():
                    def __init__(self) -> None:
                        size = 64
                        class Minecraft():
                            def __init__(self) -> None:
                                self.bold = pygame.font.Font('textures/gui/font/Minecraft Bold.otf', size)
                                self.italic = pygame.font.Font('textures/gui/font/Minecraft Italic.otf', size)
                                self.regualr = pygame.font.Font('textures/gui/font/Minecraft.otf', size)
                                self.bold_italic = pygame.font.Font('textures/gui/font/Minecraft Bold-Italic.otf', size)
                        self.minecraft = Minecraft()

                        self.minecraftTen = pygame.font.Font('textures/gui/font/Minecraft Ten.ttf', size)
                self.font = Font()

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
                self.glass = pygame.image.load("textures/glass.png")
                self.hay = pygame.image.load("textures/hay_block_side.png")
                self.note_block = pygame.image.load("textures/note_block.png")
                self.emerald_block = pygame.image.load("textures/emerald_block.png")
                self.wool = pygame.image.load("textures/light_blue_wool.png")
                self.soul_sand = pygame.image.load("textures/soul_sand.png")
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
                        "font": assets.GUI.font.minecraftTen,
                        "img": assets.BLOCKS.pumpkin,
                    },
                    {
                        "state": "default",
                        "text": "Goodbye!",
                        "font": assets.GUI.font.minecraft.regualr,
                        "img": assets.BLOCKS.soul_sand,
                    },
                    {
                        "state": "default",
                        "text": "Bonjour!",
                        "font": assets.GUI.font.minecraft.bold,
                        "img": assets.BLOCKS.emerald_block,
                    },
                    {
                        "state": "default",
                        "text": "Au revoir!",
                        "font": assets.GUI.font.minecraft.italic,
                        "img": assets.BLOCKS.note_block,
                    },
                    {
                        "state": "default",
                        "text": "Comment vas-tu?",
                        "font": assets.GUI.font.minecraft.bold_italic,
                        "img": assets.BLOCKS.hay,
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
            if coll and self.buttonpressed == i: changed = False
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
            
            img = self.data.drawer[i]["font"].render(self.data.drawer[i]["text"], False, (255, 255, 255))

            print("Index:" + str(i) + ", Text: " + str(self.data.drawer[i]["text"]))
    
            img = pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale / 4,
                    img.get_height() * self.scale / 4
                )
            )

            self.GUISurface.blit(
                img,
                (
                    self.scale * 4 + self.data.drawer[i]["img"].get_width() * self.scale + self.scale,
                    ((i + 1) * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2) + (self.scale * 1 if self.data.drawer[i]["font"] != assets.GUI.font.minecraftTen else self.scale * 2)
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