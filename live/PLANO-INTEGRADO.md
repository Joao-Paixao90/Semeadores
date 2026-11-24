# Plano integrado — sermões, live, cultos e cortes

Tudo aqui está produzido e verificado. O que falta depende de você — e está marcado.

---

## 1. O QUE JÁ EXISTE (medido, não estimado)

| Frente | Quantidade | Onde |
|---|---|---|
| Vídeos longos (YouTube) | 6 | `sermoes/video-*.mp4` |
| Cortes verticais dos sermões | 19 | `sermoes/cortes/` |
| Legendas (5 redes) | 80 | `sermoes/cortes-legendas/` |
| Miniaturas YouTube | 6 | `sermoes/publicacao/thumb-*.jpg` |
| Metadados de publicação | 6 | `sermoes/publicacao/youtube-*.txt` |
| Teleprompter (no ar) | 6 roteiros | joao-paixao90.github.io/Semeadores/teleprompter/ |
| Telas de live (1920×1080) | 3 | `live/abertura,intervalo,encerramento` |
| Aviso de live + story | 2 | `live/aviso-live*.jpg` |
| Cortador de culto | 1 ferramenta | `scripts/semeadores/cortar_culto.py` |
| Cortes de exemplo (validados) | 4 | `live/exemplo-cortes-culto/` |

---

## 2. O CORTADOR DE CULTO — o que ele faz e o que não faz

**Uso:**
```
python3 scripts/semeadores/cortar_culto.py culto.mp4 --render
```
Saída: `work/culto/<nome>/` com `analise.json`, `REVISAO.md` e `cortes/*.mp4` em 9:16.

**Faz:** encontra onde há voz contínua, ênfase e pausa de pregador, medindo a
banda de voz (300–3400 Hz) contra o resto do espectro. Funciona mesmo com
música de fundo — foi justamente o caso que quebrou a primeira versão.

**NÃO faz:** não transcreve. Não há ASR nesta máquina (torch, ctranslate2 e
vosk não têm wheel para ARM). Ele **não sabe o que foi dito**. Portanto:

> **Ouça cada corte antes de publicar.** O script propõe; a decisão é sua.
> Cortar culto no automático e publicar sem revisão é publicar sem ouvir.

**Desempenho real:** 17 minutos analisados em **1,4 segundo**.

**Dois modos de enquadramento** — e a escolha importa:
- `--modo fit` (padrão): o quadro inteiro cabe em 9:16 sobre fundo desfocado.
  Use quando houver **texto na tela**.
- `--modo fill`: preenche cortando as laterais. Use quando for **culto
  filmado** (pessoas no palco, sem texto).

---

## 3. LIVE — o requisito real, medido hoje

Canal consultado agora: **0 inscritos · 1 vídeo · 13 visualizações**.

| Método | Inscritos | Veredito |
|---|---|---|
| **Computador (webcam)** | **nenhum** | ✅ **liberado** |
| OBS / codificador | nenhum | ✅ liberado |
| Celular | **50** | ❌ faltam 50 |

**Consequência:** a live de hoje é **pelo computador**. Para transmitir o culto
do celular direto, faltam inscritos — o caminho alternativo é **celular ligado
ao PC por cabo**, que conta como transmissão de computador e funciona já.

**Ativação leva até 24 h.** Verifique o canal e ative em youtube.com/features
agora, mesmo que a primeira live seja semana que vem.

Estrutura de 20 minutos e cenário: `live/KIT-LIVE.md`.

---

## 4. CALENDÁRIO — a semana inteira, alternando formatos

| Semana | Terça (vídeo longo) | Quinta (live 20h) | Cortes da semana |
|---|---|---|---|
| 1 · 26/11 | Vale dos Ossos Secos | "Por que Deus permite o vale?" | 3 |
| 2 · 01/12 | Deus Não Desiste de Você | "Graça e misericórdia — a diferença" | 3 |
| 3 · 08/12 | Qual o Tamanho do Seu Deus | Perguntas sobre Romanos 8 | 3 |
| 4 · 15/12 | Deixe de Ser Cego | "Cegueira espiritual" | 3 |
| 5 · 22/12 | Não Temas, Crê Somente | Perguntas sobre Lucas 8 | 3 |
| 6 · 29/12 | Salmo 150 | "Por que louvamos" | 2 |

**Por que alternar:** vídeo longo constrói biblioteca e busca orgânica; live
constrói relacionamento e faz o público voltar. Canal pequeno não sustenta um
formato sozinho.

**Culto:** quando houver gravação, o cortador gera os cortes; eles entram na
semana como bônus, não substituem o vídeo de terça.

---

## 5. O QUE FALTA — e quem faz

| # | Passo | Tempo | Por que |
|---|---|---|---|
| 1 | Verificar canal + ativar live | 2 min + 24 h de espera | Só o dono da conta |
| 2 | Gravar abertura/fecho dos 6 sermões | 25 min | Precisa da sua voz |
| 3 | Subir 1 vídeo por semana | 8 min cada | Cota da API bloqueada |
| 4 | Criar produto dos sermões na Kiwify | 10 min | Acesso ao painel |
| 5 | Autorização do pastor p/ filmar culto | — | Direito de imagem |

**Sobre o item 5:** transmitir culto exige autorização do pastor e aviso de que
está sendo gravado. Membro aparecendo sem consentimento é problema jurídico
real, não hipótese.

---

## 6. A CONTA HONESTA

Sem gravação da sua voz, o canal é 100% sintético — o perfil que o YouTube
classificou em jul/2026 como "genérico ou repetitivo" e **inelegível para
monetização**. 60 segundos da sua voz por vídeo mudam a classificação do canal
inteiro. São 25 minutos de gravação protegendo 6 vídeos.

**4.000 horas:** 6 vídeos × 2min15 = 13,5 min. Precisa de ~17.800
visualizações completas. Isso não vem de 6 vídeos — vem de **52 vídeos em 12
meses**, 1 por semana sem falhar. As lives aceleram porque geram cortes: uma
live de 60 min deve render **no mínimo 10 cortes**.

**Culto é a maior fonte de material que você tem** — 1 culto de 90 minutos
alimenta 15 a 20 cortes por semana. É o único formato que escala sem você
gravar nada novo.
