import pygame
import random
import sys

pygame.init()

clock = pygame.time.Clock()

FPS = 60
# coolours
brown = (139, 69, 19)
red = (255, 0, 0)
greendark = (0, 128, 0)
black = 0, 0, 0
green = (124, 252, 0)
blue = (135, 206, 250)
# screen display
screen = pygame.display.set_mode((900, 600))
# background image
background = pygame.image.load("pics/back.png").convert_alpha()
screen.fill(brown)
# Wood image
wood = pygame.image.load("pics/wood.png").convert_alpha()
# character jumping image
jump = [pygame.image.load("pics/jump1.png").convert_alpha(),
        pygame.image.load("pics/jump2.png").convert_alpha(),
        pygame.image.load("pics/jump3.png").convert_alpha(),
        pygame.image.load("pics/jump4.png").convert_alpha(),
        pygame.image.load("pics/jump5.png").convert_alpha(),
        pygame.image.load("pics/jump6.png").convert_alpha(),
        pygame.image.load("pics/jump7.png").convert_alpha(),
        pygame.image.load("pics/jump8.png").convert_alpha(),
        pygame.image.load("pics/jump9.png").convert_alpha(),
        pygame.image.load("pics/jump10.png").convert_alpha()]
# character running left image
run_left = [pygame.image.load("pics/run1.png").convert_alpha(),
            pygame.image.load("pics/run2.png").convert_alpha(),
            pygame.image.load("pics/run3.png").convert_alpha(),
            pygame.image.load("pics/run4.png").convert_alpha(),
            pygame.image.load("pics/run5.png").convert_alpha(),
            pygame.image.load("pics/run6.png").convert_alpha()]
# character running right image
run_right = [pygame.image.load("pics/run1r.png").convert_alpha(),
             pygame.image.load("pics/run2r.png").convert_alpha(),
             pygame.image.load("pics/run3r.png").convert_alpha(),
             pygame.image.load("pics/run4r.png").convert_alpha(),
             pygame.image.load("pics/run5r.png").convert_alpha(),
             pygame.image.load("pics/run6r.png").convert_alpha()]
# character standing image
stand = pygame.image.load("pics/stand.png").convert_alpha()


class Ricky(pygame.sprite.Sprite):

    '''Class representing the character Ricky'''

    def __init__(self, screen, Wood):
        super(Ricky, self).__init__()
        # size of the image of ricky
        size = (5, 5)
        # x and y corrdinate of ricky's image
        self.y = 474
        self.x = 300
        self.rect = pygame.Rect((self.x, self.y), size)
        # running left images
        self.images_rl = run_left
        # running left is set to false
        self.index_rl = 0
        # runing right images
        self.images_rr = run_right
        # running right is set to false
        self.index_rr = 0
        # jumping images
        self.images_j = jump
        self.index_j = 0

        # if self is curretly jumping
        self.current_jump = 0
        # speed of self moving left or right
        self.speed = 7
        self.image_jump = jump
        # jumping is set to false
        self.jump = 0

        self.animation_time = 0.1
        self.current_time = 0
        self.animation_frames = 6

       # self is not initially moving left or right
        self.moveleft = 0
        self.moveright = 0

    def update(self, timeelapse):
        self.current_time += timeelapse
        # if moving left, translate image left
        if self.moveleft == 1:
            self.x -= self.speed
        # if moving right, translate image right
        if self.moveright == 1:
            self.x += self.speed
        # if jumping, moving left or right, loops through pics to create moving
        # effect
        if self.jump > 0:
            self.current_time = 0
            self.index_j = (self.index_j + 1) % len(self.images_j)
            self.image = self.images_j[self.index_j]
        elif self.current_time >= self.animation_time and self.moveleft:
            self.current_time = 0
            self.index_rl = (self.index_rl + 1) % len(self.images_rl)
            self.image = self.images_rl[self.index_rl]
            self.moveleft = 0
        elif self.current_time >= self.animation_time and self.moveright:
            self.current_time = 0
            self.index_rr = (self.index_rr + 1) % len(self.images_rr)
            self.image = self.images_rr[self.index_rr]
            self.moveright = 0
        elif not self.moveright and not self.moveleft and self.jump == 0:
            self.image = stand

        # if jump is set to true and self is not currently jumping, execute
        # jump
        if self.jump > 0 and self.current_jump == 0:
            self.y = self.y - self.jump
            self.jump -= 1
        # translate image back down until intial position is met
        if self.y < 474:
            self.y += 5
        # set currently jumping to false when image is at initial position
        else:
            self.current_jump = 0

        self.rect[0] = self.x
        self.rect[1] = self.y

    def jumping(self):
        '''(Ricky) -> NoneType
        If self is cureently not jumping then executes jumping
        '''
        # not currently jumping, execute jump on image
        if self.current_jump == 0:
            self.jump = 20
            # set currently jumping to true
            self.current_jump = 1

    def move_left(self):
        '''(Ricky) -> NoneType
        '''
        # set moving left to true
        self.moveleft = 1

    def move_right(self):
        '''(Ricky) -> NoneType
        '''
        # set moving right to true
        self.moveright = 1


class Wood(pygame.sprite.Sprite):

    '''A class representing the wood objects in the game'''

    def __init__(self, screen):
        super(Wood, self).__init__()
        self.screen = screen
        # horizontal gap between wood
        self.gap = 100
        # first set of x,y corrdinates for wood, chosen at random
        self.x0 = random.randint(0, 600)
        self.x1 = self.x0 - 600 - self.gap
        self.x2 = self.x0 + 600 + self.gap
        self.y0 = 0
        # second set, vertical gap is 300
        self.x3 = random.randint(0, 600)
        self.x4 = self.x3 - 600 - self.gap
        self.x5 = self.x3 + 600 + self.gap
        self.y1 = self.y0 - 300
        # third set, vertical gap is 300
        self.x6 = random.randint(0, 600)
        self.x7 = self.x6 - 600 - self.gap
        self.x8 = self.x6 + 600 + self.gap
        self.y2 = self.y1 - 300

        self.counter = 0  # score counter
        # coordinates placed in a list
        self.y = [self.y0, self.y1, self.y2]
        self.x = [self.x0, self.x1, self.x2, self.x3,
                  self.x4, self.x5, self.x6, self.x7, self.x8]
        # speed of logs translating across screen
        self.speed = 2
        # corrdinates for grass rectable
        self.grassx = 0
        self.grassy = 580

        self.start = 0

    def draw(self):
        # display wood images onto screen
        self.screen.blit(wood, (self.x[0], self.y[0]))
        self.screen.blit(wood, (self.x[1], self.y[0]))
        self.screen.blit(wood, (self.x[2], self.y[0]))

        self.screen.blit(wood, (self.x[3], self.y[1]))
        self.screen.blit(wood, (self.x[4], self.y[1]))
        self.screen.blit(wood, (self.x[5], self.y[1]))

        self.screen.blit(wood, (self.x[6], self.y[2]))
        self.screen.blit(wood, (self.x[7], self.y[2]))
        self.screen.blit(wood, (self.x[8], self.y[2]))
        # draw grass as a rectangle
        pygame.draw.rect(screen, green, (self.grassx, self.grassy, 900, 20), 0)
        # display score on sceen
        score = 'Score: ' + str(self.counter)
        font = pygame.font.SysFont("Times New Roman", 25)
        screen.blit(font.render(str(score), -1, (120, 0, 0)), (15, 80))

    def updaterock(self):
        # add to the y coordinate of each set of logs to translate down
        self.y[0] += self.speed
        self.y[1] += self.speed
        self.y[2] += self.speed
        if self.y[0] >= 580:  # once the wall is off screen start at x=580
            self.x0 = random.randint(0, 600)
            self.counter += 1
            self.x[1] = self.x[0] - 600 - self.gap
            self.x[2] = self.x[0] + 600 + self.gap
            self.y[0] = -300
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.y.append(self.y.pop(0))
        elif self.y[1] >= 580:
            self.x[4] = self.x[3] - 600 - self.gap
            self.x[5] = self.x[3] + 600 + self.gap
            self.y[1] = -300
            self.counter += 1
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.y.append(self.y.pop(0))
        elif self.y[2] >= 580:
            self.x[6] = random.randint(0, 600)
            self.x[7] = self.x[6] - 600 - self.gap
            self.x[8] = self.x[6] + 600 + self.gap
            self.y[2] = -300
            self.counter += 1
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.x.append(self.x.pop(0))
            self.y.append(self.y.pop(0))

        pygame.draw.rect(screen, green, (self.grassx, self.grassy, 900, 20), 0)
        # render Wood in game
        self.draw()
        score = 'Score: ' + str(self.counter)
        font = pygame.font.SysFont("Times New Roman", 25)
        screen.blit(font.render(str(score), -1, (120, 0, 0)), (15, 80))
        pygame.draw.rect(screen, green, (self.grassx, self.grassy, 900, 20), 0)

def text_objects(text, font):
    textSurface = font.render(text, True, brown)
    return textSurface, textSurface.get_rect()


def main():
    images_rl = run_left  # Make sure to provide the relative or full path to the images_rl directory.
    wood = Wood(screen)
    player = Ricky(screen, wood)
    pressed_left = 0
    pressed_up = 0
    pressed_right = 0
    k = False

    all_sprites = pygame.sprite.Group(
        player)  # Creates a sprite group and adds 'player' to it.
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        screen.fill(blue)
        largeText = pygame.font.SysFont('Times New Roman', 115)
        TextSurf, TextRect = text_objects("Falling Logs", largeText)
        TextRect.center = ((900 / 2), (600 / 2))
        screen.blit(TextSurf, TextRect)
        pygame.draw.rect(screen, greendark, (200, 450, 100, 50))
        pygame.draw.rect(screen, red, (600, 450, 100, 50))
        font = pygame.font.SysFont("Times New Roman", 50)
        screen.blit(font.render("Start", -1, (1, 1, 1)), (200, 440))
        font1 = pygame.font.SysFont("Times New Roman", 50)
        screen.blit(font1.render("Quit", -1, (1, 1, 1)), (600, 440))
        mouse = pygame.mouse.get_pos()

        if 200 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450 and pygame.mouse.get_pressed()[0]:
            intro = False
        elif 600 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450 and pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(15)

    next_point = False
    running = True
    while running:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pressed_left = True
                elif event.key == pygame.K_RIGHT:
                    pressed_right = True
                k = True
            elif (event.type == pygame.KEYUP):
                if(event.key == pygame.K_UP):
                    player.jumping()
                elif event.key == pygame.K_LEFT:
                    pressed_left = False
                elif event.key == pygame.K_RIGHT:
                    pressed_right = False
                k = True

        if pressed_left and not pressed_right:
            player.move_left()
        if pressed_right and not pressed_left:
            player.move_right()

        if (player.y <= wood.y[0] + 53 and player.y + 100 > wood.y[0] and (wood.x[0] - 50 <= player.x <= wood.x[0] + 563 or wood.x[1] - 5 <= player.x <= wood.x[1] + 563 or wood.x[2] - 50 <= player.y <= wood.x[2] + 563)):
            running = False

        if wood.counter % 5 != 0:
            next_point = True
        if wood.counter % 5 == 0 and next_point:
            wood.speed += 1
            player.speed += 1
            next_point = False

                #running = False
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        all_sprites.update(
            dt)  # Calls the 'update' method on all sprites in the list (currently just the player).
        screen.fill(blue)
        all_sprites.draw(screen)
        wood.draw()
        pygame.display.update()
        wood.updaterock()
    # end of game menu
    end = True
    while end:
        # if exited
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                              event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
        # game over message
        myfont = pygame.font.SysFont('Times New Roman', 115)
        textsurf = myfont.render("Game Over", False, black)
        screen.blit(textsurf, (165, 160))
        # restart button
        pygame.draw.rect(screen, greendark, (200, 450, 100, 50))
        font = pygame.font.SysFont("Times New Roman", 35)
        screen.blit(font.render("Restart", -1, (1, 1, 1)), (200, 456))
        # quit button
        pygame.draw.rect(screen, red, (600, 450, 100, 50))
        font1 = pygame.font.SysFont("Times New Roman", 35)
        screen.blit(font1.render("Quit", -1, (1, 1, 1)), (610, 455))

        # use mouse to strike restart or quit button
        mouse = pygame.mouse.get_pos()

        if (200 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450 and
                pygame.mouse.get_pressed()[0]):
            main()
        elif (600 + 100 > mouse[0] > 150 and 450 + 50 > mouse[1] > 450 and
              pygame.mouse.get_pressed()[0]):
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main()
