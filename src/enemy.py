import random

import pygame

from src.assets import load_image
from src.settings import IMAGE_FILES, SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, difficulty: int = 0):
        super().__init__()
        size = random.randint(34, 48)
        self.image = load_image(IMAGE_FILES["enemy"], (size, size))
        self.rect = self.image.get_rect(midbottom=(random.randint(24, SCREEN_WIDTH - 24), 0))
        self.speed = random.uniform(1.4 + difficulty * 0.12, 3.4 + difficulty * 0.18)

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    TYPES = ("fast", "life")

    def __init__(self):
        super().__init__()
        self.kind = random.choice(self.TYPES)
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        color = (77, 213, 255) if self.kind == "fast" else (255, 90, 116)
        pygame.draw.circle(self.image, color, (12, 12), 11)
        pygame.draw.circle(self.image, (255, 255, 255), (12, 12), 5, 2)
        self.rect = self.image.get_rect(midbottom=(random.randint(30, SCREEN_WIDTH - 30), 0))
        self.speed = random.uniform(1.3, 2.2)

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
