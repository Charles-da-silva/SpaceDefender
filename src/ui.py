import pygame

from src.assets import load_image
from src.settings import BLACK, CYAN, GREEN, IMAGE_FILES, ORANGE, SCREEN_WIDTH, SHADOW, VICTORY_KILLS, WHITE, YELLOW


class UI:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Lucida Console", 46, bold=True)
        self.large_font = pygame.font.SysFont("Lucida Console", 28, bold=True)
        self.font = pygame.font.SysFont("Lucida Console", 18, bold=True)
        self.small_font = pygame.font.SysFont("Lucida Console", 14)
        self.heart = load_image(IMAGE_FILES["heart"], (24, 24))

    def draw_text(
        self,
        text: str,
        size: str,
        color: tuple[int, int, int],
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> pygame.Rect:
        font = {"title": self.title_font, "large": self.large_font, "small": self.small_font}.get(size, self.font)
        surf = font.render(text, True, color)
        shadow = font.render(text, True, SHADOW)
        rect = surf.get_rect(center=center) if center else surf.get_rect(topleft=topleft)
        self.screen.blit(shadow, rect.move(2, 2))
        self.screen.blit(surf, rect)
        return rect

    def draw_overlay(self) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

    def draw_menu_options(self, options: tuple[str, ...], selected: int, y: int) -> None:
        for index, option in enumerate(options):
            color = YELLOW if index == selected else WHITE
            prefix = "> " if index == selected else "  "
            self.draw_text(f"{prefix}{option}", "normal", color, center=(SCREEN_WIDTH // 2, y + index * 34))

    def draw_hud(self, score: int, lives: int, time_left: int, kills: int, high_score: int) -> None:
        panel = pygame.Surface((SCREEN_WIDTH, 42), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 110))
        self.screen.blit(panel, (0, 0))
        self.draw_text(f"Pontos: {score}", "small", WHITE, topleft=(12, 8))
        self.draw_text(f"Recorde: {high_score}", "small", CYAN, topleft=(128, 8))
        self.draw_text(f"Tempo: {time_left:03d}", "small", YELLOW, topleft=(270, 8))
        self.draw_text(f"Abates: {kills}/{VICTORY_KILLS}", "small", GREEN, topleft=(390, 8))
        for index in range(lives):
            self.screen.blit(self.heart, (SCREEN_WIDTH - 32 - index * 28, 8))

    def draw_button_hint(self, y: int) -> None:
        self.draw_text("Use setas/W/S para navegar e ENTER para confirmar", "small", ORANGE, center=(SCREEN_WIDTH // 2, y))

    def clear_with_panel(self, rect: pygame.Rect | None = None) -> pygame.Rect:
        if rect is None:
            rect = pygame.Rect(58, 54, SCREEN_WIDTH - 116, 276)
        pygame.draw.rect(self.screen, (BLACK[0], BLACK[1], BLACK[2], 205), rect, border_radius=8)
        pygame.draw.rect(self.screen, CYAN, rect, 2, border_radius=8)
        return rect
