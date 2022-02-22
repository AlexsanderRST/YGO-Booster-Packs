"""
Created by Alexsander Rosante 2021
Github: https://github.com/AlexsanderRST
"""


from urllib import request, error
from pygame.locals import *


import json
import math
import random
import pygame

pygame.init()

info_sample = {'name': (),
               'cover': '',
               '#cards': 9,
               'head height': 20,
               'rarity pos': 'middle',
               'Common': (),
               'Rare': (),
               'Super Rare': (),
               'Ultra Rare': (),
               '%R': 1, '%SR': 5, '%UR': 12}


def cursor_by_context():
    if len(hovered):
        pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)


def draw_gradient_pattern(surface: pygame.Surface, rows: int, cols: int, spaccing=3, padx=5, pady=5,
                          color_0=(180, 180, 180), color_f=(150, 150, 150), vertical=False):
    rect_width = (surface.get_width() - padx * 2 - spaccing * (cols - 1)) / cols
    rect_height = (surface.get_height() - pady * 2 - spaccing * (rows - 1)) / rows
    color_r_speed = round((color_f[0] - color_0[0]) / rows) if vertical else round((color_f[0] - color_0[0]) / cols)
    color_g_speed = round((color_f[1] - color_0[1]) / rows) if vertical else round((color_f[1] - color_0[1]) / cols)
    color_b_speed = round((color_f[2] - color_0[2]) / rows) if vertical else round((color_f[2] - color_0[2]) / cols)
    color = list(color_0)
    for row in range(rows):
        for col in range(cols):
            left = (rect_width + spaccing) * col + padx
            top = (rect_height + spaccing) * row + pady
            pygame.draw.rect(surface, color, [left, top, rect_width, rect_height])
            color = get_next_color(color, color_r_speed, color_g_speed, color_b_speed) if not vertical else color
        color = get_next_color(color, color_r_speed, color_g_speed, color_b_speed) if vertical else color_0


def get_next_color(color, r_speed, g_speed, b_speed):
    next_color = [color[0] + r_speed, color[1] + g_speed, color[2] + b_speed]
    for i, ch in enumerate(next_color):
        if ch < 0:
            next_color[i] = 0
        elif ch > 255:
            next_color[i] = 255
    return next_color


def download_packs_info():
    url = 'https://raw.githubusercontent.com/AlexsanderRST/EDOPro-Booster-Packs/main/BoosterPacks.json'
    try:
        request.urlretrieve(url, 'BoosterPacks.json')
        with open('BoosterPacks.json', 'r') as fp:
            return json.load(fp)
    except error.URLError:
        game.leave()


# OBJECTS
class BoosterPack(pygame.sprite.Group):
    def __init__(self, code, init_mode='unpack'):
        super().__init__()
        # properties
        self.code = code
        self.info = packs_info[code]
        self.width, self.height = 290, 530
        self.head_height = self.info['head height']
        self.openning = False

        # surface
        surface = self.get_surface()

        # head
        self.head = pygame.sprite.Sprite()
        self.head.image = pygame.Surface((self.width, self.head_height), SRCALPHA)
        self.head.image.blit(surface, (0, 0))
        self.head.rect = self.head.image.get_rect()

        # body
        self.body = pygame.sprite.Sprite()
        self.body.image = pygame.Surface((self.width, self.height - self.head_height), SRCALPHA)
        self.body.image.blit(surface, (0, -self.head_height))
        self.body.rect = self.body.image.get_rect()

        # positioning
        self.rect = pygame.Rect(0, 0, self.body.rect.w, self.body.rect.h + self.head.rect.h)
        self.rect.center = display_w / 2, display_h / 2
        self.head.rect.topleft = self.rect.topleft
        self.body.rect.topleft = self.head.rect.bottomleft
        self.body_pos = pygame.math.Vector2(self.body.rect.center)

        # preview
        self.preview = pygame.sprite.Sprite()
        self.preview.image = pygame.transform.smoothscale(
            surface.copy(), (round(self.width * 0.75), round(self.height * 0.75)))
        self.preview.rect = self.preview.image.get_rect()

        # miniature
        self.mini = pygame.sprite.Sprite()
        self.mini.image = pygame.transform.smoothscale(
            surface.copy(), (round(self.width * 0.2), round(self.height * 0.2)))
        self.mini.rect = self.mini.image.get_rect()
        pygame.draw.rect(self.mini.image, 'darkgray', [0, 0, *self.mini.rect.size], width=1)

        self.set_mode(init_mode)

    @staticmethod
    def get_cropped_art(card_id):
        pic = pygame.image.load(f'pics/{card_id}.jpg').convert()
        pic = pygame.transform.smoothscale(pic.copy(), (421, 614))
        art = pygame.Surface((323, 323))
        art.blit(pic, (-48, -110))
        return art

    def get_surface(self):
        try:
            surface = pygame.image.load(f'pics/booster/{self.code}.png').convert_alpha()
        except FileNotFoundError:
            # presets
            self.head_height = 40
            surface = pygame.Surface((self.width, self.height))
            hole_r = 14

            # head and bottom
            head = pygame.Surface((self.width, self.head_height))
            head.fill((192, 192, 192))
            draw_gradient_pattern(head, 4, 30)
            bottom = head.copy()
            pygame.draw.ellipse(
                head, 'pink', [head.get_width() / 2 - hole_r, head.get_height() / 2 - hole_r, hole_r * 2, hole_r * 2])
            head.set_colorkey('pink')
            surface.blit(head, (0, 0))
            surface.blit(bottom, (0, self.height - bottom.get_height()))

            # body
            body_height = self.height - self.head_height * 2
            body = self.get_cropped_art(self.info['cover'])
            body = pygame.transform.smoothscale(body.copy(), (body_height, body_height))

            # body shadow
            shadow = pygame.Surface((self.width, round(self.head_height / 5)))
            shadow.set_alpha(120)
            body.blit(shadow, (shadow.get_width() / 2, 0))
            body.blit(shadow, (shadow.get_width() / 2, body_height - shadow.get_height()))

            # body reflex
            reflex = pygame.image.load('textures/mask.png').convert_alpha()
            reflex = pygame.transform.scale(reflex, (self.height, self.height))
            reflex = pygame.transform.flip(reflex, True, False)
            reflex.set_alpha(180)
            body.blit(reflex, (30, 0))

            surface.blit(body, (-surface.get_width() / 2, self.head_height))

            # name
            font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 25)
            last_bottom = 2 / 3 * surface.get_height()
            for i in self.info['name']:
                text = font.render(i, True, Color('white'), Color('black'))
                text_rect = text.get_rect(midtop=(surface.get_width() / 2, last_bottom))
                surface.blit(text, text_rect)
                last_bottom = text_rect.bottom

        return surface

    def hovered(self, event_pos):
        if self.mini.rect.collidepoint(event_pos):
            return True
        return False

    def set_mode(self, mode):
        self.empty()
        if mode == 'unpack':
            self.add(self.head, self.body)
        elif mode == 'preview':
            self.add(self.preview)
        elif mode == 'mini':
            self.add(self.mini)

    def unpack(self, speed=18):
        head_width = self.head.image.get_width() - speed
        if head_width <= 0:
            self.remove(self.head)
            if self.body.rect.top <= display_h:
                self.body_pos.y += speed
                self.body.rect.center = self.body_pos.xy
            else:
                game.screen.open_pack = True
        else:
            self.head.image = pygame.transform.scale(
                self.head.image.copy(), (head_width, self.head.image.get_height()))
            self.head.rect = self.head.image.get_rect(bottomright=self.body.rect.topright)

    def draw(self, surface):
        super().draw(surface)

    def update(self):
        self.body_pos = pygame.math.Vector2(self.body.rect.center)
        if self.openning:
            self.unpack()
        else:
            self.head.rect.topleft = self.rect.topleft
            self.body.rect.topleft = self.head.rect.bottomleft
        super().update()


class Card(pygame.sprite.Sprite):
    def __init__(self, card_id, pack_info):
        super().__init__()
        # properties
        self.id = card_id
        self.rarity = self.get_rarity(pack_info)
        self.width, self.height = 288, 420

        # surf
        self.pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        self.pic = pygame.transform.smoothscale(self.pic.convert(), (self.width, self.height))
        self.image = self.pic.copy()

        # motion
        self.rect = self.image.get_rect()
        self.pos = self.rect.center
        self.vel = pygame.math.Vector2()
        self.anim = self.idle

        # effecs
        self.label = self.Label(self.rarity)
        self.label.rect.topright = self.rect.topright

        # rarity effect
        match self.rarity:
            case 'Rare':
                self.rarity_effect = self.ROverlay(self.image)
            case 'Super Rare':
                self.rarity_effect = self.SROverlay(self.image)
            case 'Ultra Rare':
                self.rarity_effect = self.UROverlay(self.image)
            case _:
                self.rarity_effect = self.Overlay(self.image)

    def idle(self):
        pass

    def get_rarity(self, pack_info):
        for rarity in ('Common', 'Rare', 'Super Rare', 'Ultra Rare'):
            if self.id in pack_info[rarity]:
                return rarity

    def move_to_back(self, speed=20.):
        cards = game.screen.cards
        if self == cards.get_top_sprite():
            if self.rect.left < display_w / 2 + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = display_w / 2 + self.width / 2
                self.vel.x = 0.
                cards.move_to_back(self)
        else:
            if self.rect.centerx > display_w / 2:
                self.vel.x = -speed
            else:
                self.rect.centerx = display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.screen.card_moving = False

    def move_to_front(self, speed=20.):
        cards = game.screen.cards
        if self == game.screen.get_bottom_card():
            if self.rect.left < display_w / 2 + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = display_w / 2 + self.width / 2
                self.vel.x = 0.
                cards.move_to_front(self)
        else:
            if self.rect.centerx > display_w / 2:
                self.vel.x = -speed
            else:
                self.rect.centerx = display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.screen.card_moving = False

    def redraw(self):
        self.image = self.pic.copy()
        self.rarity_effect.apply(self.image)
        pygame.sprite.GroupSingle(self.label).draw(self.image)

    def update(self):
        self.redraw()
        self.pos = self.rect.center
        self.pos += self.vel
        self.rect.center = self.pos
        self.anim()

    class Label(pygame.sprite.Sprite):
        def __init__(self, rarity):
            super().__init__()
            try:
                self.image = pygame.image.load(f'pics/booster/{rarity}.png').convert_alpha()
            except FileNotFoundError:
                self.image = pygame.Surface((83, 21))
                image_center = self.image.get_width() / 2, self.image.get_height() / 2
                font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 18)
                font.set_bold(True)
                match rarity:
                    case 'Rare':
                        symbol, color = 'R', '#307cf3'
                    case 'Super Rare':
                        symbol, color = 'SR', '#f8d100'
                    case 'Ultra Rare':
                        symbol, color = 'UR', '#0de6ea'
                    case _:
                        symbol, color = 'N', '#b6c8cb'
                self.image.fill(color)
                text = font.render(symbol, True, 'white', color)
                text_rect = text.get_rect(center=image_center)
                self.image.blit(text, text_rect)
            self.rect = self.image.get_rect()

    class Overlay:
        def __init__(self, card_surf: pygame.Surface):
            self.surf = card_surf

        def apply(self, *args):
            pass

    class ROverlay(Overlay):
        def __init__(self, card_surf: pygame.Surface):
            super().__init__(card_surf)
            self.mask = pygame.image.load('textures/mask.png').convert_alpha()
            self.mask = pygame.transform.smoothscale(self.mask, 2 * [self.surf.get_height()])
            self.mask_end_x = self.surf.get_width() * 3
            self.mask_start_x = - self.mask_end_x
            self.mask_rect = self.mask.get_rect(left=self.mask_start_x)
            self.mask_pos = pygame.math.Vector2(self.mask_rect.center)
            self.mask_speed = 10

        def apply(self, surface: pygame.Surface):
            self.mask_pos = pygame.math.Vector2(self.mask_rect.center)
            self.mask_pos.x += self.mask_speed
            if self.mask_pos.x > self.mask_end_x:
                self.mask_pos.x = self.mask_start_x
            self.mask_rect.center = self.mask_pos.xy
            surface.blit(self.mask, self.mask_rect)

    class SROverlay(Overlay):
        def __init__(self, card_surf: pygame.Surface):
            super().__init__(card_surf)
            # mask
            self.mask = pygame.Surface(card_surf.get_size(), SRCALPHA)
            self.mask_rect = self.mask.get_rect()
            pygame.draw.rect(self.mask, '#f8d100', self.mask_rect, width=10)
            self.mask.set_alpha(50)
            self.mask_alpha_speed = 1
            self.mask_alpha_max = 128
            self.mask_alpha_min = 64

            # particles
            self.particles = pygame.sprite.Group()
            self.particle_max = 20

        def set_mask_alpha(self):
            mask_alpha = self.mask.get_alpha()
            mask_alpha += self.mask_alpha_speed
            if mask_alpha > self.mask_alpha_max:
                mask_alpha = self.mask_alpha_max
                self.mask_alpha_speed *= -1
            elif mask_alpha < self.mask_alpha_min:
                mask_alpha = self.mask_alpha_min
                self.mask_alpha_speed *= -1
            self.mask.set_alpha(round(mask_alpha))

        def update_particles(self):
            if len(self.particles.sprites()) < self.particle_max:
                particle = Particle(4, '#f8d100')
                particle.rect.centerx = random.randint(0, self.mask.get_width())
                particle.rect.centery = random.randint(0, self.mask.get_height())
                self.particles.add(particle)
            self.particles.update()

        def apply(self, surface: pygame.Surface):
            self.set_mask_alpha()
            self.update_particles()
            surface.blit(self.mask, self.mask_rect)
            self.particles.draw(surface)

    class UROverlay(Overlay):
        def __init__(self, card_surf: pygame.Surface):
            super().__init__(card_surf)
            self.colors = ('#f664ed', '#6b6efe', '#0fe4eb', '#05bb41')

            # mask
            self.mask = pygame.Surface(card_surf.get_size(), SRCALPHA)
            self.mask_rect = self.mask.get_rect()
            pygame.draw.rect(self.mask, random.choice(self.colors), self.mask_rect, width=10)
            self.mask.set_alpha(50)
            self.mask_alpha_speed = 2.2
            self.mask_alpha_max = 128
            self.mask_alpha_min = 0

            # particles
            self.particles = pygame.sprite.Group()
            self.particle_max = 30

        def set_mask_alpha(self):
            mask_alpha = self.mask.get_alpha()
            mask_alpha += self.mask_alpha_speed
            if mask_alpha > self.mask_alpha_max:
                mask_alpha = self.mask_alpha_max
                self.mask_alpha_speed *= -1
            elif mask_alpha < self.mask_alpha_min:
                mask_alpha = self.mask_alpha_min
                self.mask_alpha_speed *= -1
                self.mask = pygame.Surface(self.mask.get_size(), SRCALPHA)
                pygame.draw.rect(self.mask, random.choice(self.colors), self.mask_rect, width=10)
            self.mask.set_alpha(round(mask_alpha))

        @staticmethod
        def particle_a():
            return 4, 'white'

        def particle_b(self):
            return random.randint(10, 20), random.choice(self.colors)

        def update_particles(self):
            if len(self.particles.sprites()) < self.particle_max:
                size, color = random.choice([self.particle_a, self.particle_b])()
                particle = Particle(size, color)
                particle.rect.centerx = random.randint(0, self.mask.get_width())
                particle.rect.centery = random.randint(0, self.mask.get_height())
                self.particles.add(particle)
            self.particles.update()

        def apply(self, surface: pygame.Surface):
            self.set_mask_alpha()
            self.update_particles()
            surface.blit(self.mask, self.mask_rect)
            self.particles.draw(surface)


class Particle(pygame.sprite.Sprite):
    def __init__(self, size, color='white', start_alpha=128):
        super().__init__()
        self.alpha_speed = 5.0
        self.image = pygame.Surface(2 * [size], SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, color, self.rect)
        self.image.set_alpha(start_alpha)

    def update(self):
        alpha = self.image.get_alpha()
        alpha -= self.alpha_speed
        if alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(alpha)


# SCREENS
class DetailScreen:
    def __init__(self, card_id):
        card = pygame.sprite.Sprite()
        card.image = pygame.image.load(f'pics/{card_id}.jpg')
        card_w, card_h = card.image.get_size()
        card.image = pygame.transform.smoothscale(card.image, (624, round(card_h / card_w * 624)))
        card.rect = card.image.get_rect(midbottom=(512, 500))
        self.card = pygame.sprite.GroupSingle(card)

    def draw(self, surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.card.draw(surface)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()

    @staticmethod
    def quit():
        game.screen = game.screens['unpack']

    def update(self):
        self.event_check()
        self.card.update()


class SelectionScreen:
    def __init__(self):
        # setup
        self.spaccing = 7
        self.preview_bg_w = round(0.213 * display_w) + 2 * self.spaccing

        # sample pack
        pack = BoosterPack('LOB')

        # preview bg
        self.preview_bg = pygame.Surface((self.preview_bg_w, display_h))
        self.preview_bg.set_alpha(128)

        # calculates the number of packs per row and col
        selection_w = display_w - self.preview_bg_w
        self.cols = int((selection_w + self.spaccing) / (pack.mini.rect.w + self.spaccing))
        self.rows = int((display_h + self.spaccing) / (pack.mini.rect.h + self.spaccing)) - 1

        # calculates the margin x and y
        self.margin_x = (selection_w - (pack.mini.rect.w * self.cols + self.spaccing * (self.cols - 1))) / 2
        self.margin_y = (display_h - (pack.mini.rect.h * self.rows + self.spaccing * (self.rows - 1))) / 2

        # pages
        self.pages = {}
        self.cur_page = 0
        self.set_pages(list(packs_info.keys()))

        # preview image
        preview = pygame.sprite.Sprite()
        preview.image = pygame.Surface(pack.preview.image.get_size())
        preview.rect = preview.image.get_rect(midtop=(self.preview_bg_w / 2, self.spaccing))
        self.preview_image = pygame.sprite.GroupSingle(preview)

        # preview description
        preview_text_w = self.preview_bg.get_width()
        preview_text_h = display_h - preview.image.get_height()
        self.description = pygame.Surface((preview_text_w, preview_text_h), SRCALPHA)
        self.description_rect = self.description.get_rect(top=preview.rect.bottom)

    def check_events(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.switch_previous_page()
                elif event.button == 5:
                    self.switch_next_page()
                elif event.button == 1:
                    for pack in self.pages[self.cur_page]:
                        if pack.hovered(event.pos):
                            game.screens['unpack'] = UnpackScreen(pack.code)
                            game.screen = game.screens['unpack']
                            pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)

    def check_pack_hovered(self):
        global hovered
        for pack in self.pages[self.cur_page]:
            if pack.hovered(pygame.mouse.get_pos()):
                self.preview_image.sprite.image = pack.preview.image
                self.set_description(pack)
                hovered.add(pack)
            else:
                hovered.remove(pack)

    def get_pages(self, packs):
        """Gets a page configuration list from a packs list"""
        pages = []
        packs_per_page = self.rows * self.cols
        n_pages = math.ceil(len(packs) / packs_per_page)
        for i in range(n_pages):
            page = []
            for j in range(self.rows):
                page.append(
                    packs[i * packs_per_page: (i + 1) * packs_per_page][j * self.cols: (j + 1) * self.cols])
            pages.append(page)
        return pages

    @staticmethod
    def get_page_packs(page):
        return [pack for row in page for pack in row]

    def set_description(self, pack, space=10):
        self.description = pygame.Surface(self.description.get_size(), SRCALPHA)
        font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 13)
        last_bottom = space
        rarity = [len(pack.info[i]) for i in ('Common', 'Rare', 'Super Rare', 'Ultra Rare')]
        probability = [pack.info[i] for i in ('%R', '%SR', '%UR')]
        for i in (f'{pack.info["description"]}',
                  f'Release: {pack.info["release"]}',
                  f'Cards per pack: {pack.info["#cards"]}',
                  f'Common: {rarity[0]}',
                  f'Rare: {rarity[1]} (1:{probability[0]})',
                  f'Super Rare: {rarity[2]} (1:{probability[1]})',
                  f'Ultra Rare: {rarity[3]} (1:{probability[2]})',
                  f'Total: {sum(rarity)}'):
            text = font.render(i, True, (255, 255, 255))
            text_rect = text.get_rect(topleft=(space, last_bottom))
            self.description.blit(text, text_rect)
            last_bottom = text_rect.bottom

    def set_pages(self, packs):
        """Creates a dict with all packs in position"""
        pack = BoosterPack('LOB')
        for i, page in enumerate(self.get_pages(packs)):
            pack_sprites = self.Packs()
            last_bottom = self.margin_y
            for row in page:
                last_right = self.preview_bg_w + self.margin_x
                for pack_code in row:
                    pack = BoosterPack(pack_code, init_mode='mini')
                    pack.mini.rect.topleft = last_right, last_bottom
                    pack_sprites.add(pack)
                    last_right = pack.mini.rect.right + self.spaccing
                last_bottom = pack.mini.rect.bottom + self.spaccing
            self.pages[i] = pack_sprites

    def switch_next_page(self):
        if self.cur_page < len(self.pages):
            self.cur_page += 1

    def switch_previous_page(self):
        if self.cur_page > 0:
            self.cur_page -= 1

    def draw(self, surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.pages[self.cur_page].draw(surface)
        surface.blit(self.preview_bg, (0, 0))
        self.preview_image.draw(surface)
        surface.blit(self.description, self.description_rect)

    def update(self):
        cursor_by_context()
        self.check_events()
        self.check_pack_hovered()
        self.pages[self.cur_page].update()
        self.preview_image.update()

    class Packs(list):
        def add(self, pack: BoosterPack):
            self.append(pack)

        def draw(self, surface: pygame.Surface):
            for pack in self:
                pack.draw(surface)

        def update(self):
            for pack in self:
                pack.update()


class UnpackScreen:
    def __init__(self, current_pack):
        pack = packs_info[current_pack]
        self.pack = BoosterPack(current_pack)
        self.cards = pygame.sprite.LayeredUpdates()
        self.generate_pack(pack)
        self.card_moving = False
        self.open_pack = False
        self.rarity_viewed = False

        # counter
        self.counter = 1
        self.card_midbottom = self.cards.sprites()[0].rect.midbottom

        # font
        self.font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 18)
        self.font.set_bold(True)

        # detail button
        self.detail_button = pygame.Rect(376, 320, 271, 180)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False

            # Mouse input
            elif event.type == MOUSEBUTTONDOWN:
                if not self.open_pack:
                    if event.button in (1, 3) and not self.pack.openning:
                        self.pack.openning = True
                        sfx_open_pack.play()
                else:
                    card = self.cards.sprites()[0]
                    if event.button == 1:
                        if card.rect.collidepoint(event.pos):
                            self.switch_next_card()
                        else:
                            game.screens['unpack'] = UnpackScreen(self.pack.code)
                            game.screen = game.screens['unpack']
                    elif event.button == 2:
                        if self.detail_button.collidepoint(event.pos):
                            game.screens['detail'] = DetailScreen(self.get_top_card().id)
                            game.screen = game.screens['detail']
                    elif event.button == 3:
                        if card.rect.collidepoint(event.pos):
                            self.switch_previous_card()
                        else:
                            game.screen = game.screens['choose']

            # keyboard input
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.screen = game.screens['choose']

    def generate_pack(self, info):
        self.cards.empty()

        # Fill with common cards
        cards = [random.choice(info['Common']) for _ in range(info['#cards'] - 1)]

        # Get the rare card
        rarity = {'Super Rare': info['%SR'], 'Ultra Rare': info['%UR']}
        probability = [i for i in list(rarity.values()) if i > 0]
        avaible_rarity = [i for i in rarity if rarity[i] > 0]
        lcm = math.lcm(*probability)
        lst = []
        for i in avaible_rarity:
            for j in range(int(lcm / rarity[i])):
                lst.append(random.choice(info[i]))
        lst.extend([random.choice(info['Rare']) for _ in range(lcm - len(lst))])  # if 0 Rares?
        random.shuffle(lst)
        picked_rare = random.choice(lst)

        # Rarity pos
        if info['rarity pos'] == 'middle':
            cards.insert(info['#cards'] // 2, picked_rare)
        else:
            cards.insert(0, picked_rare)

        # Put cards into pack:
        for index, card_id in enumerate(cards):
            card = Card(card_id, info)
            card.rect.center = display_w / 2, display_h / 2
            self.cards.add(card)
            self.cards.change_layer(card, index)

        # purchase cards
        game.purchase += cards

    def get_bottom_card(self):
        bottom_card, bottom_layer = None, 5
        for card in self.cards:
            if card.layer < bottom_layer:
                bottom_layer = card.layer
                bottom_card = card
        return bottom_card

    def get_next_card_rarity(self, card):
        cards = self.cards.sprites()
        return cards[cards.index(card) - 1].rarity

    def get_switch_card_sound(self, rarity=''):
        if self.rarity_viewed:
            return sfx_next_card
        match rarity:
            case 'Super Rare':
                self.rarity_viewed = True
                return sfx_next_srcard
            case 'Ultra Rare':
                self.rarity_viewed = True
                return sfx_next_urcard
            case _:
                return sfx_next_card

    def get_top_card(self):
        return self.cards.get_top_sprite()

    def switch_next_card(self):
        if not self.card_moving:
            card = self.get_top_card()
            self.get_next_card_rarity(card)
            card.anim = card.move_to_back
            self.get_switch_card_sound(self.get_next_card_rarity(card)).play()
            self.counter += 1
            if self.counter > len(self.cards):
                self.counter = 1
            self.card_moving = True

    def switch_previous_card(self):
        if not self.card_moving:
            card = self.get_bottom_card()
            card.anim = card.move_to_front
            sfx_next_card.play()
            self.counter -= 1
            if self.counter < 1:
                self.counter = len(self.cards)
            self.card_moving = True

    def draw(self, surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.cards.draw(surface)

        # counter
        counter = self.font.render(f'({self.counter}/{len(self.cards)})', True, Color('white'))
        counter_rect = counter.get_rect(midtop=(self.card_midbottom[0] + 13, self.card_midbottom[1]))
        surface.blit(counter, counter_rect)

        self.pack.draw(surface)

    def update(self):
        self.event_check()
        if self.open_pack:
            self.cards.update()
        else:
            self.pack.update()


# APP
class Game:
    def __init__(self):
        # display
        self.display = pygame.display.set_mode((display_w, display_h))
        pygame.display.set_caption(f'Booster Packs {version}')

        # icon
        icon = pygame.image.load('textures/AppIcon.png').convert_alpha()
        icon = pygame.transform.smoothscale(icon.copy(), (32, 32))
        pygame.display.set_icon(icon)

        # bg
        self.bg = pygame.transform.smoothscale(
            pygame.image.load('textures/bg_deck.png').convert(), (display_w, display_h))
        self.bg.set_alpha(128)

        # properties
        self.clock = pygame.time.Clock()
        self.loop = True
        self.events = pygame.event.get()

        # screens
        self.screens = {}
        self.screen = None

        self.purchase = []

    def event_check(self):
        self.events = pygame.event.get()

    def leave(self):
        self.loop = False

    def save_purchase(self):
        with open('deck/Booster Packs.ydk', 'w') as deck:
            deck.write('#Created by AlexsanderRosante\n')
            deck.write('#main\n')
            for card in self.purchase:
                deck.write(card + '\n')
            deck.write('#extra\n')
            deck.write('!side\n')

    def run(self):
        self.screens['choose'] = SelectionScreen()
        self.screen = self.screens['choose']
        while self.loop:
            self.event_check()
            self.screen.update()
            self.screen.draw(self.display)
            pygame.display.update()
            self.clock.tick(60)
        self.save_purchase()
        pygame.quit()


if __name__ == '__main__':

    # settings
    version = '1.1.0r4'
    display_w = 1152
    display_h = 648
    hovered = pygame.sprite.GroupSingle()

    # Game
    game = Game()

    # Packs info
    packs_info = download_packs_info()

    # SFXs
    sfx_open_pack = pygame.mixer.Sound('sound/attack.wav')
    sfx_next_card = pygame.mixer.Sound('sound/draw.wav')
    sfx_next_srcard = pygame.mixer.Sound('sound/activate.wav')
    sfx_next_urcard = pygame.mixer.Sound('sound/summon.wav')

    # volumes
    sfx_open_pack.set_volume(0.2)
    sfx_next_srcard.set_volume(0.4)

    game.run()
