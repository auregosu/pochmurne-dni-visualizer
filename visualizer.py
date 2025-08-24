import mido
import time
import threading
import pygame
from just_playback import Playback

dt = 0

class Shadow(pygame.sprite.Sprite):
    def __init__(self, filename="", opacity=128, fade_rate=100):
        super().__init__()
        if filename != "":
            self.image = pygame.image.load(filename)
            self.image.set_alpha(int(opacity))
            self.rect = self.image.get_rect()
        self.starting_opacity = opacity
        self.opacity = opacity
        self.fade_rate = fade_rate

class Lyrics(Shadow):
    def __init__(self):
        super().__init__(opacity=0, fade_rate=50)
        self.spritesheet = pygame.image.load("assets/lyrics.png")
        self.animation = []
        for x in range(42):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()
        self.frame = -1
        self.x = 0
        # 0 - still
        # 1 - fade in
        # 2 - fade out
        self.state = 0

    def update(self):
        match self.state:
            case 1:
                if self.opacity <= 150:
                    self.opacity += (1050/self.fade_rate)*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))
            case 2:
                if self.opacity >= 0:
                    self.opacity -= (1050/self.fade_rate)*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))
        self.x += 3*dt
        self.rect.x = self.x

    def fade_out(self, rate):
        self.state = 2
        self.fade_rate = rate

    def fade_in(self, rate):
        self.state = 1
        self.fade_rate = rate
        self.frame = (self.frame + 1) % 42
        self.image = self.animation[self.frame]
        self.image.set_alpha(int(self.opacity))
        self.x = -10
        self.rect.x = self.x

class LightsRight(Shadow):
    active = False
    def __init__(self):
        super().__init__(opacity=0, fade_rate=125)
        self.spritesheet = pygame.image.load("assets/lights-right.png")
        self.animation = []
        for x in range(12):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()

    def update(self):
        self.opacity -= self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

    def change_note(self, note):
        self.opacity = 255
        # range from 59 to 86
        self.image = self.animation[note]
        self.image.set_alpha(int(self.opacity))


class LightsLeft(Shadow):
    def __init__(self):
        super().__init__(opacity=0, fade_rate=125)
        self.spritesheet = pygame.image.load("assets/lights-left.png")
        self.animation = []
        for x in range(12):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()

    def update(self):
        self.opacity -= self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

    def change_note(self, note):
        self.opacity = 255
        # range from 59 to 86
        self.image = self.animation[note]
        self.image.set_alpha(int(self.opacity))

class Night(Shadow):
    def __init__(self):
        super().__init__(opacity=0, fade_rate=4)
        self.spritesheet = pygame.image.load("assets/night.png")
        self.animation = []
        for x in range(5):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()
        self.frame = 0
        # 0 - still
        # 1 - fade in
        # 2 - fade out
        self.state = 0
    def update(self):
        match self.state:
            case 1:
                if self.opacity <= 255:
                    self.opacity += self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))
            case 2:
                if self.opacity >= 0:
                    self.opacity -= self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))

    def change_state(self, state):
        self.state = state

    def next_frame(self):
            self.frame = (self.frame + 1) % 5
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.image.set_alpha(int(self.opacity))

class Rainclouds(Shadow):
    def __init__(self):
        super().__init__(opacity=0, fade_rate=50)
        self.spritesheet = pygame.image.load("assets/rainclouds.png")
        self.animation = []
        for x in range(10):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()
        self.frame = 0
        # 0 - still
        # 1 - fade in
        # 2 - fade out
        # 3 - move with bass
        self.state = 0
    def update(self):
        match self.state:
            case 1:
                if self.opacity <= 255:
                    self.opacity += self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))
            case 2:
                if self.opacity >= 0:
                    self.opacity -= self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))

    def change_state(self, state):
        self.state = state

    def next_frame(self):
            self.frame = (self.frame + 1) % 10
            self.image = self.animation[self.frame]
            self.image.set_alpha(int(self.opacity))

class Rain(Shadow):
    def __init__(self):
        super().__init__(opacity=0, fade_rate=50)
        self.spritesheet = pygame.image.load("assets/rain.png")
        self.animation = []
        for x in range(7):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()
        self.frame = 0
        # 0 - still
        # 1 - fade in
        # 2 - fade out
        self.state = 0
    def update(self):
        match self.state:
            case 1:
                if self.opacity <= 255:
                    self.opacity += self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))
            case 2:
                if self.opacity >= 0:
                    self.opacity -= self.fade_rate*dt
                else:
                    self.state = 0
                self.image.set_alpha(int(self.opacity))

    def change_state(self, state):
        self.state = state

    def next_frame(self):
            self.frame = (self.frame + 1) % 7
            self.image = self.animation[self.frame]
            self.image.set_alpha(int(self.opacity))

class River(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/river-base.png")
        self.rect = self.image.get_rect()

class RiverShadow(Shadow):
    def __init__(self):
        super().__init__(opacity=190, fade_rate=100)
        self.spritesheet = pygame.image.load("assets/river-shadow.png")
        self.animation = []
        for x in range(6):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.frame = 0

    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

    def next_frame(self):
            self.frame = (self.frame + 1) % 6
            self.image = self.animation[self.frame]
            self.image.set_alpha(int(self.opacity))

class Smoke(Shadow):
    def __init__(self):
        super().__init__(opacity=255, fade_rate=100)
        self.spritesheet = pygame.image.load("assets/smoke.png")
        self.animation = []
        for x in range(12):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.frame = 0

    def update(self):
        if self.opacity >= 0:
            self.opacity -= self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

    def brighten(self, extra_opacity=80):
        if self.opacity <= 255 - extra_opacity:
            self.opacity += extra_opacity
        self.image.set_alpha(int(self.opacity))

    def next_frame(self):
            self.frame = (self.frame + 1) % 12
            self.image = self.animation[self.frame]
            self.image.set_alpha(int(self.opacity))

class Flats(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/flats-base.png")
        self.rect = self.image.get_rect()

class FlatsShadow(Shadow):
    def __init__(self):
        super().__init__("assets/flats-shadow.png")
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

class Mountains(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/mountains-base.png")
        self.rect = self.image.get_rect()

class MountainsShadow(Shadow):
    def __init__(self):
        super().__init__("assets/mountains-shadow.png", 128, 30)
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

class Street(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/street-base.png")
        self.rect = self.image.get_rect()

class StreetShadow(Shadow):
    def __init__(self):
        super().__init__("assets/street-shadow.png", 220, 25)
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

class Buildings(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/buildings-base.png")
        self.rect = self.image.get_rect()

class BuildingsShadow(Shadow):
    def __init__(self):
        Shadow.__init__(self, "assets/buildings-shadow.png", 220, 50)
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))

class Trees(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/trees-base.png")
        self.animation = []
        for x in range(3):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.frame = 0
    def next_frame(self):
            self.frame = (self.frame + 1) % 3
            self.image = self.animation[self.frame]

class TreesShadow(Shadow):
    def __init__(self):
        Shadow.__init__(self, opacity=160, fade_rate=92)
        self.spritesheet = pygame.image.load("assets/trees-shadow.png")
        self.animation = []
        for x in range(3):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.frame = 0
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))
    def next_frame(self):
            self.frame = (self.frame + 1) % 3
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()

class Riverside(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/riverside-base.png")
        self.rect = self.image.get_rect()


class RiversideShadow(Shadow):
    def __init__(self):
        Shadow.__init__(self, opacity=200, fade_rate=14)
        self.spritesheet = pygame.image.load("assets/riverside-shadow.png")
        self.animation = []
        for x in range(2):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.image.set_alpha(int(self.opacity))
        self.rect = self.image.get_rect()
        self.frame = 0
    def update(self):
        self.opacity += self.fade_rate*dt
        self.image.set_alpha(int(self.opacity))
    def next_frame(self):
            self.frame = (self.frame + 1) % 2
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()

class SkyShadow(Shadow):
    def __init__(self):
        super().__init__(opacity=255, fade_rate=100)
        self.spritesheet = pygame.image.load("assets/skyshadow.png")
        self.animation = []
        for x in range(9):
            image = self.spritesheet.subsurface((x*400, 0, 400, 300))
            self.animation.append(image)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.ending_opacity = 100
        self.fade_out = 0

    def update(self):
        if self.opacity >= self.ending_opacity:
            self.opacity -= self.fade_rate*dt
        if self.fade_out == 1:
            if self.starting_opacity >= 0:
                self.starting_opacity -= 50*dt
            if self.ending_opacity >= 0:
                self.ending_opacity -= 50*dt
        self.image.set_alpha(int(self.opacity))

    def next_frame(self):
            self.frame = (self.frame + 1) % 9
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.image.set_alpha(int(self.opacity))

# setup playback and midi file
playback = Playback()
playback.load_file("assets/ciekawe-remake12.mp3")
file = mido.MidiFile("assets/ciekawe-remake.mid")

def play_audio():
    playback.play()


# create midi files for each instrument
instrument_files = []
track_count = len(file.tracks)-1
for i in range(track_count):
    track = file.tracks[i+1]
    new_file = mido.MidiFile()
    new_file.ticks_per_beat = file.ticks_per_beat
    new_file.tracks.append(track)
    instrument_files.append(new_file)

pygame.init()
screen = pygame.display.set_mode((1200, 900))
#time.sleep(5)
clock = pygame.time.Clock()
running = True

all_sprites = pygame.sprite.Group()
shadow_sprites = pygame.sprite.Group()

lights_right = []
lights_left = []
for i in range(12):
    lights_right.append(LightsRight())
    lights_left.append(LightsLeft())
lyrics = Lyrics()
night = Night()
rain = Rain()
rainclouds = Rainclouds()
river = River()
river_shadow = RiverShadow()
flats = Flats()
flats_shadow = FlatsShadow()
mountains = Mountains()
mountains_shadow = MountainsShadow()
street = Street()
street_shadow = StreetShadow()
buildings = Buildings()
buildings_shadow = BuildingsShadow()
trees = Trees()
trees_shadow = TreesShadow()
riverside = Riverside()
riverside_shadow = RiversideShadow()
sky_shadow = SkyShadow()
smoke = Smoke()

all_sprites.add(night)
all_sprites.add(sky_shadow)
all_sprites.add(river)
all_sprites.add(river_shadow)
all_sprites.add(flats)
all_sprites.add(flats_shadow)
all_sprites.add(mountains)
all_sprites.add(mountains_shadow)
all_sprites.add(street)
all_sprites.add(street_shadow)
all_sprites.add(riverside)
all_sprites.add(riverside_shadow)
all_sprites.add(trees)
all_sprites.add(trees_shadow)
all_sprites.add(lyrics)
all_sprites.add(buildings)
all_sprites.add(buildings_shadow)
all_sprites.add(smoke)
for i in range(12):
    all_sprites.add(lights_right[i])
    all_sprites.add(lights_left[i])
all_sprites.add(rain)
all_sprites.add(rainclouds)
shadow_sprites.add(street_shadow)
shadow_sprites.add(riverside_shadow)
shadow_sprites.add(trees_shadow)
shadow_sprites.add(buildings_shadow)
shadow_sprites.add(mountains_shadow)
shadow_sprites.add(flats_shadow)

def play_midi():
    global running
    for msg in file.play():
        if not msg.is_meta and msg.type == "note_on":
                match msg.channel:
                    # acoustic guitar
                    case 0:
                        trees.next_frame()
                        trees_shadow.next_frame()
                        #print("g")
                    # smoke
                    case 1:
                            smoke.next_frame()
                            rain.next_frame()
                        #print("s")
                    # riverside
                    case 2:
                        riverside_shadow.next_frame()
                        river_shadow.next_frame()
                        if rainclouds.state != 3:
                            rainclouds.next_frame()
                        #print("r")
                    # drums
                    case 3:
                        # kick
                        if msg.note == 36:
                            sky_shadow.opacity = sky_shadow.starting_opacity
                            #print(".")
                        # snare
                        elif msg.note == 38:
                            river_shadow.opacity = river_shadow.starting_opacity
                    # tambourine
                    case 4:
                        for sprite in shadow_sprites:
                            sprite.opacity = sprite.starting_opacity
                        #print("X")
                    # piano
                    case 5:
                        smoke.brighten()
                        note = msg.note % 12
                        lights_left[note].change_note(note)
                        #print("IOIO")
                    # bass
                    case 6:
                        sky_shadow.next_frame()
                        night.next_frame()
                        #print("CHUMP")
                    # weird guitar/rain
                    case 7:
                        match msg.note:
                            case 65:
                                LightsRight.active = True
                            case 67:
                                rainclouds.change_state(1)
                            case 69:
                                rain.change_state(1)
                                night.change_state(1)
                            case 71:
                                sky_shadow.fade_out = 1
                            case 73:
                                rainclouds.change_state(3)
                            case 75:
                                rainclouds.change_state(0)
                        #print("www")
                    # electric guitar
                    case 8:
                        if LightsRight.active:
                            note = msg.note % 12
                            lights_right[note].change_note(note)
                        #print("x")
                    # voice
                    case 9:
                        if msg.note == 48:
                            lyrics.fade_in(msg.velocity)
                        elif msg.note == 47:
                            lyrics.fade_out(msg.velocity)
                        #print("v")
    running = False

# create threads for each track
midi_thread = threading.Thread(target=play_midi)
thread_playback = threading.Thread(target=play_audio)

thread_playback.start()
midi_thread.start()

# pygame loop
while running:
    zoom_screen = pygame.Surface((400, 300))
    zoom_screen.fill("#fdf6fe")

    all_sprites.update()

    # draw
    all_sprites.draw(zoom_screen)
    zoom_screen = pygame.transform.scale(zoom_screen, (1200, 900))
    screen.blit(zoom_screen, (0, 0))
    pygame.display.flip()

    dt = clock.tick(30) / 1000

thread_playback.join()
midi_thread.join()
