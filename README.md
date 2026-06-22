# Space Defender

Jogo 2D em Python e Pygame desenvolvido para a disciplina de Linguagem de Programação Aplicada.

## Requisitos

- Python 3.12 ou superior
- Windows
- Pygame

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

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

Controle a nave na parte inferior da tela, destrua os inimigos que descem do topo e sobreviva até vencer.

O jogador vence ao destruir 50 inimigos ou sobreviver por 180 segundos. A derrota acontece quando as 3 vidas acabam.

No menu inicial, a opção `Instruções` mostra o objetivo, as condições de fim de jogo e os controles.

Ao final de cada partida, o jogo pede o nome do jogador e salva a pontuação localmente em `data/high_score.txt`.
A tela `Pontuação` mostra as 10 melhores pontuações, ordenadas por maior número de pontos e, em caso de empate, pelo menor tempo.

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

## Gerar executável com PyInstaller

Depois de instalar as dependências (passo Instalação) basta executar o comando abaixo:

```powershell
pyinstaller --onefile --windowed main.py
```

Depois de compilar, copie a pasta `assets` para o mesmo diretório do executável gerado em `dist`.

Estrutura esperada apos a compilação:

```text
dist/
  main.exe
  assets/
    Enemy1.png
    Player1.png
    heart.png
    sounds/
```
