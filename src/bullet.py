import pygame

from src.assets import load_image
from src.settings import BULLET_SPEED, IMAGE_FILES, SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = load_image(IMAGE_FILES["bullet"], (12, 24))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = BULLET_SPEED

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
