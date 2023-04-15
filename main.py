import os
import random

import pygame

from bullet import Bullet
from game import Game
from high_score import read_high_score
from player import Player

pygame.init()

# Constants
BACKGROUND_MUSIC = 'assets/music/action.mp3'
GAME_FONT = "assets/fonts/AtariClassic.ttf"
GAME_OVER_SOUND_EFFECT = 'assets/sound_effects/game/game-over.wav'
GAME_START_SOUND_EFFECT = 'assets/sound_effects/game/coin.mp3'
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_SPEED = 5
BACKGROUND_SCROLLING = False
CLOCK_SPEED = 15
FONT_COLOUR_BLACK = (0, 0, 0)
FONT_COLOUR_WHITE = (255, 255, 255)
FONT_COLOUR_GRAY = (200, 200, 200)

# Coordinates
LTR_BULLET_X_OFFSET = 175
LTR_BULLET_Y_OFFSET = 102
RTL_BULLET_X_OFFSET = 100
RTL_BULLET_Y_OFFSET = 102
LTR_ZOMBIE_ATTACK_X_STARTING = 10
LTR_ZOMBIE_ATTACK_Y_STARTING = 443
RTL_ZOMBIE_ATTACK_X_STARTING = 750
RTL_ZOMBIE_ATTACK_Y_STARTING = 443
LEFT_FRAME_OFFSET = -40
RIGHT_FRAME_OFFSET = 200
AMMO_BOX_X = [40, 700]
AMMO_BOX_Y = 475
HERO_X = 200
HERO_Y = 390
BOSS_X = 10
BOSS_Y = 443

# Initialize window, background and default font
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Rambo')

background_list = ['forest.png']
background_filename = random.choice(background_list)

with open(os.path.join('assets/background', background_filename), 'rb') as f:
    background = pygame.image.load(f).convert()
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

with open(os.path.join('assets/background', 'cover.jpg'), 'rb') as f:
    cover = pygame.image.load(f).convert()
    cover = pygame.transform.scale(cover, (WINDOW_WIDTH, WINDOW_HEIGHT))

large_font = pygame.font.Font(GAME_FONT, 20)
small_font = pygame.font.Font(GAME_FONT, 18)

# Load background music
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(0.2)

# Initialize clock
clock = pygame.time.Clock()

# Initialise game state
high_score = read_high_score()
game = Game(Player(HERO_X, HERO_Y), high_score)


def play_start_game_sound():
    sound_effect = pygame.mixer.Sound(GAME_START_SOUND_EFFECT)
    sound_effect.set_volume(0.25)
    sound_effect.play()

    pygame.mixer.music.play(-1, 0, 3000)


def play_game_over_sound():
    sound_effect = pygame.mixer.Sound(GAME_OVER_SOUND_EFFECT)
    sound_effect.set_volume(1)
    sound_effect.play()

    pygame.mixer.music.fadeout(3000)


def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game.hero.dying:
                    game.hero.resurrect()
                    game.zombies = []
                    game.ammo_boxes = []
                if not game.started:
                    game.started = True

                play_start_game_sound()

            if not game.hero.dying and game.started:
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                elif event.key == pygame.K_3:
                    game.hero.gasping = True
                elif event.key == pygame.K_SPACE:
                    game.hero.jumping = True
                if event.key == pygame.K_RIGHT:
                    game.hero.running = True
                    game.hero.facing_right = True
                if event.key == pygame.K_LEFT:
                    game.hero.running = True
                    game.hero.facing_right = False
                if event.key == pygame.K_1:
                    if game.hero.bullets > 0 and not game.hero.slashing:
                        game.hero.shooting = True

                        if game.hero.facing_right:
                            bullet = Bullet(game.hero.facing_right, game.hero.x + LTR_BULLET_X_OFFSET,
                                            game.hero.y + LTR_BULLET_Y_OFFSET)
                        else:
                            bullet = Bullet(game.hero.facing_right, game.hero.x + RTL_BULLET_X_OFFSET,
                                            game.hero.y + RTL_BULLET_Y_OFFSET)

                        game.hero.bullets -= 1

                        game.bullets.append(bullet)
                if event.key == pygame.K_2:
                    if not game.hero.slash_freeze:
                        game.hero.slashing = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                game.hero.running = False
            if event.key == pygame.K_LEFT:
                game.hero.running = False


def update_game():
    game.randomly_add_ammo_boxes(AMMO_BOX_X, AMMO_BOX_Y)
    game.randomly_add_zombies(LTR_ZOMBIE_ATTACK_X_STARTING, LTR_ZOMBIE_ATTACK_Y_STARTING, RTL_ZOMBIE_ATTACK_X_STARTING,
                              RTL_ZOMBIE_ATTACK_Y_STARTING)

    game.prevent_hero_from_walking_off_the_screen(LEFT_FRAME_OFFSET, RIGHT_FRAME_OFFSET, WINDOW_WIDTH)

    game.detect_if_hero_finds_ammo_box()
    game.detect_if_bullets_hit_zombie()
    game.detect_if_machete_hits_zombie()

    if game.detect_if_monster_kills_hero():
        play_game_over_sound()

    game.cleanup_dead_or_escaped_zombies(WINDOW_WIDTH)
    game.cleanup_bullets_that_missed(WINDOW_WIDTH)


def draw():
    win.blit(background, (0, 0))
    game.hero.draw(win)

    for bullet in game.bullets:
        bullet.draw(win)

    for zombie in game.zombies:
        zombie.draw(win)

    for ammo_box in game.ammo_boxes:
        ammo_box.draw(win)

    draw_info()

    pygame.display.update()


def play_sound():
    game.hero.play_sound_effects()

    for zombie in game.zombies:
        zombie.play_sound_effects()


def draw_text(font, text, colour, x, y):
    img = font.render(text, True, colour)
    win.blit(img, (x, y))


def draw_info():
    # display bullets
    draw_text(large_font, 'AMMO', FONT_COLOUR_WHITE, 15, 15)
    draw_text(small_font, f'{game.hero.bullets:03}', FONT_COLOUR_GRAY, 20, 42)

    # display high score
    draw_text(large_font, f'HIGH SCORE', FONT_COLOUR_WHITE, WINDOW_WIDTH / 2 - 100, 15)
    draw_text(small_font, f'{game.high_score:03}', FONT_COLOUR_GRAY, WINDOW_WIDTH / 2 - 40, 42)

    # display score
    draw_text(large_font, 'SCORE', FONT_COLOUR_WHITE, WINDOW_WIDTH - 120, 15)
    draw_text(small_font, f'{game.hero.score:03}', FONT_COLOUR_GRAY, WINDOW_WIDTH - 100, 42)

    if game.hero.dying:
        draw_text(large_font, 'GAME OVER', FONT_COLOUR_WHITE, WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 100)
        draw_text(large_font, 'Press ENTER to play again', FONT_COLOUR_GRAY, WINDOW_WIDTH / 2 - 240, WINDOW_HEIGHT / 2)

    if not game.started:
        draw_text(large_font, 'Press ENTER to play', FONT_COLOUR_BLACK, WINDOW_WIDTH / 2 - 210, WINDOW_HEIGHT / 2)


while game.run:
    handle_input()

    if game.started:
        if game.paused:
            draw_text(large_font, 'PAUSED', FONT_COLOUR_WHITE, WINDOW_WIDTH / 2 - 80, WINDOW_HEIGHT / 2)
            pygame.display.update()
        else:
            update_game()
            draw()
            play_sound()
    else:
        # show game splash screen
        win.blit(cover, (0, 0))
        draw_info()
        pygame.display.update()

    clock.tick(CLOCK_SPEED)

pygame.mixer.music.stop()
pygame.quit()
