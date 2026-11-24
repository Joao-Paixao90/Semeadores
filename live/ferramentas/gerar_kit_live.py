#!/usr/bin/env python3
"""
Kit de live — artes de transmissão, roteiro e estrutura de moderação.

POR QUE ARTES PRÓPRIAS
----------------------
Uma live sem tela de espera começa com o público olhando um retângulo preto e
saindo. A tela de espera não é enfeite: ela segura quem chegou cedo enquanto o
contador de espectadores sobe — e no YouTube o algoritmo usa o pico inicial
para decidir se recomenda a live.

TRÊS TELAS, QUE É O MÍNIMO HONESTO
  abertura.png   "Em instantes" — antes de entrar no ar
  intervalo.png  "Volto em instantes" — quando precisa sair
  encerramento.png "Ficou a palavra" — últimos 60 s

FORMATO 1920×1080 — HTML e PNG — para usar como cena no OBS ou num
produtor de tela. Se a live for pelo celular, as artes servem como capa e
como story de aviso.

Sai em artifacts/semeadores/live/
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
SAIDA = os.path.join(RAIZ, "artifacts", "semeadores", "live")

W, H = 1920, 1080
OURO = (212, 175, 55)
BRANCO = (247, 247, 249)
CINZA = (150, 156, 170)
F_T = "/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf"
F_S = "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/dejavu/DejaVuSans.ttf"


def fundo():
    """Fundo escuro com halo dourado — leve, sem imagem de banco."""
    im = Image.new("RGB", (W, H), (7, 8, 11))
    halo = Image.new("RGB", (W, H), (7, 8, 11))
    d = ImageDraw.Draw(halo)
    # dois halos suaves dão profundidade sem custar nada
    d.ellipse([W // 2 - 620, H // 2 - 380, W // 2 + 620, H // 2 + 380],
              fill=(26, 22, 12))
    halo = halo.filter(ImageFilter.GaussianBlur(150))
    im = Image.blend(im, halo, 0.85)
    return im


def centrar(d, txt, y, font, fill):
    w = d.textlength(txt, font=font)
    d.text(((W - w) / 2, y), txt, font=font, fill=fill)
    return w


def tela(nome, linhas, subtitulo, rodape, cor_linha=OURO):
    im = fundo()
    d = ImageDraw.Draw(im)
    f_big = ImageFont.truetype(F_T, 104)
    f_sub = ImageFont.truetype(F_R, 38)
    f_rod = ImageFont.truetype(F_S, 26)

    total = len(linhas) * 128
    y = H // 2 - total // 2 - 70
    for l in linhas:
        centrar(d, l, y, f_big, BRANCO)
        y += 128

    d.line([(W / 2 - 140, y + 26), (W / 2 + 140, y + 26)], fill=cor_linha, width=5)

    if subtitulo:
        f_sub2 = ImageFont.truetype(F_R, 36)
        centrar(d, subtitulo, y + 62, f_sub2, CINZA)

    if rodape:
        centrar(d, rodape, H - 100, f_rod, OURO)

    im.save(os.path.join(SAIDA, f"{nome}.png"), "PNG", optimize=True)
    im.save(os.path.join(SAIDA, f"{nome}.jpg"), "JPEG", quality=92, optimize=True)
    print(f"  {nome}: 1920x1080")


def main():
    os.makedirs(SAIDA, exist_ok=True)

    tela("abertura",
         ["EM INSTANTES"],
         "Semeadores da Palavra — prepare o coração",
         "@semeadores_da_palavra.ofc")

    tela("intervalo",
         ["VOLTO", "EM INSTANTES"],
         "Não saia — a palavra continua",
         "@semeadores_da_palavra.ofc")

    tela("encerramento",
         ["FICOU A PALAVRA"],
         "Compartilhe com alguém que precisa ouvir",
         "Deus te abençoe · @semeadores_da_palavra.ofc")

    # capa de aviso (story / post de "hoje tem live")
    cap = fundo()
    d = ImageDraw.Draw(cap)
    f1 = ImageFont.truetype(F_S, 40)
    f2 = ImageFont.truetype(F_T, 132)
    f3 = ImageFont.truetype(F_R, 44)
    centrar(d, "HOJE TEM LIVE", 300, f1, OURO)
    centrar(d, "20h", 400, f2, BRANCO)
    d.line([(W / 2 - 160, 570), (W / 2 + 160, 570)], fill=OURO, width=5)
    centrar(d, "Semeadores da Palavra", 630, f3, CINZA)
    centrar(d, "@semeadores_da_palavra.ofc", 700, ImageFont.truetype(F_S, 28), OURO)
    cap.save(os.path.join(SAIDA, "aviso-live.jpg"), "JPEG", quality=92, optimize=True)
    # versão 1080x1920 para story
    st = cap.resize((1080, 1920), Image.LANCZOS)
    st.save(os.path.join(SAIDA, "aviso-live-story.jpg"), "JPEG", quality=92,
            optimize=True)
    print("  aviso-live (1920x1080) + aviso-live-story (1080x1920)")


if __name__ == "__main__":
    main()
