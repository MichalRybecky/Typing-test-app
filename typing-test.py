# 27.8.2020
# Typing Test

import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Test")

BG = pygame.image.load(os.path.join("assets", "bg.jpeg"))
main_font = pygame.font.Font("abeezee.ttf", 50)

FPS = 120
clock = pygame.time.Clock()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    click = False

    dur = 0
    wpm = 0
    label_font = pygame.font.Font("abeezee.ttf", 50)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        dur_label = label_font.render(f"{dur}", 1, (255, 255, 255))
        wpm_label = label_font.render(f"{wpm}", 1, (255, 255, 255))

        WIN.blit(dur_label, (30, 10))
        WIN.blit(wpm_label, (WIDTH - 100, 10))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    pass


def main_menu():
    run = True
    click = False

    while run:
        clock.tick(FPS)
        WIN.blit(BG, (0, 0))
        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button_play = pygame.Rect(
            (WIDTH / 2) - 160, (HEIGHT / 2) - 100, 320, 80)
        button_settings = pygame.Rect(
            (WIDTH / 2) - 160, (HEIGHT / 2), 320, 80)

        pygame.draw.rect(WIN, (50, 75, 50), button_play)
        pygame.draw.rect(WIN, (50, 75, 50), button_settings)

        # Menu Labels
        label_play = main_font.render("Play", 1, (255, 255, 255))
        WIN.blit(label_play, ((WIDTH / 2) - 50, 275))

        label_settings = main_font.render("Settings", 1, (255, 255, 255))
        WIN.blit(label_settings, ((WIDTH / 2) - 90, 370))

        # Button Activations
        if click:
            if button_play.collidepoint((pos_x, pos_y)):
                main()
            if button_settings.collidepoint((pos_x, pos_y)):
                settings_menu()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
    pygame.quit()



def settings_menu():
    pass


def post_menu():
    pass


main_menu()
