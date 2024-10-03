import colorsys
from tkinter import filedialog
from wonderwords import RandomWord
import pygame, os, math, copy, tkinter, json

pygame.init()

chopString=lambda s,n:s[:-n]

clock = pygame.time.Clock()

GUI_SCALE = 3

rnWrd = RandomWord()

# Window size, change as you wish
winSize = (1000, 600)
WIN = pygame.display.set_mode(winSize, pygame.RESIZABLE)

def recolor_surface(s, rgb):
    r, g, b = rgb
    h, _, _ = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    colourHue = h
    tintedSurface = pygame.Surface(s.get_size(), pygame.SRCALPHA)

    for x in range(s.get_width()):
        for y in range(s.get_height()):
            current_color = s.get_at((x, y))
            oV = max(current_color.r, current_color.g, current_color.b) / 255.0

            nS = 1.0

            nH = colourHue

            # Convert HSV to RGB
            new_r, new_g, new_b = colorsys.hsv_to_rgb(nH, nS, oV)
            new_alpha = current_color.a

            tintedSurface.set_at((x, y), (int(new_r * 255), int(new_g * 255), int(new_b * 255), new_alpha))

    return tintedSurface

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
                                self.reg = pygame.font.Font('textures/gui/font/Minecraft.otf', size)
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
                self.title = pygame.image.load("textures/gui/title.png")
                self.scroll = pygame.image.load("textures/gui/other/scroll.png")
                class Animation():
                    def __init__(self) -> None:
                        self.blockGlintStages = []

                        _, _, files = next(os.walk("textures/gui/other/anim"))

                        for i in range(len(files)):
                            self.blockGlintStages.append(pygame.image.load("textures/gui/other/anim/animStage" + str(i + 1) + ".png"))

                self.anim = Animation()
        self.GUI = Gui()
        class Blocks:
            def __init__(self, directory="textures/") -> None:
                # Ensure the directory exists
                if not os.path.isdir(directory):
                    raise ValueError(f"The directory {directory} does not exist.")

                self.images = {}
                
                # Load all PNG images from the directory
                for filename in os.listdir(directory):
                    if filename.endswith('.png'):
                        # Remove the .png extension and replace spaces with underscores
                        image_name = os.path.splitext(filename)[0].replace(' ', '_')
                        image_path = os.path.join(directory, filename)
                        self.images[image_name] = pygame.image.load(image_path)
                
                # Create attributes dynamically
                for name, image in self.images.items():
                    setattr(self, name, image)

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
                self.pressed = pygame.key.get_pressed()
        self.KEYBOARD = Keyboard()

        class Mouse():
            def __init__(self) -> None:
                self.pos = pygame.mouse.get_pos()
                self.pos = pygame.mouse.get_pos()
                self.pressed = pygame.mouse.get_pressed()
                self.up = [False, False, False]
                self.down = [False, False, False]
        self.MOUSE = Mouse()

    def update(self, event):
        self.MOUSE.pos = pygame.mouse.get_pos()
        self.MOUSE.pressed = pygame.mouse.get_pressed()
        self.MOUSE.down = [False, False, False]
        self.MOUSE.up = [False, False, False]
        self.KEYBOARD.pressed = pygame.key.get_pressed()
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.MOUSE.down[event.button - 1] = True
        except IndexError: pass
        try:
            if event.type == pygame.MOUSEBUTTONUP:
                self.MOUSE.up[event.button - 1] = True
        except IndexError: pass

inp = Input()

# GUI class...
class Gui():
    def getImgDrawerFromStr(self, state):
        if False: raise Exception("Error: False == True")
        elif state == "default": return assets.GUI.drawer.default
        elif state == "hover": return assets.GUI.drawer.hover
        elif state == "clicking": return assets.GUI.drawer.pushing
        elif state == "pushed": return assets.GUI.drawer.push
        else: raise TypeError("state is invalid.")
    
    def __init__(self) -> None:
        self.hasUpdated = True
        self.buttonpressed = 0#-1
        self.scale = GUI_SCALE

        self.isScrollingScrollbar = False
        self.scrollingScrollBarY_Difference = 0
        class Data():
            def __init__(self) -> None:
                self.isStartupTick = True
                        
                self.drawerX_True = 0
                self.drawerX = self.drawerX_True
                
                self.drawerY_True = 0
                self.drawerY = self.drawerY_True
                
                self.drawerX += (self.drawerX - self.drawerX_True) / 2
                self.drawerIsOpen = False
                self.rainbowColourOoooOOOOooooOOOO = 0

                with open('GUI Layout.json', 'r') as file:
                    self.gui = json.load(file)
                
                self.drawer = self.gui["sidebar"]


        self.data = Data()
        
        self.realWinSize = (WIN.get_width(), len(self.data.drawer) * self.scale * self.getImgDrawerFromStr("default").get_height())
        
        self.SidebarGUI_underlay = pygame.Surface(self.realWinSize, pygame.SRCALPHA, 32).convert_alpha()
        self.SidebarGUI_overlay = pygame.Surface(self.realWinSize, pygame.SRCALPHA, 32).convert_alpha()
        self.SidebarGUI_overoverlay = pygame.Surface(self.realWinSize, pygame.SRCALPHA, 32).convert_alpha()
        self.SidebarGUI_scrolloverlay = pygame.Surface(self.realWinSize, pygame.SRCALPHA, 32).convert_alpha()
        
        self.SidebarGUI_underlay.fill((1, 2, 3))
        self.SidebarGUI_overlay.fill((1, 2, 3))
        self.SidebarGUI_overoverlay.fill((1, 2, 3))
        self.SidebarGUI_scrolloverlay.fill((1, 2, 3))
        
        self.SidebarGUI_underlay.set_colorkey((1, 2, 3))
        self.SidebarGUI_overlay.set_colorkey((1, 2, 3))
        self.SidebarGUI_overoverlay.set_colorkey((1, 2, 3))
        self.SidebarGUI_scrolloverlay.set_colorkey((1, 2, 3))
        
        self.GUISurface = pygame.Surface(self.realWinSize)

        self.getY = lambda curScr, elementHeight, scrHeight, scrollbarHeight: -((max(0, min(curScr, elementHeight - scrHeight)) / (elementHeight - scrHeight)) * (scrollbarHeight - scrHeight))
        self.setY = lambda scrollbarY, elementHeight, scrHeight, scrollbarHeight: max(0, min(-scrollbarY / (scrollbarHeight - scrHeight) * (elementHeight - scrHeight), elementHeight - scrHeight))

    def update(self):
        self.hasUpdated = True
        self.data.isStartupTick = True
        self.redrawGUI()

    def redrawGUI(self):

        #self.SidebarGUI_underlay.fill((1, 2, 3))
        self.SidebarGUI_overoverlay.fill((1, 2, 3))
        self.SidebarGUI_scrolloverlay.fill((1, 2, 3))
        
        if self.data.isStartupTick:
            self.SidebarGUI_overlay.fill((1, 2, 3))

        self.GUISurface = pygame.Surface(self.realWinSize)
        
        global GUI_SCALE
        if self.scale != GUI_SCALE:
            GUI_SCALE = self.scale
        changed = False
        doGlint = False
        defState = self.getImgDrawerFromStr("default")
        mp = pygame.mouse.get_pressed()[0]

        if self.data.isStartupTick:
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
            if self.data.drawerIsOpen:
                coll = pygame.Rect(
                    0,
                    i * defState.get_height() * self.scale,
                    defState.get_width() * self.scale - self.scale * 9,
                    defState.get_height() * self.scale).collidepoint((inp.MOUSE.pos[0], inp.MOUSE.pos[1] - self.data.drawerY * self.scale))
            else: coll = False
            if coll:
                changed = True
            if mp and coll:
                img = self.getImgDrawerFromStr("clicking")
                self.data.drawer[i]["state"] = "clicking"
            elif coll and self.buttonpressed != i:
                img = self.getImgDrawerFromStr("hover")
                self.data.drawer[i]["state"] = "hover"
            else:
                img = self.getImgDrawerFromStr(["default", "pushed"][self.buttonpressed == i])
                self.data.drawer[i]["state"] = ["default", "pushed"][self.buttonpressed == i]
            if coll and self.buttonpressed == i: changed = False
            if inp.MOUSE.up[0] and coll:
                #if self.buttonpressed == i:
                #    self.buttonpressed = -1
                #else:
                doGlint = True
                self.buttonpressed = i
                inp.MOUSE.up[0] = False
                
            if self.data.isStartupTick or self.data.drawer[i]["prevState"] != self.data.drawer[i]["state"]:
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
            
            self.data.drawer[i]["prevState"] = self.data.drawer[i]["state"]

            if self.data.isStartupTick:
                        
                # 88 88 90 is scroll bar thingy colour RGB
                
                if self.data.drawer[i]["imgBG"] != "":
                    img = eval(self.data.drawer[i]["imgBG"])
                    self.SidebarGUI_overlay.blit(
                        pygame.transform.scale(
                            recolourImage(img, (0, 0, 0)),
                            (
                                img.get_width() * self.scale,
                                img.get_height() * self.scale
                            )
                        ),
                        (
                            self.scale * 3 + self.scale,
                            (i * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2) + self.scale
                        )
                    )
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
                    
                img = eval(self.data.drawer[i]["img"])
                self.SidebarGUI_overlay.blit(
                    pygame.transform.scale(
                        recolourImage(img, (0, 0, 0)),
                        (
                            img.get_width() * self.scale,
                            img.get_height() * self.scale
                        )
                    ),
                    (
                        self.scale * 3 + self.scale,
                        (i * defState.get_height() * self.scale) + (defState.get_height() * self.scale / 2 - img.get_height() * self.scale / 2) + self.scale
                    )
                )
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
                
                img = eval(self.data.drawer[i]["font"]).render(self.data.drawer[i]["text"], False, (255, 255, 255))

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

            pygame.draw.rect(self.SidebarGUI_overoverlay, (30, 30, 31), pygame.Rect(self.data.drawerX - self.scale, 0, self.scale, self.realWinSize[1]))
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

        if len(self.data.drawer) * self.scale * self.getImgDrawerFromStr("default").get_height() > WIN.get_height(): # Checks if it needs to scroll or not
            pygame.draw.rect(self.SidebarGUI_scrolloverlay, (88, 88, 90), pygame.Rect(
                    defState.get_width() * self.scale - self.scale * 6,
                    0,
                    self.scale * 2,
                    WIN.get_height()
                )
            )
            
            img = assets.GUI.scroll
            img = pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale,
                    img.get_height() * self.scale
                )
            )
            scrollBarSze = pygame.Rect(
                defState.get_width() * self.scale - self.scale * 8,
                self.getY(-self.data.drawerY * self.scale, self.realWinSize[1], WIN.get_height(), img.get_height() - self.scale * 2),
                img.get_width(),
                img.get_height() - self.scale * 2
            )
            
            if scrollBarSze.collidepoint(inp.MOUSE.pos) and inp.MOUSE.pressed[0] and not self.isScrollingScrollbar:
                self.isScrollingScrollbar = True
                self.scrollingScrollBarY_Difference = scrollBarSze.y - inp.MOUSE.pos[1]
                print(self.scrollingScrollBarY_Difference)
            
            if not inp.MOUSE.pressed[0]:
                self.isScrollingScrollbar = False
            
            if self.isScrollingScrollbar:
                changed = True
                scrollBarSze.y = inp.MOUSE.pos[1] + self.scrollingScrollBarY_Difference
                self.data.drawerY_True = -self.setY(scrollBarSze[1], self.realWinSize[1], WIN.get_height(), img.get_height() - self.scale * 2) / self.scale


            self.SidebarGUI_scrolloverlay.blit(
                img,
                (
                    scrollBarSze[0],
                    scrollBarSze[1],
                )
            )

        self.data.isStartupTick = False
        self.hasUpdated = False

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if changed or scrollBarSze.collidepoint(inp.MOUSE.pos) else pygame.SYSTEM_CURSOR_ARROW)
        
        self.GUISurface.blit(self.SidebarGUI_underlay, (0, GUI.data.drawerY * GUI.scale), (0, 0, self.data.drawerX, self.realWinSize[1]))
        self.GUISurface.blit(self.SidebarGUI_overlay, (0, GUI.data.drawerY * GUI.scale), (0, 0, self.data.drawerX, self.realWinSize[1]))
        self.GUISurface.blit(self.SidebarGUI_overoverlay, (0, GUI.data.drawerY * GUI.scale), (0, 0, self.data.drawerX, self.realWinSize[1]))
        self.GUISurface.blit(self.SidebarGUI_scrolloverlay, (0, 0), (0, 0, self.data.drawerX, self.realWinSize[1]))

    def tick(self):
        for event in pygame.event.get():
            inp.update(event)
            if False:
                print(f"Event ID: {event.type}, Event Name: {pygame.event.event_name(event.type)}")
                try: print(f"Event key: {event.key}")
                except: pass
                try: print(f"Event button: {event.button}")
                except: pass
                try: print(f"Event X: {event.x}")
                except: pass
                try: print(f"Event Y: {event.y}")
                except: pass
                print("-" * len(f"Event ID: {event.type}, Event Name: {pygame.event.event_name(event.type)}"))
            if False: raise Exception("Error: False == True")
            elif event.type == pygame.WINDOWLEAVE and not self.isScrollingScrollbar:
                self.data.drawerIsOpen = False
            elif event.type == pygame.QUIT:
                game.DONE = True
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION and inp.MOUSE.pos[0] < self.data.drawerX:
                self.data.drawerIsOpen = True
            elif event.type == pygame.MOUSEWHEEL and self.data.drawerIsOpen:
                self.data.drawerY_True += event.y * 10
            if event.type == pygame.KEYDOWN:
                if False: raise Exception("Error: False == True")
                elif event.key == pygame.K_MINUS:
                    self.scale -= 1
                    self.data.drawerX = self.data.drawerX_True
                    self.data.drawerY = self.data.drawerY_True
                    self.realWinSize = (WIN.get_width(), len(self.data.drawer) * self.scale * self.getImgDrawerFromStr("default").get_height())
                    GUI.update()
                elif event.key == pygame.K_EQUALS:
                    self.scale += 1
                    self.data.drawerX = self.data.drawerX_True
                    self.data.drawerY = self.data.drawerY_True
                    self.realWinSize = (WIN.get_width(), len(self.data.drawer) * self.scale * self.getImgDrawerFromStr("default").get_height())
                    GUI.update()
                elif event.key == pygame.K_ESCAPE:
                    GUI.update()

        if inp.MOUSE.pos[0] > self.data.drawerX and not self.isScrollingScrollbar:
            self.data.drawerIsOpen = False

        if self.data.drawerIsOpen:
            self.data.drawerX_True = assets.GUI.drawer.default.get_width() * self.scale
        else:
            self.data.drawerX_True = self.scale * 23
        if self.data.drawerY_True > 0: self.data.drawerY_True = 0
        if self.data.drawerY_True * self.scale < -(self.realWinSize[1] - WIN.get_height()): self.data.drawerY_True = -(self.realWinSize[1] - WIN.get_height()) / self.scale

        self.data.drawerX += (-(self.data.drawerX - self.data.drawerX_True)) / 4
        
        if len(self.data.drawer) * self.scale * self.getImgDrawerFromStr("default").get_height() > WIN.get_height():
            self.data.drawerY += (-(self.data.drawerY - self.data.drawerY_True)) / 4
        else:
            self.data.drawerY_True = 0
            self.data.drawerY = self.data.drawerY_True

        if pygame.key.get_pressed()[pygame.K_EQUALS] or pygame.key.get_pressed()[pygame.K_PLUS]:
            self.data.drawerX = self.data.drawerX_True
            self.data.drawerY = self.data.drawerY_True
        
        if self.scale <= 0:
            self.scale = 1

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

    game.tick()
    GUI.tick()

    GUI.redrawGUI()
    WIN.blit(GUI.GUISurface, (0, 0))

    game.isSetupTick = False

    pygame.display.flip()
    clock.tick(game.TargetFPS)

pygame.quit()