"""Alexsander Rosante's creation"""
import pygame
from pygame.locals import *
import random
import math

pygame.init()

packs_info = {0: {'name': ('Legend of', 'Blue Eyes White Dragon',),
                  'cover': '89631140',
                  'head height': 20,
                  '#cards': 9,
                  'Common': ('76184692',
                             '32274490',
                             '89091579',
                             '40374923',
                             '90357090',
                             '9159938',
                             '77827521',
                             '90963488',
                             '32864',
                             '34460851',
                             '36121917',
                             '53293545',
                             '53375573',
                             '2863439',
                             '37313348',
                             '75356564',
                             '38142739',
                             '96851799',
                             '15401633',
                             '57305373',
                             '40826495',
                             '39004808',
                             '18710707',
                             '22910685',
                             '85309439',
                             '84686841',
                             '83464209',
                             '44287299',
                             '85705804',
                             '87430998',
                             '23424603',
                             '50913601',
                             '86318356',
                             '22702055',
                             '59197169',
                             '38199696',
                             '76103675',
                             '46130346',
                             '51482758',
                             '72842870',
                             '32452818',
                             '1784619',
                             '36304921',
                             '94675535',
                             '20060230',
                             '93553943',
                             '56342351',
                             '92731455',
                             '53153481',
                             '63308047',
                             '98818516',
                             '98818516',
                             '76211194',
                             '75376965',
                             '71407486',
                             '33064647',
                             '85326399',
                             '45042329',
                             '10202894',
                             '73051941',
                             '33178416',
                             '29172562',
                             '55444629',
                             '43500484',
                             '16353197',
                             '17535588',
                             '55291359',
                             '4614116',
                             '77007920',
                             '39774685',
                             '1557499',
                             '1435851',
                             '37820550',
                             '36607978',
                             '77027445',
                             '91595718',
                             '15052462',
                             '46009906',
                             '61854111',
                             '51267887',
                             '98252586',
                             '25769732'),
                  'Rare': ('37421579',
                           '17881964',
                           '1641882',
                           '85639257',
                           '58528964',
                           '50045299',
                           '66788016',
                           '83887306',
                           '82542267',
                           '54541900',
                           '13039848',
                           '33066139',
                           '80770678',
                           '70681994',
                           '63102017',
                           '11868825',
                           '73134081',
                           '9293977',
                           '9076207',
                           '95952802',
                           '7089711',
                           '55144522'),
                  'Super Rare': ('45231177',
                                 '91152256',
                                 '53129443',
                                 '12580477',
                                 '4206964',
                                 '24094653',
                                 '15025844',
                                 '28279543',
                                 '72302403',
                                 '54652250'),
                  'Ultra Rare': ('89631140',
                                 '46986414',
                                 '6368038',
                                 '74677425',
                                 '83764719',
                                 '8124921',
                                 '44519536',
                                 '70903634',
                                 '7902349',
                                 '33396948'),
                  'Secret Rare': ('39111158',
                                  '66889139'),
                  '%R': 1,
                  '%SR': 5,
                  '%UR': 12,
                  '%SctR': 31,
                  },

              1: {'name': ('Lightning Overdrive',),
                  'cover': '75402014',
                  'head height': 22,
                  '#cards': 9,
                  'Common': ('32164201',
                             '68258355',
                             '67436768',
                             '30829071',
                             '66192538',
                             '92586237',
                             '65479980',
                             '91642007',
                             '27036706',
                             '53535814',
                             '80529459',
                             '89707961',
                             '15792576',
                             '52296675',
                             '88685329',
                             '15079028',
                             '51474037',
                             '87468732',
                             '14957440',
                             '49407319',
                             '36346532',
                             '4017398',
                             '31002402',
                             '7496001',
                             '6374519',
                             '69167267',
                             '6552971',
                             '32056070',
                             '68045685',
                             '5439384',
                             '68223137',
                             '94317736',
                             '31712840',
                             '67100549',
                             '93595154',
                             '93473606',
                             '29867611',
                             '55262310',
                             '28645123',
                             '91534476',
                             '27923575',
                             '54927180',
                             '11110218',
                             '84903021',
                             '19275188',
                             '46660187',
                             '76029419',
                             '80088625',
                             '7984540',
                             '70473293',),
                  'Rare': ('92919429',
                           '94821366',
                           '26914168',
                           '40139997',
                           '1174075',
                           '73345237',
                           '70389815',
                           '10497636',
                           '53318263',
                           '31834488'),
                  'Super Rare': ('31042659',
                                 '93708824',
                                 '29107423',
                                 '29981935',
                                 '91864689',
                                 '76524506',
                                 '12018201',
                                 '2896663',
                                 '48285768',
                                 '47163170',
                                 '74567889',
                                 '36224040',
                                 '62623659',
                                 '34995106',
                                 '33773528',
                                 '20989253',
                                 '85847157',
                                 '12332865',
                                 '58720904',
                                 '84125619',
                                 '47504322',
                                 '83880473',
                                 '96352326',
                                 '49964567',
                                 '44478599',
                                 '9839945'),
                  'Ultra Rare': ('4647954',
                                 '67314110',
                                 '28868394',
                                 '40352445',
                                 '87746184',
                                 '13735899',
                                 '75402014',
                                 '74689476',
                                 '952523',
                                 '66984907',
                                 '92650018',
                                 '55049722',
                                 '47882774',
                                 '54257392',
                                 '73580471'),
                  'Secret Rare': (),
                  '%R': 1,
                  '%SR': 2,
                  '%UR': 6,
                  '%SctR': 0,
                  }}


# OBJECTS

class Card(pygame.sprite.Sprite):
    def __init__(self, code, rarity='Common'):
        super().__init__()

        self.pic = pygame.image.load(f'pics/{code}.jpg')
        self.width, self.height = 288, 420

        self.image = pygame.transform.smoothscale(self.pic.convert(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2()
        self.anim = self.idle

        if rarity != 'Common':  # make a function?
            label = pygame.sprite.Sprite()
            try:
                label.image = pygame.image.load(f'pics/booster/{rarity}.png').convert_alpha()
            except FileNotFoundError:
                label_info = {'Rare':        {'Text': 'R', 'Color': (48, 124, 243)},
                              'Super Rare':  {'Text': 'SR', 'Color': (248, 209, 0)},
                              'Ultra Rare':  {'Text': 'UR', 'Color': (13, 230, 234)},
                              'Secret Rare': {'Text': 'SE', 'Color': (32, 32, 32)}}
                font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 18)
                font.set_bold(True)
                label.image = pygame.Surface((83, 21))
                label.image.fill(label_info[rarity]['Color'])
                text = font.render(label_info[rarity]['Text'], True, Color('white'), label_info[rarity]['Color'])
                text_rect = text.get_rect(center=(label.image.get_width()/2, label.image.get_height()/2))
                label.image.blit(text, text_rect)
            label.rect = label.image.get_rect(topright=self.rect.topright)
            self.image.blit(label.image, label.rect)

    def update(self):
        self.rect.center += self.vel
        self.anim()

    def idle(self):
        pass

    def move_to_back(self, speed=20.):
        cards = game.screen.cards
        if self == cards.get_top_sprite():
            if self.rect.left < game.display_w / 2 + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = game.display_w / 2 + self.width / 2
                self.vel.x = 0.
                cards.move_to_back(self)
        else:
            if self.rect.centerx > game.display_w / 2:
                self.vel.x = -speed
            else:
                self.rect.centerx = game.display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.screen.card_moving = False

    def move_to_front(self, speed=20.):
        cards = game.screen.cards
        if self == game.screen.get_bottom_card():
            if self.rect.left < game.display_w / 2 + self.width / 2:
                self.vel.x = speed
            else:
                self.rect.left = game.display_w / 2 + self.width / 2
                self.vel.x = 0.
                cards.move_to_front(self)
        else:
            if self.rect.centerx > game.display_w / 2:
                self.vel.x = -speed
            else:
                self.rect.centerx = game.display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.screen.card_moving = False


def get_rarity(pack_info, card):
    for i in ('Common', 'Rare', 'Super Rare', 'Ultra Rare', 'Secret Rare'):
        if card in pack_info[i]:
            return i


class BoosterPack(pygame.sprite.Group):
    def __init__(self, n):
        super().__init__()

        self.n = n
        info = packs_info[n]
        width, height = 290, 530
        head_height = info['head height']
        self.openning = False

        # head
        self.head = pygame.sprite.Sprite()
        self.head.image = pygame.Surface((width, head_height), SRCALPHA)

        # body
        self.body = pygame.sprite.Sprite()
        self.body.image = pygame.Surface((width, height - head_height), SRCALPHA)

        try:
            self.img = pygame.image.load(f'pics/booster/{n}.png').convert_alpha()
            self.head.image.blit(self.img, (0, 0))
            self.body.image.blit(self.img, (0, -head_height))
        except FileNotFoundError:
            skin = pygame.image.load('skin/Purple - Obsessed/button.png').convert_alpha()
            self.img = pygame.transform.smoothscale(skin.copy(), (width, head_height))
            self.head.image.blit(self.img, (0, 0))
            self.img = pygame.transform.smoothscale(skin.copy(), (width, height - head_height))
            self.body.image.blit(self.img, (0, 0))

            # pack's cover art
            cover_img = pygame.transform.smoothscale(pygame.image.load(f'pics/{info["cover"]}.jpg').convert(),
                                                     (288, 420))
            cover = pygame.Surface((222, 222))
            cover.blit(cover_img, (-33, -75))
            cover_rect = cover.get_rect(center=(width / 2, 1 / 3 * height))
            self.body.image.blit(cover, cover_rect)

            # pack's name
            font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 23)
            last_bottom = cover_rect.bottom + 10
            for i in info['name']:
                text = font.render(i, True, Color('white'))
                text_rect = text.get_rect(midtop=(cover_rect.centerx, last_bottom))
                self.body.image.blit(text, text_rect)
                last_bottom = text_rect.bottom

        self.add(self.head, self.body)

        # Positioning
        self.rect = pygame.Rect(367, 35, 1, 1)
        self.head.rect = self.head.image.get_rect(topleft=self.rect.topleft)
        self.body.rect = self.body.image.get_rect(topleft=self.head.rect.bottomleft)

    def update(self):
        if self.openning:
            self.unpack()
        else:
            self.head.rect.topleft = self.rect.topleft
            self.body.rect.topleft = self.head.rect.bottomleft

        super().update()

    def draw(self, surface):
        super().draw(surface)

    def unpack(self, speed=18):
        head_width = self.head.image.get_width() - speed
        if head_width <= 0:
            self.remove(self.head)
            if self.body.rect.top <= game.display_h:
                self.body.rect.y += speed
            else:
                game.screen.open_pack = True
        else:
            self.head.image = pygame.transform.scale(self.head.image.copy(),
                                                     (head_width, self.head.image.get_height()))
            self.head.rect = self.head.image.get_rect(bottomright=self.body.rect.topright)

    def hovered(self, event_pos):
        if self.head.rect.collidepoint(event_pos) or self.body.rect.collidepoint(event_pos):
            return True
        return False


# SCREENS

class SelectionScreen:
    def __init__(self):
        self.packs = []

        # packs setup
        space = 10
        last_right = space
        for i in packs_info:
            pack = BoosterPack(i)
            pack.rect.topleft = last_right + space, 35
            pack.update()
            self.packs.append(pack)
            last_right = pack.body.rect.right

    def update(self):
        self.event_check()
        for pack in self.packs:
            pack.update()

    def draw(self, surface):
        surface.fill((33, 23, 34))
        for pack in self.packs:
            pack.draw(surface)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                for pack in self.packs:
                    if pack.hovered(event.pos):
                        game.screens['unpack'] = UnpackScreen(pack.n)
                        game.screen = game.screens['unpack']


class UnpackScreen:
    def __init__(self, current_pack):
        pack = packs_info[current_pack]
        self.pack = BoosterPack(current_pack)
        self.cards = pygame.sprite.LayeredUpdates()
        self.generate_pack(pack)
        self.card_moving = False
        self.open_pack = False

        self.bg_color = (33, 23, 34)

        # counter
        self.counter = 1
        for card in self.cards:
            self.card_midbottom = card.rect.midbottom
            break

        self.font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 20)
        self.font.set_bold(True)

    def update(self):
        self.event_check()
        if self.open_pack:
            self.cards.update()
        else:
            self.pack.update()

    def draw(self, surface):
        surface.fill(self.bg_color)
        self.cards.draw(surface)

        # counter
        counter = self.font.render(f'({self.counter}/{len(self.cards)})', True, Color('white'), self.bg_color)
        counter_rect = counter.get_rect(midtop=(self.card_midbottom[0] + 13, self.card_midbottom[1]))
        surface.blit(counter, counter_rect)

        self.pack.draw(surface)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False

            # Mouse input
            elif event.type == MOUSEBUTTONDOWN:
                if self.open_pack:
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            if not self.card_moving:
                                if event.button == 1:
                                    chosen_card = self.get_top_card()
                                    chosen_card.anim = chosen_card.move_to_back
                                    self.counter += 1
                                    if self.counter > len(self.cards):
                                        self.counter = 1
                                elif event.button == 3:
                                    chosen_card = self.get_bottom_card()
                                    chosen_card.anim = chosen_card.move_to_front
                                    self.counter -= 1
                                    if self.counter < 1:
                                        self.counter = len(self.cards)
                                else:
                                    break
                                self.card_moving = True
                                break
                else:
                    if event.button == 1 or 3:
                        self.pack.openning = True

            # keyboard input
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.screen = game.screens['choose']

    def generate_pack(self, info):
        self.cards.empty()

        # Get Cards:
        # Fill with common cards
        cards = [random.choice(info['Common']) for _ in range(info['#cards'] - 1)]
        # Get the rare card
        rarity = {'Super Rare': info['%SR'], 'Ultra Rare': info['%UR'], 'Secret Rare': info['%SctR']}
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
        cards.insert(info['#cards'] // 2, picked_rare)

        # Put cards into pack:
        for index, code in enumerate(cards):
            card = Card(code, get_rarity(info, code))
            card.rect.center = 512, 300  # Screen center
            self.cards.add(card)
            self.cards.change_layer(card, index)

    def get_top_card(self):
        return self.cards.get_top_sprite()

    def get_bottom_card(self):
        bottom_card, bottom_layer = None, 5
        for card in self.cards:
            if card.layer < bottom_layer:
                bottom_layer = card.layer
                bottom_card = card
        return bottom_card


# APP
class Game:
    def __init__(self):
        # display
        self.display_w, self.display_h = 1024, 600
        self.display = pygame.display.set_mode((self.display_w, self.display_h))
        pygame.display.set_caption('Booster Packs')

        # properties
        self.clock = pygame.time.Clock()
        self.loop = True
        self.events = pygame.event.get()

        self.screens = {'unpack': UnpackScreen(0),
                        'choose': SelectionScreen()}
        self.screen = self.screens['choose']

    def run(self):
        while self.loop:
            self.event_check()
            self.screen.update()
            self.screen.draw(self.display)
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

    def event_check(self):
        self.events = pygame.event.get()


if __name__ == '__main__':
    game = Game()
    game.run()
