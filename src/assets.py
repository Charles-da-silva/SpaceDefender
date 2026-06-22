import pygame

from src.settings import ASSETS_DIR, SOUNDS_DIR


def asset_path(filename: str):
    """Procura arquivos de som na pasta sounds e imagens direto em assets."""
    sound_path = SOUNDS_DIR / filename
    if sound_path.exists():
        return sound_path
    return ASSETS_DIR / filename


def load_image(filename: str, size: tuple[int, int] | None = None) -> pygame.Surface:
    image = pygame.image.load(asset_path(filename)).convert_alpha()
    if size:
        image = pygame.transform.smoothscale(image, size)
    return image


def load_sound(filename: str) -> pygame.mixer.Sound | None:
    try:
        return pygame.mixer.Sound(str(asset_path(filename)))
    except pygame.error:
        return None


def play_sound(sound: pygame.mixer.Sound | None) -> None:
    if sound:
        sound.play()


def play_music(filename: str, volume: float = 0.35, loops: int = -1) -> None:
    try:
        pygame.mixer.music.load(str(asset_path(filename)))
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
    except pygame.error:
        pass
