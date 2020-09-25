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

BG = pygame.image.load(os.path.join("assets", "bg2.jpeg"))
MAIN_FONT = pygame.font.Font("abeezee.ttf", 50)
TEXT_FONT = pygame.font.Font("abeezee.ttf", 35)

WHITE_C = (255, 255, 255)
ORANGE_C = (204, 102, 0)


FPS = 60
clock = pygame.time.Clock()


class Word(object):
    def __init__(self, text):
        self.text = text
        self.width, self.height = TEXT_FONT.size(self.text)
        self.x = 0
        self.y = 0
        self.wrong = False
        self.current = False
        self.displayed = False


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def get_words(quantity, words_number):
    word_list = []
    for _ in range(quantity):
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


def line_change(word_list): # Moves the words up a line
    for word in word_list:
        word.y -= 62


def keystroke_validation(current_word, text): # Checks if the key is correct
    text_lenght = len(text)
    curr_word_striped = current_word[:text_lenght]
    if text == curr_word_striped:
        return True


def main():
    run = True
    word_list = []

    text = ''
    clock_reg = 0

    started = False
    curr_word_control = 0

    dur = 0
    wpm = 0
    time_left = 10
    words_counter = [0, 0]
    keyst_counter = [0, 0, 0]

    word_list = get_words(300, 200)
    word_setup(word_list)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        x = WIDTH / 2
        y = 35
        dur_label = MAIN_FONT.render(f"{time_left}", 1, WHITE_C)
        WIN.blit(dur_label, (int(x - (dur_label.get_width() / 2)), y))

        # BG for displayed words
        word_rect = pygame.Rect(200, 150, (WIDTH - 400), (HEIGHT - 400))
        pygame.draw.rect(WIN, (150, 150, 150), word_rect)

        # BG for typed text
        type_rect = pygame.Rect(200, 600, (WIDTH - 400), (HEIGHT - 800))
        pygame.draw.rect(WIN, (150, 150, 150), type_rect)

        # Typed text
        text_surface = TEXT_FONT.render(text, True, (0, 0, 0))
        WIN.blit(text_surface, (((WIDTH / 2) - 50), 540))

        # Displayed words
        for word in word_list:
            if 150 < word.y < 450:
                if word.current and not word.wrong:
                    color = WHITE_C
                elif word.wrong:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)
                word_surface = TEXT_FONT.render(word.text, True, color)
                WIN.blit(word_surface, (word.x, word.y))

        # Typing line
        if not current_word.wrong:
            typing_line_x = (current_word.x - 2) + text_surface.get_width()
            typing_line = pygame.Rect(typing_line_x, current_word.y, 2, 40)
            pygame.draw.rect(WIN, ORANGE_C, typing_line)

        pygame.display.update()


    while run:
        clock.tick(FPS)

        # Gives current word
        word_list[curr_word_control - 1].current = False
        current_word = word_list[curr_word_control]
        current_word.current = True

        redraw_window()

        if current_word.y == 284:
            line_change(word_list)

        if time_left == 0:
            run = False
            post_game(wpm, words_counter,keyst_counter)

        if started:
            if dur != 0:
                wpm = words_counter[0] / (dur / FPS)
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
                    if current_word.text == text:
                        words_counter[0] += 1
                    elif text == "":
                        break
                    else:
                        words_counter[1] += 1
                        current_word.wrong = True
                    curr_word_control += 1
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    if not keystroke_validation(current_word.text, text):
                        current_word.wrong = True
                    else:
                        current_word.wrong = False
                else:
                    text += event.unicode
                    if not started:
                        started = True
                    if keystroke_validation(current_word.text, text):
                        keyst_counter[0] += 1
                        current_word.wrong = False
                    else:
                        current_word.wrong = True
                        keyst_counter[1] += 1
                    keyst_counter[2] += 1


def post_game(wpm, words_counter, keyst_counter):
    run = True
    click = False

    while run:
        clock.tick(FPS)
        WIN.blit(BG, (0, 0))
        pos_x, pos_y = pygame.mouse.get_pos()

        # WPM and percentage
        x = (WIDTH / 2)
        y = (HEIGHT / 4)
        perc = keyst_counter[0] * 100 / keyst_counter[2]
        label_wpm = MAIN_FONT.render(f"WPM: {int(wpm)}", 1, WHITE_C)
        WIN.blit(label_wpm, (x - (label_wpm.get_width() / 2), y))
        label_perc = MAIN_FONT.render(f"{int(perc)}%", 1, WHITE_C)
        WIN.blit(label_perc, (x - (label_perc.get_width() / 2), y + 70))

        # Words
        x = (WIDTH / 4) + 100
        y = (HEIGHT / 2)
        label_words = MAIN_FONT.render("Words", 1, WHITE_C)
        WIN.blit(label_words, (x - (label_words.get_width() / 2), y))

        word_line_rect = pygame.Rect(x - 150, y + 70, 300, 3)
        pygame.draw.rect(WIN, ORANGE_C, word_line_rect)

        label_corr_words = TEXT_FONT.render(f"Correct: {words_counter[0]}", 1, WHITE_C)
        WIN.blit(label_corr_words, (x - (label_corr_words.get_width() / 2), y + 80))
        label_incorr_words = TEXT_FONT.render(f"Incorrect: {words_counter[1]}", 1, WHITE_C)
        WIN.blit(label_incorr_words, (x - (label_incorr_words.get_width() / 2), y + 140))

        # Keystrokes
        x = (WIDTH / 4) * 3 - 100
        y = (HEIGHT / 2)
        label_keystrokes = MAIN_FONT.render("Keystrokes", 1, WHITE_C)
        WIN.blit(label_keystrokes, (x - (label_keystrokes.get_width() / 2), y))

        keyst_line_rect = pygame.Rect(x - 150, y + 70, 300, 3)
        pygame.draw.rect(WIN, ORANGE_C, keyst_line_rect)

        label_corr_words = TEXT_FONT.render(f"Correct: {keyst_counter[0]}", 1, WHITE_C)
        WIN.blit(label_corr_words, (x - (label_corr_words.get_width() / 2), y + 80))
        label_incorr_words = TEXT_FONT.render(f"Incorrect: {keyst_counter[1]}", 1, WHITE_C)
        WIN.blit(label_incorr_words, (x - (label_incorr_words.get_width() / 2), y + 140))

        # Restart button
        x = (WIDTH / 2)
        y = (HEIGHT - 120)
        button_restart = pygame.Rect(x - 160, y - 10, 320, 80)
        #pygame.draw.rect(WIN, ORANGE_C, button_restart)
        label_restart = MAIN_FONT.render("Restart", 1, WHITE_C)
        WIN.blit(label_restart, (x - (label_restart.get_width() / 2), y))

        pygame.display.update()

        if click:
            if button_restart.collidepoint((pos_x, pos_y)):
                run = False
                main()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    main()


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

        pygame.draw.rect(WIN, ORANGE_C, button_play)
        pygame.draw.rect(WIN, ORANGE_C, button_settings)

        # Menu Labels
        label_play = MAIN_FONT.render("Play", 1, WHITE_C)
        WIN.blit(label_play, ((WIDTH / 2) - 50, 275))

        label_settings = MAIN_FONT.render("Settings", 1, WHITE_C)
        WIN.blit(label_settings, ((WIDTH / 2) - 90, 370))

        # Button Activations
        if click:
            if button_play.collidepoint((pos_x, pos_y)):
                run = False
                main()
            # if button_settings.collidepoint((pos_x, pos_y)):
            #     run = False
            #     settings_menu()

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


# def settings_menu():
#     run = True
#     click = False

#     while run:
#         clock.tick(FPS)
#         WIN.blit(BG, (0, 0))
#         pos_x, pos_y = pygame.mouse.get_pos()

#         # Menu Buttons
#         button = pygame.Rect(
#             (WIDTH / 2) - 160, (HEIGHT / 2) - 100, 320, 80)
#         button_settings = pygame.Rect(
#             (WIDTH / 2) - 160, (HEIGHT / 2), 320, 80)

#         pygame.draw.rect(WIN, (50, 75, 50), button_play)
#         pygame.draw.rect(WIN, (50, 75, 50), button_settings)

#         # Menu Labels
#         label_play = MAIN_FONT.render("Play", 1, WHITE_C)
#         WIN.blit(label_play, ((WIDTH / 2) - 50, 275))

#         label_settings = MAIN_FONT.render("Settings", 1, WHITE_C)
#         WIN.blit(label_settings, ((WIDTH / 2) - 90, 370))

#         # Button Activations
#         if click:
#             if .collidepoint((pos_x, pos_y)):
#                 run = False
#                 main()

#             if button_settings.collidepoint((pos_x, pos_y)):
#                 run = False
#                 settings_menu()

#         pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
