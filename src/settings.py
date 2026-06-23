import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATA_DIR = BASE_DIR / "data"
HIGH_SCORE_FILE = DATA_DIR / "high_score.txt"
HIGH_SCORE_DB = DATA_DIR / "high_score.db"

SCREEN_WIDTH = 693
SCREEN_HEIGHT = 392
FPS = 60

TITLE = "Space Defender"
GAME_DURATION = 120
VICTORY_KILLS = 200
PLAYER_LIVES = 3

PLAYER_SPEED = 6
BULLET_SPEED = -9
PLAYER_SHOT_DELAY = 280
ENEMY_SPAWN_EVENT = 25
POWERUP_SPAWN_EVENT = 26
ENEMY_BASE_SPAWN_MS = 900
POWERUP_SPAWN_MS = 16000

SCORE_PER_ENEMY = 10
FAST_SHOT_DURATION_MS = 7000

WHITE = (245, 247, 255)
YELLOW = (255, 218, 91)
ORANGE = (255, 139, 46)
RED = (236, 71, 71)
GREEN = (82, 220, 143)
CYAN = (69, 212, 255)
BLACK = (7, 9, 19)
SHADOW = (0, 0, 0)

MENU_OPTIONS = ("Jogar", "Pontuação", "Instruções", "Sair")
PAUSE_OPTIONS = ("Continuar", "Reiniciar", "Voltar ao menu")
END_OPTIONS = ("Jogar Novamente", "Sair")

IMAGE_FILES = {
    "menu_bg": "menu_bg.png",
    "level1_bg": "level1_bg.png",
    "player": "Player1.png",
    "enemy": "Enemy1.png",
    "bullet": "Player1_shot1.png",
    "heart": "heart.png",
}

SOUND_FILES = {
    "menu": "menu_sound.wav",
    "level1": "level1_sound.wav",
    "shot": "player1_shot_sound.wav",
    "explosion": "enemy_explosion_sound.wav",
    "player_dead": "player1_dead.mp3",
    "gameover1": "gameover1.wav",
    "gameover2": "gameover2.wav",
}
