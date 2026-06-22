# Space Defender

Jogo 2D em Python e Pygame desenvolvido para a disciplina de Linguagem de Programacao Aplicada.

## Requisitos

- Python 3.12 ou superior
- Windows
- Pygame

## Instalacao

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Execucao

```powershell
python main.py
```

## Controles

- A ou seta esquerda: mover para esquerda
- D ou seta direita: mover para direita
- Espaco: atirar
- ESC: pausar
- ENTER: confirmar opcao de menu

## Objetivo

Controle a nave na parte inferior da tela, destrua os inimigos que descem do topo e sobreviva ate vencer.

O jogador vence ao destruir 50 inimigos ou sobreviver por 180 segundos. A derrota acontece quando as 3 vidas acabam.

No menu inicial, a opcao `Instrucoes` mostra o objetivo, as condicoes de fim de jogo e os controles.

Ao final de cada partida, o jogo pede o nome do jogador e salva a pontuacao localmente em `data/high_score.txt`.
A tela `Pontuacao` mostra as 10 melhores pontuacoes, ordenadas por maior numero de pontos e, em caso de empate, pelo menor tempo.

## Estrutura

```text
main.py
assets/
assets/sounds/
src/
  assets.py
  bullet.py
  enemy.py
  game.py
  menu.py
  player.py
  settings.py
  ui.py
requirements.txt
README.md
```

## Gerar executavel com PyInstaller

Instale as dependencias e execute:

```powershell
pyinstaller --onefile --windowed main.py
```

Depois de compilar, copie a pasta `assets` para o mesmo diretorio do executavel gerado em `dist`.

Para entregar em ZIP, compacte o executavel gerado e a pasta `assets`.

Estrutura esperada apos a compilacao:

```text
dist/
  main.exe
  assets/
    Enemy1.png
    Player1.png
    heart.png
    sounds/
```
