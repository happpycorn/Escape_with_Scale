import sys
import pygame as pg
from random import sample

pg.init()
pg.mixer.init()
pg.mixer.music.set_volume(0.5)

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

music = {

    "home" : "asset\home.mp3",
    "game" : "asset\game.mp3"
}

img_path = {

    "info" : "asset\info.png",
    "dig" : "asset\dig.png",
    "walk" : "asset\walk.png"
}

color = {

    "gress" : (150, 216, 70),
    "fl-l" : (152, 217, 142),
    "fl-d" : (104, 190, 141),
    "ground" : (67, 52, 27)
}

def playMusic(musicName : str) -> None:

    pg.mixer.music.stop()
    pg.mixer.music.load(music[musicName])
    pg.mixer.music.play(-1)

class GameController:

    screen = pg.display.set_mode((1000, 800))
    screen_rect = screen.get_rect()
    pg.display.set_caption("Save Watermelon!")

    farmland_side = 6
    watermelon_count = 10

    def __init__(self) -> None:

        self.gameMode = Home()
        playMusic("home")

        self.farmland = [[Block(x, y) for x in range(self.farmland_side)] for y in range(self.farmland_side)]
        self.frame_rect = pg.Rect(175, 75, 650, 650)
    
    def blitBackground(self):

        gameController.screen.fill(color["gress"])
        pg.draw.rect(gameController.screen, color["ground"], self.frame_rect)

        for i in self.farmland:
            for j in i:
                j.draw()

class Img:

    def __init__(self, path) -> None:
        self.img = pg.image.load(path).convert_alpha()
        self.rect = self.img.get_rect()

class Button:

    def __init__(self, txt, x, y, width=100, height=50,
                 button_color=color["fl-l"], frame_color=color["fl-d"], txt_color=color["ground"]) -> None:
        
        self.frame_rect = pg.Rect(x, y, width, height)
        self.button_rect = pg.Rect(x+5, y+5, width-10, height-10)

        self.frame_color = frame_color
        self.button_color = button_color

        font = pg.font.SysFont(None, 48)        
        self.txt_img = font.render(txt, True, txt_color, button_color)
        self.txt_rect = self.txt_img.get_rect()
        self.txt_rect.center = self.button_rect.center
    
    def setRect(self, x, y, width, height):

        self.frame_rect = pg.Rect(x, y, width, height)
        self.button_rect = pg.Rect(x+5, y+5, width-10, height-10)
        self.txt_rect = self.frame_rect

    def draw(self) -> None:
        
        pg.draw.rect(gameController.screen, self.frame_color, self.frame_rect)
        pg.draw.rect(gameController.screen, self.button_color, self.button_rect)
        gameController.screen.blit(self.txt_img, self.txt_rect)
    
    def isClick(self, pos) -> bool:
        return self.frame_rect.collidepoint(pos)

class Block:

    side_pixel = 100

    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

        self.rect = pg.Rect(200+x*100, 100+y*100, self.side_pixel, self.side_pixel)

        self.orgcolor = color["fl-l"] if (x+(y%2))%2 == 0 else color["fl-d"]
        self.opencolor = color["ground"]

        self.watermelon = 0
        self.isopen = False

    def init(self):

        self.isopen = False

    def draw(self) -> None:

        pg.draw.rect(gameController.screen, self.opencolor if self.isopen else self.orgcolor, self.rect)
    
    def isClick(self, pos) -> bool:
        return self.frame_rect.collidepoint(pos)

class GameMode:
    
    def buttonClickDetect(self, pos) -> str:
        
        for key, button in self.buttons.items():
            if button.isClick(pos):
                return key
        
        return None

    def blit(self) -> None:
        
        for img in self.imgs:
            gameController.screen.blit(img.img, img.rect)
        
        for button in self.buttons.values():
            button.draw()

class Home(GameMode):

    imgs = []

    buttons = {

        "start" : Button("start", 450, 475),
        "info" : Button("info", 450, 575)
    }

    def isclick(self, button):

        match button:

            case "start":
                gameController.gameMode = Game()
                playMusic("game")

            case "info":
                gameController.gameMode = Info()

            case _:
                return

class Info(GameMode):

    imgs = []

    buttons = {

        "close" : Button("X", 900, 100, 50, 50)
    }

    def __init__(self) -> None:

        self.info_img = Img(img_path["info"])
        self.info_img.rect.center = gameController.screen_rect.center
        self.imgs.append(self.info_img)
    
    def isclick(self, button):

        match button:

            case "close":
                gameController.gameMode = Home()

            case _:
                return

class Game(GameMode):

    imgs = []

    buttons = {

        "dig" : Button("", 800, 700, 50, 50, frame_color=color["ground"]),
        "walk" : Button("", 850, 650, 100, 100, frame_color=color["ground"])
    }

    def __init__(self) -> None:

        self.dig_img = [pg.image.load(img_path["dig"]).convert_alpha()]
        self.dig_img.append(pg.transform.scale(self.dig_img[0], (50, 50)))
        self.walk_img = [pg.image.load(img_path["walk"]).convert_alpha()]
        self.walk_img.append(pg.transform.scale(self.walk_img[0], (50, 50)))

        self.buttons["dig"].txt_img = self.dig_img[1]
        self.buttons["walk"].txt_img = self.walk_img[0]
        self.buttons["dig"].txt_rect = self.buttons["dig"].frame_rect
        self.buttons["walk"].txt_rect = self.buttons["walk"].frame_rect

        watermelon_position = sample(range(gameController.farmland_side**2), gameController.watermelon_count)

        for i in watermelon_position:
            gameController.farmland[i//gameController.farmland_side][i%gameController.farmland_side].watermelon = 1

        self.famer = Farmer()
        
        self.startAnime()
    
    def buttonClickDetect(self, pos):
        
        if self.buttons["dig"].isClick(pos):

            self.buttons["dig"].setRect(800, 650, 100, 100)
            self.buttons["walk"].setRect(900, 700, 50, 50)
            self.buttons["dig"].txt_img = self.dig_img[0]
            self.buttons["walk"].txt_img = self.walk_img[1]
            self.famer.isdig = True
        
        if self.buttons["walk"].isClick(pos):
            
            self.buttons["dig"].setRect(800, 700, 50, 50)
            self.buttons["walk"].setRect(850, 650, 100, 100)
            self.buttons["dig"].txt_img = self.dig_img[1]
            self.buttons["walk"].txt_img = self.walk_img[0]
            self.famer.isdig = False
        
        for x, y in self.famer.canMoveBlock():

            if not gameController.farmland[x][y].isClick(pos):
                continue
            
            if self.isdig:
                gameController.farmland[x][y].isopen = True

            else:
                pass
        
        return None
    
    def startAnime(self) -> None:
        pass

class GameOver(GameMode):

    imgs = []

    buttons = {

        "again" : Button("again", 450, 475),
        "back" : Button("back", 450, 575)
    }

    def isclick(self, button):

        match button:

            case "again":
                gameController.gameMode = Game()
                playMusic("game")

            case "back":
                gameController.gameMode = Home()
                playMusic("home")

            case _:
                return

class Farmer:

    x = 6
    y = 3

    isdig = False

    def __init__(self) -> None:
        pass

    def canMoveBlock(self) -> list:

        return [[self.x+dr, self.y+dc] for dr, dc in DIRECTIONS if 0<=self.x+dr<7 and 0<=self.y+dc<6]

gameController = GameController()

while 1:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            button = gameController.gameMode.buttonClickDetect(event.pos)
            if button is None:
                continue
            gameController.gameMode.isclick(button)

    gameController.blitBackground()
    gameController.gameMode.blit()
    pg.display.update()