import sys
import time as t
import random as r
import pygame as pg

music = {

    "home" : "asset\home.mp3",
    "game" : "asset\game.mp3"
}

img_path = {

    "info" : "asset\info.png",
    "title" : "asset\\title.png"
}

color = {

    "light" : (245, 251, 249),
    "ground" : (113, 151, 164),
    "main" : (166, 194, 206),
    "bg" : (202, 220, 234),
    "mark" : (177, 201, 211)
}

class GameController:

    screen = pg.display.set_mode((1000, 800))
    screen_rect = screen.get_rect()
    pg.display.set_caption("Escape with Scale!")
    logo = pg.image.load("asset\\logo.png").convert_alpha()
    pg.display.set_icon(logo)

    pg.init()
    pg.mixer.init()
    pg.mixer.music.set_volume(0.5)
    click = pg.mixer.Sound("asset\click.ogg")
    hit = pg.mixer.Sound("asset\hit.ogg")
    blade = pg.mixer.Sound("asset\Blade.ogg")

    ground_rect = pg.Rect(0, 650, 1000, 600)
    obstacle_rect = ground_rect

    clock = pg.time.Clock()
    fps = 30

    mousePos = (0, 0)
    surrive_time = 0
    record = 0
    speed = 10

    def __init__(self) -> None:

        self.gameMode = Home()
        self.playMusic("home")
        self.bgObj1 = layer1(self.speed)
        self.bgObj2 = layer2(self.speed)
    
    def blitBackground(self):

        gameController.screen.fill(color["bg"])
        pg.draw.rect(gameController.screen,color["ground"], self.ground_rect)
        self.bgObj2.blit()
        self.bgObj1.blit()
    
    def playMusic(self, musicName : str) -> None:

        pg.mixer.music.stop()
        pg.mixer.music.load(music[musicName])
        pg.mixer.music.play(-1)

class Img:

    def __init__(self, path) -> None:

        if path is None:
            self.img = None
            self.rect = None
        else:
            self.img = pg.image.load(path).convert_alpha()
            self.rect = self.img.get_rect()

class Button:

    def __init__(self, txt, x, y, width=100, height=50,
                 button_color=color["light"], frame_color=color["mark"], txt_color=color["ground"]) -> None:
        
        self.frame_rect = pg.Rect(x, y, width, height)
        self.button_rect = pg.Rect(x+5, y+5, width-10, height-10)

        self.frame_color = frame_color
        self.button_color = button_color

        font = pg.font.SysFont(None, 48)        
        self.txt_img = font.render(txt, True, txt_color, button_color)
        self.txt_rect = self.txt_img.get_rect()
        self.txt_rect.center = self.button_rect.center

    def draw(self) -> None:
        
        pg.draw.rect(gameController.screen, self.frame_color, self.frame_rect)
        pg.draw.rect(gameController.screen, self.button_color, self.button_rect)
        gameController.screen.blit(self.txt_img, self.txt_rect)
    
    def isClick(self, pos) -> bool:
        return self.frame_rect.collidepoint(pos)
    
class GameMode:

    def __init__(self) -> None:
        
        self.imgs = []
        self.buttons = {}
    
    def buttonClickDetect(self, pos) -> str:
        
        for key, button in self.buttons.items():
            if button.isClick(pos):
                gameController.click.play()
                return key
        
        return None

    def blit(self) -> None:
        
        for img in self.imgs:
            gameController.screen.blit(img.img, img.rect)
        
        for button in self.buttons.values():
            button.draw()

class Home(GameMode):
        
    def __init__(self) -> None:

        super().__init__()

        self.buttons["start"] = Button("start", 450, 475)
        self.buttons["info"] = Button("info", 450, 575)

        title_img = Img(img_path["title"])
        title_img.img = pg.transform.scale(title_img.img, (800, 450))
        title_img.rect = title_img.img.get_rect()
        title_img.rect.centerx = 500
        title_img.rect.y = 50
        self.imgs.append(title_img)

    def isclick(self, button):

        match button:

            case "start":
                gameController.gameMode = Game()
                gameController.playMusic("game")

            case "info":
                gameController.gameMode = Info()

            case _:
                return

class Info(GameMode):

    def __init__(self) -> None:

        super().__init__()

        self.buttons["close"] = Button("X", 900, 100, 50, 50)

        info_img = Img(img_path["info"])
        info_img.rect.center = gameController.screen_rect.center
        self.imgs.append(info_img)
    
    def isclick(self, button):

        match button:

            case "close":
                gameController.gameMode = Home()

            case _:
                return
    
class GameOver(GameMode):

    def __init__(self) -> None:

        super().__init__()

        gameController.hit.play()        
        gameController.screen.fill(color["light"])

        pg.display.update()
        t.sleep(0.2)

        font = pg.font.SysFont(None, 48)

        surrive_time = Img(None)
        surrive_time.img = font.render(f"Surrive Time : {gameController.surrive_time}", True, color["ground"], color["light"])
        surrive_time.rect = surrive_time.img.get_rect()
        surrive_time.rect.centerx = gameController.screen_rect.centerx
        surrive_time.rect.y = 275

        record = Img(None)
        record.img = font.render(f"Record : {gameController.record}", True, color["ground"], color["light"])
        record.rect = surrive_time.img.get_rect()
        record.rect.centerx = gameController.screen_rect.centerx
        record.rect.y = 375

        self.imgs.append(surrive_time)
        self.imgs.append(record)

        self.buttons["again"] = Button("again", 450, 475)
        self.buttons["back"] = Button("back", 450, 575)
    
    def blit(self) -> None:

        rect = pg.Rect(0, 225, 1000, 225)
        pg.draw.rect(gameController.screen,color["light"], rect)

        return super().blit()

    def isclick(self, button):

        match button:

            case "again":
                gameController.gameMode = Game()
                gameController.playMusic("game")
                gameController.speed = 10

            case "back":
                gameController.gameMode = Home()
                gameController.playMusic("home")
                gameController.speed = 10

            case _:
                return

class Game(GameMode):

    clock_img = pg.image.load("asset\\clock.png").convert_alpha()
    clock_rect = clock_img.get_rect()
    clock_rect.x = 25
    clock_rect.y = 25

    def __init__(self) -> None:

        self.speed = 10
        
        super().__init__()

        self.block = Block()
        self.obstacle = Pipe(self.speed)
        gameController.obstacle_rect = gameController.ground_rect

        self.obstacles = [HorizontalBlade, Blade, Gap, Drop, Clip, Pipe]
        r.shuffle(self.obstacles)

        self.obstacles_counter = 0

        self.startTime = t.time()
    
    def blit(self) -> None:

        if gameController.surrive_time > 3:
            self.obstacle.blit()

        self.block.blit()

        if self.obstacle.outOfScreen():

            self.obstacle = self.obstacles[self.obstacles_counter](self.speed)

            self.obstacles_counter += 1

            if self.obstacles_counter == len(self.obstacles):

                self.obstacles_counter = 0
                r.shuffle(self.obstacles)

        self.time_blit()
    
    def time_blit(self):

        surrive_time = int(t.time()-self.startTime)
        gameController.surrive_time = surrive_time

        if int(t.time()-self.startTime) > gameController.record:
            gameController.record = surrive_time

        font = pg.font.SysFont(None, 48)
        txt_img = font.render(str(surrive_time), True, color["ground"], color["bg"])
        txt_rect = txt_img.get_rect()
        txt_rect.x = 85

        bg_rect = pg.Rect(25, 25, 125, 50)
        frame_rect = pg.Rect(20, 20, 135, 60)
        txt_rect.centery = bg_rect.centery

        pg.draw.rect(gameController.screen, color["mark"], frame_rect)
        pg.draw.rect(gameController.screen, color["bg"], bg_rect)
        gameController.screen.blit(txt_img, txt_rect)
        gameController.screen.blit(self.clock_img, self.clock_rect)

        self.speed = 10 + int(surrive_time/2)
        self.block.dropSpeed = self.speed*3
        gameController.speed = self.speed

class Block:

    rect = pg.Rect(100, 0, 200, 200)
    dropSpeed = 10

    def blit(self) -> None:

        self.rect.width = 200 * 2**min(max(-1+2/800*(sum(gameController.mousePos)-400), -1), 1)
        self.rect.height = 200 * 2**min(max(-(-1+2/800*(sum(gameController.mousePos)-400)), -1), 1)

        if self.rect.x+self.rect.width > gameController.obstacle_rect.x and self.rect.x < gameController.obstacle_rect.x+gameController.obstacle_rect.width:
            self.rect.y = min(self.rect.y+self.dropSpeed, min(gameController.obstacle_rect.y, gameController.ground_rect.y)-self.rect.height)
        else:
            self.rect.y = min(self.rect.y+self.dropSpeed, gameController.ground_rect.y-self.rect.height)
        
        pg.draw.rect(gameController.screen, color["main"], self.rect)

class Obstacle:

    def __init__(self, x, y, w, h, speed) -> None:
        
        self.speed = speed
        self.rect = pg.Rect(x, y, w, h)
    
    def blit(self) -> None:

        self.rect.x -= self.speed
        pg.draw.rect(gameController.screen, color["mark"], self.rect)

        if pg.Rect.colliderect(gameController.gameMode.block.rect, self.rect):
            gameController.gameMode = GameOver()

    def outOfScreen(self) -> bool:

        return self.rect.x + self.rect.width < 0

class Pipe(Obstacle):

    def __init__(self, speed) -> None:

        super().__init__(r.randrange(900, 1100), -500, 100, 500, speed)

        self.max_y = r.randrange(-200, 0)
        
        self.dropSpeed = speed*3
    
    def blit(self) -> None:
        
        self.rect.y = min(self.rect.y+self.dropSpeed, self.max_y)

        super().blit()

class Clip(Obstacle):

    def __init__(self, speed) -> None:

        self.max_gap = r.randrange(100, 300)
        self.max_y = r.randrange(-500, 50-self.max_gap)

        show = max(self.max_y+600, 200-self.max_y-self.max_gap)

        super().__init__(800, -600, show*4, 600, speed)
        self.ground_rect = pg.Rect(800, 800, show*4, 600)
        
        self.dropSpeed = speed / 4
        gameController.obstacle_rect = self.ground_rect

    def blit(self) -> None:

        self.rect.y = min(self.rect.y+self.dropSpeed, self.max_y)

        self.ground_rect.y = max(self.ground_rect.y-self.dropSpeed, self.max_y+600+self.max_gap)

        super().blit()

        self.ground_rect.x = self.rect.x

        pg.draw.rect(gameController.screen, color["mark"], self.ground_rect)

class Drop(Obstacle):

    def __init__(self, speed) -> None:

        self.max_y = r.randrange(400, 600)

        super().__init__(800+self.max_y*3 + 300, 800-self.max_y-600-90, 400, 600, speed)
        self.ground_rect = pg.Rect(800, 800, self.max_y*3, 600)
        
        self.dropSpeed = speed / 3
        gameController.obstacle_rect = self.ground_rect
    
    def blit(self) -> None:

        self.ground_rect.y = max(self.ground_rect.y-self.dropSpeed, 800-self.max_y)

        super().blit()

        self.ground_rect.x = self.rect.x - self.max_y*3 - 300

        pg.draw.rect(gameController.screen, color["mark"], self.ground_rect)

class Gap(Obstacle):

    def __init__(self, speed) -> None:

        self.max_y = r.randrange(200, 400)
        self.gap = r.randrange(150, 390)

        self.F_ground_rect = pg.Rect(800, 800, self.max_y*4, 600)
        self.B_ground_rect = pg.Rect(800 + self.max_y*4 + self.gap, 800, 400, 600)
        super().__init__(800+self.max_y*4+self.gap-1, 1000, 1, 400, speed)
        self.ground_rect = pg.Rect(800 + self.max_y*4, 800, self.gap, 600)
        
        self.dropSpeed = speed / 4
        gameController.obstacle_rect = self.F_ground_rect
    
    def blit(self) -> None:

        self.F_ground_rect.y = max(self.F_ground_rect.y-self.dropSpeed, 800-self.max_y)
        self.F_ground_rect.x -= self.speed
        self.B_ground_rect.x -= self.speed
        self.B_ground_rect.y = self.F_ground_rect.y
        self.rect.x -= self.speed
        self.ground_rect.x -= self.speed
        self.rect.y = self.F_ground_rect.y+40
        self.ground_rect.y = self.F_ground_rect.y+100

        pg.draw.rect(gameController.screen, color["mark"], self.F_ground_rect)
        pg.draw.rect(gameController.screen, color["mark"], self.B_ground_rect)

        if pg.Rect.colliderect(gameController.gameMode.block.rect, self.ground_rect):
            gameController.obstacle_rect = gameController.ground_rect

        elif self.F_ground_rect.x + self.F_ground_rect.width <= 100:
            gameController.obstacle_rect = self.B_ground_rect

        if pg.Rect.colliderect(gameController.gameMode.block.rect, self.rect):
            gameController.gameMode = GameOver()
    
    def outOfScreen(self):

        return self.B_ground_rect.x + self.B_ground_rect.width < 0

class Blade(Obstacle):

    def __init__(self, speed) -> None:

        super().__init__(r.randrange(250, 400), -1000, 100, 650, speed)

        self.sight_rect = self.rect.copy()

        self.isHited = False

        self.isfinish = False
    
    def blit(self) -> None:

        if self.sight_rect.y < 0:
            self.sight_rect.y = min(self.sight_rect.y+10, 0)
            pg.draw.rect(gameController.screen, color["light"], self.sight_rect)
        elif not self.isHited:
            self.rect.y = min(self.rect.y+100, 0)
            if self.rect.y == 0:
                self.isHited = True
                gameController.blade.play()
            pg.draw.rect(gameController.screen, color["light"], self.sight_rect)
        else:
            self.rect.y -= 10
            if self.rect.y < -self.rect.height:
                self.isfinish = True

        pg.draw.rect(gameController.screen, color["mark"], self.rect)

        if pg.Rect.colliderect(gameController.gameMode.block.rect, self.rect):
            gameController.gameMode = GameOver()
        
    def outOfScreen(self) -> bool:
        return self.isfinish

class HorizontalBlade(Obstacle):

    def __init__(self, speed) -> None:

        super().__init__(2000, r.randrange(300, 450), 1000, 100, speed)

        self.sight_rect = self.rect.copy()

        self.isHited = False

        self.isfinish = False
    
    def blit(self) -> None:

        if self.sight_rect.x > 0:
            self.sight_rect.x = max(self.sight_rect.x-20, 0)
            pg.draw.rect(gameController.screen, color["light"], self.sight_rect)
        elif not self.isHited:
            self.rect.x -= 200
            if self.rect.x <= 0:
                self.isHited = True
            pg.draw.rect(gameController.screen, color["light"], self.sight_rect)
        else:
            self.rect.x -= 200
            if self.rect.x < -self.rect.width:
                self.isfinish = True

        pg.draw.rect(gameController.screen, color["mark"], self.rect)

        if pg.Rect.colliderect(gameController.gameMode.block.rect, self.rect):
            gameController.gameMode = GameOver()
        
    def outOfScreen(self) -> bool:
        return self.isfinish

class BGObj:

    def __init__(self, img, speed, mines) -> None:
        
        self.speed = speed / mines
        self.mines = mines
        self.img = img

    def blit(self) -> None:

        self.rect.x -= self.speed
        gameController.screen.blit(self.img, self.rect)

        if self.rect.x + self.rect.width < 0:
            self.speed = gameController.speed / self.mines
            self.rect.x = 1000
            self.img = self.imgs[r.randrange(0, len(self.imgs))]

class layer1(BGObj):

    imgs = [

        pg.transform.scale(pg.image.load("asset\\0.png").convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load("asset\\1_1.png").convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load("asset\\1_2.png").convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load("asset\\1_3.png").convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load("asset\\1_4.png").convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load("asset\\1_5.png").convert_alpha(), (200, 200))
    ]

    def __init__(self, speed) -> None:

        img = self.imgs[r.randrange(0, len(self.imgs))]
        self.rect = pg.Rect(1000, 450, 200, 200)
        super().__init__(img, speed, 2)

class layer2(BGObj):

    imgs = [

        pg.transform.scale(pg.image.load("asset\\0.png").convert_alpha(), (500, 500)),
        pg.transform.scale(pg.image.load("asset\\2_1.png").convert_alpha(), (500, 500)),
        pg.transform.scale(pg.image.load("asset\\2_2.png").convert_alpha(), (500, 500)),
        pg.transform.scale(pg.image.load("asset\\2_3.png").convert_alpha(), (500, 500)),
        pg.transform.scale(pg.image.load("asset\\2_4.png").convert_alpha(), (500, 500)),
    ]

    def __init__(self, speed) -> None:

        img = self.imgs[r.randrange(0, len(self.imgs))]
        self.rect = pg.Rect(1000, 150, 500, 500)
        super().__init__(img, speed, 4)

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
        
        if event.type == pg.MOUSEMOTION:
            gameController.mousePos = event.pos

    gameController.blitBackground()
    gameController.gameMode.blit()
    pg.display.update()
    gameController.clock.tick(gameController.fps)