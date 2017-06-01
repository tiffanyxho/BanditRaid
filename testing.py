#pygame treats the top left-hand corner as (0,0) and the bottom right-hand corner as (WIN_W, WIN_H)

import pygame, sys, random, time, os

WIN_W = 1000
WIN_H = 600
DEF_WIDTH = DEF_HEIGHT = 100
ARROW_WIDTH = 50
ARROW_HEIGHT = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TIMER = 0
MANA = 0


class Game():
    def __init__(self, intro, play, outros, clock, fps, beg_time, again):
        self.intro = intro
        self.play = play
        self.outros = outros
        self.clock = clock
        self.fps = fps
        self.move_up_left = False
        self.move_down_left = False
        self.move_up_right = False
        self.move_down_right = False
        self.beg_time = beg_time
        self.again = again

    def blink(self):
        self.cur_time = pygame.time.get_ticks()
        if ((self.cur_time - self.beg_time) % 1000) < 500:
            return True
        else:
            return False

    def build_troops(self):
        pass


class Defenders(pygame.sprite.Sprite):
    def __init__(self, x, y, soldier, fight):
        pygame.sprite.Sprite.__init__(self)
        self.width = DEF_WIDTH
        self.height = DEF_HEIGHT
        self.soldier = soldier
        self.x = x
        self.y = y
        if self.soldier == 'archer':
            self.image = pygame.image.load("images/archer.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.fight = fight


class Attack(pygame.sprite.Sprite):
    def __init__(self, weapon_width, weapon_height, soldier, soldier_position):
        pygame.sprite.Sprite.__init__(self)
        self.width = weapon_width
        self.height = weapon_height
        self.soldier = soldier
        self.x = soldier_position.x/5*9-5
        self.y = soldier_position.y + 30
        if self.soldier == 'archer':
            self.weapon = 'arrow'
            self.image = pygame.image.load("images/bronze_arrow.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIN_W + 150:
            self.rect.x = self.x


class Text_2():
    def __init__(self, centx, centy, text, font, size):
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, 1, BLACK)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = centx
        self.image_rect.centery = centy
        self.size = size

    def blit_text(self, screen):
        screen.blit(self.image, self.image_rect)

def main():
    global TITLE, screen, TIMER, pill_group

    pygame.display.set_caption('Tiffany_BOYG')
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)

    # initializing variables


    # text - title, subtitle (click)
    TITLE = Text_2(screen.get_rect().centerx, 100, "BYOG", None, 150)
    click = Text_2(screen.get_rect().centerx, screen.get_rect().centery, "-- Press enter or click to start --", None, 50)
    outrotext = Text_2(screen.get_rect().centerx, screen.get_rect().centery,
                     "-- Click or press enter to retry the level --", None, 60)
    one = Text_2(25, 25, "1", None, 20)
    avail_troops = Text_2(WIN_W/14, WIN_H*14/16, "TROOPS: ", None, 30)
    Archer = Text_2(WIN_W/7, WIN_H*14/16, "A", None, 30)

    # create game objects
    archer = Defenders(WIN_W*3/20, WIN_H*13/16, 'archer', True)

    # create groups
    defenders_group = pygame.sprite.Group()
    defenders_group.add(archer)
    attack_group = pygame.sprite.Group()

    # create game
    game = Game(True, True, False, pygame.time.Clock(), 60, pygame.time.get_ticks(), True)


    while game.again:
        while game.intro:
            # print background & title
            screen.fill(WHITE)
            TITLE.blit_text(screen)

            # Blinking Text: Click here to start
            if game.blink():
                screen.blit(click.image, click.image_rect)

            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # starts the game if the mouse button is pressed down or if the return key is pressed.
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    click.blit_text(screen)
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    game.intro = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Limits frames per iteration of while loop
            game.clock.tick(game.fps)

            # Writes to main surface
            pygame.display.flip()

        while game.play:
            screen.fill(WHITE)

            # build troops
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        one.image = 50
                        print(one.size)
                        archer_1 = Defenders(WIN_W / 8, WIN_H / 20 * 9, 'archer', False)
                        defenders_group.add(archer_1)
                        arrow_1 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_1)
                        attack_group.add(arrow_1)

            # update groups
            attack_group.update()

            # print groups
            defenders_group.draw(screen)
            attack_group.draw(screen)

            # blit text
            one.blit_text(screen)
            avail_troops.blit_text(screen)
            Archer.blit_text(screen)

            # limits frames per iteration of while loop
            game.clock.tick(game.fps)
            # writes to main surface
            pygame.display.flip()

        while game.outros:
            screen.fill(WHITE)


            if game.blink():
                outrotext.blit_text(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    outrotext.blit_text(screen)

                    pygame.display.flip()
                    pygame.time.wait(1000)
                    game.outros = False
                    game.intro = True
                    game.play = True

                    if game.outros == False:
                        pass

            game.clock.tick(game.fps)
            pygame.display.flip()


if __name__ == "__main__":
    # force static position of screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # runs imported module
    pygame.init()

    main()