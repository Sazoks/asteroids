import sys
import pygame
from enum import Enum
from typing import List
from pathlib import Path


# Настройки игрового окна.
WIDTH = 1100
HEIGHT = 900
FPS = 60


class Collors(Enum):
    """Цвета для игры"""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (235, 235, 0)


# Пути папок до медиа файлов.
# Проверка необходима, если программа запускается из скомпилированного
# .exe-файла.
if getattr(sys, 'frozen', False):
    base_dir = Path(sys.executable).parent
else:
    base_dir = Path(__file__).parent
sprites_dir = base_dir / 'media/sprites'
audio_dir = base_dir / 'media/audio'


# Создаем игру, окно, в которое будут отрисовываться все спрайты,
# инициализируем микшер для звуков, создаем таймер и шрифты.
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
pygame.font.init()
main_font = pygame.font.SysFont('Comic Sans MS', 30)
health_font = pygame.font.SysFont('Comic Sans MS', 12)


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
attack_speed_powerup_skin = pygame.image.load(sprites_dir / 'PNG/Power-ups/things_gold.png')
speed_powerup_skin = pygame.image.load(sprites_dir / 'PNG/Power-ups/powerupBlue_bolt.png')
health_powerup_skin = pygame.image.load(sprites_dir / 'PNG/Power-ups/pill_green.png')

# Загружаем спрайты для анимации взрыва.
explosion_anim: List[pygame.Surface] = []
for i in range(9):
    filename = f'Explosions_kenney/regularExplosion0{i}.png'
    img = pygame.image.load(sprites_dir / filename).convert()
    img.set_colorkey(Collors.BLACK.value)
    explosion_anim.append(img)


# Загрузка звуков.
shoot_sound = pygame.mixer.Sound(audio_dir / 'sfx_laser1.ogg')
shoot_sound.set_volume(0.2)
expl_sounds = []
for i in range(2, 4):
    sound = pygame.mixer.Sound(audio_dir / f'expls/type2/explosion{i + 1}.ogg')
    sound.set_volume(0.1)
    expl_sounds.append(sound)
chunky_expl = pygame.mixer.Sound(audio_dir / f'expls/chunky_expl.mp3')
chunky_expl.set_volume(0.5)

# Загрузка музыки.
# pygame.mixer.music.load(audio_dir / 'music/acdc_thunderstruck.mp3')
# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.play(-1)
