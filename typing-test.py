# 27.8.2020
# Typing Test

import linecache
import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Test")

BG = pygame.image.load(os.path.join("assets", "bg.jpeg"))
main_font = pygame.font.Font("abeezee.ttf", 50)
text_font = pygame.font.Font("abeezee.ttf", 35)


FPS = 144
clock = pygame.time.Clock()


class Word(object):
    def __init__(self, text):
        self.text = text
        self.width, self.height = text_font.size(self.text)
        self.pos_x = 0
        self.pos_y = 0
        self.displayed = False
        self.highlight = False


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def get_words(quantity, words_number):
    word_list = []
    for i in range(quantity):
        rng = random.randint(1, words_number + 1)
        word = linecache.getline('words200.txt', rng).strip()
        if word == "" or word == "\\n":
            continue
        word_list.append(word)
    return word_list


def main():
    run = True
    click = False
    word_obj = []
    i = 0

    text = ''
    current_word = ''

    dur = 0
    wpm = 0
    correct_keyst = 0
    incorrect_keyst = 0

    clock_reg = 0
    label_font = pygame.font.Font("abeezee.ttf", 50)

    word_list = get_words(300, 200)

    # Makes every word in wordlist a object
    for word in word_list:
        word = Word(word)
        word_obj.append(word)

    def evaluate(current_word, text):
        print("evaluating, jk")

    def redraw_window():
        WIN.blit(BG, (0, 0))

        dur_label = label_font.render(f"{dur}", 1, (255, 255, 255))
        wpm_label = label_font.render(f"{wpm}", 1, (255, 255, 255))
        WIN.blit(dur_label, (30, 10))
        WIN.blit(wpm_label, (WIDTH - 100, 10))

        # BG for displayed words
        word_rect = pygame.Rect(200, 150, (WIDTH - 400), (HEIGHT - 400))
        pygame.draw.rect(WIN, (150, 150, 150), word_rect)

        # BG for typed words
        type_rect = pygame.Rect(200, 600, (WIDTH - 400), (HEIGHT - 800))
        pygame.draw.rect(WIN, (150, 150, 150), type_rect)

        # Typed text
        text_surface = text_font.render(text, True, (0, 0, 0))
        WIN.blit(text_surface, (250, 540))

        # Displayed words
        x, y = 210, 160
        i = 1
        while y < (HEIGHT - 300):
            while True:
                for word in word_obj:
                    if word.text == word_list[i]:
                        curr_word = word
                word_surface = text_font.render(curr_word.text, True, (0, 0, 0))
                WIN.blit(word_surface, (x, y))
                if x + curr_word.width > WIDTH - 400:
                    break
                x += curr_word.width + 40
                print(word.width)
                i += 1
            x = 210
            y += 50




        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        if len(word_list):
            current_word = word_list[i]
            i += 1

        if clock_reg == 0:
            pass
        else:
            if clock_reg % FPS == 0:
                dur += 1
        clock_reg += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    evaluate(current_word, text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode


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


def settings_menu():
    pass


def post_menu():
    pass


if __name__ == '__main__':
    main_menu()
    pygame.quit()
