import random

from ammo import Ammo
from monster import Monster


class Game():
    def __init__(self, hero, hiscore):
        self.high_score = hiscore
        self.run = True
        self.paused = False
        self.started = False
        self.hero = hero
        self.zombies = []
        self.bullets = []

        self.ammo_boxes = []
        self.ammo_box_chance = [1, 350]  # there's a 1 in a 350 chance for ammo boxes to appear
        self.ammo_loot = [5, 15]  # players can get between 15 and 30 bullets in an ammo crate
        self.ammo_limit = 80  # ammo boxes will stop appearing if player is above this limit

        self.maximum_zombies = 5
        self.monster_types = ['zombie1', 'zombie2', 'zombie3']
        self.monster_type_weights = [0.5, 0.4, 0.1]

    def get_zombie_chance(self):
        if 0 <= self.hero.score < 20:
            return 50
        elif 20 <= self.hero.score < 30:
            return 40
        elif 30 <= self.hero.score < 50:
            return 30
        elif 50 <= self.hero.score < 70:
            return 15
        elif 70 <= self.hero.score < 80:
            return 10
        else:
            return 5

    def get_monster_speed_multiplier(self):
        if 0 <= self.hero.score < 20:
            return 0.8
        elif 20 <= self.hero.score < 30:
            return 0.9
        elif 30 <= self.hero.score < 50:
            return 1
        elif 50 <= self.hero.score < 70:
            return 1.1
        elif 70 <= self.hero.score < 80:
            return 1.2
        elif 80 <= self.hero.score < 90:
            return 1.3
        else:
            return 1.4

    def randomly_add_ammo_boxes(self, x_coords, y_coord):
        ammo_box_roll = random.randint(self.ammo_box_chance[0], self.ammo_box_chance[1])
        if ammo_box_roll == 1 and len(
                self.ammo_boxes) == 0 and not self.hero.dying and self.hero.bullets < self.ammo_limit:
            ammo_capacity = random.randint(self.ammo_loot[0], self.ammo_loot[1])
            ammo = Ammo(random.randint(x_coords[0], x_coords[1]), y_coord, ammo_capacity)
            self.ammo_boxes.append(ammo)

    def randomly_add_zombies(self, ltr_x_coord, ltr_y_coord, rtl_x_coord, rtl_y_coord):
        # add random zombies
        zombie_odds = self.get_zombie_chance()
        zombie_roll = random.randint(1, zombie_odds)
        if zombie_roll == 1 and len(self.zombies) < self.maximum_zombies:
            # randomise zombies
            monster_type = random.choices(self.monster_types, weights=self.monster_type_weights, k=1)[0]

            # randomise where the zombie is attacking from
            facing_right = bool(random.getrandbits(1))
            if facing_right:
                zombie = Monster(monster_type, True, ltr_x_coord, ltr_y_coord, self.get_monster_speed_multiplier())

            else:
                zombie = Monster(monster_type, False, rtl_x_coord, rtl_y_coord, self.get_monster_speed_multiplier())

            zombie.roaring = True

            self.zombies.append(zombie)

    def detect_if_hero_finds_ammo_box(self):
        for ammo_box in self.ammo_boxes:
            if self.hero.collide(ammo_box.hitbox):
                self.hero.bullets += ammo_box.capacity
                self.ammo_boxes.remove(ammo_box)

    def detect_if_bullets_hit_zombie(self):
        for bullet in self.bullets:
            for zombie in self.zombies:
                if zombie.dead:
                    continue

                if zombie.collide(bullet.hitbox):
                    # add to player score if zombie is not already dying or dead
                    if not zombie.dying and not zombie.dead:
                        self.hero.score += zombie.points

                    if zombie.armor > 0:
                        zombie.armor -= 1
                    else:
                        zombie.dying = True

                    if self.bullets.__contains__(bullet):
                        self.bullets.remove(bullet)
                    continue

    def detect_if_machete_hits_zombie(self):
        if self.hero.slashing:
            self.hero.slash_freeze = True
            for zombie in self.zombies:
                if zombie.dead:
                    continue

                if self.hero.facing_right:
                    melee_hitbox = self.hero.ltr_melee_hitbox
                else:
                    melee_hitbox = self.hero.rtl_melee_hitbox

                if zombie.collide(melee_hitbox):
                    # add to player score if zombie is not already dying or dead
                    if not zombie.dying and not zombie.dead:
                        self.hero.score += zombie.points

                    zombie.dying = True

                    continue

    def detect_if_monster_kills_hero(self):
        for zombie in self.zombies:
            if not zombie.dying and not self.hero.dying and self.hero.collide(zombie.hitbox):
                self.hero.dying = True
                self.hero.shooting = False
                self.hero.running = False
                self.hero.slashing = False

                return True

        return False

    def cleanup_dead_or_escaped_zombies(self, window_width):
        for zombie in self.zombies:
            # remove dead zombie bodies on the floor
            if zombie.decayed:
                self.zombies.remove(zombie)
            # remove zombies who have gone off the screen
            if zombie.x >= window_width or zombie.x <= 0:
                self.zombies.remove(zombie)

    def cleanup_bullets_that_missed(self, window_width):
        # remove bullets that have gone off the screen
        for bullet in self.bullets:
            if bullet.x >= window_width or bullet.x <= 0:
                self.bullets.remove(bullet)

    def prevent_hero_from_walking_off_the_screen(self, left_frame_offset, right_frame_offset, window_width):
        self.hero.x = max(left_frame_offset, min(self.hero.x, window_width - right_frame_offset))
