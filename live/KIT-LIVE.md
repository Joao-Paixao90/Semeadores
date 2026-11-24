# Kit de Live — Semeadores da Palavra

## O que você já tem aqui

| Item | Arquivo | Uso |
|---|---|---|
| Tela de espera | `artifacts/semeadores/live/abertura.png` | Antes de entrar no ar |
| Tela de pausa | `artifacts/semeadores/live/intervalo.png` | Se precisar sair |
| Encerramento | `artifacts/semeadores/live/encerramento.png` | Últimos 60 s |
| Aviso de live | `aviso-live.jpg` (1920×1080) | Post "hoje tem live" |
| Aviso story | `aviso-live-story.jpg` (1080×1920) | Story no dia |

Todas as telas são 1920×1080, prontas para cena no OBS ou para compartilhar tela.

---

## O requisito real, medido hoje

Consultei o canal: **0 inscritos · 1 vídeo · 13 visualizações**.

A regra do YouTube, verificada em 24/10/2026:

| Método | Inscritos exigidos | Outro requisito |
|---|---|---|
| **Computador (webcam)** | **nenhum** | Canal verificado + sem restrição nos últimos 90 dias |
| **OBS / codificador** | **nenhum** | Canal verificado + chave de transmissão |
| **Celular** | **50** | Canal verificado + recurso ativado |

**Conclusão prática:** a live **pelo computador já está liberada**. A do celular não — faltam 50 inscritos.

Isso muda a estratégia: **a live de hoje é pelo computador**, com a câmera do notebook ou do PC. Se você quiser live na rua ou no culto, aí precisa dos 50 inscritos no celular (ou espelhar o celular no PC por cabo, que conta como computador).

**Atenção:** a primeira ativação de live pode levar **até 24 horas**. Ativar hoje para transmitir amanhã, não ativar e tentar no mesmo minuto.

Fontes:
- [Elegibilidade geral](https://support.google.com/youtube/answer/9228390?hl=pt-BR) — YouTube Ajuda
- [How to Go Live on YouTube (2026)](https://www.tubeanalytics.net/pt/blog/how-to-go-live-on-youtube) — verificado 24/10/2026

---

## Ativação — 3 passos, uma vez só

1. **Verificar o canal**: youtube.com/verify — número de telefone, leva 1 minuto.
2. **Ativar transmissão ao vivo**: youtube.com/features → "Transmissão ao vivo" → ativar. **Pode levar 24 h.**
3. **Testar privado**: faça uma live de 2 minutos como "privada", só para ver se o áudio e a câmera funcionam.

**Faça o 1 e o 2 agora**, mesmo que a primeira live seja semana que vem. A espera de 24 h é o único passo que não dá para acelerar.

---

## A live de 20 minutos — estrutura

Sem estrutura, live de igreja vira conversa solta que ninguém assiste até o fim.

| Tempo | Bloco | O que dizer |
|---|---|---|
| 0:00–2:00 | **Abertura** | "Estamos ao vivo. Hoje vamos ver [tema] em [passagem]. Escreve de onde você está assistindo." |
| 2:00–6:00 | **Leitura** | Ler o texto inteiro, devagar. Uma vez. Sem comentar ainda. |
| 6:00–14:00 | **Ensino** | Três pontos. Um por bloco. Cada ponto com uma pergunta ao chat. |
| 14:00–18:00 | **Perguntas** | Ler 3 ou 4 perguntas do chat e responder. É o que faz a live valer mais que um vídeo. |
| 18:00–20:00 | **Fecho** | Oração + "comenta AMÉM" + dizer qual é o próximo tema |

**A pergunta ao chat é obrigatória.** Live sem interação é vídeo ruim com atraso. Pergunta concreta ("onde você está assistindo?", "qual desses três te pegou?") produz comentário; pergunta vaga ("alguma dúvida?") produz silêncio.

---

## Cenário — o que resolve 90% da qualidade

| Item | O que fazer | Por quê |
|---|---|---|
| **Luz** | Janela na sua frente, nunca atrás | Luz atrás = rosto preto |
| **Som** | Fone com microfone, ou celular como mic a 30 cm | Áudio ruim afasta mais que imagem ruim |
| **Fundo** | Parede limpa, sem bagunça | O cérebro julga credibilidade em 3 s |
| **Enquadramento** | Rosto no terço superior, olhos na linha de 1/3 | Você olha para a câmera, não para a tela |
| **Internet** | Cabo se possível; 5 Mbps de subida | Wi-Fi caindo no meio da live mata o alcance |

---

## Moderação — o que fazer com o chat

- **Palavra-chave bloqueada**: configure a lista de palavras ofensivas antes de ir ao vivo (Studio → Configurações → Chat).
- **Moderador**: se tiver alguém de confiança, promova a moderador. Sozinho, você não consegue ensinar e moderar.
- **Não discuta**: herege no chat existe para desviar sua atenção. Silencie sem anunciar.
- **Comentário bom**: marque como "destacado". Isso ensina o público o que você quer ali.

---

## Depois da live — o que a live deixa de valor

A live em si rende pouco tempo de exibição para as 4.000 horas. O valor real dela é o **material**:

1. **O arquivo da live** vira 8 a 15 cortes verticais. O `cortar_culto.py` faz isso.
2. **Os melhores momentos** viram Shorts que puxam gente para a live seguinte.
3. **O tema da live** vira um vídeo longo editado, se o conteúdo foi bom.

**Regra:** uma live de 60 minutos deve virar **no mínimo 10 cortes**. Se não render isso, a live foi conversa sem tema — e a próxima precisa de roteiro.

---

## Calendário sugerido (alternando com os sermões)

| Semana | Terça (vídeo) | Quinta (live) |
|---|---|---|
| 1 | Vale dos Ossos Secos | Live: "Por que Deus permite o vale?" |
| 2 | Deus Não Desiste de Você | Live: "Graça e misericórdia — a diferença" |
| 3 | Qual o Tamanho do Seu Deus | Live: perguntas sobre Romanos 8 |
| 4 | Deixe de Ser Cego | Live: "Cegueira espiritual" |

**Por que alternar:** vídeo longo constrói biblioteca e busca; live constrói relacionamento e faz o público voltar. Um sem o outro não sustenta canal pequeno.

---

## O que falta para culto ao vivo

Transmitir o **culto** (não você na frente do PC) exige uma das duas:

**A) Celular com os 50 inscritos** — grátis, mas precisa chegar a 50.

**B) Celular no PC por cabo** — o celular entra como webcam do computador. Funciona hoje, com 0 inscritos, porque conta como transmissão de computador. Custo: um cabo USB e um app de webcam (a maioria dos Androids suporta nativo).

Recomendo o **B** para o primeiro culto. É o único caminho que funciona agora, sem esperar inscrito.

**Cuidado com direito de imagem:** transmitir culto ao vivo precisa da autorização do pastor e aviso de que está sendo gravado. Membros da igreja aparecendo sem consentimento é problema real, não teórico.
