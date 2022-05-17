import pygame
from typing import (
    Tuple,
)

from settings import explosion_anim


class Explosion(pygame.sprite.Sprite):
    """Класс анимации взрыва"""

    def __init__(self, center: Tuple[float, float], size: float,
                 frame_rate: int = 55):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.transform.scale(explosion_anim[0], (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = frame_rate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.transform.scale(explosion_anim[self.frame],
                                                    (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.center = center
