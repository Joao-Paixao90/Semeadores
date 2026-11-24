#!/usr/bin/env python3
"""
Cortador de culto — encontra trechos publicáveis medindo o ÁUDIO, sem transcrever.

LIMITE DECLARADO: não há ASR nesta máquina (torch, ctranslate2 e vosk não têm
wheel para aarch64). Este script NÃO entende o que é dito. Ele mede onde há
voz, onde há ênfase e onde há pausa de pregador. O julgamento do conteúdo é seu.

POR QUE ISSO AINDA FUNCIONA NUM CULTO
--------------------------------------
Voz humana ocupa 300 Hz–3,4 kHz (formantes). Música de fundo, ventilador e
ar-condicionado ocupam sobretudo abaixo de 250 Hz e acima de 6 kHz. Medindo a
razão entre a banda de voz e o resto, o detector separa FALA de RUÍDO DE FUNDO
mesmo quando a música é contínua e o volume total não muda.

A primeira versão media energia total e falhou no teste real: a música de fundo
do culto deixou a faixa dinâmica em 9,9 dB, e o limiar não separava nada.
Energia total sozinha não distingue voz de música. Banda de voz distingue.

USO
  python3 cortar_culto.py culto.mp4                 # analisa
  python3 cortar_culto.py culto.mp4 --render        # analisa e corta 9:16
  python3 cortar_culto.py culto.mp4 --top 12 --min 18 --max 55
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

SR = 16000
JANELA = 0.20
MIN_CORTE = 18.0
MAX_CORTE = 58.0


def rodar(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def dur_seg(arq):
    o = rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", arq])
    try:
        return float(o.strip())
    except Exception:
        return 0.0


def pcm(arq, destino):
    rodar(["ffmpeg", "-y", "-v", "error", "-i", arq, "-vn", "-ac", "1",
           "-ar", str(SR), "-f", "s16le", destino])
    return os.path.exists(destino) and os.path.getsize(destino) > 0


def energia_bandas(arq):
    """Energia por janela em duas bandas: voz (300-3400 Hz) e o resto."""
    x = np.frombuffer(open(arq, "rb").read(), dtype=np.int16).astype(np.float32)
    n = int(SR * JANELA)
    blocos = x.size // n
    if blocos < 20:
        return None
    x = x[:blocos * n].reshape(blocos, n)

    # janela de Hann evita vazamento espectral que borra a separação
    win = np.hanning(n).astype(np.float32)
    freqs = np.fft.rfftfreq(n, 1 / SR)

    voz = (freqs >= 300) & (freqs <= 3400)
    resto = ~voz

    voz_e = np.empty(blocos, dtype=np.float32)
    tot_e = np.empty(blocos, dtype=np.float32)
    for i in range(blocos):
        sp = np.abs(np.fft.rfft(x[i] * win)) ** 2
        voz_e[i] = sp[voz].sum()
        tot_e[i] = sp[resto].sum()

    db_voz = 10 * np.log10(voz_e + 1e-12)
    db_tot = 10 * np.log10(voz_e + tot_e + 1e-12)
    # razão voz/resto: alto quando é voz, baixo quando é música/ruído
    razao = 10 * np.log10((voz_e + 1e-12) / (tot_e + 1e-12))
    return {"db": db_tot, "db_voz": db_voz, "razao": razao,
            "janela": JANELA, "n": blocos}


def suavizar(x, k):
    """Média móvel — o sinal bruto oscila janela a janela e fragmenta os blocos."""
    if x.size > k > 1:
        return np.convolve(x, np.ones(k) / k, mode="same")
    return x


def eh_fala(perf):
    """
    Decide, janela a janela, se há voz — com HISTERESE.

    O primeiro teste usou um limiar único e o resultado foi inútil: 17 blocos
    de 1 a 5 s num vídeo de 133 s, porque a energia oscila a cada 0,2 s e o
    sinal cruza o limiar o tempo todo. Histerese — limiar de entrada e limiar
    de saída diferentes — é como detecção de fala de verdade funciona: entra
    quando o sinal é claramente voz, só sai quando cai bem abaixo.
    """
    j = perf["janela"]
    k = max(2, int(0.6 / j))
    db = suavizar(perf["db"], k)
    rz = suavizar(perf["razao"], k)

    lo_db = float(np.percentile(db, 15))
    rz_in = float(np.percentile(rz, 35))
    rz_out = rz_in - 2.0

    fala = np.zeros(db.size, dtype=bool)
    ativo = False
    for i in range(db.size):
        if not ativo:
            if db[i] > lo_db and rz[i] > rz_in:
                ativo = True
        else:
            if db[i] < lo_db * 0.985 or rz[i] < rz_out:
                ativo = False
        fala[i] = ativo
    return fala, lo_db, float(np.percentile(db, 97)), rz_in


def blocos_fala(fala, j, min_seg=3.0):
    """Junta janelas de fala em blocos, tolerando pausas curtas de respiração."""
    tol = int(1.2 / j)  # pausa de até 1.2 s não quebra o bloco
    out, i, n = [], 0, len(fala)
    while i < n:
        if not fala[i]:
            i += 1
            continue
        ini = i
        fim = i
        buraco = 0
        while i < n:
            if fala[i]:
                fim = i
                buraco = 0
            else:
                buraco += 1
                if buraco > tol:
                    break
            i += 1
        if (fim - ini) * j >= min_seg:
            out.append([ini * j, (fim + 1) * j])
    return out


def pausas_longas(fala, j, min_p=0.9):
    """Pausas de verdade (>=0.9 s) dentro de bloco = marca de pregador."""
    out, i, n = [], 0, len(fala)
    while i < n:
        if fala[i]:
            i += 1
            continue
        ini = i
        while i < n and not fala[i]:
            i += 1
        if (i - ini) * j >= min_p:
            out.append((ini * j, i * j))
    return out


def recortar(blocos, min_c, max_c, db, j):
    """Divide blocos longos no ponto de menor energia (fim de frase)."""
    cands = []
    for t0, t1 in blocos:
        p = t0
        while t1 - p >= min_c:
            alvo = min(p + max_c, t1)
            if alvo - p > max_c:
                a, b = int(p / j), int(alvo / j)
                seg = db[a:b]
                if seg.size > 10:
                    ini_busca = int(seg.size * 0.55)
                    sub = seg[ini_busca:]
                    if sub.size:
                        alvo = p + (ini_busca + int(np.argmin(sub))) * j
            d = alvo - p
            if d < min_c:
                break
            cands.append([round(p, 2), round(alvo, 2), round(d, 1)])
            p = alvo
    return cands


def pontuar(cands, perf, pausas, piso, teto):
    j = perf["janela"]
    k = max(2, int(0.6 / j))
    db = suavizar(perf["db"], k)
    razao = suavizar(perf["razao"], k)
    faixa = max(teto - piso, 3.0)
    for c in cands:
        ini, fim = c[0], c[1]
        a, b = int(ini / j), int(fim / j)
        seg_db, seg_rz = db[a:b], razao[a:b]
        if seg_db.size == 0:
            c.extend([0, 0, 0]); continue
        nrg = float(np.clip((seg_db.mean() - piso) / faixa, 0, 1))
        vz = float(np.clip((seg_rz.mean() - np.percentile(razao, 20)) /
                           max(np.percentile(razao, 95) - np.percentile(razao, 20), 1), 0, 1))
        n_p = sum(1 for s0, s1 in pausas if s0 >= ini and s1 <= fim)
        dur_ok = 1.0 if 22 <= c[2] <= 45 else 0.65
        nota = (0.38 * nrg + 0.42 * vz + 0.12 * dur_ok) * 100
        nota = min(100, nota + (6 if n_p >= 2 else 0))
        c.extend([round(nota), n_p, round(vz, 2)])
    return cands


def escolher(cands, top):
    """Ordena por nota e tira sobreposição — dois cortes não repetem trecho."""
    cands.sort(key=lambda c: -c[3])
    out = []
    for c in cands:
        if all(min(c[1], o[1]) - max(c[0], o[0]) < 0.35 * min(c[2], o[2]) for o in out):
            out.append(c)
        if len(out) >= top:
            break
    out.sort(key=lambda c: c[0])
    return out


def filtro_video(modo):
    """
    Dois enquadramentos, porque um só quebra metade dos casos.

    fill  = preenche 9:16 escalando e cortando as laterais. Serve para culto
            filmado (pessoas no palco): o miolo é a ação, a lateral é cenário.
    fit   = cabe 9:16 mantendo o quadro inteiro, sobre fundo desfocado. É o
            único jeito de conteúdo com TEXTO na tela sobreviver: no modo fill
            "Deus Não Desiste de Você" vira "ão Desiste c" — o corte lateral
            come metade das palavras. Verificado no frame, não suposto.
    """
    if modo == "fill":
        return ("scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,setsar=1[v]")
    # fit: fundo desfocado preenche, quadro original inteiro por cima
    return ("split[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,gblur=sigma=32,eq=brightness=-0.22[bg2];"
            "[fg]scale=1080:-2[fg2];"
            "[bg2][fg2]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")


def render(arq, cands, pasta, modo="fit"):
    """
    Corta os trechos em 9:16.

    TRÊS DEFEITOS CORRIGIDOS AQUI, TODOS ACHADOS MEDINDO O ARQUIVO:

    1. `-t` antes do `-i` limita a LEITURA da entrada, não a saída. Com
       `filter_complex` o resultado saiu com 109 s num corte pedido de 54 s.
       Correto: buscar rápido no keyframe anterior, e cortar exato na saída.

    2. Saída SEM faixa de áudio em 9 dos 12 cortes, porque com `filter_complex`
       o ffmpeg deixa de selecionar áudio automaticamente. Correto: `-map`
       explícito no vídeo filtrado e no áudio de entrada.

    3. `-c copy` na concatenação de origem deixa PTS descontínuo, e o seek
       então erra o alvo. Correto: seek em dois tempos (bruto + fino).

    O erro passou na primeira verificação porque eu só olhei se o arquivo
    existia e tinha mais de 20 KB. Existir não é estar correto: agora a
    verificação compara a duração real do vídeo e do áudio com o pedido.
    """
    os.makedirs(pasta, exist_ok=True)
    feitos, ruins = [], []
    vf = filtro_video(modo)

    for n, c in enumerate(cands, 1):
        saida = os.path.join(pasta, f"culto-c{n:02d}.mp4")
        ini, dur = float(c[0]), float(c[2])
        # busca bruta 1,5 s antes (rápida, cai em keyframe) + busca fina na saída
        pre = max(0.0, ini - 1.5)
        fino = ini - pre
        cmd = ["ffmpeg", "-y", "-v", "error"]
        if pre > 0:
            cmd += ["-ss", f"{pre:.3f}"]
        cmd += ["-i", arq]
        if fino > 0:
            cmd += ["-ss", f"{fino:.3f}"]
        cmd += ["-t", f"{dur:.3f}", "-filter_complex", vf,
                "-map", "[v]", "-map", "0:a?",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-shortest",
                "-movflags", "+faststart", saida]
        rodar(cmd)

        ok, motivo = conferir_corte(saida, dur)
        if ok:
            c.append(f"culto-c{n:02d}.mp4")
            feitos.append(c)
        else:
            ruins.append(f"c{n:02d}: {motivo}")
            print(f"  ! corte {n:02d} rejeitado — {motivo}")
    if ruins:
        print(f"  {len(ruins)} cortes rejeitados na verificação")
    return feitos


def conferir_corte(saida, pedido):
    """Existir não é estar certo: compara duração e presença de áudio."""
    if not os.path.exists(saida):
        return False, "não foi criado"
    if os.path.getsize(saida) < 20000:
        return False, "arquivo vazio"

    def d(sel):
        o = rodar(["ffprobe", "-v", "error", "-select_streams", sel,
                   "-show_entries", "stream=duration", "-of", "csv=p=0", saida])
        try:
            return float(o.strip().split(",")[0])
        except Exception:
            return 0.0

    dv, da = d("v:0"), d("a:0")
    if dv <= 0:
        return False, "sem vídeo"
    if da <= 0:
        return False, "sem áudio"
    if abs(dv - pedido) > max(1.5, pedido * 0.08):
        return False, f"duração {dv:.0f}s, pedido {pedido:.0f}s"
    return True, ""


def escrever_revisao(nome, cands, dur, base, achou_voz):
    L = [f"# Cortes propostos — {nome}", "",
         f"Origem: **{dur/60:.0f} min** · {len(cands)} trechos", "",
         "> **Isto é medido pelo áudio, não pelo texto.** O script não entende o",
         "> que foi dito. Ele encontrou voz contínua, ênfase e pausa de pregador.",
         "> Ouça cada trecho antes de publicar — a decisão do conteúdo é sua.", ""]
    if not achou_voz:
        L += ["## Nenhuma fala detectada", "",
              "O áudio é música/instrumental contínuo ou o limiar não separou voz.",
              "Confira se o arquivo tem faixa de áudio e se o culto tem pregação.",
              "Se for só louvor, use `--min` menor e publique como clipe musical."]
    else:
        L += ["| # | Início | Duração | Nota | Pausas | Voz | Aprovar |",
              "|---|---|---|---|---|---|---|"]
        for n, c in enumerate(cands, 1):
            mm, ss = int(c[0] // 60), int(c[0] % 60)
            L.append(f"| {n:02d} | {mm}:{ss:02d} | {c[2]:.0f}s | {c[3]} | {c[4]} | "
                     f"{c[5]:.2f} | ☐ |")
        L += ["", "## Como ler a nota", "",
              "- **42%** presença de banda de voz (300–3400 Hz) sobre o fundo",
              "- **38%** energia acima do piso do próprio arquivo",
              "- **12%** duração na faixa ideal (22–45 s)",
              "- **+6** quando há 2 ou mais pausas longas (marca de ênfase)",
              "",
              "Nota alta = **boa acústica de púlpito**. Não é atestado de conteúdo."]
    with open(os.path.join(base, "REVISAO.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--min", type=float, default=MIN_CORTE)
    ap.add_argument("--max", type=float, default=MAX_CORTE)
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--modo", choices=["fit", "fill"], default="fit",
                    help="fit=cabe o quadro (texto na tela sobrevive); "
                         "fill=preenche cortando laterais (culto filmado)")
    a = ap.parse_args()

    if not os.path.exists(a.video):
        print(f"não encontrado: {a.video}")
        return 1
    nome = os.path.splitext(os.path.basename(a.video))[0]
    base = os.path.join("work", "culto", nome)
    os.makedirs(base, exist_ok=True)

    dur = dur_seg(a.video)
    print(f"  {nome} — {dur/60:.1f} min")

    tmp = os.path.join(base, "a.pcm")
    if not pcm(a.video, tmp):
        print("  ! sem faixa de áudio utilizável")
        return 1

    perf = energia_bandas(tmp)
    os.remove(tmp)
    if not perf:
        print("  ! áudio curto demais para analisar")
        return 1

    fala, piso, teto, lim_rz = eh_fala(perf)
    pct = fala.mean() * 100
    print(f"  voz detectada em {pct:.0f}% do tempo "
          f"(piso {piso:.0f} dB, limiar de voz {lim_rz:.1f} dB)")

    blocos = blocos_fala(fala, perf["janela"])
    print(f"  {len(blocos)} blocos de fala")

    pausas = pausas_longas(fala, perf["janela"])
    cands = recortar(blocos, a.min, a.max, perf["db"], perf["janela"])
    cands = pontuar(cands, perf, pausas, piso, teto)
    cands = escolher(cands, a.top)

    json.dump({"video": os.path.basename(a.video), "duracao": dur,
               "voz_pct": round(float(pct), 1), "blocos": len(blocos),
               "candidatos": [{"inicio": c[0], "fim": c[1], "dur": c[2],
                               "nota": c[3], "pausas": c[4], "voz": c[5]}
                              for c in cands]},
              open(os.path.join(base, "analise.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    escrever_revisao(nome, cands, dur, base, bool(cands))
    print(f"  {len(cands)} candidatos -> {base}/")

    if a.render and cands:
        print("  renderizando 9:16...")
        feitos = render(a.video, cands, os.path.join(base, "cortes"), a.modo)
        print(f"  {len(feitos)} cortes em {base}/cortes/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
