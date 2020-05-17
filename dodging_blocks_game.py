#dodgging_the_blocks
import pygame
import random

pygame.init()

display_width = 1200
display_height = 700

yellow = (255, 250, 0)
blue = (0, 0, 100)
green = (0, 100, 0)
bright_blue = (0, 0, 255)
bright_green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
purple = (255, 0, 255)
white = (255, 255, 255)
color_list = [bright_blue, red, orange, bright_green, purple]

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("MY GAME")

clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
car_width = 127  # 129
car_height = 100  # 95

high1 = 0
high2 = 0
highest = max(high1, high2)

pause = False


def dodged(score, highest):  # function to calculate and display score
    score_style = pygame.font.SysFont(None, 30)
    score_text = score_style.render("Score:" + str(score), True, black)
    highest_style = pygame.font.SysFont(None, 30)
    highest_text = highest_style.render("Highest score:" + str(highest), True, black)
    gameDisplay.blit(score_text, (0, 0))
    gameDisplay.blit(highest_text, (1000, 0))


def things(thingx, thingy, thingw, thingh, color):  # function to draw the obstacle
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x, y):  # specifying position of the car
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font, Color):  # specifying the font of text and its position
    textSurface = font.render(text, True, Color)
    return textSurface, textSurface.get_rect()


def game_loop():  # main game loop
    global highest
    global high1
    global high2
    global pause
    pause = False
    myscore = 0

    x = (display_width * 0.40)
    y = (display_height * 0.85)
    x_change = 0
    x_speed = 6
    thing_w = 150
    thing_x = random.randrange(0, display_width - thing_w)
    thing_y = -300
    thing_h = 200
    thing_speed = 4

    gameExit = False
    color = random.choice(color_list)

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -x_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = x_speed
                elif event.key == pygame.K_p:
                    paused()

        x += x_change
        gameDisplay.fill(yellow)

        things(thing_x, thing_y, thing_w, thing_h, color)  # creating first obstacle
        thing_y += thing_speed

        car(x, y)

        dodged(myscore, highest)
        if thing_y > display_height:  # creating obstacles one by one
            thing_x = random.randrange(0, display_width - thing_w)
            thing_y = 0 - thing_h
            myscore += 1
            if myscore % 5 == 0:  # after dodging every 5 blocks,width of obstacle is increased by 2,speed of racecar is increased by 1 and speed of obstacle is increased by 2
                x_speed += 1
                thing_speed += 2
                thing_w += 2
            color = random.choice(color_list)
        if myscore > highest:
            high2 = high1
            high1 = myscore
            highest = max(high1, high2)
        else:
            highest = max(high1, high2)

        if x <= 0 or x >= display_width - car_width:
            x_change = 0
        # if y<thing_y+thing_h:
        if y <= thing_y + thing_h and y + car_height >= thing_y:
            if (x + car_width >= thing_x and x + car_width <= thing_x + thing_w) or (
                    x <= thing_x + thing_w and x >= thing_x):
                crashed()
        pygame.display.update()

        clock.tick(90)


def draw_button(x, y, w, h, color, msg):  # designing button
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])
    font = pygame.font.SysFont(None, 30)
    text_surf, text_rect = text_objects(msg, font, white)
    text_rect.center = (x + (w / 2), y + (h / 2))
    gameDisplay.blit(text_surf, text_rect)


def button(x, y, w, h, color, new_color, msg, action=None):  # specifying function of the button
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        draw_button(x, y, w, h, new_color, msg)
        if click[0] == 1 and action != None:
            action()
    else:
        draw_button(x, y, w, h, color, msg)


def exit_game():
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


def paused():  # function that pauses the game when p is pressed
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        gameDisplay.fill(yellow)
        font = pygame.font.SysFont("arial.ttf", 120)
        text_surf, text_rect = text_objects("Game Paused", font, black)
        text_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(text_surf, text_rect)

        button(300, 500, 200, 50, blue, bright_blue, "CONTINUE", unpause)
        button(700, 500, 200, 50, green, bright_green, "QUIT", exit_game)

        pygame.display.update()
        clock.tick(15)


def crashed():  # function that operates when the car gets crashed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        gameDisplay.fill(yellow)
        font = pygame.font.SysFont("arial.ttf", 120)
        text_surf, text_rect = text_objects("Crashed! Want to play again?", font, black)
        text_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(text_surf, text_rect)

        button(300, 500, 200, 50, blue, bright_blue, "YES", game_loop)
        button(700, 500, 200, 50, green, bright_green, "NO", exit_game)

        pygame.display.update()
        clock.tick(15)


def intro_page():  # intro to the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        gameDisplay.fill(yellow)
        font = pygame.font.SysFont("arial.ttf", 120)
        text_surf, text_rect = text_objects("Dodge The Blocks", font, black)
        text_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(text_surf, text_rect)

        button(300, 500, 200, 50, blue, bright_blue, "PLAY", game_loop)
        button(700, 500, 200, 50, green, bright_green, "QUIT", exit_game)

        pygame.display.update()
        clock.tick(15)


intro_page()

