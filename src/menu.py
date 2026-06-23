import pygame

from src.assets import load_image, play_music
from src.settings import IMAGE_FILES, MENU_OPTIONS, SCREEN_HEIGHT, SCREEN_WIDTH, SOUND_FILES, WHITE, YELLOW
from src.ui import UI


class Menu:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.ui = UI(screen)
        self.background = load_image(IMAGE_FILES["menu_bg"], (SCREEN_WIDTH, SCREEN_HEIGHT))

    def run(self) -> str:
        play_music(SOUND_FILES["menu"])
        selected = 0
        while True:
            self.screen.blit(self.background, (0, 0))
            self.ui.draw_text("Space Defender", "title", YELLOW, center=(SCREEN_WIDTH // 2, 86))
            self.ui.draw_menu_options(MENU_OPTIONS, selected, 176)
            self.ui.draw_button_hint(SCREEN_HEIGHT - 28)
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Sair"
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % len(MENU_OPTIONS)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % len(MENU_OPTIONS)
                    elif event.key == pygame.K_RETURN:
                        return MENU_OPTIONS[selected]

    def show_score(self, scores: list[dict[str, int | str]]) -> None:
        while True:
            self.screen.blit(self.background, (0, 0))
            self.ui.clear_with_panel()
            self.ui.draw_text("Pontuação", "large", YELLOW, center=(SCREEN_WIDTH // 2, 74))
            self.ui.draw_text("Pos  Nome          Pontos  Tempo", "small", WHITE, center=(SCREEN_WIDTH // 2, 112))

            if not scores:
                self.ui.draw_text("Nenhuma pontuação salva.", "normal", WHITE, center=(SCREEN_WIDTH // 2, 184))
            else:
                for index, item in enumerate(scores[:10], start=1):
                    line = f"{index:02d}   {str(item['name'])[:12]:<12}  {int(item['score']):>5}   {int(item['time']):>3}s"
                    self.ui.draw_text(line, "small", WHITE, center=(SCREEN_WIDTH // 2, 118 + index * 20))

            self.ui.draw_text("ENTER ou ESC para voltar", "small", WHITE, center=(SCREEN_WIDTH // 2, 344))
            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return

    def show_controls(self) -> None:
        lines = (
            "Objetivo: abater 200 inimigos ou sobreviver 120 segundos.",
            "Você perde se acabarem as vidas (corações).",
            "Se pegar bolas vermelhas você ganha mais vidas.",
            "Bolas azuis aumentam temporariamente a quantidade de tiros.",
            " ",
            "Comandos:",
            "A ou seta esquerda: mover para esquerda",
            "D ou seta direita: mover para direita",
            "ESPACO: atirar",
            "ESC: pausar",
            "ENTER ou ESC para voltar",
        )
        self._info_screen("Instruções", lines)

    def _info_screen(self, title: str, lines: tuple[str, ...]) -> None:
        while True:
            self.screen.blit(self.background, (0, 0))
            panel = self.ui.clear_with_panel(pygame.Rect(20, 34, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 68))
            center_x = panel.centerx
            y = panel.top + 24

            self.ui.draw_text(title, "large", YELLOW, center=(center_x, y))
            y += 44

            for line in lines:
                if line.strip():
                    self.ui.draw_text(line, "small", WHITE, center=(center_x, y))
                    y += 22
                else:
                    y += 14

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
