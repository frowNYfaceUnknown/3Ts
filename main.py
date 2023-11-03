## Tic Tac T(w)o(e)
## Game:
##     Designed by: Oats Jenkins (YouTube https://www.youtube.com/@OatsJenkins)
##     Programmed by (including pixel art): Aarya Parekh (itch.io https://sickandsleazy.itch.io)
## Pygame version: Pygame-CE 2.2.1 (SDL 2.26.4, Python 3.11.3)
## Font courtesy: Pixel Overload: Baskic8 (itch.io https://pixeloverload.itch.io)

import pygame, data.fonts as fonts, math
from pygame.locals import *; from sys import exit
from data.scene import *; from data.sprites import *
import data.tictactoe as tictactoe, data.tictactwo as tictactwo

## Initialising pygame and fonts
pygame.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
GAMEFONT = fonts.getFont(size = 64)
TITLEFONT = fonts.getFont(size = 128)
INSTFONT = fonts.getFont(size = 32)

pygame.mouse.set_visible(False)
cursor_imgs = [pygame.image.load(f"Assets/cursor_{i}.png") for i in range(2)]
cursor = Cursor(cursor_imgs, 2)
cg = pygame.sprite.Group()
cg.add(cursor)

class TitleScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        
        ## Setting up fonts, colors and loading images
        global GAMEFONT, TITLEFONT, INSTFONT
        self.BG_COLOR, self.TEXT_COLOR, self.INST_COLOR, self.S_COLOR = (0, 0, 0), (74, 122, 150), (200, 200, 200), (51, 63, 88)
        self.GAMEFONT, self.TITLEFONT, self.INSTFONT = GAMEFONT, TITLEFONT, INSTFONT
        self.TITLE_POS = (100, 100)

        ## Connecting to the main display and declaring necessary variables
        self.screen = screen
        self.menu_choice = 0 ## 0: tic tac toe; 1: tic tac two; 2: rules; 3: exit.
        
        ## animation offsets and variables
        self.x_offset, self.y_offset, self.multiplier = self.TITLE_POS[0], self.TITLE_POS[1] + self.TITLEFONT.get_height() + 100, 45
        self.anim_timer, self.anim_delay = pygame.time.get_ticks(), 100
        self.frame = 0

    def handle_events(self, events: list) -> None:
        
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_UP and self.menu_choice != 0:
                    self.menu_choice -= 1
                if event.key == K_DOWN and self.menu_choice != 3:
                    self.menu_choice += 1
                if event.key == K_SPACE:
                    if self.menu_choice == 0:
                        self.manager.go_to(TictactoeScene(self.screen))
                    elif self.menu_choice == 1:
                        self.manager.go_to(TictactwoScene(self.screen))
                    elif self.menu_choice == 2:
                        self.manager.go_to(RulesScene(self.screen))
                    elif self.menu_choice == 3:
                        pygame.quit()
                        exit()

    def update(self) -> None:
        if self.menu_choice == 0:
            self.bgTextColor1 = self.S_COLOR
            self.bgTextColor2 = self.BG_COLOR
            self.bgTextColor3 = self.BG_COLOR
            self.bgTextColor4 = self.BG_COLOR
        elif self.menu_choice == 1:
            self.bgTextColor1 = self.BG_COLOR
            self.bgTextColor2 = self.S_COLOR
            self.bgTextColor3 = self.BG_COLOR
            self.bgTextColor4 = self.BG_COLOR
        if self.menu_choice == 2:
            self.bgTextColor1 = self.BG_COLOR
            self.bgTextColor2 = self.BG_COLOR
            self.bgTextColor3 = self.S_COLOR
            self.bgTextColor4 = self.BG_COLOR
        if self.menu_choice == 3:
            self.bgTextColor1 = self.BG_COLOR
            self.bgTextColor2 = self.BG_COLOR
            self.bgTextColor3 = self.BG_COLOR
            self.bgTextColor4 = self.S_COLOR
    
    def draw(self) -> None:

        ## Rendering the background and resetting the y_offset
        self.screen.fill(self.BG_COLOR)
        self.y_offset = self.TITLE_POS[1] + self.TITLEFONT.get_height() + 100

        ## Rendering all the images/fonts
        title = self.TITLEFONT.render("tic - tac - t(w)o(e)", False, self.TEXT_COLOR)
        self.screen.blit(title, self.TITLE_POS)

        self.ttt1 = self.GAMEFONT.render("tic-tac-toe", False, self.TEXT_COLOR, self.bgTextColor1)
        self.screen.blit(self.ttt1, (self.x_offset, self.y_offset))
        self.y_offset += self.ttt1.get_height() + 50
        
        self.ttt2 = self.GAMEFONT.render("tic-tac-two", False, self.TEXT_COLOR, self.bgTextColor2)
        self.screen.blit(self.ttt2, (self.x_offset, self.y_offset))
        self.y_offset += self.ttt2.get_height() + 50

        self.rules = self.GAMEFONT.render("rules", False, self.TEXT_COLOR, self.bgTextColor3)
        self.screen.blit(self.rules, (self.x_offset, self.y_offset))
        self.y_offset += self.rules.get_height() + 50

        self.gquit = self.GAMEFONT.render("quit", False, self.TEXT_COLOR, self.bgTextColor4)
        self.screen.blit(self.gquit, (self.x_offset, self.y_offset))

        inst = self.INSTFONT.render("Press space to select", False, self.INST_COLOR)
        self.animate_instruction(inst)
        self.screen.blit(inst, (WIDTH/2 - inst.get_width()/2, HEIGHT - 75))

    def animate_instruction(self, instance: pygame.Surface) -> pygame.Surface:
        curr_time = pygame.time.get_ticks()
        alpha_val = (math.sin(curr_time % 60000) + 1) * 255/2
        instance.set_alpha(alpha_val)

class TictactoeScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        
        ## Initializing the game board containing all the logic
        self.ttt_gb = tictactoe.GameBoard()

        ## Variables related to rendering
        self.BG_COLOR = (41, 40, 49)
        self.tileGroup = pygame.sprite.Group()
        self.quit_UI = pygame.sprite.Group()
        self.retry_UI = pygame.sprite.Group()
        self.scale = 10
        self.screen = screen

        ## Loading images
        self.BG = pygame.image.load("Assets/tictactoeBoard.png").convert()
        self.BG = pygame.transform.scale(self.BG, (self.BG.get_width() * self.scale, self.BG.get_height() * self.scale))
        
        self.cross_imgs = [pygame.image.load(f"Assets/cross_{i}.png") for i in range(4)]
        self.circle_imgs = [pygame.image.load(f"Assets/circle_{i}.png") for i in range(4)]

        self.popUp_imgs = [pygame.image.load(f"Assets/popUp_{i}.png") for i in range(8)]
        self.quit_imgs = [pygame.image.load(f"Assets/quit_{i}.png") for i in range(2)]
        self.retry_imgs = [pygame.image.load(f"Assets/retry_{i}.png") for i in range(2)]
        
        self.quitPos = (WIDTH/4 - self.BG.get_width()/4 - (self.quit_imgs[1].get_width()/2 * self.scale), HEIGHT/2 - (self.quit_imgs[0].get_height()/2 * self.scale))
        self.retryPos = (3*WIDTH/4 + self.BG.get_width()/4 - (self.quit_imgs[1].get_width()/2 * self.scale), HEIGHT/2 - (self.quit_imgs[0].get_height()/2 * self.scale))
        self.quit = Button(self.quit_imgs, self.quitPos[0], self.quitPos[1], self.scale)
        self.retry = Button(self.retry_imgs, self.retryPos[0], self.retryPos[1], self.scale)

        self.quit_UI.add(self.quit)
        self.retry_UI.add(self.retry)

        self.TEXT_COLOR = (255, 255, 255)
        self.GAMEFONT = fonts.getFont(size = 64)
        self.popUp = 0 ## Just to initialize the variable

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONUP and not self.tileGroup.has(self.popUp):
                pos = event.pos
                self.calcMove(pos)
            elif event.type == MOUSEBUTTONDOWN:
                pos = event.pos
                self.calcUIinteraction(pos, 0)
            if event.type == MOUSEBUTTONUP:
                pos = event.pos
                self.calcUIinteraction(pos, 1)

    def update(self) -> None:
        self.tileGroup.update()
        self.quit_UI.update()
        self.retry_UI.update()

        ## updating the pop-up if the game is over
        if self.ttt_gb.gameOver:
            self.WINNER_TEXT_1 = self.GAMEFONT.render("The winner is", False, self.TEXT_COLOR)
            self.WINNER_TEXT_2 = self.GAMEFONT.render(f"player {self.winner + 1}", False, self.TEXT_COLOR)

    def draw(self) -> None:
        
        ## Filling the background with the board and background color
        self.screen.fill(self.BG_COLOR)
        self.screen.blit(self.BG, (WIDTH/2 - self.BG.get_width()/2, HEIGHT/2 - self.BG.get_height()/2))

        ## Drawing all the sprites on scene
        self.tileGroup.draw(self.screen)
        self.quit_UI.draw(self.screen)
        self.retry_UI.draw(self.screen)

        ## drawing a pop-up if the game is over
        if self.ttt_gb.gameOver and not self.popUp.is_animating:
            self.screen.blit(self.WINNER_TEXT_1, (WIDTH/2 - self.WINNER_TEXT_1.get_width()/2, HEIGHT/2 - self.WINNER_TEXT_1.get_height()/2 - 50))
            self.screen.blit(self.WINNER_TEXT_2, (WIDTH/2 - self.WINNER_TEXT_2.get_width()/2, HEIGHT/2 - self.WINNER_TEXT_2.get_height()/2 + 50))

    def screenPosToWorldPos(self, x: float, y: float) -> tuple:
        
        ## Mapping screen position to world tiles:
            ## Row 1
                ## Col 1
        if WIDTH/2 - self.BG.get_width()/2 < x < WIDTH/2 - self.BG.get_width()/6 and HEIGHT/2 - self.BG.get_height()/2 < y < HEIGHT/2 - self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/2 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/2 + (3 * self.scale))
            return (0, 0)
        
                ## Col 2
        if WIDTH/2 - self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/6 and HEIGHT/2 - self.BG.get_height()/2 < y < HEIGHT/2 - self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/2 + (3 * self.scale))
            return (0, 1)
        
                ## Col 3
        if WIDTH/2 + self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/2 and HEIGHT/2 - self.BG.get_height()/2 < y < HEIGHT/2 - self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 + self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/2 + (3 * self.scale))
            return (0, 2)
        
            ## Row 2
                ## Col 1
        if WIDTH/2 - self.BG.get_width()/2 < x < WIDTH/2 - self.BG.get_width()/6 and HEIGHT/2 - self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/2 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/6 + (3 * self.scale))
            return (1, 0)
        
                ## Col 2
        if WIDTH/2 - self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/6 and HEIGHT/2 - self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/6 + (3 * self.scale))
            return (1, 1)
        
                ## Col 3
        if WIDTH/2 + self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/2 and HEIGHT/2 - self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/6:
            self.worldPos = (WIDTH/2 + self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 - self.BG.get_height()/6 + (3 * self.scale))
            return (1, 2)
        
            ## Row 3
                ## Col 1
        if WIDTH/2 - self.BG.get_width()/2 < x < WIDTH/2 - self.BG.get_width()/6 and HEIGHT/2 + self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/2:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/2 + (3 * self.scale), HEIGHT/2 + self.BG.get_height()/6 + (3 * self.scale))
            return (2, 0)
        
                ## Col 2
        if WIDTH/2 - self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/6 and HEIGHT/2 + self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/2:
            self.worldPos = (WIDTH/2 - self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 + self.BG.get_height()/6 + (3 * self.scale))
            return (2, 1)
        
                ## Col 3
        if WIDTH/2 + self.BG.get_width()/6 < x < WIDTH/2 + self.BG.get_width()/2 and HEIGHT/2 + self.BG.get_height()/6 < y < HEIGHT/2 + self.BG.get_height()/2:
            self.worldPos = (WIDTH/2 + self.BG.get_width()/6 + (3 * self.scale), HEIGHT/2 + self.BG.get_height()/6 + (3 * self.scale))
            return (2, 2)
        
        return (-1, -1)

    def calcUIinteraction(self, pos, key): ## key represents whether the function is called during
                                           ## a MOUSEBUTTONDOWN (0) or a MOUSEBUTTONUP (1) event.
        quitCondition = self.quitPos[0] < pos[0] < (self.quitPos[0] + self.quit_imgs[0].get_width() * self.scale) and self.quitPos[1] < pos[1] < (self.quitPos[1] + self.quit_imgs[0].get_height() * self.scale)
        retryCondition = self.retryPos[0] < pos[0] < (self.retryPos[0] + self.retry_imgs[0].get_width() * self.scale) and self.retryPos[1] < pos[1] < (self.retryPos[1] + self.retry_imgs[0].get_height() * self.scale)
        
        if (quitCondition and not key):
            self.quit.is_animating = True
        elif (retryCondition and not key):
            self.retry.is_animating = True

        if (quitCondition and key):
            self.manager.go_to(TitleScene(self.screen))
        elif (retryCondition and key):
            self.reset()

    def calcMove(self, pos: tuple) -> None:
        if not self.ttt_gb.gameOver:
            indices = self.screenPosToWorldPos(pos[0], pos[1])
            if indices == (-1, -1):
                return
            val = self.ttt_gb.moveTo(indices[0], indices[1])
            if val == -1:
                return
            if val == 0:
                circle = TilePiece(self.circle_imgs, self.worldPos[0], self.worldPos[1], self.scale)
                self.tileGroup.add(circle)
            else:
                cross = TilePiece(self.cross_imgs, self.worldPos[0], self.worldPos[1], self.scale)
                self.tileGroup.add(cross)
            self.winner = self.ttt_gb.checkWin()

        if self.ttt_gb.gameOver:
            self.popUp = PopUp(self.popUp_imgs, WIDTH/2 - self.popUp_imgs[7].get_width()/2 * self.scale, HEIGHT/2 - self.popUp_imgs[0].get_height()/2 * self.scale, self.scale)
            self.tileGroup.add(self.popUp)

    def reset(self):
        self.ttt_gb.resetGB()
        self.__init__(self.screen)

class TictactwoScene(TictactoeScene):

    def __init__(self, screen: pygame.Surface) -> None:
        
        ## Initializing the game board containing all the logic
        self.ttt_gb = tictactwo.GameBoard()

        ## Variables related to rendering
        self.BG_COLOR = (41, 40, 49)
        self.tileGroup = pygame.sprite.Group()
        self.quit_UI = pygame.sprite.Group()
        self.retry_UI = pygame.sprite.Group()
        self.scale = 10
        self.screen = screen

        ## Loading images
        self.BG = pygame.image.load("Assets/tictactwoBoard.png").convert()
        self.BG = pygame.transform.scale(self.BG, (self.BG.get_width() * self.scale, self.BG.get_height() * self.scale))
        
        self.vTile_imgs = [pygame.image.load(f"Assets/vTile_{i}.png") for i in range(6)]
        self.hTile_imgs = [pygame.image.load(f"Assets/hTile_{i}.png") for i in range(6)]

        self.popUp_imgs = [pygame.image.load(f"Assets/popUp_{i}.png") for i in range(8)]
        self.quit_imgs = [pygame.image.load(f"Assets/quit_{i}.png") for i in range(2)]
        self.retry_imgs = [pygame.image.load(f"Assets/retry_{i}.png") for i in range(2)]
        
        self.quitPos = (WIDTH/4 - self.BG.get_width()/4 - (self.quit_imgs[1].get_width()/2 * self.scale), HEIGHT/2 - (self.quit_imgs[0].get_height()/2 * self.scale))
        self.retryPos = (3*WIDTH/4 + self.BG.get_width()/4 - (self.quit_imgs[1].get_width()/2 * self.scale), HEIGHT/2 - (self.quit_imgs[0].get_height()/2 * self.scale))
        self.quit = Button(self.quit_imgs, self.quitPos[0], self.quitPos[1], self.scale)
        self.retry = Button(self.retry_imgs, self.retryPos[0], self.retryPos[1], self.scale)

        self.quit_UI.add(self.quit)
        self.retry_UI.add(self.retry)

        self.TEXT_COLOR = (255, 255, 255)
        self.GAMEFONT = fonts.getFont(size = 64)
        self.popUp = 0 ## Just to initialize the variable
        
    def handle_events(self, events):
        return super().handle_events(events)
    
    def update(self) -> None:
        return super().update()
    
    def draw(self) -> None:
        return super().draw()
    
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TO BE CHANGED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    def screenPosToWorldPos(self, x: float, y: float) -> tuple:
        return super().screenPosToWorldPos(x, y)
    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TO BE CHANGED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    def calcUIinteraction(self, pos, key):
        return super().calcUIinteraction(pos, key)

    def calcMove(self, pos: tuple) -> None:
        if not self.ttt_gb.gameOver:
            indices = self.screenPosToWorldPos(pos[0], pos[1])
            if indices == (-1, -1):
                return
            val = self.ttt_gb.moveTo(indices[0], indices[1])
            if val == -1:
                return
            if val == 0:
                hTile = TilePiece(self.hTile_imgs, self.worldPos[0], self.worldPos[1], self.scale)
                self.tileGroup.add(hTile)
            else:
                vTile = TilePiece(self.vTile_imgs, self.worldPos[0], self.worldPos[1], self.scale)
                self.tileGroup.add(vTile)
            self.winner = self.ttt_gb.checkWin()

        if self.ttt_gb.gameOver:
            self.popUp = PopUp(self.popUp_imgs, WIDTH/2 - self.popUp_imgs[7].get_width()/2 * self.scale, HEIGHT/2 - self.popUp_imgs[0].get_height()/2 * self.scale, self.scale)
            self.tileGroup.add(self.popUp)
    
    def reset(self):
        return super().reset()

class RulesScene(Scene):
    def __init__(self, screen: pygame.Surface) -> None:
        self.BG_COLOR, self.TEXT_COLOR, self.INST_COLOR = (0, 0, 0), (74, 122, 150), (200, 200, 200)
        self.TITLEFONT, self.INSTFONT = TITLEFONT, INSTFONT
        self.x_offset, self.y_offset = 100, 100
        self.screen = screen
        self.scale = 8

        self.quit_imgs = [pygame.image.load(f"Assets/quit_{i}.png") for i in range(2)]
        self.quitPos = (WIDTH - self.quit_imgs[0].get_width()*self.scale - 100, self.y_offset)
        self.quit = Button(self.quit_imgs, self.quitPos[0], self.quitPos[1], self.scale)

        self.quit_UI = pygame.sprite.Group()
        self.quit_UI.add(self.quit)

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                pos = event.pos
                self.calcUIinteraction(pos, 0)
            if event.type == MOUSEBUTTONUP:
                pos = event.pos
                self.calcUIinteraction(pos, 1)

    def update(self) -> None:
        self.quit_UI.update()

    def draw(self) -> None:
        
        self.screen.fill(self.BG_COLOR)
        self.y_offset = 100

        title = self.TITLEFONT.render("Rules:", False, self.TEXT_COLOR)
        self.screen.blit(title, (self.x_offset, self.y_offset))
        self.quit_UI.draw(self.screen)
        self.y_offset += title.get_height() + 25

        head1 = self.INSTFONT.render("Tic-Tac-Toe", False, self.INST_COLOR)
        self.screen.blit(head1, (WIDTH/4 - head1.get_width()/2, self.y_offset))
        line = pygame.draw.line(self.screen, self.INST_COLOR, (WIDTH/2, self.y_offset), (WIDTH/2, HEIGHT - 50))
        head2 = self.INSTFONT.render("Tic-Tac-Two", False, self.INST_COLOR)
        self.screen.blit(head2, ((WIDTH/2 + WIDTH/4) - head2.get_width()/2, self.y_offset))
        self.y_offset += head1.get_height() + 25

        body1 = self.INSTFONT.render("1. Player one playes circle, and player two\nplays cross.\n\n2. Player cannot fill a grid that is already\nfilled.\n\n3. The first player to get three circles/\ncrosses horizontally, vertically or\ndiagonally wins the game.", False, self.INST_COLOR)
        self.screen.blit(body1, (self.x_offset, self.y_offset))
        body2 = self.INSTFONT.render("1. Player one playes horizontal, and player\ntwo plays vertical.\n\n2. Each player can stack their tile on top of\nthe other players tile exactly once to form\na +.\n\n3. The current player cannot stack a tile on\nthe opponent players' last tile.\n\n4. The first player to form three +'s in any\ndirection wins the game.", False, self.INST_COLOR)
        self.screen.blit(body2, (WIDTH/2 + 50, self.y_offset))

        cg.draw(self.screen)

    def calcUIinteraction(self, pos, key): ## key represents whether the function is called during
                                           ## a MOUSEBUTTONDOWN (0) or a MOUSEBUTTONUP (1) event.
        quitCondition = self.quitPos[0] < pos[0] < (self.quitPos[0] + self.quit_imgs[0].get_width() * self.scale) and self.quitPos[1] < pos[1] < (self.quitPos[1] + self.quit_imgs[0].get_height() * self.scale)
        
        if (quitCondition and not key):
            self.quit.is_animating = True
        if (quitCondition and key):
            self.manager.go_to(TitleScene(self.screen))

def main():

    ## Setting up the screen
    FPS = 12
    running = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac T(w)o(e)")
    clock = pygame.time.Clock()
    sm = SceneManager(TitleScene(screen))
    
    while running:

        clock.tick(FPS)

        if pygame.event.get(QUIT):
            running = False
        
        events = pygame.event.get()
        cg.update(events)

        sm.scene.handle_events(events)
        sm.scene.update()
        sm.scene.draw()

        cg.draw(screen)
        
        pygame.display.flip()

main()
pygame.quit()