import os

import pygame

RUNNER_GROWL = 'assets/sound_effects/monsters/runner_growl.wav'
WALKER_GROWL = 'assets/sound_effects/monsters/walker_growl.wav'


class Monster():
    def __init__(self, monster_type, facing_right, x, y, speed_multiplier):
        self.scale = 0.2
        self.x = x
        self.y = y
        self.original_y = y
        self.width = 194
        self.height = 379
        self.hitbox = pygame.Rect(self.x, self.y, self.width * self.scale, self.height * self.scale)
        self.dead = False
        self.facing_right = facing_right

        self.idle_sprite_index = 0
        self.idle_sprite_count = 4


        if monster_type == 'zombie1':
            self.points = 1
            self.armor = 0
            self.walking = True
            self.running = False
        elif monster_type == 'zombie2':
            self.points = 2
            self.armor = 0
            self.walking = False
            self.running = True
        else:
            self.points = 3
            self.armor = 1
            self.walking = False
            self.running = True

        self.idle_sprites = [self.__load_monster_sprite(monster_type, f'Idle{i}.png') for i in
                             range(1, self.idle_sprite_count + 1)]

        self.walk_speed = 4 * speed_multiplier
        self.walk_sprite_index = 0
        self.walk_sprite_count = 6
        self.walk_sprites = [self.__load_monster_sprite(monster_type, f'Walk{i}.png') for i in
                             range(1, self.walk_sprite_count + 1)]

        self.run_speed = 9 * speed_multiplier
        self.run_sprite_index = 0
        self.run_sprite_count = 10
        self.run_sprites = [self.__load_monster_sprite(monster_type, f'Run{i}.png') for i in
                            range(1, self.run_sprite_count + 1)]

        self.dying = False
        self.decay = 0
        self.decayed = False
        self.max_decay = 15
        self.dead = False
        self.dead_sprite_index = 0
        self.dead_sprite_count = 8
        self.dead_sprites = [self.__load_monster_sprite(monster_type, f'Dead{i}.png') for i in
                             range(1, self.dead_sprite_count + 1)]

        self.roaring = False

    def __load_monster_sprite(self, monster_type, filename):
        monster_image = pygame.image.load(os.path.join(f'assets/sprites/characters/{monster_type}', filename)).convert_alpha()
        return pygame.transform.scale(monster_image,
                                      (monster_image.get_width() * self.scale, monster_image.get_height() * self.scale))

    def draw(self, win):
        if self.dying:

            if self.dead_sprite_index < self.dead_sprite_count - 1:
                self.dead_sprite_index += 1
                # adjust y position so monster lies dead on the ground
                self.y += 6
            else:
                # adjust y position so monster lies dead on the ground
                self.y = self.original_y + 50
                self.dead = True
                self.decay += 1
                if self.decay > self.max_decay:
                    self.decayed = True

            if self.facing_right:
                dead_sprite = self.dead_sprites[self.dead_sprite_index]
            else:
                dead_sprite = pygame.transform.flip(self.dead_sprites[self.dead_sprite_index], True, False)

            win.blit(dead_sprite, (self.x, self.y))
        elif self.walking:
            self.walk_sprite_index += 1
            if self.walk_sprite_index >= self.walk_sprite_count:
                self.walk_sprite_index = 0

            if self.facing_right:
                self.x += self.walk_speed
                walk_sprite = self.walk_sprites[self.walk_sprite_index]
            else:
                self.x -= self.walk_speed
                walk_sprite = pygame.transform.flip(self.walk_sprites[self.walk_sprite_index], True, False)

            win.blit(walk_sprite, (self.x, self.y))
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
            if self.idle_sprite_index >= self.idle_sprite_count:
                self.idle_sprite_index = 0
            idle_sprite = pygame.transform.flip(self.idle_sprites[self.idle_sprite_index], True, False)
            win.blit(idle_sprite, (self.x, self.y))

        self.hitbox = pygame.Rect(self.x, self.y, self.width * self.scale, self.height * self.scale)
        # debug
        # pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.hitbox),  2)

    def collide(self, rect):
        if self.hitbox is None or rect is None:
            return False

        return self.hitbox.colliderect(rect)

    def play_sound_effects(self):
        if self.roaring:
            if self.walking:
                sound_effect = pygame.mixer.Sound(WALKER_GROWL)
            else:
                sound_effect = pygame.mixer.Sound(RUNNER_GROWL)

            sound_effect.set_volume(0.25)
            sound_effect.play()
            self.roaring = False
