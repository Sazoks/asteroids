import pygame
from typing import List

from pathlib import Path
from enum import Enum
from quadtree import (
    Quadtree,
)
from my_dataclasses import (
    Area,
    Point,
)


# Настройки игрового окна.
WIDTH = 1600
HEIGHT = 800
FPS = 100


# Задаем цвета.
class Collors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (235, 235, 0)


# Создаем игру и окно.
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


# Пути папок до файлов.
sprites_dir = Path(__file__).parent / 'sprites'
audio_dir = Path(__file__).parent / 'audio'


# Создаем квадродерево.
# Задаем начальный сектор и разброс поиска (в px).
quadtree = Quadtree(area=Area(Point(0, 0), Point(WIDTH, HEIGHT)),
                    search_accuracy=50)

# Создаем группы объектов.
players_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
asteroids_sprites = pygame.sprite.Group()
explosions_sprites = pygame.sprite.Group()


# Загружаем спрайты.
background = pygame.image.load(sprites_dir / 'Backgrounds/black.png').convert()
asteroid_skins = {
    'tiny': [
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_tiny1.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_tiny2.png').convert(),
    ],
    'small': [
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_small1.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_small2.png').convert(),
    ],
    'medium': [
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_med1.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_med2.png').convert(),
    ],
    'large': [
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_big1.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_big2.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_big3.png').convert(),
        pygame.image.load(sprites_dir / 'PNG/Meteors/meteorBrown_big4.png').convert(),
    ],
}
player_skin = pygame.image.load(sprites_dir / 'PNG/playerShip1_orange.png')
bullet_skin = pygame.image.load(sprites_dir / 'PNG/Lasers/laserBlue01.png')

# Загружаем спрайты для анимации взрыва.
explosion_anim: List[pygame.Surface] = []
for i in range(9):
    filename = f'Explosions_kenney/regularExplosion0{i}.png'
    img = pygame.image.load(sprites_dir / filename).convert()
    img.set_colorkey(Collors.BLACK.value)
    explosion_anim.append(img)


# Загрузка звуков.
shoot_sound = pygame.mixer.Sound(audio_dir / 'sfx_laser1.ogg')
shoot_sound.set_volume(0.3)
expl_sounds = []
for i in range(2, 4):
    sound = pygame.mixer.Sound(audio_dir / f'expls/type2/explosion{i + 1}.ogg')
    sound.set_volume(0.1)
    expl_sounds.append(sound)
chunky_expl = pygame.mixer.Sound(audio_dir / f'expls/chunky_expl.mp3')
chunky_expl.set_volume(0.7)

# Загрузка музыки.
# pygame.mixer.music.load(audio_dir / 'music/acdc_thunderstruck.mp3')
# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.play(-1)
