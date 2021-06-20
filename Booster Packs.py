"""Alexsander Rosante's creation"""
import pygame
from pygame.locals import *
import random
import math

pygame.init()

packs_info = {0: {'name': 'Legend of Blue Eyes White Dragon',
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
                  }}


class Card(pygame.sprite.Sprite):
    def __init__(self, code, rarity='Common'):
        super().__init__()

        self.pic = pygame.image.load(f'pics/{code}.jpg')
        self.width, self.height = 288, 420

        self.image = pygame.transform.smoothscale(self.pic.convert(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2()
        self.anim = self.idle

        if rarity != 'Common':
            label = pygame.sprite.Sprite()
            label.image = pygame.image.load(f'pics/booster/{rarity}.png').convert_alpha()
            label.rect = label.image.get_rect(topright=self.rect.topright)
            self.image.blit(label.image, label.rect)

    def update(self):
        self.rect.center += self.vel
        self.anim()

    def idle(self):
        pass

    def move_to_back(self):
        if self == game.cards.get_top_sprite():
            if self.rect.left < game.display_w / 2 + self.width / 2:
                self.vel.x = 32.
            else:
                self.rect.left = game.display_w / 2 + self.width / 2
                self.vel.x = 0.
                game.cards.move_to_back(self)
        else:
            if self.rect.centerx > game.display_w / 2:
                self.vel.x = -16.
            else:
                self.rect.centerx = game.display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.card_moving = False

    def move_to_front(self):
        if self == game.get_bottom_card():
            if self.rect.left < game.display_w / 2 + self.width / 2:
                self.vel.x = 16.
            else:
                self.rect.left = game.display_w / 2 + self.width / 2
                self.vel.x = 0.
                game.cards.move_to_front(self)
        else:
            if self.rect.centerx > game.display_w / 2:
                self.vel.x = -16.
            else:
                self.rect.centerx = game.display_w / 2
                self.vel.x = 0.
                self.anim = self.idle
                game.card_moving = False


class BoosterPack(pygame.sprite.Group):
    def __init__(self, n):
        super().__init__()

        info = packs_info[n]
        width, height = 290, 530
        head_height = info['head height']

        # head
        self.head = pygame.sprite.Sprite()
        self.head.image = pygame.Surface((width, head_height), SRCALPHA)
        self.head.rect = self.head.image.get_rect(topleft=(367, 35))

        # body
        self.body = pygame.sprite.Sprite()
        self.body.image = pygame.Surface((width, height - head_height), SRCALPHA)
        self.body.rect = self.body.image.get_rect(topleft=self.head.rect.bottomleft)

        try:
            self.img = pygame.image.load('pics/booster/0.png').convert()
            self.head.image.blit(self.img, (0, 0))
            self.body.image.blit(self.img, (0, -head_height))
        except FileNotFoundError:
            skin = pygame.image.load('skin/Purple - Obsessed/button.png').convert_alpha()
            self.img = pygame.transform.smoothscale(skin.copy(), (width, head_height))
            self.head.image.blit(self.img, (0, 0))
            self.img = pygame.transform.smoothscale(skin.copy(), (width, height - head_height))
            self.body.image.blit(self.img, (0, 0))

            # test
            cover_img = pygame.transform.smoothscale(pygame.image.load(f'pics/{info["cover"]}.jpg').convert(),
                                                     (288, 420))
            cover = pygame.Surface((222, 222))
            cover.blit(cover_img, (-33, -75))
            cover_rect = cover.get_rect(center=(width/2, 1/3*height))
            self.body.image.blit(cover, cover_rect)

        self.add(self.head, self.body)

        self.openning = False

    def update(self):
        if self.openning:
            self.unpack()
        super().update()

    def draw(self, surface):
        super().draw(surface)

    def unpack(self, speed=12):
        head_width = self.head.image.get_width() - speed
        if head_width <= 0:
            self.remove(self.head)
            if self.body.rect.top <= game.display_h:
                self.body.rect.y += speed
            else:
                game.open_pack = True
        else:
            self.head.image = pygame.transform.scale(self.head.image.copy(),
                                                     (head_width, self.head.image.get_height()))
            self.head.rect = self.head.image.get_rect(bottomright=self.body.rect.topright)


class Game:
    def __init__(self):
        # display
        self.display_w, self.display_h = 1024, 600
        self.display = pygame.display.set_mode((self.display_w, self.display_h))
        pygame.display.set_caption('Booster Packs')

        self.clock = pygame.time.Clock()
        self.loop = True
        self.events = pygame.event.get()
        
        # status
        self.card_moving = False
        self.open_pack = False

        # properties
        self.cards = pygame.sprite.LayeredUpdates()

        self.current_pack = 0
        pack = packs_info[self.current_pack]
        self.generate_pack(pack)
        self.pack = BoosterPack(self.current_pack)

    def run(self):
        while self.loop:
            self.event_check()

            # update
            if self.open_pack:
                self.cards.update()
            else:
                self.pack.update()

            # draw
            self.display.fill((33, 23, 34))
            self.cards.draw(self.display)
            self.pack.draw(self.display)

            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()

    def event_check(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                #
                if self.open_pack:
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            if not self.card_moving:
                                if event.button == 1:
                                    selected_card = self.get_top_card()
                                    selected_card.anim = selected_card.move_to_back
                                elif event.button == 3:
                                    selected_card = self.get_bottom_card()
                                    selected_card.anim = selected_card.move_to_front
                                else:
                                    break
                                self.card_moving = True
                                break
                else:
                    self.pack.openning = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.new_pack()

    def get_top_card(self):
        return self.cards.get_top_sprite()

    def get_bottom_card(self):
        bottom_card, bottom_layer = None, 5
        for card in self.cards:
            if card.layer < bottom_layer:
                bottom_layer = card.layer
                bottom_card = card
        return bottom_card

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
            card = Card(code, self.get_rarity(info, code))
            card.rect.center = self.display_w / 2, self.display_h / 2
            self.cards.add(card)
            self.cards.change_layer(card, index)

    def new_pack(self):
        pack = packs_info[self.current_pack]
        self.generate_pack(pack)
        self.pack = BoosterPack(self.current_pack)
        self.open_pack = False

    @staticmethod
    def get_rarity(pack_info, card):
        for i in ('Common', 'Rare', 'Super Rare', 'Ultra Rare', 'Secret Rare'):
            if card in pack_info[i]:
                return i


if __name__ == '__main__':
    game = Game()
    game.run()
