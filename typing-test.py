# 27.8.2020
# Typing Test

import linecache
import random
import os
import pygame


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
        self.x = 0
        self.y = 0
        self.wrong = False
        self.current = False
        self.displayed = False


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def get_words(quantity, words_number):
    word_list = []
    for i in range(quantity):
        rng = random.randint(1, words_number + 1)
        word = linecache.getline('words200.txt', rng).strip()
        if word == "" or word == "\\n" or word in word_list:
            continue
        word = Word(word)
        word_list.append(word)
    return word_list


def word_setup(word_list):
    x, y = 220, 160
    for word in word_list:
        if x + word.width > WIDTH - 220:
            word.x = 220
            x = 220
            x += word.width + 35
            y += 62
            word.y = y
        else:
            word.x = x
            word.y = y
            x += word.width + 35


def line_change(word_list):
    # Moves the words up a line
    for word in word_list:
        word.y -= 62


def keystroke_validation(current_word, text):
    # Checks each keypress, if the key is correct
    text_lenght = len(text)
    curr_word_striped = current_word[:text_lenght]
    if text != curr_word_striped:
        return False


def main():
    run = True
    click = False
    word_list = []

    text = ''
    word_control = 0
    clock_reg = 0

    started = False
    curr_word_control = 0

    dur = 0
    wpm = 0
    time_left = 10
    corr_words = 0
    incorr_words = 0
    corr_keyst = 0
    incorr_keyst = 0
    total_keyst = 0

    word_list = get_words(300, 200)
    word_setup(word_list)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        dur_label = main_font.render(f"{time_left}", 1, (255, 255, 255))
        wpm_label = main_font.render(f"{int(wpm)}", 1, (255, 255, 255))
        WIN.blit(dur_label, (30, 10))
        WIN.blit(wpm_label, (WIDTH - 100, 10))

        # Temporary labels for (in)correct words
        corr_label = main_font.render(f"{corr_keyst}", 1, (255, 255, 255))
        incorr_label = main_font.render(f"{incorr_keyst}", 1, (255, 255, 255))
        WIN.blit(corr_label, (30, HEIGHT - 70))
        WIN.blit(incorr_label, (WIDTH - 100, HEIGHT - 70))

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
        for word in word_list:
            if 150 < word.y < 450:
                if word.current and word.wrong == False:
                    color = (255, 255, 255)
                elif word.wrong:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)
                word_surface = text_font.render(word.text, True, color)
                WIN.blit(word_surface, (word.x, word.y))

        # Typing line
        if current_word.wrong == False:
            typing_line_x = (current_word.x - 2) + text_surface.get_width()
            typing_line = pygame.Rect(typing_line_x, current_word.y, 2, 40)
            pygame.draw.rect(WIN, (255, 192, 84), typing_line)

        pygame.display.update()


    while run:
        clock.tick(FPS)

        for word in word_list:
            if word.current:
                word.current = False

        current_word = word_list[curr_word_control]
        current_word.current = True

        redraw_window()

        if current_word.y == 284:
            line_change(word_list)

        if time_left == 0:
            run = False
            post_game(wpm, corr_words, incorr_words, curr_word_control,
                corr_keyst, incorr_keyst, total_keyst)

        if started:
            if dur != 0:
                wpm = corr_words / (dur / 60)
            if clock_reg != 0:
                if clock_reg % FPS == 0:
                    dur += 1
                    time_left -= 1
            clock_reg += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Validation manipulation
                    if text == "":
                        break
                    elif current_word.text == text:
                        corr_words += 1
                    else:
                        incorr_words += 1
                        current_word.wrong = True
                    curr_word_control += 1
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    if keystroke_validation(current_word.text, text) == False:
                        current_word.wrong = True
                    else:
                        current_word.wrong = False
                else:
                    text += event.unicode
                    if started == False:
                        started = True
                    if keystroke_validation(current_word.text, text) == False:
                        incorr_keyst += 1
                        current_word.wrong = True
                    else:
                        current_word.wrong = False
                        corr_keyst += 1
                    total_keyst += 1


def post_game(wpm, corr_words, incorr_words, total_words,
    corr_keyst, incorr_keyst, total_keyst):
    run = True
    click = False

    while run:
        clock.tick(FPS)
        WIN.blit(BG, (0, 0))
        pos_x, pos_y = pygame.mouse.get_pos()

        # Words
        x = (WIDTH / 4) + 100
        y = (HEIGHT / 2)
        perc = corr_words * 100 / total_words
        label_words = main_font.render("Words", 1, (255, 255, 255))
        WIN.blit(label_words, (x - (label_words.get_width() / 2), y - 200))
        label_wpm = text_font.render(f"WPM: {int(wpm)}", 1, (255, 255, 255))
        WIN.blit(label_wpm, (x - (label_wpm.get_width() / 2), y - 100))
        label_perc = text_font.render(f"{int(perc)}%", 1, (255, 255, 255))
        WIN.blit(label_perc, (x - (label_perc.get_width() / 2), y - 40))

        # Keystrokes
        label_keystrokes = main_font.render("Keystrokes", 1, (255, 255, 255))
        WIN.blit(label_keystrokes, (((WIDTH / 4) * 3) - (label_words.get_width() / 2) - 100, HEIGHT / 2 - 200))

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
    run = True
    click = False

    while run:
        clock.tick(FPS)
        WIN.blit(BG, (0, 0))
        pos_x, pos_y = pygame.mouse.get_pos()

        # Menu Buttons
        button = pygame.Rect(
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


if __name__ == '__main__':
    main()
    pygame.quit()
