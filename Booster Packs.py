"""Alexsander Rosante's creation"""
import pygame
from pygame.locals import *
import random
import math

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
               '%R': 1,
               '%SR': 5,
               '%UR': 12}

packs_info = {0: {'name': ('Legend of', 'Blue Eyes White Dragon',),
                  'cover': '89631140',
                  '#cards': 9,
                  'head height': 20,
                  'rarity pos': 'middle',

                  'Common': ('76184692', '32274490', '89091579', '40374923', '90357090', '9159938', '77827521',
                             '90963488', '32864', '34460851', '36121917', '53293545', '53375573', '2863439',
                             '37313348', '75356564', '38142739', '96851799', '15401633', '57305373', '40826495',
                             '39004808', '18710707', '22910685', '85309439', '84686841', '83464209', '44287299',
                             '85705804', '87430998', '23424603', '50913601', '86318356', '22702055', '59197169',
                             '38199696', '76103675', '46130346', '51482758', '72842870', '32452818', '1784619',
                             '36304921', '94675535', '20060230', '93553943', '56342351', '92731455', '53153481',
                             '63308047', '98818516', '98818516', '76211194', '75376965', '71407486', '33064647',
                             '85326399', '45042329', '10202894', '73051941', '33178416', '29172562', '55444629',
                             '43500484', '16353197', '17535588', '55291359', '4614116', '77007920', '39774685',
                             '1557499', '1435851', '37820550', '36607978', '77027445', '91595718', '15052462',
                             '46009906', '61854111', '51267887', '98252586', '25769732'
                             ),
                  'Rare': ('37421579', '17881964', '1641882', '85639257', '58528964', '50045299', '66788016',
                           '83887306', '82542267', '54541900', '13039848', '33066139', '80770678', '70681994',
                           '63102017', '11868825', '73134081', '9293977', '9076207', '95952802', '7089711',
                           '55144522'
                           ),
                  'Super Rare': ('45231177', '91152256', '53129443', '12580477', '4206964', '24094653', '15025844',
                                 '28279543', '72302403', '54652250'
                                 ),
                  'Ultra Rare': ('89631140', '46986414', '6368038', '74677425', '83764719', '8124921', '44519536',
                                 '70903634', '7902349', '33396948', '39111158', '66889139'
                                 ),
                  '%R': 1,
                  '%SR': 5,
                  '%UR': 12,
                  },
              1: {'name': ('Lightning Overdrive',),
                  'cover': '75402014',
                  '#cards': 9,
                  'head height': 22,
                  'rarity pos': 'middle',
                  'Common': ('32164201', '68258355', '67436768', '30829071', '66192538', '92586237', '65479980',
                             '91642007', '27036706', '53535814', '80529459', '89707961', '15792576', '52296675',
                             '88685329', '15079028', '51474037', '87468732', '14957440', '49407319', '36346532',
                             '4017398', '31002402', '7496001', '6374519', '69167267', '6552971', '32056070',
                             '68045685', '5439384', '68223137', '94317736', '31712840', '67100549', '93595154',
                             '93473606', '29867611', '55262310', '28645123', '91534476', '27923575', '54927180',
                             '11110218', '84903021', '19275188', '46660187', '76029419', '80088625', '7984540',
                             '70473293'
                             ),
                  'Rare': ('92919429', '94821366', '26914168', '40139997', '1174075', '73345237', '70389815',
                           '10497636', '53318263', '31834488'
                           ),
                  'Super Rare': ('31042659', '93708824', '29107423', '29981935', '91864689', '76524506', '12018201',
                                 '2896663', '48285768', '47163170', '74567889', '36224040', '62623659', '34995106',
                                 '33773528', '20989253', '85847157', '12332865', '58720904', '84125619', '47504322',
                                 '83880473', '96352326', '49964567', '44478599', '9839945'
                                 ),
                  'Ultra Rare': ('4647954', '67314110', '28868394', '40352445', '87746184', '13735899', '75402014',
                                 '74689476', '952523', '66984907', '92650018', '55049722', '47882774', '54257392',
                                 '73580471'
                                 ),
                  '%R': 1,
                  '%SR': 2,
                  '%UR': 6,
                  },
              2: {'name': ('Eternal Stream',),
                  'cover': '39272762',
                  '#cards': 3,
                  'head height': 86,
                  'rarity pos': 'end',
                  'Common': ('46918794',),
                  'Rare': ('18446701',),
                  'Super Rare': ('4206964',),
                  'Ultra Rare': ('39272762',),
                  '%R': 1,
                  '%SR': 5,
                  '%UR': 12}

              }

# SFXs
sfx_open_pack = pygame.mixer.Sound('sound/attack.wav')
sfx_next_card = pygame.mixer.Sound('sound/draw.wav')


# OBJECTS
class Card(pygame.sprite.Sprite):
    def __init__(self, card_id, pack_info):
        super().__init__()

        self.id = card_id
        self.rarity = self.get_rarity(pack_info)
        self.pic = pygame.image.load(f'pics/{card_id}.jpg')
        self.width, self.height = 288, 420

        self.image = pygame.transform.smoothscale(self.pic.convert(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2()
        self.anim = self.idle

        label = pygame.sprite.Sprite()
        try:
            label.image = pygame.image.load(f'pics/booster/{self.rarity}.png').convert_alpha()
        except FileNotFoundError:
            label_info = {'Common': {'symbol': 'N', 'color': (182, 200, 203)},
                          'Rare': {'symbol': 'R', 'color': (48, 124, 243)},
                          'Super Rare': {'symbol': 'SR', 'color': (248, 209, 0)},
                          'Ultra Rare': {'symbol': 'UR', 'color': (13, 230, 234)}}
            font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 18)
            font.set_bold(True)
            label.image = pygame.Surface((83, 21))
            label.image.fill(label_info[self.rarity]['color'])
            text = font.render(label_info[self.rarity]['symbol'], True, Color('white'),
                               label_info[self.rarity]['color'])
            text_rect = text.get_rect(center=(label.image.get_width() / 2, label.image.get_height() / 2))
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

    def get_rarity(self, pack_info):
        for rarity in ('Common', 'Rare', 'Super Rare', 'Ultra Rare'):
            if self.id in pack_info[rarity]:
                return rarity


class BoosterPack(pygame.sprite.Group):
    def __init__(self, n):
        super().__init__()

        self.n = n
        self.info = packs_info[n]
        self.width, self.height = 290, 530
        self.head_height = self.info['head height']
        self.openning = False

        # surface
        surface = self.get_surface()

        # head
        self.head = pygame.sprite.Sprite()
        self.head.image = pygame.Surface((self.width, self.head_height), SRCALPHA)
        self.head.image.blit(surface, (0, 0))

        # body
        self.body = pygame.sprite.Sprite()
        self.body.image = pygame.Surface((self.width, self.height - self.head_height), SRCALPHA)
        self.body.image.blit(surface, (0, -self.head_height))

        # positioning
        self.rect = pygame.Rect(367, 35, 1, 1)
        self.head.rect = self.head.image.get_rect(topleft=self.rect.topleft)
        self.body.rect = self.body.image.get_rect(topleft=self.head.rect.bottomleft)

        # view
        self.view = pygame.sprite.Sprite()
        self.view.image = pygame.transform.smoothscale(surface.copy(), (self.width, self.height))
        self.view.rect = self.view.image.get_rect()

        # miniature
        self.mini = pygame.sprite.Sprite()

        self.add(self.body, self.head)

    def update(self):
        if self.openning:
            self.unpack()
        else:
            self.head.rect.topleft = self.rect.topleft
            self.body.rect.topleft = self.head.rect.bottomleft
            self.view.rect.topleft = self.rect.topleft

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

    def get_surface(self):
        try:
            surface = pygame.image.load(f'pics/booster/{self.n}.png').convert_alpha()
        except FileNotFoundError:

            # presets
            self.head_height = 40
            surface = pygame.Surface((self.width, self.height))

            # head
            head = pygame.Surface((self.width, self.head_height))
            head.fill((43, 43, 43))
            surface.blit(head, (0, 0))

            # body
            body_height = self.height - self.head_height
            body = self.get_cropped_art(self.info['cover'])
            body = pygame.transform.smoothscale(body.copy(), (body_height, body_height))
            surface.blit(body, (-surface.get_width()/2, self.head_height))

            # name
            font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 23)
            last_bottom = 2/3 * surface.get_height()
            for i in self.info['name']:
                text = font.render(i, True, Color('white'), Color('black'))
                text_rect = text.get_rect(midtop=(surface.get_width()/2, last_bottom))
                surface.blit(text, text_rect)
                last_bottom = text_rect.bottom

        return surface

    @staticmethod
    def get_cropped_art(card_id):
        pic = pygame.image.load(f'pics/{card_id}.jpg').convert()
        pic = pygame.transform.smoothscale(pic.copy(), (421, 614))
        art = pygame.Surface((323, 323))
        art.blit(pic, (-48, -110))
        return art


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
        surface.fill((0, 0, 0))
        surface.blit(game.bg, (0, 0))
        for pack in self.packs:
            pack.draw(surface)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for pack in self.packs:
                        if pack.hovered(event.pos):
                            game.screens['unpack'] = UnpackScreen(pack.n)
                            game.screen = game.screens['unpack']
                elif event.button == 4:
                    for pack in self.packs:
                        pack.rect.x -= 80
                elif event.button == 5:
                    for pack in self.packs:
                        pack.rect.x += 80


class UnpackScreen:
    def __init__(self, current_pack):
        pack = packs_info[current_pack]
        self.pack = BoosterPack(current_pack)
        self.cards = pygame.sprite.LayeredUpdates()
        self.generate_pack(pack)
        self.card_moving = False
        self.open_pack = False

        # counter
        self.counter = 1
        for card in self.cards:
            self.card_midbottom = card.rect.midbottom
            break

        self.font = pygame.font.Font('fonts/NotoSansJP-Regular.otf', 20)
        self.font.set_bold(True)

        self.detail_button = pygame.Rect(376, 320, 271, 180)

    def update(self):
        self.event_check()
        if self.open_pack:
            self.cards.update()
        else:
            self.pack.update()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(game.bg, (0, 0))
        self.cards.draw(surface)

        # counter
        counter = self.font.render(f'({self.counter}/{len(self.cards)})', True, Color('white'))
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
                                    sfx_next_card.play()
                                    self.counter += 1
                                    if self.counter > len(self.cards):
                                        self.counter = 1
                                elif event.button == 3:
                                    chosen_card = self.get_bottom_card()
                                    chosen_card.anim = chosen_card.move_to_front
                                    sfx_next_card.play()
                                    self.counter -= 1
                                    if self.counter < 1:
                                        self.counter = len(self.cards)
                                else:
                                    break
                                self.card_moving = True
                                break
                    if self.detail_button.collidepoint(event.pos) and event.button == 2:
                        game.screens['detail'] = DetailScreen(self.get_top_card().id)
                        game.screen = game.screens['detail']

                else:
                    if event.button == 1 or event.button == 3:
                        if not self.pack.openning:
                            self.pack.openning = True
                            sfx_open_pack.play()

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
            card.rect.center = 512, 300  # Screen center
            self.cards.add(card)
            self.cards.change_layer(card, index)

        # purchase cards
        game.purchase += cards

    def get_top_card(self):
        return self.cards.get_top_sprite()

    def get_bottom_card(self):
        bottom_card, bottom_layer = None, 5
        for card in self.cards:
            if card.layer < bottom_layer:
                bottom_layer = card.layer
                bottom_card = card
        return bottom_card


class DetailScreen:
    def __init__(self, card_id):
        card = pygame.sprite.Sprite()
        card.image = pygame.image.load(f'pics/{card_id}.jpg')
        card_w, card_h = card.image.get_size()
        card.image = pygame.transform.smoothscale(card.image,
                                                  (624, round(card_h / card_w * 624)))
        card.rect = card.image.get_rect(midbottom=(512, 500))
        self.card = pygame.sprite.GroupSingle(card)

    def update(self):
        self.event_check()
        self.card.update()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(game.bg, (0, 0))
        self.card.draw(surface)

    def event_check(self):
        for event in game.events:
            if event.type == QUIT:
                game.loop = False
            elif event.type == MOUSEBUTTONDOWN:
                self.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()

    @staticmethod
    def quit():
        game.screen = game.screens['unpack']


# APP
class Game:
    def __init__(self):
        # display
        self.display_w, self.display_h = 1024, 600
        self.display = pygame.display.set_mode((self.display_w, self.display_h))
        pygame.display.set_caption('Booster Packs')

        # bg
        self.bg = pygame.transform.smoothscale(
            pygame.image.load('textures/bg_deck.png').convert(),
            (self.display_w, self.display_h)
        )
        self.bg.set_alpha(128)

        # properties
        self.clock = pygame.time.Clock()
        self.loop = True
        self.events = pygame.event.get()

        self.screens = {}
        self.screen = None

        self.purchase = []

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

    def event_check(self):
        self.events = pygame.event.get()

    def save_purchase(self):
        with open('deck/Booster Packs.ydk', 'w') as deck:
            deck.write('#Created by AlexsanderRosante\n')
            deck.write('#main\n')
            for card in self.purchase:
                deck.write(card + '\n')
            deck.write('#extra\n')
            deck.write('!side\n')


if __name__ == '__main__':
    game = Game()
    game.run()
