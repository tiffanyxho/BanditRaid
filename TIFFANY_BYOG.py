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
TIMER2 = 50
MANA = 0


class Game():
    def __init__(self, intro, instructions, play, outros, clock, fps, beg_time, again):
        self.intro = intro
        self.play = play
        self.instructions = instructions
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


    def update(self, bandit_1, bandit_2):
        if bandit_1.rect.x < WIN_W or bandit_2.rect.x < WIN_W:
            self.play = False
            self.outros = True


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


class Bandits(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = DEF_WIDTH
        self.height = DEF_HEIGHT
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.image.load("images/bandit_attacking.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def update(self):
        self.rect.x -= self.speed


class Attack(pygame.sprite.Sprite):
    def __init__(self, weapon_width, weapon_height, soldier, soldier_position, alive):
        pygame.sprite.Sprite.__init__(self)
        self.width = weapon_width
        self.height = weapon_height
        self.soldier = soldier
        self.x = soldier_position.x + soldier_position.width/2
        self.y = soldier_position.y + 30
        if self.soldier == 'archer':
            self.weapon = 'arrow'
            self.image = pygame.image.load("images/bronze_arrow.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)
        self.speed = 5
        self.alive = alive

    def update(self, bandits_group):
        self.rect.x += self.speed
        if self.rect.x > WIN_W + 150:
            self.rect.x = self.x

        collisions = pygame.sprite.spritecollide(self, bandits_group, True)
        for key in collisions:
            self.kill()
            self.alive = False



class Text_2():
    def __init__(self, centx, centy, text, font, size, color):
        self.font = pygame.font.Font(font, size)
        self.image = self.font.render(text, 1, color)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = centx
        self.image_rect.centery = centy
        self.size = size
        self.centx = centx
        self.centy = centy

    def blit_text(self, screen):
        screen.blit(self.image, self.image_rect)


def main():
    global TITLE, screen, TIMER, TIMER2, pill_group, MANA

    pygame.display.set_caption('Tiffany_BOYG')
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.SRCALPHA)

    # initializing variables
    times_one_pressed = times_two_pressed = times_three_pressed = times_four_pressed = 0
    level_1_bandits = 0

    # text - title, subtitle (click)
    TITLE = Text_2(screen.get_rect().centerx, 100, "BANDIT RAID", None, 150, BLACK)
    click = Text_2(screen.get_rect().centerx, screen.get_rect().centery, "-- Press enter or click to continue --", None, 50, BLACK)
    outrotext = Text_2(screen.get_rect().centerx, screen.get_rect().centery - WIN_H/10,
                     "The bandits have raided your house!", None, 40, BLACK)
    outrotext2 = Text_2(screen.get_rect().centerx, screen.get_rect().centery, "Click or press enter when you're ready to"
                                                                              " protect your house again!", None, 40, BLACK)
    INSTRUCTIONS = Text_2(screen.get_rect().centerx, WIN_H/15, "INSTRUCTIONS", None, 60, BLACK)
    instruct_line_1 = Text_2(screen.get_rect().centerx, WIN_H*2/15, "Your job is to stop the bandits that approach you and your house!",
                          None, 40, BLACK)
    instruct_line_2 = Text_2(screen.get_rect().centerx, WIN_H*3/15, "To summon your defense, first press the number position that you ",
                          None, 40, BLACK)
    instruct_line_3 = Text_2(screen.get_rect().centerx, WIN_H*4/15, "want to summon a troop at and then press the letter troop that you want",
                          None, 40, BLACK)
    instruct_line_4 =Text_2(screen.get_rect().centerx, WIN_H*5/15, "to summon.  Troops require mana to summon, so manage it well!", None, 40, BLACK)
    one = Text_2(WIN_W / 40, WIN_H / 16, "1", None, 20, BLACK)
    two = Text_2(WIN_W / 40, WIN_H * 7 / 16, "2", None, 20, BLACK)
    three = Text_2(WIN_W * 4 / 20, WIN_H / 16, "3", None, 20, BLACK)
    four = Text_2(WIN_W * 4 / 20, WIN_H * 7 / 16, "4", None, 20, BLACK)
    avail_troops = Text_2(WIN_W / 14, WIN_H * 14 / 16, "TROOPS: ", None, 30, BLUE)
    Archer = Text_2(WIN_W / 7, WIN_H * 14 / 16, "A", None, 30, BLUE)
    mana = Text_2(WIN_W * 16 / 20, WIN_H / 16, "MANA: " + str(MANA), None, 50, BLUE)
    no_mana = Text_2(WIN_W / 2, WIN_H / 18, "YOU DO NOT HAVE ENOUGH MANA.", None, 25, WHITE)
    archer_mana_cost = Text_2(WIN_W * 20 / 100, WIN_H * 51 / 64, "30", None, 25, BLUE)
    select_position = Text_2(WIN_W/5, WIN_H / 18, "SELECT A POSITION.", None, 25, WHITE)


    # create game objects
    archer = Defenders(WIN_W * 3 / 20, WIN_H * 13 / 16, 'archer', True)
    archer_1 = Defenders(WIN_W / 16, WIN_H / 14, 'archer', False)
    arrow_1 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_1, False)
    archer_2 = Defenders(WIN_W / 16, WIN_H * 9 / 20, 'archer', False)
    arrow_2 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_2, False)

    archer_3 = Defenders(WIN_W * 4 / 16, WIN_H / 14, 'archer', False)
    arrow_3 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_3, False)
    archer_4 = Defenders(WIN_W * 4 / 16, WIN_H * 9 / 20, 'archer', False)
    arrow_4 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_4, False)

    bandit_1 = Bandits(WIN_W * 1.1, WIN_H / 13)
    bandit_2 = Bandits(WIN_W * 1.1, WIN_H / 2)

    # create groups
    defenders_group = pygame.sprite.Group()
    defenders_group.add(archer)
    attack_group = pygame.sprite.Group()
    bandits_group = pygame.sprite.Group()

    # create game
    game = Game(True, True, True, False, pygame.time.Clock(), 60, pygame.time.get_ticks(), True)


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

        while game.instructions:
            screen.fill(WHITE)
            INSTRUCTIONS.blit_text(screen)
            instruct_line_1.blit_text(screen)
            instruct_line_2.blit_text(screen)
            instruct_line_3.blit_text(screen)
            instruct_line_4.blit_text(screen)

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
                    game.instructions = False
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

            screen.fill(WHITE)

            # build troops
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_1:
                        times_one_pressed += 1
                        if times_one_pressed % 2 == 1:
                            one.color = RED
                            one.size = 50
                        elif times_one_pressed % 2 == 0:
                            one.color = BLACK
                            one.size = 20

                        if two.size == 50:
                            two.size = 20
                            times_two_pressed += 1

                        if three.size == 50:
                            three.size = 20
                            times_three_pressed += 1

                        if four.size == 50:
                            four.size = 20
                            times_four_pressed += 1

                        one.font = pygame.font.Font(None, one.size)
                        one.image = one.font.render("1", 1, one.color)

                        two.font = pygame.font.Font(None, two.size)
                        two.image = two.font.render("2", 1, BLACK)

                        three.font = pygame.font.Font(None, three.size)
                        three.image = three.font.render("3", 1, BLACK)

                        four.font = pygame.font.Font(None, three.size)
                        four.image = four.font.render("4", 1, BLACK)

                    if event.key == pygame.K_2:
                        times_two_pressed += 1
                        if times_two_pressed % 2 == 1:
                            two.color = RED
                            two.size = 50
                        elif times_two_pressed % 2 == 0:
                            two.color = BLACK
                            two.size = 20

                        if one.size == 50:
                            one.size = 20
                            times_one_pressed += 1

                        if three.size == 50:
                            three.size = 20
                            times_three_pressed += 1

                        if four.size == 50:
                            four.size = 20
                            times_four_pressed += 1

                        two.font = pygame.font.Font(None, two.size)
                        two.image = two.font.render("2", 1, two.color)

                        one.font = pygame.font.Font(None, one.size)
                        one.image = one.font.render("1", 1, BLACK)

                        three.font = pygame.font.Font(None, three.size)
                        three.image = three.font.render("3", 1, BLACK)

                        four.font = pygame.font.Font(None, three.size)
                        four.image = four.font.render("4", 1, BLACK)

                    if event.key == pygame.K_3:
                        times_three_pressed += 1
                        if times_three_pressed % 2 == 1:
                            three.color = RED
                            three.size = 50

                        elif times_three_pressed % 2 == 0:
                            three.color = BLACK
                            three.size = 20

                        if one.size == 50:
                            one.size = 20
                            times_one_pressed += 1

                        if two.size == 50:
                            two.size = 20
                            times_two_pressed += 1

                        if four.size == 50:
                            four.size = 20
                            times_four_pressed += 1

                        one.font = pygame.font.Font(None, one.size)
                        one.image = one.font.render("1", 1, BLACK)

                        two.font = pygame.font.Font(None, two.size)
                        two.image = two.font.render("2", 1, BLACK)

                        three.font = pygame.font.Font(None, three.size)
                        three.image = three.font.render("3", 1, three.color)

                        four.font = pygame.font.Font(None, four.size)
                        four.image = four.font.render("4", 1, BLACK)


                    if event.key == pygame.K_4:
                        times_four_pressed += 1
                        if times_four_pressed % 2 == 1:
                            four.color = RED
                            four.size = 50

                        elif times_four_pressed % 2 == 0:
                            four.color = BLACK
                            four.size = 20

                        if one.size == 50:
                            one.size = 20
                            times_one_pressed += 1

                        if two.size == 50:
                            two.size = 20
                            times_two_pressed += 1

                        if three.size == 50:
                            three.size = 20
                            times_three_pressed += 1

                        one.font = pygame.font.Font(None, one.size)
                        one.image = one.font.render("1", 1, BLACK)

                        two.font = pygame.font.Font(None, two.size)
                        two.image = two.font.render("2", 1, BLACK)

                        three.font = pygame.font.Font(None, three.size)
                        three.image = three.font.render("3", 1, BLACK)

                        four.font = pygame.font.Font(None, four.size)
                        four.image = four.font.render("4", 1, four.color)


                    if event.key == pygame.K_a:
                        if MANA < 30 and one.size == 50 or MANA < 30 and two.size == 50:
                            no_mana.color = BLUE
                            no_mana.image = no_mana.font.render("YOU DO NOT HAVE ENOUGH MANA.", 1, no_mana.color)
                            no_mana.blit_text(screen)

                        if one.size == 50 and MANA >= 30.0 and archer_1.fight == False:
                            archer_1.fight = True
                            MANA -= 30.0
                            one.size = 20
                            one.color = BLACK

                        if two.size == 50 and MANA >= 30.0 and archer_2.fight == False:
                            archer_2.fight = True
                            MANA -= 30.0
                            two.size = 20
                            two.color = BLACK

                            two.font = pygame.font.Font(None, two.size)

                        if three.size == 50 and MANA >= 30.0 and archer_3.fight == False:
                            archer_3.fight = True
                            MANA -= 30.0
                            three.size = 20
                            three.color = BLACK

                            three.font = pygame.font.Font(None, three.size)

                        if four.size == 50 and MANA >= 30.0 and archer_4.fight == False:
                            archer_4.fight = True
                            MANA -= 30.0
                            four.size = 20
                            four.color = BLACK

                            four.font = pygame.font.Font(None, four.size)

                        if one.size == 20 and archer_1.fight == False and two.size == 20 and archer_2.fight == False and three.size == 20\
                                and archer_3.fight == False and four.size == 20 and archer_4.fight == False:
                            select_position.image = select_position.font.render("SELECT A POSITION.", 1,
                                                                                    BLUE)
                            select_position.blit_text(screen)
                        else:
                            select_position.image = select_position.font.render("SELECT A POSITION.", 1,
                                                                                WHITE)

                    if archer_1.fight == True:
                        no_mana.color = WHITE
                        no_mana.image = no_mana.font.render("YOU DO NOT HAVE ENOUGH MANA.", 1, no_mana.color)
                        no_mana.blit_text(screen)

                        defenders_group.add(archer_1)
                        attack_group.add(arrow_1)
                        arrow_1.alive = True

                    if archer_2.fight == True:
                        no_mana.color = WHITE
                        no_mana.image = no_mana.font.render("YOU DO NOT HAVE ENOUGH MANA.", 1, no_mana.color)
                        no_mana.blit_text(screen)

                        defenders_group.add(archer_2)
                        attack_group.add(arrow_2)
                        arrow_2.alive = True

                    if archer_3.fight == True:
                        no_mana.color = WHITE
                        no_mana.image = no_mana.font.render("YOU DO NOT HAVE ENOUGH MANA.", 1, no_mana.color)
                        no_mana.blit_text(screen)

                        defenders_group.add(archer_3)
                        attack_group.add(arrow_3)
                        arrow_3.alive = True

                    if archer_4.fight == True:
                        no_mana.color = WHITE
                        no_mana.image = no_mana.font.render("YOU DO NOT HAVE ENOUGH MANA.", 1, no_mana.color)
                        no_mana.blit_text(screen)

                        defenders_group.add(archer_4)
                        attack_group.add(arrow_4)
                        arrow_4.alive = True

            if MANA < 99.9:
                MANA += 0.1

            if TIMER % 350 == 0:
                if archer_1.fight == True and arrow_1.alive == False:
                    arrow_1 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_1, False)
                    arrow_1.add(attack_group)

            if TIMER2 % 350 == 0:
                if archer_2.fight == True and arrow_2.alive == False:
                    arrow_2 = Attack(ARROW_WIDTH, ARROW_HEIGHT, 'archer', archer_2, False)
                    arrow_2.add(attack_group)

            if TIMER > 600 and TIMER % 300 == 0:
                bandits_group.add(bandit_1)
                level_1_bandits += 1


            if TIMER > 700 and TIMER % 290 == 0:
                bandits_group.add(bandit_2)
                level_1_bandits += 1


            # update groups
            attack_group.update(bandits_group)
            bandits_group.update()
            game.update(bandit_1, bandit_2)

            # print groups
            defenders_group.draw(screen)
            attack_group.draw(screen)
            bandits_group.draw(screen)

            TIMER += 1
            TIMER2 += 1

            # blit text
            one.blit_text(screen)
            two.blit_text(screen)
            four.blit_text(screen)
            avail_troops.blit_text(screen)
            Archer.blit_text(screen)
            archer_mana_cost.blit_text(screen)
            mana.image = mana.font.render("MANA: " + str(MANA), 1, BLUE)
            mana.blit_text(screen)
            no_mana.blit_text(screen)
            select_position.blit_text(screen)
            three.blit_text(screen)

            # limits frames per iteration of while loop
            game.clock.tick(game.fps)
            # writes to main surface
            pygame.display.flip()

        while game.outros:
            screen.fill(WHITE)

            if game.blink():
                outrotext.blit_text(screen)
                outrotext2.blit_text(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                    outrotext.blit_text(screen)
                    outrotext2.blit_text(screen)

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