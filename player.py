import os

import pygame

HERO_GASP = 'assets/sound_effects/hero/gasp.wav'
MACHETE_SLASH = 'assets/sound_effects/machete/slash.wav'
GUN_SHOT = 'assets/sound_effects/gun_shots/single.mp3'


class Player():
    def __init__(self, x, y):
        self.bullets = 15
        self.score = 0
        self.hitbox = None
        self.ltr_melee_hitbox = None
        self.rtl_melee_hitbox = None
        self.scale = 4
        self.x = x
        self.y = y
        self.width = 256
        self.height = 128
        self.original_x = x
        self.original_y = y
        self.facing_right = True

        self.idle_sprite_index = 0
        self.idle_sprite_count = 4
        self.idle_sprites = [self.__load_player_sprite(f'rambo-idle-{i}.png') for i in range(0, self.idle_sprite_count)]

        self.run_speed = 10
        self.running = False
        self.run_sprite_index = 0
        self.run_sprite_count = 6
        self.run_sprites = [self.__load_player_sprite(f'rambo-run-{i}.png') for i in range(0, self.run_sprite_count)]

        self.dying = False
        self.die_sprite_index = 0
        self.die_sprite_count = 10
        self.die_sprites = [self.__load_player_sprite(f'rambo-death-{i}.png') for i in range(0, self.die_sprite_count)]

        self.shooting = False
        self.shoot_sprite_index = 0
        self.shoot_sprite_count = 5
        self.shoot_sprites = [self.__load_player_sprite(f'rambo-shoot-{i}.png') for i in
                              range(0, self.shoot_sprite_count)]

        self.slashing = False
        self.gasping = False
        self.slash_freeze_delay_limit = 8
        self.slash_freeze_delay = self.slash_freeze_delay_limit
        self.slash_freeze = False
        self.slash_sprite_index = 0
        self.slash_sprite_count = 3
        self.slash_sprites = [self.__load_player_sprite(f'rambo-slash-{i}.png') for i in
                              range(0, self.slash_sprite_count)]

        self.jumping = False
        self.jump_length = 20
        self.jump_sprite_index = 0
        self.jump_sprite_count = 5
        self.jump_list = [0, 15, 30, 15]
        self.jump_sprites = [self.__load_player_sprite(f'rambo-jump-{i}.png') for i in
                             range(0, self.jump_sprite_count)]

    def resurrect(self):
        self.bullets = 25
        self.score = 0
        self.idle_sprite_index = 0
        self.dying = False
        self.die_sprite_index = 0
        self.running = False
        self.jumping = False
        self.run_sprite_index = 0
        self.slashing = False
        self.shooting = False
        self.gasping = False
        self.shoot_sprite_index = 0
        self.x = self.original_x
        self.y = self.original_y
        self.facing_right = True

    def __load_player_sprite(self, filename):
        player_image = pygame.image.load(os.path.join('assets/sprites/characters/player', filename)).convert_alpha()
        return pygame.transform.scale(player_image,
                                      (player_image.get_width() * self.scale, player_image.get_height() * self.scale))

    def draw(self, win):
        if self.dying:
            self.running = False
            self.jumping = False
            self.slashing = False
            self.y = self.original_y
            if self.die_sprite_index < self.die_sprite_count - 1:
                self.die_sprite_index += 1

            if self.facing_right:
                die_sprite = self.die_sprites[self.die_sprite_index]
            else:
                die_sprite = pygame.transform.flip(self.die_sprites[self.die_sprite_index], True, False)

            win.blit(die_sprite, (self.x, self.y))
        elif self.jumping:
            if self.jump_sprite_index < self.jump_sprite_count - 1:
                self.y = self.original_y - self.jump_list[self.jump_sprite_index]
                self.jump_sprite_index += 1
                if (self.facing_right):
                    self.x += self.jump_length
                else:
                    self.x -= self.jump_length
            else:
                self.jump_sprite_index = 0
                self.y = self.original_y
                self.jumping = False

            if self.facing_right:
                jump_sprite = self.jump_sprites[self.jump_sprite_index]
            else:
                jump_sprite = pygame.transform.flip(self.jump_sprites[self.jump_sprite_index], True, False)

            win.blit(jump_sprite, (self.x, self.y))

        elif self.shooting:
            if self.shoot_sprite_index < self.shoot_sprite_count - 1:
                self.shoot_sprite_index += 1
            else:
                self.shoot_sprite_index = 0
                self.shooting = False

            if self.facing_right:
                shoot_sprite = self.shoot_sprites[self.shoot_sprite_index]
            else:
                shoot_sprite = pygame.transform.flip(self.shoot_sprites[self.shoot_sprite_index], True, False)

            win.blit(shoot_sprite, (self.x, self.y))

        elif self.slashing:
            if self.slash_sprite_index < self.slash_sprite_count - 1:
                self.slash_sprite_index += 1
            else:
                self.slash_sprite_index = 0
                self.slashing = False
            if self.facing_right:
                slash_sprite = self.slash_sprites[self.slash_sprite_index]
            else:
                slash_sprite = pygame.transform.flip(self.slash_sprites[self.slash_sprite_index], True, False)
            win.blit(slash_sprite, (self.x, self.y))

        elif self.running:
            self.run_sprite_index += 1
            if self.run_sprite_index >= self.run_sprite_count:
                self.run_sprite_index = 0

            if self.facing_right:
                self.x += self.run_speed
                run_sprite = self.run_sprites[self.run_sprite_index]
            else:
                self.x -= self.run_speed
                run_sprite = pygame.transform.flip(self.run_sprites[self.run_sprite_index], True, False)

            win.blit(run_sprite, (self.x, self.y))

        else:
            self.idle_sprite_index += 1

            if self.slash_freeze:
                self.slash_freeze_delay -= 1
                if self.slash_freeze_delay <= 0:
                    self.slash_freeze_delay = self.slash_freeze_delay_limit
                    self.slash_freeze = False

            if self.idle_sprite_index >= self.idle_sprite_count:
                self.idle_sprite_index = 0

            if self.facing_right:
                idle_sprite = self.idle_sprites[self.idle_sprite_index]
            else:
                idle_sprite = pygame.transform.flip(self.idle_sprites[self.idle_sprite_index], True, False)

            win.blit(idle_sprite, (self.x, self.y))

        self.hitbox = pygame.Rect(self.x + 100, self.y + 55, self.width - 200, self.height - 50)
        self.ltr_melee_hitbox = pygame.Rect(self.x + 140, self.y + 55, self.width - 205, self.height - 50)
        self.rtl_melee_hitbox = pygame.Rect(self.x + 65, self.y + 55, self.width - 205, self.height - 50)

        # debug
        # pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.rtl_melee_hitbox),  2)

    def collide(self, rect):
        if self.hitbox is None or rect is None:
            return False

        return self.hitbox.colliderect(rect)
    def play_sound_effects(self):
        if self.shooting:
            sound_effect = pygame.mixer.Sound(GUN_SHOT)
            sound_effect.set_volume(0.5)
            sound_effect.play()
        if self.slashing:
            sound_effect = pygame.mixer.Sound(MACHETE_SLASH)
            sound_effect.set_volume(1)
            sound_effect.play()
        if self.gasping:
            sound_effect = pygame.mixer.Sound(HERO_GASP)
            sound_effect.set_volume(1)
            sound_effect.play()
            self.gasping = False