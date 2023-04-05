"""
Created by Alexsander Rosante 2023
Github: https://github.com/AlexsanderRST
"""
import string

# from urllib import request, error
from pygame.locals import *
from string import ascii_uppercase

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
        self.rect.center = display_c
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
        try:
            pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        except FileNotFoundError:
            pic = pygame.image.load(f'pics/holder.png').convert_alpha()
        pic = pygame.transform.smoothscale(pic.copy(), (421, 614))
        art_height = 323 - 50 if 'pendulum cover' in self.info else 323
        art = pygame.Surface(2 * [art_height])
        x, y = -49, -110
        art.blit(pic, (x, y))
        return art

    def get_surface(self):
        try:
            surface = pygame.image.load(f'pics/booster/{self.code}.png').convert_alpha()
        except FileNotFoundError:
            
            # setup
            self.head_height = 40
            surface = pygame.Surface((self.width, self.height), SRCALPHA)

            # artwork
            art = self.get_cropped_art(self.info['cover'])
            art = pygame.transform.smoothscale(art.copy(), 2 * [self.height - self.head_height * 2])
            art_x = self.info['art x'] if 'art x' in self.info else 0
            surface.blit(art, (-art.get_width() / 4 + art_x, self.head_height))

            # mask
            mask = pygame.image.load('textures/bpack_mask.png')
            mask.set_colorkey('#ff2a7f')
            mask = pygame.transform.smoothscale(mask.copy(), (self.width, self.height))
            surface.blit(mask, (0, 0))

            # name
            font = pygame.font.Font('fonts/ArchivoBlack-Regular.ttf', 48)
            last_top = surface.get_height() - self.head_height * 1.5
            for i in self.info['name'][::-1]:
                text = font.render(i.upper(), True, 'white')
                text = pygame.transform.smoothscale(text.copy(), (surface.get_width() * .9, text.get_height()))
                text_rect = text.get_rect(midbottom=(surface.get_width() / 2, last_top))
                outline = font.render(i.upper(), True, 'black')
                outline_size = 4
                outline = pygame.transform.scale(outline.copy(), text_rect.size)
                outline.set_alpha(200)
                for j in ((-outline_size, -outline_size), (0, -outline_size), (outline_size, -outline_size),
                          (-outline_size, 0), (outline_size, 0),
                          (-outline_size, outline_size), (0, outline_size), (outline_size, outline_size)):
                    surface.blit(outline, (text_rect.left + j[0], text_rect.top + j[1]))
                surface.blit(text, text_rect)
                last_top = text_rect.top

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

    def update(self):
        self.body_pos = pygame.math.Vector2(self.body.rect.center)
        if self.openning:
            self.unpack()
        else:
            self.head.rect.topleft = self.rect.topleft
            self.body.rect.topleft = self.head.rect.bottomleft
        super().update()


class ButtonText(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, text='', on_click=lambda: None):
        super().__init__()

        # properties
        self.on_click = on_click

        # image and rect
        self.image = pygame.Surface((width, height))
        self.image.fill('black')
        self.rect = self.image.get_rect()

        # text
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 13)
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


class ButtonIcon(pygame.sprite.Sprite):
    def __init__(self,
                 size: tuple[float, float],
                 icon: str,
                 on_activation=lambda: None):
        super().__init__()

        # properties
        self.on_activation = on_activation

        # surfs
        self.surf_on = pygame.image.load(f'textures/btn_{icon}_on.png').convert_alpha()
        self.surf_off = pygame.image.load(f'textures/btn_{icon}_off.png').convert_alpha()

        # resize surfs
        self.surf_on = pygame.transform.smoothscale(self.surf_on.copy(), size)
        self.surf_off = pygame.transform.smoothscale(self.surf_off.copy(), size)

        # image & rect
        self.image = self.surf_off.copy()
        self.rect = self.image.get_rect()

    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            game.hovered.remove(self)
            self.image = self.surf_off.copy()
        else:
            game.hovered.add(self)
            self.image = self.surf_on.copy()
            for event in game.events:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.on_activation()


class ButtonToggle(pygame.sprite.Sprite):
    def __init__(self,
                 width=100,
                 height=70,
                 border_size=2,
                 text='',
                 text_size=32,
                 icon_path='',
                 idle_color='black',
                 idle_alpha=150,
                 idle_border_color='#b3b3b3',
                 toggled_color='black',
                 toggled_alpha=150,
                 toggled_border_color='#80ff94',
                 start_activated=False,
                 deactivate_on_click=False,
                 on_activation=lambda: None,
                 on_activation_args=(),
                 on_deactivation=lambda: None,
                 on_deactivation_args=()
                 ):
        super().__init__()

        # properties
        self.activated = False
        self.border_size = border_size
        self.deactivate_on_click = deactivate_on_click
        self.idle_border_color = idle_border_color
        self.on_activation = on_activation
        self.on_activation_args = on_activation_args
        self.on_deactivation = on_deactivation
        self.on_deactivation_args = on_deactivation_args
        self.size = width, height
        self.toggled_border_color = toggled_border_color

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

        # content
        self.content_surf = pygame.Surface((50, 50), SRCALPHA)
        if icon_path:
            self.content_surf = pygame.image.load(icon_path).convert_alpha()
            icon_h = round(self.rect.h * .5)
            icon_w = round(self.content_surf.get_width() / self.content_surf.get_height() * icon_h)
            self.content_surf = pygame.transform.smoothscale(self.content_surf, (icon_w, icon_h))
        elif text:
            font = pygame.font.Font('fonts/Roboto-Regular.ttf', text_size)
            self.content_surf = font.render(text, True, 'white')
        self.content_rect = self.content_surf.get_rect()
        self.content_rect.midtop = round(self.rect.w / 2), round(self.rect.h * .25)

        # draw button
        styles = {0: [self.idle_surf, self.idle_border_color], 1: [self.toggled_surf, self.toggled_border_color]}
        self.redraw(*styles[bool(start_activated)])

    def activate(self):
        self.on_activation(*self.on_activation_args)
        self.activated = True
        self.redraw(self.toggled_surf, self.toggled_border_color)

    def deactivate(self):
        self.on_deactivation(*self.on_deactivation_args)
        self.activated = False
        self.redraw(self.idle_surf, self.idle_border_color)

    def redraw(self, surface: pygame.Surface, border_color: str):
        self.image = pygame.Surface(self.size, SRCALPHA)
        self.image.blit(surface, (0, 0))
        self.image.blit(self.content_surf, self.content_rect)
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
        try:
            self.pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        except FileNotFoundError:
            self.pic = pygame.image.load(f'pics/holder.png').convert_alpha()
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
            if self.rect.left < display_c.x + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = display_c.x + self.width / 2
                self.vel.x = 0.
                cards.move_to_back(self)
        else:
            if self.rect.centerx > display_c.x:
                self.vel.x = -speed
            else:
                self.rect.centerx = display_c.x
                self.vel.x = 0.
                self.anim = self.idle
                game.screen.card_moving = False

    def move_to_front(self, speed=20.):
        cards = game.screen.cards
        if self == game.screen.get_bottom_card():
            if self.rect.left < display_c.x + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = display_c.x + self.width / 2
                self.vel.x = 0.
                cards.move_to_front(self)
        else:
            if self.rect.centerx > display_c.x:
                self.vel.x = -speed
            else:
                self.rect.centerx = display_c.x
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
        try:
            self.pic = pygame.image.load(f'pics/{card_id}.jpg').convert_alpha()
        except FileNotFoundError:
            self.pic = pygame.image.load(f'pics/holder.png').convert_alpha()
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


class CounterPackCards(pygame.sprite.Sprite):
    def __init__(self, width=100, height=100):
        super().__init__()

        # properties
        self.cards_cur = 0
        self.cards_total = 0
        self.font = pygame.font.Font('fonts/Roboto-Regular.ttf', 18)
        self.size = width, height

        # image & rect
        self.image = pygame.Surface(self.size, SRCALPHA)
        self.rect = self.image.get_rect()

    def redraw(self):
        self.image = pygame.Surface(self.size, SRCALPHA)
        bg = pygame.Surface(self.size)
        bg.fill('black')
        text = self.font.render(f'{self.cards_cur}/{self.cards_total}', True, 'white')
        text_rect = text.get_rect(midright=(self.rect.w * .95, self.rect.h * .5))
        self.image.blit(bg, (0, 0))
        pygame.draw.rect(self.image, 'darkgray', [-1, 0, self.rect.w + 2, self.rect.h], 1)
        self.image.blit(text, text_rect)

    def update(self, cards_cur: int, cards_total: int):
        self.cards_cur, self.cards_total = cards_cur, cards_total
        self.redraw()


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
                 pack_id: str,
                 container_w: float,
                 container_right: float,
                 custom_filter=lambda: None):
        super().__init__()

        # properties
        container_w *= .8
        pack_info = packs_info[pack_id]
        self.tool = PacksTool(packs_info[pack_id])

        # define filters
        filters = [['all', '']]
        for r in all_rarities:
            if r in pack_info and len(pack_info[r]):
                filters.append([rarity_symbol[r], r])

        # set button filters
        btn_w, btn_h, y = round(container_w / len(filters)), round(display_h * .0875), round(display_h * .015)
        last_left = container_right
        for r in filters[::-1]:
            btn_args = {'width': btn_w, 'height': btn_h, 'on_activation': custom_filter, 'on_activation_args': [r[1]]}
            if r[0] == 'all':
                btn_args['text'], btn_args['text_size'] = 'ALL', 26
            else:
                btn_args['icon_path'] = f'textures/rlabel_{r[0]}.png'
            btn = ButtonToggle(**btn_args)
            btn.rect.topright = last_left, y
            self.add(btn)
            last_left = btn.rect.left

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


class SlideCard(pygame.sprite.Group):
    def __init__(self,
                 n_cards: int,
                 buttons_height: float,
                 buttons_bottom: float,
                 rare_pos='middle'):
        super().__init__()

        # w_ratio
        ratio_w = round((.25 - .075) / 6 * n_cards, 3)
        ratio_w = ratio_w if ratio_w < .65 else .65

        # rect
        self.rect = pygame.Rect(0, 0, display_w * ratio_w, buttons_height / 2)
        self.rect.midbottom = display_c.x, buttons_bottom

        # set cards size
        self.card_max_h = self.rect.h
        self.card_max_w = round(card_size[0] / card_size[1] * self.card_max_h)
        self.card_min_h = self.rect.h * .75
        self.card_min_w = round(card_size[0] / card_size[1] * self.card_min_h)

        # set spaccing
        spacing = (self.rect.w - self.card_max_w * n_cards) / (n_cards - 1)

        # rarity pos at middle
        if rare_pos == 'middle':
            rare_i = math.floor(n_cards / 2)
        else:
            rare_i = n_cards - 1

        # set cards
        last_right = self.rect.left
        for i in range(n_cards):
            card = pygame.sprite.Sprite()
            card.active_color = '#989596' if i != rare_i else '#d4af37'
            card.inactive_color = '#595154' if i != rare_i else '#b08f26'
            card.image = pygame.Surface((self.card_max_w, self.card_max_h))
            card.image.fill('gray')
            card.rect = card.image.get_rect()
            card.rect.bottomleft = last_right, self.rect.bottom
            self.add(card)
            last_right = card.rect.right + spacing

    def update(self, counter: int):
        for i, card in enumerate(self.sprites()):
            if i != counter - 1:
                color, size = card.inactive_color, (self.card_min_w, self.card_min_h)
            else:
                color, size = card.active_color, (self.card_max_w, self.card_max_h)
            card.image = pygame.Surface(size)
            card.image.fill(color)
            card.rect = card.image.get_rect(midbottom=card.rect.midbottom)


class TextBox(pygame.sprite.Sprite):
    def __init__(self, text: str, width=0):
        super().__init__()
        padx, pady = 10, 10
        font = pygame.font.Font('fonts/Roboto-MediumItalic.ttf', 25)
        text_surf = font.render(text, True, 'white', 'black')
        width = text_surf.get_width() + 2 * padx if not width else width
        self.image = pygame.Surface((width, text_surf.get_height() + 2 * pady))
        self.image.fill('black')
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'darkgray', [-1, 0, self.rect.w + 2, self.rect.h], 1)
        self.image.blit(text_surf, (padx, pady))


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


class ConfigScreen:
    def __init__(self):
        # properties
        self.buttons = pygame.sprite.Group()
        self.text_boxes = pygame.sprite.Group()
        offset_y = display_h * .05

        # back button
        btn = ButtonIcon(2 * [display_w * .04], 'back', self.quit)
        btn.rect.topleft = 2 * [display_h * .025]
        self.buttons.add(btn)

        # fullscreen option
        '''tbox = TextBox('Fullscreen', display_w * .85)
        tbox.rect.topleft = btn.rect.right + display_h * .05, offset_y
        btn_w = tbox.rect.h * .7
        btn = ButtonToggle(
            width=btn_w, height=btn_w,
            idle_color='red', toggled_color='green',
            idle_border_color='gray', toggled_border_color='gray',
            deactivate_on_click=True,
            on_activation=game.set_fullscreen,
            on_deactivation=game.set_fullscreen
        )
        btn.rect.midright = tbox.rect.midright
        self.buttons.add(btn)
        self.text_boxes.add(tbox)
        '''

    def draw(self, surface: pygame.Surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.text_boxes.draw(surface)
        self.buttons.draw(surface)

    @staticmethod
    def quit():
        game.hovered.empty()
        game.screen = game.screens['choose']

    def update(self):
        self.buttons.update()


class PackContentScreen:
    def __init__(self, pack_id: str):

        # settings
        game.hovered.empty()

        # properties
        self.container_w = display_w * .875
        self.card_size = 118, 192
        self.col = 8
        self.offset_x = display_w * .05
        self.offset_y = display_h * .15
        self.pack_info = packs_info[pack_id]
        self.tool = PacksTool(self.pack_info)

        # cards
        self.cards_surf = {}
        self.load_cards()
        self.cards = pygame.sprite.Group()
        self.set_cards(self.tool.get_all_cards_from_pack())
        self.counter_cards_total = len(self.cards)

        # container
        self.container = pygame.Rect([0, 0, 0, 0])
        self.container_floor = 0
        self.set_container()

        # rarity filter buttons
        self.filter_buttons = RarityFilters(pack_id, self.container_w, self.container.right, self.filter)

        # slide bar
        self.slide_bar = None
        self.set_slide_bar()

        # back buton
        filter_button_rect = self.filter_buttons.sprites()[0].rect
        button_back = ButtonIcon(2 * [filter_button_rect.h * .9], 'back', self.quit)
        button_back.rect.midleft = self.container.left, filter_button_rect.centery
        self.button_back = pygame.sprite.GroupSingle(button_back)

        # card pack counter
        filter_button = self.filter_buttons.sprites()[-1]
        counter_cards_w = filter_button.rect.left - self.container.left
        counter_cards_h = filter_button.rect.h * .5
        counter_cards = CounterPackCards(counter_cards_w, counter_cards_h)
        counter_cards.rect.bottomright = self.container.right, display_h * .9725
        self.counter_cards = pygame.sprite.GroupSingle(counter_cards)

    def check_events(self):
        for event in game.events:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or \
               (event.type == MOUSEBUTTONDOWN and event.button == 3):
                self.quit()

    def filter(self, rarity=''):
        if rarity:
            self.set_cards(self.pack_info[rarity])
        else:
            self.set_cards(self.tool.get_all_cards_from_pack())
        self.reset()

    def load_cards(self):
        cards = self.tool.get_all_cards_from_pack()
        self.cards_surf = {card_id: CardMiniature(card_id, self.pack_info) for card_id in cards}

    @staticmethod
    def quit():
        game.hovered.empty()
        game.screen = game.screens['choose']

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
        self.button_back.draw(surface)
        self.counter_cards.draw(surface)

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
        self.button_back.update()
        self.counter_cards.update(len(self.cards), self.counter_cards_total)


class PackFilterScreen:
    def __init__(self):

        # properties
        self.buttons = pygame.sprite.Group()
        self.buttons_filters = pygame.sprite.Group()
        self.cols = 5
        self.container_w = display_w * .8
        self.filters = []
        self.letters = ascii_uppercase
        self.offset_y = display_h * .05
        self.releases = []
        self.spacing = 10
        self.tags = []
        self.text_boxes = pygame.sprite.Group()

        # back button
        btn_back = ButtonIcon(2 * [display_w * .04], 'back', self.quit)
        btn_back.rect.topleft = 2 * [display_h * .025]

        # clean button
        btn_clean = ButtonIcon(btn_back.rect.size, 'clean', self.clean_filters)
        btn_clean.rect.topleft = btn_back.rect.left, btn_back.rect.bottom + display_h * .025

        self.buttons.add(btn_back, btn_clean)

        # get data from pack
        for pack_id in packs_info:
            pack = packs_info[pack_id]
            self.tags.append(pack["description"])
            self.releases.append(int(pack["release"]))
        self.tags = list(set(self.tags))[::-1]
        self.releases = sorted(list(set(self.releases)))

        # setup tags and buttons
        btn, last_right, last_bottom = None, display_w * .1, self.offset_y
        for f in [['Tags', self.tags], ['Release', self.releases], ['Name', self.letters]]:

            # text box
            tbox = TextBox(f[0], display_w * .8)
            tbox.rect.topleft = last_right, last_bottom
            self.text_boxes.add(tbox)
            tbox.yi = tbox.rect.y
            last_bottom = tbox.rect.bottom + self.spacing * 2

            # filter buttons
            btn_w = round((tbox.rect.w - (self.cols - 1) * self.spacing) / self.cols)
            rows = math.ceil(len(f[1]) / self.cols)
            for i in range(rows):
                for j in range(self.cols):
                    idx = i * self.cols + j
                    if len(f[1]) > idx:
                        btn = ButtonToggle(
                            width=btn_w,
                            height=tbox.rect.h,
                            text=str(f[1][idx]),
                            text_size=25,
                            on_activation=self.add_filter,
                            on_activation_args=[str(f[1][idx])],
                            on_deactivation=self.remove_filter,
                            on_deactivation_args=[str(f[1][idx])],
                            deactivate_on_click=True,
                        )
                        btn.rect.topleft = last_right, last_bottom
                        self.buttons.add(btn)
                        self.buttons_filters.add(btn)
                        last_right = btn.rect.right + self.spacing
                        btn.yi = btn.rect.y
                last_right = tbox.rect.left
                last_bottom = btn.rect.bottom + self.spacing
            last_bottom = btn.rect.bottom + self.spacing * 3

        # container
        container_size = tbox.rect.w, btn.rect.bottom - self.text_boxes.sprites()[0].rect.top
        self.container = pygame.Rect(*self.text_boxes.sprites()[0].rect.topleft, *container_size)
        floor = round(display_h - self.offset_y)
        self.container_floor = floor if self.container.bottom >= floor else self.container.bottom

        # slide bar
        distance = self.container.bottom - self.container_floor
        slider_r = 1 - distance / self.container.h
        slider_r = slider_r if slider_r < 1 else 1.
        self.slide_bar = SlideBar(slider_r)

    @staticmethod
    def add_filter(fl: str):
        screen = game.screens['choose']
        screen.filters.append(fl)
        screen.set_filters()

    def clean_filters(self):
        game.screens['choose'].filters.clear()
        for btn in self.buttons_filters.sprites():
            btn.deactivate()

    def draw(self, surface: pygame.Surface):
        surface.fill('black')
        surface.blit(game.bg, (0, 0))
        self.buttons.draw(surface)
        self.text_boxes.draw(surface)
        self.slide_bar.draw(surface)

    @staticmethod
    def quit():
        game.hovered.empty()
        game.screen = game.screens['choose']

    @staticmethod
    def remove_filter(fl: str):
        screen = game.screens['choose']
        if fl in screen.filters:
            screen.filters.remove(fl)
        screen.set_filters()

    def update_container_pos(self):
        p1 = self.slide_bar.bg_rect.bottom
        p2 = self.slide_bar.slider.sprite.rect.bottom
        h1 = self.container.h
        h2 = self.slide_bar.bg_rect.h
        dy = h1 / h2 * (p1 - p2)
        self.container.bottom = self.container_floor + dy

    def update_objs_pos(self):
        dy = self.offset_y - self.container.top
        for sprite in [*self.buttons_filters.sprites(), *self.text_boxes]:
            sprite.rect.y = sprite.yi - dy

    def update(self):
        self.buttons.update()
        self.slide_bar.update()
        self.update_container_pos()
        self.update_objs_pos()


class PullScreen(PackContentScreen):
    def __init__(self, pack_id: str, last_pull: list):
        super().__init__(pack_id)

        # properties
        self.card_list = last_pull
        self.card_set = list(set(self.card_list))
        self.organize_pull()

        # settings
        game.hovered.empty()
        self.set_counter()
        self.set_cards(self.card_set)
        self.reset()
        self.filter_buttons = RarityFilters(pack_id, self.container_w, self.container.right, self.filter)

    def filter(self, rarity=''):
        if rarity:
            self.set_cards(self.tool.get_rarities_from_list(self.card_set)[rarity])
        else:
            self.set_cards(self.card_set)
        self.reset()

    def organize_pull(self):
        organized_list = []
        for rarity in all_rarities[::-1]:
            if rarity in self.pack_info:
                for card_id in self.pack_info[rarity]:
                    if card_id in self.card_set:
                        organized_list.append(card_id)
        self.card_set = organized_list

    def set_counter(self):
        for card_id in self.cards_surf:
            self.cards_surf[card_id].blit_counter(self.card_list.count(card_id))


class SelectionScreen:
    def __init__(self):

        # properties
        self.filters = []
        self.packs = {}
        self.pack_hovered = None
        self.pack_locked = None
        self.spaccing = 7
        self.tags = {'tag': [], 'release': [], 'name': []}

        # settings
        self.preview_bg_w = round(0.213 * display_w) + 2 * self.spaccing
        self.set_tags()

        # packs
        self.load_packs()
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

        # buttons
        self.buttons = pygame.sprite.Group()

        # button detail setup
        button_w = round(self.preview_bg_w * .8)
        button_h = round(display_h * .05)
        button = ButtonText(button_w, button_h, 'Pack Content', self.go_to_pack_content_screen)
        button.rect.bottomleft = round(display_h * .025), round(display_h - display_h * .025)
        self.buttons.add(button)

        # button config setup
        button_h = display_h * .08
        button = ButtonIcon(2 * [button_h], 'config', self.go_to_config_screen)
        button.rect.topright = display_w - display_h * .025, display_h * .025
        last_left = button.rect.left
        self.buttons.add(button)

        # button filter setup
        button = ButtonIcon(2 * [button_h], 'filter', self.go_to_filter_screen)
        button.rect.topright = last_left - display_h * .025, display_h * .025
        self.buttons.add(button)

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
                            game.hovered.empty()
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

    @staticmethod
    def go_to_filter_screen():
        if "filter" not in game.screens:
            game.screens["filter"] = PackFilterScreen()
        game.hovered.empty()
        game.screen = game.screens["filter"]

    @staticmethod
    def go_to_config_screen():
        if "config" not in game.screens:
            game.screens["config"] = ConfigScreen()
        game.hovered.empty()
        game.screen = game.screens["config"]

    def go_to_pack_content_screen(self):
        if self.pack_hovered is not None:
            game.screen = PackContentScreen(self.pack_hovered)

    def load_packs(self):
        for pack_id in packs_info:
            self.packs[pack_id] = BoosterPack(pack_id, init_mode='mini')

    def set_description(self, pack, space=10):

        # setup description
        description = [f'{pack.info["description"]}',
                       f'Release: {pack.info["release"]}',
                       f'Cards per pack: {pack.info["#cards"]}']
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
        font = pygame.font.Font('fonts/Roboto-Regular.ttf', 13)
        last_bottom = space
        for i in description:
            text = font.render(i, True, 'white')
            text_rect = text.get_rect(topleft=(space, last_bottom))
            self.description.blit(text, text_rect)
            last_bottom = text_rect.bottom

    def set_filters(self):
        pack_list = list(packs_info.keys())
        if not self.filters:
            self.set_pages(pack_list)
            return

        tags = [fl for fl in self.filters if fl in self.tags['tag']]
        releases = [fl for fl in self.filters if fl in self.tags['release']]
        names = [fl for fl in self.filters if fl in self.tags['name']]

        # tag/description filter
        if tags:
            filtered_packs = [pack_id for pack_id in pack_list if packs_info[pack_id]['description'] in tags]
            pack_list = filtered_packs

        # release filter
        if releases:
            filtered_packs = [pack_id for pack_id in pack_list if packs_info[pack_id]['release'] in releases]
            pack_list = filtered_packs

        # name filter
        if names:
            filtered_packs = [pack_id for pack_id in pack_list if packs_info[pack_id]['name'][0][0] in names]
            pack_list = filtered_packs

        self.set_pages(pack_list)

    def set_pages(self, packs):
        """Creates a dict with all packs in position"""
        pack = BoosterPack('LOB')
        for i, page in enumerate(self.get_pages(packs)):
            pack_sprites = self.Packs()
            last_bottom = self.margin_y
            for row in page:
                last_right = self.preview_bg_w + self.margin_x
                for pack_id in row:
                    pack = self.packs[pack_id]
                    pack.mini.rect.topleft = last_right, last_bottom
                    pack_sprites.add(pack)
                    last_right = pack.mini.rect.right + self.spaccing
                last_bottom = pack.mini.rect.bottom + self.spaccing
            self.pages[i] = pack_sprites

    def set_tags(self):
        for pack in packs_info.values():
            if pack['description'] not in self.tags['tag']:
                self.tags['tag'].append(pack['description'])
            if pack['release'] not in self.tags['release']:
                self.tags['release'].append(pack['release'])
        self.tags['name'] = list(string.ascii_uppercase)

    def switch_next_page(self):
        if self.cur_page < len(self.pages) - 1:
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
        self.buttons.draw(surface)
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
        self.buttons.update()

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
    def __init__(self, current_pack, last_pull=[]):

        # properties
        self.pack_id = current_pack
        self.pack = BoosterPack(current_pack)
        self.cards = pygame.sprite.LayeredUpdates()
        self.card_moving = False
        self.open_pack = False
        self.rarity_viewed = False
        self.pull = last_pull

        # settings
        self.generate_pack(packs_info[current_pack])
        self.pack.rect.centerx = self.cards.sprites()[0].rect.centerx
        self.pack.rect.centery = self.cards.sprites()[0].rect.centery + self.pack.head_height / 2

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
        btn_new_pack = ButtonText(*btn_size, 'New Pack', self.new_pack)
        btn_new_pack.rect.bottomright = round(display_w * .985), round(display_h * .9725)
        btn_check_pull = ButtonText(*btn_size, 'Check Pull', self.check_pull)
        btn_check_pull.rect.bottomleft = round(display_w * .015), round(display_h * .9725)
        self.buttons.add(btn_new_pack, btn_check_pull)

        # card slide
        btn_h, btn_bottom = btn_new_pack.rect.h, btn_new_pack.rect.bottom
        self.slide_card = SlideCard(len(self.cards.sprites()), btn_h, btn_bottom, self.pack.info['rarity pos'])

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
        game.screen = PullScreen(self.pack_id, self.pull)

    def generate_pack(self, info):

        # setup
        self.cards.empty()
        cards = []

        # Fill with common cards
        commons_available = list(info['Common'])
        for _ in range(info['#cards'] - 1):
            card = random.choice(commons_available)
            cards.append(card)
            commons_available.remove(card)

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
            card.rect.center = display_c.x, round(display_c.y - card.rlabel.image.get_height())
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
        game.screens['unpack'] = UnpackScreen(self.pack_id, self.pull)
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
            self.buttons.draw(surface)
            self.slide_card.draw(surface)

    def update(self):
        self.check_event()
        if self.open_pack:
            self.cards.update()
            self.buttons.update()
            self.slide_card.update(self.counter)
        else:
            self.pack.update()


# UTILITY
class PacksTool:
    def __init__(self, pack_info: dict):
        self.pack_info = pack_info

    @staticmethod
    def get_all_cards():
        cards = []
        for pack in packs_info.values():
            for rarity in all_rarities:
                if rarity in pack:
                    cards += pack[rarity]
        return cards

    def get_all_cards_from_pack(self):
        main_card, rarities_list = self.pack_info['cover'], []
        if main_card in self.pack_info['Ultra Rare']:
            rarities_list = alt_rarities[::-1]
        elif 'Secret Rare' in self.pack_info and main_card in self.pack_info['Secret Rare']:
            rarities_list = all_rarities[::-1]
        cards_list = []
        rarities = [r for r in rarities_list if r in self.pack_info]
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
            for rarity in all_rarities:
                if rarity in self.pack_info and card_id in self.pack_info[rarity]:
                    rarities[rarity].append(card_id)
        return rarities


# APP
class Game:
    def __init__(self):
        # display
        self.display = pygame.display.set_mode((display_w, display_h))

        # icon
        icon = pygame.image.load('textures/icon.png').convert_alpha()
        pygame.display.set_icon(icon)

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
    display_c = pygame.math.Vector2(round(display_w / 2), round(display_h / 2))

    card_size = 288, 420
    card_mini_size = 118, 172

    # rarities
    rarity_symbol = {'Common': 'n', 'Rare': 'r', 'Super Rare': 'sr', 'Ultra Rare': 'ur', 'Secret Rare': 'se'}
    all_rarities = ('Common', 'Rare', 'Super Rare', 'Ultra Rare', 'Secret Rare')
    alt_rarities = ('Common', 'Rare', 'Secret Rare', 'Super Rare', 'Ultra Rare')

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

    print(PacksTool({}).get_all_cards())

    game.run()
