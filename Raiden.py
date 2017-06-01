#pygame treats the top left-hand corner as (0,0) and the bottom right-hand corner as (WIN_W, WIN_H)

import pygame, os, sys

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Force static position of screen

# Constants
WIN_W = 16*32
WIN_H = 700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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


class Text_2():
    def __init__(self, centx, centy, text, font, size):
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, 1, BLACK)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = centx
        self.image_rect.centery = centy

    def blit_text(self, screen):
        screen.blit(self.image, self.image_rect)


def main():
    global TITLE, screen
    # rmr to add sound and background

    pygame.init()

    # Create Game Variables
    fps = 60
    clock = pygame.time.Clock()
    play = True
    pygame.display.set_caption('Raiden 2 Clone')
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)

    # Create Game Objects

    # Create Groups

    # Load Level
    level = [
        "PPPPPPPPPPPPPPPP",
        "P              P",
        "P              P",
        "P          PPPPP",
        "P              P",
        "PPPPPPPP       P",
        "P              P",
        "P              P"
        "P              P",
        "P          PPPPP",
        "P              P",
        "P              P",
        "PPPP           P",
        "P              P",
        "P           PPPP",
        "PPPPP          P",
        "P              P",
        "P              P",
        "P        PPPPPPP",
        "P              P",
        "PPPPPP         P",
        "P              P",
        "PPPPPPPPPPPPPPPP", ]
    
    # Build Level

    # Gameplay

    # text - title, subtitle (click)
    TITLE = Text_2(screen.get_rect().centerx, 100, "RAIDEN", None, 230)
    click = Text_2(screen.get_rect().centerx, screen.get_rect().centery, "-- Press enter or click to start --", None, 80)
    outrotext = Text_2(screen.get_rect().centerx, screen.get_rect().centery,
                     "-- Click or press enter to play again --", None, 60)

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
            # Checks if window exit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Update
            screen.fill(WHITE)

            # Draw Everything

            # Limits frames per iteration of while loop
            clock.tick(fps)
            # Writes to main surface
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