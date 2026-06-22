import pygame

from src.assets import load_image, load_sound, play_sound
from src.bullet import Bullet
from src.settings import (
    FAST_SHOT_DURATION_MS,
    IMAGE_FILES,
    PLAYER_LIVES,
    PLAYER_SHOT_DELAY,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOUND_FILES,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, bullets: pygame.sprite.Group):
        super().__init__()
        self.image = load_image(IMAGE_FILES["player"], (60, 52))
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 14))
        self.bullets = bullets
        self.lives = PLAYER_LIVES
        self.last_shot = 0
        self.shot_delay = PLAYER_SHOT_DELAY
        self.fast_shot_until = 0
        self.shot_sound = load_sound(SOUND_FILES["shot"])

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        movement = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            movement -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            movement += PLAYER_SPEED

        self.rect.x += movement
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        now = pygame.time.get_ticks()
        self.shot_delay = 110 if now < self.fast_shot_until else PLAYER_SHOT_DELAY

    def shoot(self) -> None:
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shot_delay:
            self.last_shot = now
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top + 8))
            play_sound(self.shot_sound)

    def add_life(self) -> None:
        self.lives = min(self.lives + 1, 5)

    def activate_fast_shot(self) -> None:
        self.fast_shot_until = pygame.time.get_ticks() + FAST_SHOT_DURATION_MS
