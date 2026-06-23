import sqlite3
import sys

import pygame

from src.assets import load_image, load_sound, play_music, play_sound
from src.enemy import Enemy, PowerUp
from src.menu import Menu
from src.player import Player
from src.settings import (
    DATA_DIR,
    END_OPTIONS,
    ENEMY_BASE_SPAWN_MS,
    ENEMY_SPAWN_EVENT,
    FPS,
    GAME_DURATION,
    HIGH_SCORE_DB,
    HIGH_SCORE_FILE,
    IMAGE_FILES,
    MENU_OPTIONS,
    PAUSE_OPTIONS,
    POWERUP_SPAWN_EVENT,
    POWERUP_SPAWN_MS,
    SCORE_PER_ENEMY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOUND_FILES,
    TITLE,
    VICTORY_KILLS,
    WHITE,
    YELLOW,
)
from src.ui import UI


class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.menu = Menu(self.screen, self.clock)
        self.init_score_db()
        self.scores = self.load_scores()

    def run(self) -> None:
        while True:
            option = self.menu.run()
            if option == MENU_OPTIONS[0]:
                self.play_level()
            elif option == MENU_OPTIONS[1]:
                self.menu.show_score(self.scores)
            elif option == MENU_OPTIONS[2]:
                self.menu.show_controls()
            else:
                self.quit()

    def play_level(self) -> None:
        play_music(SOUND_FILES["level1"])
        background = load_image(IMAGE_FILES["level1_bg"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player(bullets)
        all_sprites.add(player)

        explosion_sound = load_sound(SOUND_FILES["explosion"])
        player_dead_sound = load_sound(SOUND_FILES["player_dead"])
        score = 0
        kills = 0
        started_at = pygame.time.get_ticks()
        paused_ms = 0
        difficulty = 0

        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_BASE_SPAWN_MS)
        pygame.time.set_timer(POWERUP_SPAWN_EVENT, POWERUP_SPAWN_MS)

        while True:
            elapsed = (pygame.time.get_ticks() - started_at - paused_ms) // 1000
            time_left = max(0, GAME_DURATION - elapsed)
            difficulty = min(12, elapsed // 15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == ENEMY_SPAWN_EVENT:
                    enemy = Enemy(difficulty)
                    enemies.add(enemy)
                    all_sprites.add(enemy)
                    spawn_ms = max(330, ENEMY_BASE_SPAWN_MS - difficulty * 45)
                    pygame.time.set_timer(ENEMY_SPAWN_EVENT, spawn_ms)
                if event.type == POWERUP_SPAWN_EVENT:
                    powerup = PowerUp()
                    powerups.add(powerup)
                    all_sprites.add(powerup)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                    elif event.key == pygame.K_ESCAPE:
                        paused_at = pygame.time.get_ticks()
                        action = self.pause_screen(background)
                        paused_ms += pygame.time.get_ticks() - paused_at
                        if action == "Reiniciar":
                            self.stop_level_timers()
                            return self.play_level()
                        if action == "Voltar ao menu":
                            self.stop_level_timers()
                            return

            all_sprites.update()
            bullets.update()

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for _enemy in hits:
                score += SCORE_PER_ENEMY
                kills += 1
                play_sound(explosion_sound)

            player_hits = pygame.sprite.spritecollide(player, enemies, True)
            if player_hits:
                player.lives -= len(player_hits)
                play_sound(player_dead_sound)

            powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
            for powerup in powerup_hits:
                if powerup.kind == "life":
                    player.add_life()
                else:
                    player.activate_fast_shot()

            self.screen.blit(background, (0, 0))
            all_sprites.draw(self.screen)
            bullets.draw(self.screen)
            self.ui.draw_hud(score, player.lives, time_left, kills, self.high_score)
            pygame.display.flip()
            self.clock.tick(FPS)

            if player.lives <= 0:
                self.stop_level_timers()
                self.finish_game("Derrota", score, kills, elapsed)
                return
            if kills >= VICTORY_KILLS or elapsed >= GAME_DURATION:
                self.stop_level_timers()
                self.finish_game("Vitoria", score, kills, elapsed)
                return

    def pause_screen(self, background: pygame.Surface) -> str:
        selected = 0
        while True:
            self.screen.blit(background, (0, 0))
            self.ui.draw_overlay()
            self.ui.draw_text("Pausado", "large", YELLOW, center=(SCREEN_WIDTH // 2, 102))
            self.ui.draw_menu_options(PAUSE_OPTIONS, selected, 166)
            pygame.display.flip()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN) and selected == 0:
                        return "Continuar"
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(PAUSE_OPTIONS)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % len(PAUSE_OPTIONS)
                    elif event.key == pygame.K_RETURN:
                        return PAUSE_OPTIONS[selected]

    def finish_game(self, result: str, score: int, kills: int, elapsed: int) -> None:
        if result == "Derrota":
            pygame.mixer.music.stop()
            play_sound(load_sound(SOUND_FILES["gameover1"]))
            pygame.time.wait(3000)
            play_sound(load_sound(SOUND_FILES["gameover2"]))
            pygame.time.wait(900)
        play_music(SOUND_FILES["menu"])

        background = load_image(IMAGE_FILES["menu_bg"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        player_name = self.ask_player_name(background)
        self.add_score(player_name, score, elapsed)
        selected = 0
        title = "Parabens, voce venceu!" if result == "Vitoria" else "Fim de jogo"
        while True:
            self.screen.blit(background, (0, 0))
            self.ui.clear_with_panel()
            self.ui.draw_text(title, "large", YELLOW, center=(SCREEN_WIDTH // 2, 84))
            self.ui.draw_text(f"Pontuacao final: {score}", "normal", WHITE, center=(SCREEN_WIDTH // 2, 132))
            self.ui.draw_text(f"Inimigos destruidos: {kills}", "normal", WHITE, center=(SCREEN_WIDTH // 2, 164))
            self.ui.draw_text(f"Tempo sobrevivido: {elapsed}s", "normal", WHITE, center=(SCREEN_WIDTH // 2, 196))
            self.ui.draw_menu_options(END_OPTIONS, selected, 250)
            pygame.display.flip()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_UP, pygame.K_w):
                        selected = 1 - selected
                    elif event.key == pygame.K_RETURN:
                        if END_OPTIONS[selected] == "Jogar Novamente":
                            self.play_level()
                        return

    @property
    def high_score(self) -> int:
        return int(self.scores[0]["score"]) if self.scores else 0

    def load_scores(self) -> list[dict[str, int | str]]:
        self.migrate_legacy_scores()
        with sqlite3.connect(HIGH_SCORE_DB) as conn:
            rows = conn.execute(
                """
                SELECT name, score, time
                FROM scores
                ORDER BY score DESC, time ASC
                LIMIT 10
                """
            ).fetchall()
        return [{"name": row[0], "score": row[1], "time": row[2]} for row in rows]

    def init_score_db(self) -> None:
        DATA_DIR.mkdir(exist_ok=True)
        with sqlite3.connect(HIGH_SCORE_DB) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    time INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def migrate_legacy_scores(self) -> None:
        if not HIGH_SCORE_FILE.exists():
            return

        with sqlite3.connect(HIGH_SCORE_DB) as conn:
            score_count = conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0]
            if score_count > 0:
                return

            legacy_scores = self.load_legacy_scores()
            conn.executemany(
                "INSERT INTO scores (name, score, time) VALUES (?, ?, ?)",
                [(str(item["name"]), int(item["score"]), int(item["time"])) for item in legacy_scores],
            )

    def load_legacy_scores(self) -> list[dict[str, int | str]]:
        scores = []
        try:
            lines = HIGH_SCORE_FILE.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            return []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ";" not in line:
                try:
                    scores.append({"name": "Jogador", "score": int(line), "time": 999})
                except ValueError:
                    pass
                continue
            parts = line.split(";")
            if len(parts) >= 3:
                try:
                    scores.append({"name": parts[0][:12] or "Jogador", "score": int(parts[1]), "time": int(parts[2])})
                except ValueError:
                    pass
        return self.sort_scores(scores)[:10]

    def add_score(self, name: str, score: int, elapsed: int) -> None:
        with sqlite3.connect(HIGH_SCORE_DB) as conn:
            conn.execute(
                "INSERT INTO scores (name, score, time) VALUES (?, ?, ?)",
                (name[:12] or "Jogador", score, elapsed),
            )
        self.scores = self.load_scores()

    def sort_scores(self, scores: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
        return sorted(scores, key=lambda item: (-int(item["score"]), int(item["time"])))

    def ask_player_name(self, background: pygame.Surface) -> str:
        name = ""
        while True:
            self.screen.blit(background, (0, 0))
            self.ui.clear_with_panel()
            self.ui.draw_text("Salvar pontuacao", "large", YELLOW, center=(SCREEN_WIDTH // 2, 92))
            self.ui.draw_text("Digite seu nome:", "normal", WHITE, center=(SCREEN_WIDTH // 2, 148))
            shown_name = name if name else "_"
            self.ui.draw_text(shown_name, "large", YELLOW, center=(SCREEN_WIDTH // 2, 192))
            self.ui.draw_text("ENTER confirma | BACKSPACE apaga", "small", WHITE, center=(SCREEN_WIDTH // 2, 252))
            pygame.display.flip()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return name.strip() or "Jogador"
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 12 and event.unicode and event.unicode.isprintable() and event.unicode not in ";":
                        name += event.unicode

    def stop_level_timers(self) -> None:
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, 0)
        pygame.time.set_timer(POWERUP_SPAWN_EVENT, 0)

    def quit(self) -> None:
        pygame.quit()
        sys.exit()
