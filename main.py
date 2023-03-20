"""
Created by Alexsander Rosante 2023
Github: https://github.com/AlexsanderRST
"""

# from urllib import request, error
from pygame.locals import *

import json
import math
import random
import pygame

pygame.init()

info_sample = {"name": [],
               "cover": "",
               "description": "",
               "release": "",
               "#cards": 9,
               "head height": 20,
               "art x": -48,
               "rarity pos": "middle",
               "Common": [],
               "Rare": [],
               "Super Rare": [],
               "Ultra Rare": [],
               "%R": 1, "%SR": 5, "%UR": 12},


# Short Print = Common


def download_packs_info():
    """url = 'https://raw.githubusercontent.com/AlexsanderRST/EDOPro-Booster-Packs/main/BoosterPacks.json'
    try:
        request.urlretrieve(url, 'BoosterPacks.json')
        with open('BoosterPacks.json', 'r') as fp:
            return json.load(fp)
    except error.URLError:
        game.leave()"""
    with open('BoosterPacks.json', 'r') as fp:
        return json.load(fp)


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
            left = round((rect_width + spaccing) * col + padx)
            top = round((rect_height + spaccing) * row + pady)
            pygame.draw.rect(surface, color, (left, top, rect_width, rect_height))
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

    def get_cropped_art(self, card_id):
        pic = pygame.image.load(f'pics/{card_id}.jpg').convert()
        pic = pygame.transform.smoothscale(pic.copy(), (421, 614))
        art = pygame.Surface((323, 323))
        x, y = -48, -110
        if "art x" in self.info:
            x = self.info["art x"]
        art.blit(pic, (x, y))
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
            reflex.set_alpha(100)
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


class Button(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, text='', on_click=lambda: None):
        super().__init__()

        # properties
        self.on_click = on_click

        # image and rect
        self.image = pygame.Surface((width, height))
        self.image.fill('black')
        self.rect = self.image.get_rect()

        # text
        font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 13)
        self.text_surf = font.render(text, True, 'white')
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.w // 2, self.rect.h // 2
        self.image.blit(self.text_surf, self.text_rect)

        # border
        pygame.draw.rect(self.image, 'white', [0, 0, *self.rect.size], 1)

    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            game.hovered.remove(self)
        else:
            game.hovered.add(self)
            for event in game.events:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click()


class ButtonToggle(pygame.sprite.Sprite):
    def __init__(self,
                 width=100,
                 height=70,
                 border_size=2,
                 icon_path='',
                 idle_color='black',
                 idle_alpha=150,
                 idle_border_color='darkgray',
                 toggled_color='black',
                 toggled_alpha=150,
                 toggled_border_color='blue',
                 start_activated=False,
                 deactivate_on_click=False,
                 on_activation=lambda _: None,
                 on_activation_args=(),
                 ):
        super().__init__()

        # properties
        self.size = width, height
        self.border_size = border_size
        self.on_activation = on_activation
        self.on_activation_args = on_activation_args
        self.activated = False
        self.idle_border_color = idle_border_color
        self.toggled_border_color = toggled_border_color
        self.deactivate_on_click = deactivate_on_click

        # image and rect
        self.image = pygame.Surface(self.size, SRCALPHA)
        self.rect = self.image.get_rect()

        # idle surf
        self.idle_surf = pygame.Surface(self.size)
        self.idle_surf.fill(idle_color)
        self.idle_surf.set_alpha(idle_alpha)

        # toggled surf
        self.toggled_surf = pygame.Surface(self.size)
        self.toggled_surf.fill(toggled_color)
        self.toggled_surf.set_alpha(toggled_alpha)

        # icon surf
        self.icon_surf = pygame.Surface((50, 50), SRCALPHA)
        if icon_path:
            self.icon_surf = pygame.image.load(icon_path).convert_alpha()
            icon_h = round(self.rect.h * .5)
            icon_w = round(self.icon_surf.get_width() / self.icon_surf.get_height() * icon_h)
            self.icon_surf = pygame.transform.smoothscale(self.icon_surf, (icon_w, icon_h))
        self.icon_rect = self.icon_surf.get_rect()
        self.icon_rect.midtop = round(self.rect.w / 2), round(self.rect.h * .25)

        # draw button
        styles = {0: [self.idle_surf, self.idle_border_color], 1: [self.toggled_surf, self.toggled_border_color]}
        self.redraw(*styles[bool(start_activated)])

    def activate(self):
        self.on_activation(*self.on_activation_args)
        self.activated = True
        self.redraw(self.toggled_surf, self.toggled_border_color)

    def deactivate(self):
        self.redraw(self.idle_surf, self.idle_border_color)
        self.activated = False

    def redraw(self, surface: pygame.Surface, border_color: str):
        self.image = pygame.Surface(self.size, SRCALPHA)
        self.image.blit(surface, (0, 0))
        self.image.blit(self.icon_surf, self.icon_rect)
        pygame.draw.rect(self.image, border_color, [0, 0, *self.rect.size], self.border_size)

    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            game.hovered.remove(self)
        else:
            game.hovered.add(self)
            for event in game.events:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if not self.activated:
                        self.activate()
                    elif self.deactivate_on_click:
                        self.deactivate()


class Card(pygame.sprite.Sprite):
    def __init__(self, card_id, pack_info, overlay=False):
        super().__init__()

        # properties
        self.tool = PacksTool(pack_info)
        self.id = card_id
        self.rarity = self.tool.get_rarity(self.id)
        self.width, self.height = card_size

        # pic
        self.pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        self.pic = pygame.transform.smoothscale(self.pic.convert(), (self.width, self.height))

        # rarity label
        self.rlabel = RarityLabel(self.rarity)
        self.rlabel.rect.right = self.pic.get_width()

        # image
        self.image_size = self.pic.get_width(), self.pic.get_height() + self.rlabel.image.get_height()
        self.image = pygame.Surface(self.image_size, SRCALPHA)
        self.image.blit(self.pic, (0, self.rlabel.image.get_height()))

        # motion
        self.rect = self.image.get_rect()
        self.pos = self.rect.center
        self.vel = pygame.math.Vector2()
        self.anim = self.idle

        # rarity effect
        if not overlay:
            self.rarity_effect = self.Overlay(self.image)
        else:
            match self.rarity:
                case 'Rare':
                    self.rarity_effect = self.ROverlay(self.image)
                case 'Super Rare':
                    self.rarity_effect = self.SROverlay(self.image)
                case 'Ultra Rare':
                    self.rarity_effect = self.UROverlay(self.image)
                case _:
                    self.rarity_effect = self.Overlay(self.image)

    def check_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            game.hovered.add(self)
        else:
            game.hovered.remove(self)

    def idle(self):
        pass

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
        self.image = pygame.Surface(self.image_size, SRCALPHA)
        self.image.blit(self.pic, (0, self.rlabel.image.get_height()))
        self.rarity_effect.apply(self.image)
        pygame.sprite.GroupSingle(self.rlabel).draw(self.image)

    def update(self):
        # self.check_hovered()
        self.redraw()
        self.pos = self.rect.center
        self.pos += self.vel
        self.rect.center = self.pos
        self.anim()

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


class CardMiniature(pygame.sprite.Sprite):
    def __init__(self, card_id: str, pack_info: dict):
        super().__init__()

        # properties
        self.tool = PacksTool(pack_info)

        # pic
        self.pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        self.pic = pygame.transform.smoothscale(self.pic, card_mini_size)

        # rarity label
        rarity = self.tool.get_rarity(card_id)
        self.rlabel = RarityLabel(rarity, .275)
        self.rlabel.rect.right = self.pic.get_width()

        # image
        self.image_size = self.pic.get_width(), self.pic.get_height() + self.rlabel.rect.h
        self.image = pygame.Surface(self.image_size, SRCALPHA)

        # blits
        self.image.blit(self.pic, (0, self.rlabel.rect.h))
        self.image.blit(self.rlabel.image, self.rlabel.rect)

        # rect
        self.rect = self.image.get_rect()

    def blit_counter(self, counter: int):
        width = round(self.image.get_width() * .2)
        height = width
        surf = pygame.Surface((width, height))
        surf.fill('black')
        rect = surf.get_rect(bottomright=self.image.get_size())
        font = pygame.font.Font('fonts/Jetbrains.ttf', 14)
        text_surf = font.render(str(counter), True, 'white')
        text_rect = text_surf.get_rect()
        text_rect.center = round(width / 2), round(height / 2)
        surf.blit(text_surf, text_rect)
        self.image.blit(surf, rect)


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


class RarityLabel(pygame.sprite.Sprite):
    def __init__(self, rarity: str, scale=.45):
        super().__init__()
        self.image = pygame.image.load(f'textures/rlabel_{rarity_symbol[rarity]}.png').convert_alpha()
        new_size = round(self.image.get_width() * scale), round(self.image.get_height() * scale)
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect()
        self.frame = 0


class RarityFilters(pygame.sprite.Group):
    def __init__(self,
                 pack_name: str,
                 container_w: float,
                 container_left: float,
                 custom_filter=lambda: None):
        super().__init__()

        # properties
        pack_info = packs_info[pack_name]
        self.tool = PacksTool(packs_info[pack_name])

        # define filters
        filters = [['all', '']]
        for r in all_rarities:
            if r in pack_info and len(pack_info[r]):
                filters.append([rarity_symbol[r], r])

        # set button filters
        width, height, y = round(container_w / len(filters)), round(display_h * .1), round(display_h * .015)
        last_right = container_left
        for r in filters:
            button = ButtonToggle(width, height,
                                  icon_path=f'textures/rlabel_{r[0]}.png',
                                  on_activation=custom_filter,
                                  on_activation_args=[r[1]])
            button.rect.topleft = last_right, y
            self.add(button)
            last_right = button.rect.right

    def deactivate_all(self):
        for button in self:
            button.deactivate()


class SlideBar:
    def __init__(self, slider_ratio=1.):
        # properties
        offset = round(display_h * .025)
        width = round(display_w * .0125)
        self.slider_ceil = offset
        self.slider_floor = display_h - offset
        self.follow_mouse = False

        # background
        self.bg_surf = pygame.Surface((width, display_h - 2 * offset))
        self.bg_surf.set_alpha(150)

        # slider
        slider = pygame.sprite.Sprite()
        slider.image = pygame.Surface((width, self.bg_surf.get_height() * slider_ratio))
        slider.image.fill('darkgray')
        slider.rect = slider.image.get_rect()
        slider.pos = pygame.math.Vector2(slider.rect.center)
        self.slider = pygame.sprite.GroupSingle(slider)

        # rects
        self.bg_rect = self.bg_surf.get_rect()
        self.bg_rect.topright = display_w - offset, offset
        self.slider.sprite.rect.topleft = self.bg_rect.topleft

        # movement
        self.slider_speed_y = 10
        self.slider_vel = pygame.math.Vector2()
        self.slider_decel = .5

    def draw(self, surface: pygame.Surface):
        surface.blit(self.bg_surf, self.bg_rect)
        self.slider.draw(surface)

    def check_constraint(self):
        slider = self.slider.sprite
        if slider.rect.top < self.slider_ceil:
            slider.rect.top = self.slider_ceil
            self.slider_vel.y = 0
            slider.pos.y = slider.rect.centery
        elif slider.rect.bottom > self.slider_floor:
            slider.rect.bottom = self.slider_floor
            self.slider_vel.y = 0
            slider.pos.y = slider.rect.centery

    def check_events(self):
        for event in game.events:
            if event.type == MOUSEBUTTONUP and event.button == 1:
                self.follow_mouse = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.slider_vel.y = -self.slider_speed_y
                elif event.button == 5:
                    self.slider_vel.y = self.slider_speed_y
                elif event.button == 1 and self.is_hovered():
                    self.follow_mouse = True

    def is_hovered(self):
        return self.slider.sprite.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        self.check_events()
        slider = self.slider.sprite
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        if self.follow_mouse:
            slider.rect.centery = mouse_pos.y
            self.slider_vel.y = 0
            slider.pos.y = slider.rect.centery
        else:
            slider.pos.y += self.slider_vel.y
            slider.rect.centery = slider.pos.y
            if round(self.slider_vel.y) != 0:
                self.slider_vel.y -= self.slider_vel.y/abs(self.slider_vel.y) * self.slider_decel
            else:
                self.slider_vel.y = 0
        self.check_constraint()


# SCREENS
class CardDetailScreen:
    def __init__(self, card_id):
        card = pygame.sprite.Sprite()
        card.image = pygame.image.load(f'pics/{card_id}.jpg')
        card_w, card_h = card.image.get_size()
        card.image = pygame.transform.smoothscale(card.image, (624, round(card_h / card_w * 624)))
        card.rect = card.image.get_rect(midbottom=(display_w // 2, display_h // 2 + 100))
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

        # properties
        self.spaccing = 7
        self.preview_bg_w = round(0.213 * display_w) + 2 * self.spaccing
        self.pack_hovered = None
        self.pack_locked = None

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

        # pack details button
        button_detail_w = round(self.preview_bg_w * .8)
        button_detail_h = round(display_h * .065)
        button_detail = Button(button_detail_w, button_detail_h, 'Pack Content', self.go_to_pack_content_screen)
        button_detail.rect.bottomleft = round(display_h * .025), round(display_h - display_h * .025)
        self.button_detail = pygame.sprite.GroupSingle(button_detail)

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
                elif event.button == 3:
                    for pack in self.pages[self.cur_page]:
                        if pack.hovered(event.pos):
                            if self.pack_locked is None:
                                self.pack_locked = pack
                            else:
                                if self.pack_locked == pack:
                                    self.pack_locked = None
                                else:
                                    self.pack_locked = pack

    def check_pack_hovered(self):
        for pack in self.pages[self.cur_page]:
            if not pack.hovered(pygame.mouse.get_pos()):
                game.hovered.remove(pack)
            else:
                game.hovered.add(pack)
                if any([self.pack_locked is None, pack == self.pack_locked]):
                    self.preview_image.sprite.image = pack.preview.image
                    self.set_description(pack)
                    self.pack_hovered = pack.code

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

    def go_to_pack_content_screen(self):
        if self.pack_hovered is not None:
            game.screen = PackContentScreen(self.pack_hovered)

    def set_description(self, pack, space=10):

        # setup description
        description = [f'{pack.info["description"]}', f'Cards per pack: {pack.info["#cards"]}']
        name_to_prob = {'Rare': '%R', 'Super Rare': '%SR', 'Ultra Rare': '%UR', 'Secret Rare': '%SE'}
        total_cards = 0
        for r in all_rarities:
            if r in pack.info and len(pack.info[r]) > 0:
                if r == 'Common':
                    description.append(f'{r}: {len(pack.info[r])}')
                else:
                    description.append(f'{r}: {len(pack.info[r])} (1:{pack.info[name_to_prob[r]]})')
                total_cards += len(pack.info[r])
        description.append(f'Total: {total_cards}')

        # update description
        self.description = pygame.Surface(self.description.get_size(), SRCALPHA)
        font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 13)
        last_bottom = space
        for i in description:
            text = font.render(i, True, 'white')
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

    def draw(self, surface: pygame.Surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.pages[self.cur_page].draw(surface)
        surface.blit(self.preview_bg, (0, 0))
        self.preview_image.draw(surface)
        self.button_detail.draw(surface)
        surface.blit(self.description, self.description_rect)
        self.draw_lock(surface)

    def draw_lock(self, surface: pygame.Surface):
        if self.pack_locked is not None:
            pack = self.pack_locked
            pack_size = pack.mini.rect.size
            pack_topleft = pack.mini.rect.topleft
            pygame.draw.rect(surface, 'yellow', [*pack_topleft, *pack_size], 2)

    def update(self):
        self.check_events()
        self.check_pack_hovered()
        self.pages[self.cur_page].update()
        self.preview_image.update()
        self.button_detail.update()

    class Packs(list):
        def add(self, pack: BoosterPack):
            self.append(pack)

        def draw(self, surface: pygame.Surface):
            for pack in self:
                pack.draw(surface)

        def update(self):
            for pack in self:
                pack.update()


class PackContentScreen:
    def __init__(self, pack_name: str):

        # settings
        game.hovered.empty()

        # properties
        self.container_w = display_w * .875
        self.card_size = 118, 192
        self.col = 8
        self.offset_x = display_w * .05
        self.offset_y = display_h * .15
        self.pack_info = packs_info[pack_name]
        self.tool = PacksTool(self.pack_info)

        # cards
        self.cards_surf = {}
        self.load_cards()
        self.cards = pygame.sprite.Group()
        self.set_cards(self.tool.get_all_cards_from_pack())

        # container
        self.container = pygame.Rect([0, 0, 0, 0])
        self.container_floor = 0
        self.set_container()

        # rarity filter buttons
        self.filter_buttons = RarityFilters(pack_name, self.container_w, self.container.left, self.filter)

        # slide bar
        self.slide_bar = None
        self.set_slide_bar()

    @staticmethod
    def check_events():
        for event in game.events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.screen = game.screens['choose']

    def filter(self, rarity=''):
        if rarity:
            self.set_cards(self.pack_info[rarity])
        else:
            self.set_cards(self.tool.get_all_cards_from_pack())
        self.reset()

    def load_cards(self):
        cards = self.tool.get_all_cards_from_pack()
        self.cards_surf = {card_id: CardMiniature(card_id, self.pack_info) for card_id in cards}

    def reset(self):
        self.filter_buttons.deactivate_all()
        self.set_container()
        self.set_slide_bar()

    def set_cards(self, card_list: list):
        self.cards.empty()
        card = None
        row = math.ceil(len(card_list) / self.col)
        space_x = (self.container_w - self.card_size[0] * self.col) / (self.col - 1)
        last_bottom = self.offset_y
        for i in range(row):
            last_right = self.offset_x
            for j in range(self.col):
                idx = i * self.col + j
                if idx < len(card_list):
                    card_id = card_list[idx]
                    card = self.cards_surf[card_id]
                    card.rect.topleft = last_right, last_bottom
                    last_right = card.rect.right + space_x
                    card.yi = card.rect.y
                    self.cards.add(card)
            last_bottom = card.rect.bottom + space_x

    def set_container(self):
        container_h = 50
        if self.cards.sprites():
            card0 = self.cards.sprites()[0]
            cardf = self.cards.sprites()[-1]
            container_h = cardf.rect.bottom - card0.rect.top
        self.container = pygame.Rect(self.offset_x, self.offset_y, self.container_w, container_h)
        floor = round(display_h - display_h * .025)
        self.container_floor = floor if self.container.bottom >= floor else self.container.bottom

    def set_slide_bar(self):
        distance = self.container.bottom - self.container_floor
        slider_r = 1 - distance / self.container.h
        slider_r = slider_r if slider_r < 1 else 1.
        self.slide_bar = SlideBar(slider_r)

    def draw(self, surface: pygame.Surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        # pygame.draw.rect(surface, 'darkgray', self.container)
        self.cards.draw(surface)
        self.slide_bar.draw(surface)
        self.filter_buttons.draw(surface)

    def update_container_pos(self):
        p1 = self.slide_bar.bg_rect.bottom
        p2 = self.slide_bar.slider.sprite.rect.bottom
        h1 = self.container.h
        h2 = self.slide_bar.bg_rect.h
        dy = h1 / h2 * (p1 - p2)
        self.container.bottom = self.container_floor + dy

    def update_cards_pos(self):
        dy = self.offset_y - self.container.top
        for card in self.cards.sprites():
            card.rect.y = card.yi - dy

    def update(self):
        self.check_events()
        self.slide_bar.update()
        self.update_container_pos()
        self.update_cards_pos()
        self.filter_buttons.update()


class PullScreen(PackContentScreen):
    def __init__(self, pack_name: str, last_pull: list):
        super().__init__(pack_name)

        # properties
        self.card_list = last_pull
        self.card_set = list(set(self.card_list))
        self.organize_pull()

        # settings
        game.hovered.empty()
        self.set_counter()
        self.set_cards(self.card_set)
        self.reset()
        self.filter_buttons = RarityFilters(pack_name, self.container_w, self.container.left, self.filter)

    def filter(self, rarity=''):
        if rarity:
            self.set_cards(self.tool.get_rarities_from_list(self.card_set)[rarity])
        else:
            self.set_cards(self.card_set)
        self.reset()

    def organize_pull(self):
        organized_list = []
        for rarity in ('Ultra Rare', 'Super Rare', 'Rare', 'Common'):
            for card_id in self.pack_info[rarity]:
                if card_id in self.card_set:
                    organized_list.append(card_id)
        self.card_set = organized_list

    def set_counter(self):
        for card_id in self.cards_surf:
            self.cards_surf[card_id].blit_counter(self.card_list.count(card_id))


class UnpackScreen:
    def __init__(self, current_pack, last_pull=[]):

        # properties
        self.pack_name = current_pack
        self.pack = BoosterPack(current_pack)
        self.cards = pygame.sprite.LayeredUpdates()
        self.card_moving = False
        self.open_pack = False
        self.rarity_viewed = False
        self.pull = last_pull

        # settings
        game.hovered.empty()
        self.generate_pack(packs_info[current_pack])

        # counter
        self.counter = 1
        self.card_midbottom = self.cards.sprites()[0].rect.midbottom

        # font
        self.font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 18)
        self.font.set_bold(True)

        # detail button (invisible)
        self.detail_button = pygame.Rect(376, 320, 271, 180)

        # buttons
        self.buttons = pygame.sprite.Group()
        btn_size = round(display_w * .15), round(display_w * .04)
        btn_new_pack = Button(*btn_size, 'New Pack', self.new_pack)
        btn_new_pack.rect.bottomright = round(display_w * .985), round(display_h * .9725)
        btn_check_pull = Button(*btn_size, 'Check Pull', self.check_pull)
        btn_check_pull.rect.bottomleft = round(display_w * .015), round(display_h * .9725)
        self.buttons.add(btn_new_pack, btn_check_pull)

    def check_event(self):
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
                    elif event.button == 2:
                        if self.detail_button.collidepoint(event.pos):
                            game.screens['detail'] = CardDetailScreen(self.get_top_card().id)
                            game.screen = game.screens['detail']
                    elif event.button == 3:
                        if card.rect.collidepoint(event.pos):
                            self.switch_previous_card()
                    elif event.button == 4:
                        self.switch_previous_card()
                    elif event.button == 5:
                        self.switch_next_card()

            # keyboard input
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.screen = game.screens['choose']

    def check_pull(self):
        game.screen = PullScreen(self.pack_name, self.pull)

    def draw_counter(self, surface: pygame.Surface):
        surf = self.font.render(f'{self.counter}/{len(self.cards)}', True, Color('white'))
        rect = surf.get_rect(midtop=(self.card_midbottom[0] + 13, self.card_midbottom[1]))
        surface.blit(surf, rect)

    def generate_pack(self, info):
        self.cards.empty()

        # Fill with common cards
        cards = [random.choice(info['Common']) for _ in range(info['#cards'] - 1)]

        # Get the rare card
        '''rarity = {'Super Rare': info['%SR'], 'Ultra Rare': info['%UR']}
        probability = [i for i in list(rarity.values()) if i > 0]
        avaible_rarity = [i for i in rarity if rarity[i] > 0]
        lcm = math.lcm(*probability)
        lst = []
        for i in avaible_rarity:
            for j in range(int(lcm / rarity[i])):
                lst.append(random.choice(info[i]))
        lst.extend([random.choice(info['Rare']) for _ in range(lcm - len(lst))])  # if 0 Rares?
        random.shuffle(lst)
        picked_rare = random.choice(lst)'''

        # get the main rarity and others
        main_rarity, other_rarities = '', []
        for r in ("%R", "%SR", "%UR", "%SE"):
            if r in info:
                if info[r] == 1:
                    main_rarity = r
                elif info[r] > 1:
                    other_rarities.append(r)

        # pick a rare
        probability_name = {"%R": 'Rare', "%SR": 'Super Rare', "%UR": 'Ultra Rare', "%SE": 'Secret Rare'}
        probabilities = [info[r] for r in other_rarities]
        lcm = math.lcm(*probabilities)
        lst = []
        for r in other_rarities:
            for j in range(int(lcm / info[r])):
                lst.append(random.choice(info[probability_name[r]]))
        lst.extend([random.choice(info[probability_name[main_rarity]]) for _ in range(lcm - len(lst))])
        random.shuffle(lst)
        picked_rare = random.choice(lst)

        # Rarity pos
        if info['rarity pos'] == 'middle':
            cards.insert(info['#cards'] // 2, picked_rare)
        else:
            cards.insert(0, picked_rare)

        # put cards into pull
        self.pull += cards

        # Put cards into pack:
        for index, card_id in enumerate(cards):
            card = Card(card_id, info)
            card.rect.center = round(display_w / 2), round(display_h / 2 - card.rlabel.image.get_height())
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

    def new_pack(self):
        game.hovered.empty()
        game.screens['unpack'] = UnpackScreen(self.pack_name, self.pull)
        game.screen = game.screens['unpack']

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
        if not self.open_pack:
            self.cards.draw(surface)
            self.pack.draw(surface)
        else:
            self.cards.draw(surface)
            self.draw_counter(surface)
            self.buttons.draw(surface)

    def update(self):
        self.check_event()
        if self.open_pack:
            self.cards.update()
            self.buttons.update()
        else:
            self.pack.update()


# UTILITY
class PacksTool:
    def __init__(self, pack_info):
        self.pack_info = pack_info

    def get_all_cards_from_pack(self):
        cards_list = []
        rarities = [r for r in all_rarities[::-1] if r in self.pack_info]
        for i in rarities:
            for j in self.pack_info[i]:
                cards_list.append(j)
        return cards_list

    def get_rarity(self, card_id: str):
        for rarity in all_rarities[::-1]:
            if rarity in self.pack_info and card_id in self.pack_info[rarity]:
                return rarity

    def get_rarities_from_list(self, card_list: list):
        rarities = {r: [] for r in all_rarities}
        for card_id in card_list:
            if card_id in self.pack_info['Common']:
                rarities['Common'].append(card_id)
            elif card_id in self.pack_info['Rare']:
                rarities['Rare'].append(card_id)
            elif card_id in self.pack_info['Super Rare']:
                rarities['Super Rare'].append(card_id)
            elif card_id in self.pack_info['Ultra Rare']:
                rarities['Ultra Rare'].append(card_id)
        return rarities


# APP
class Game:
    def __init__(self):
        # display
        self.display = pygame.display.set_mode((display_w, display_h))

        # icon
        '''icon = pygame.image.load('textures/AppIcon.png').convert_alpha()
        icon = pygame.transform.smoothscale(icon.copy(), (32, 32))
        pygame.display.set_icon(icon)'''

        # bg
        self.bg = pygame.transform.smoothscale(
            pygame.image.load('textures/bg_deck.png').convert(), (display_w, display_h))
        self.bg.set_alpha(128)

        # properties
        self.clock = pygame.time.Clock()
        self.loop = True
        self.events = pygame.event.get()
        self.hovered = pygame.sprite.Group()

        # screens
        self.screens = {}
        self.screen = None

        # card?
        self.purchase = []

    def cursor_by_context(self):
        cursor = SYSTEM_CURSOR_HAND if len(self.hovered.sprites()) else SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor)

    def event_check(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN and event.key == K_d:
                self.screen = PackContentScreen("LIOV")
            if event.type == QUIT:
                self.leave()

    def leave(self):
        self.loop = False

    def save_purchase(self):
        """with open('deck/Booster Packs.ydk', 'w') as deck:
            deck.write('#Created by AlexsanderRosante\n')
            deck.write('#main\n')
            for card in self.purchase:
                deck.write(card + '\n')
            deck.write('#extra\n')
            deck.write('!side\n')"""
        pass

    def run(self):
        self.screens['choose'] = SelectionScreen()
        self.screen = self.screens['choose']
        while self.loop:
            pygame.display.set_caption(f"Booster Packs {version} ({self.clock.get_fps() :.1f})")
            self.cursor_by_context()
            self.event_check()
            self.screen.update()
            self.screen.draw(self.display)
            pygame.display.update()
            self.clock.tick(60)
        self.save_purchase()
        pygame.quit()


if __name__ == '__main__':
    # settings
    version = '1.2'
    display_w = 1152
    display_h = 648
    card_size = 288, 420
    card_mini_size = 118, 172

    # rarities
    rarity_symbol = {'Common': 'n', 'Rare': 'r', 'Super Rare': 'sr', 'Ultra Rare': 'ur', 'Secret Rare': 'se'}
    all_rarities = ('Common', 'Rare', 'Super Rare', 'Ultra Rare', 'Secret Rare')

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
