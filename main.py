from tkinter import filedialog
import pygame, os, math, copy, tkinter

pygame.init()

clock = pygame.time.Clock()

GUI_SCALE = 3

# Window size, change as you wish
winSize = (1000, 600)
WIN = pygame.display.set_mode(winSize)

def recolourImage(surface, colour):
    surface = surface.convert_alpha()
    w, h = surface.get_size()

    colored_image = pygame.Surface((w, h), pygame.SRCALPHA)
    
    for x in range(w):
        for y in range(h):
            pixel_color = surface.get_at((x, y))
            a = pixel_color[3] / 255.0
            if a > 0:
                new_color = (colour[0], colour[1], colour[2], int(a * 255))
                colored_image.set_at((x, y), new_color)
    return colored_image

# Assets class...
class Assets():
    def __init__(self) -> None:
        class Gui():
            def __init__(self) -> None:
                class Font():
                    def __init__(self) -> None:
                        size = GUI_SCALE * 16
                        class Minecraft():
                            def __init__(self) -> None:
                                self.bold = pygame.font.Font('textures/gui/font/Minecraft Bold.otf', size)
                                self.italic = pygame.font.Font('textures/gui/font/Minecraft Italic.otf', size)
                                self.regualr = pygame.font.Font('textures/gui/font/Minecraft.otf', size)
                                self.bold_italic = pygame.font.Font('textures/gui/font/Minecraft Bold-Italic.otf', size)
                                self.ten = pygame.font.Font('textures/gui/font/Minecraft Ten.ttf', size)
                        self.minecraft = Minecraft()

                self.font = Font()

                class Drawer():
                    def __init__(self) -> None:
                        self.default = pygame.image.load("textures/gui/other/_drawerTile.png")
                        self.hover = pygame.image.load("textures/gui/other/_drawerTileHover.png")
                        self.pushing = pygame.image.load("textures/gui/other/_drawerTilePushedBeing.png")
                        self.push = pygame.image.load("textures/gui/other/_drawerTilePushed.png")
                self.drawer = Drawer()

                class Animation():
                    def __init__(self) -> None:
                        self.blockGlintStages = []

                        _, _, files = next(os.walk("textures/gui/other/anim"))

                        for i in range(len(files)):
                            self.blockGlintStages.append(pygame.image.load("textures/gui/other/anim/animStage" + str(i + 1) + ".png"))

                self.anim = Animation()
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

    def getFile(self):
        file_name = filedialog.askopenfilename()
        return file_name

    def getFolder(self):
        folder_path = filedialog.askdirectory()
        return folder_path

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
        self.SidebarGUI_underlay = pygame.display.set_mode(winSize)
        self.SidebarGUI_overlay = pygame.display.set_mode(winSize)
        self.SidebarGUI_overoverlay = pygame.display.set_mode(winSize)
        self.GUISurface = pygame.display.set_mode(winSize)
        self.hasUpdated = False
        self.is_mbu = False # IS Mouse Button Up
        self.buttonpressed = 0#-1
        self.scale = GUI_SCALE
        class Data():
            def __init__(self) -> None:
                self.drawerX_True = 0
                self.drawerX = self.drawerX_True
                self.drawerX += (self.drawerX - self.drawerX_True) / 2
                self.drawer = [
                    {
                        "state": "default",
                        "text": "My Projects",
                        "font": assets.GUI.font.minecraft.bold,
                        "img": assets.BLOCKS.note_block,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
                    },
                    {
                        "state": "default",
                        "text": "Options",
                        "font": assets.GUI.font.minecraft.regualr,
                        "img": assets.BLOCKS.soul_sand,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
                    },
                    {
                        "state": "default",
                        "text": "Settings",
                        "font": assets.GUI.font.minecraft.bold,
                        "img": assets.BLOCKS.emerald_block,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
                    },
                    {
                        "state": "default",
                        "text": "Help",
                        "font": assets.GUI.font.minecraft.italic,
                        "img": assets.BLOCKS.note_block,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
                    },
                    {
                        "state": "default",
                        "text": "Credits",
                        "font": assets.GUI.font.minecraft.bold_italic,
                        "img": assets.BLOCKS.hay,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
                    },
                    {
                        "state": "default",
                        "text": f"{self.drawerX}, {self.drawerX_True}",
                        "font": assets.GUI.font.minecraft.bold_italic,
                        "img": assets.BLOCKS.hay,
                        "imgAnimState": len(assets.GUI.anim.blockGlintStages)
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
        self.data.drawer[5]["text"] = f"{self.data.drawerX}, {self.data.drawerX_True}"
        global GUI_SCALE
        if self.scale != GUI_SCALE:
            GUI_SCALE = self.scale
        changed = False
        doGlint = False
        defState = self.getImgDrawerFromStr("default")
        mp = pygame.mouse.get_pressed()[0]

        img = self.getImgDrawerFromStr("default")
        self.SidebarGUI_underlay.blit(
            pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale,
                    WIN.get_height()
                )
            ),
            (
                0,
                0
            )
        )
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
                doGlint = True
                self.buttonpressed = i
                self.is_mbu = False
            self.SidebarGUI_underlay.blit(
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
            self.SidebarGUI_overlay.blit(
                pygame.transform.scale(
                    recolourImage(img, (0, 0, 0)),
                    (
                        img.get_width() * self.scale,
                        img.get_height() * self.scale
                    )
                ),
                (
                    self.scale * 3 + self.scale * 1,
                    (i * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2) + self.scale
                )
            )

            if True:
                img = self.data.drawer[i]["img"]
                self.SidebarGUI_overlay.blit(
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

                self.SidebarGUI_overlay.blit(
                    pygame.transform.scale(
                        img,
                        (
                            img.get_width() * self.scale / 4,
                            img.get_height() * self.scale / 4
                        )
                    ),
                    (
                        self.scale * 22,
                        ((i + 1) * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2) - self.scale * 4
                    )
                )
                
            try:
                if doGlint:
                    self.data.drawer[self.buttonpressed]["imgAnimState"] = 0
                doGlint = False
                img = assets.GUI.anim.blockGlintStages[math.floor(self.data.drawer[i]["imgAnimState"])]
                self.SidebarGUI_overoverlay.blit(
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
                self.data.drawer[i]["imgAnimState"] += 0.5
            except IndexError: pass

        self.hasUpdated = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if changed else pygame.SYSTEM_CURSOR_ARROW)

        self.GUISurface.blit(self.SidebarGUI_underlay, (self.data.drawerX, 0))
        self.GUISurface.blit(self.SidebarGUI_overlay, (self.data.drawerX, 0))
        self.GUISurface.blit(self.SidebarGUI_overoverlay, (self.data.drawerX, 0))

    def tick(self):
        for event in pygame.event.get():
            if False: raise Exception("Error: False == True")
            elif event.type == pygame.QUIT:
                game.DONE = True
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                GUI.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                GUI.is_mbu = True
            if event.type == pygame.KEYDOWN:
                if False: raise Exception("Error: False == True")
                elif event.key == pygame.K_MINUS:
                    if inp.keyboard.keysPressed[pygame.K_LSHIFT]:
                        self.scale -= 1
                    else:
                        self.data.drawerX_True -= 10
                elif event.key == pygame.K_EQUALS:
                    if inp.keyboard.keysPressed[pygame.K_LSHIFT]:
                        self.scale += 1
                    else:
                        self.data.drawerX_True += 10
                     
        self.data.drawerX += (-(self.data.drawerX - self.data.drawerX_True)) / 8
        self.data.drawerX = round(self.data.drawerX * 1000) / 1000
            
GUI = Gui()

# Game class...
class Game():
    def __init__(self) -> None:
        # Target FPS
        self.TargetFPS = 60
        self.DONE = False
        self.isSetupTick = True
        
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

    game.isSetupTick = False

    pygame.display.flip()
    clock.tick(game.TargetFPS)

pygame.quit()