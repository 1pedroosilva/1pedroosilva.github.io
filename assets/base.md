# Design system do portfólio · contrato

Versão 1.0, em construção · referência de origem: página do projeto CVM (`/projeto-cvm/`)

Enquanto a 1.0 não for usada nas páginas e revisada, tudo é considerado parte dela: acréscimos entram sem trocar o número. O número só passa a mudar (ver §13) depois da primeira versão estável, isto é, quando as páginas usarem o contrato de fato e você tiver revisado o conjunto funcionando.

Este documento é o contrato visual e de escrita para todas as páginas do portfólio em `1pedroosilva.github.io`. Ele tem três partes que andam juntas:

| arquivo | papel |
|---|---|
| `base.md` | as regras (este documento) |
| `assets/base.css` | a implementação das regras em tokens e componentes |
| `assets/base.js` | os comportamentos compartilhados (tema, índice, topo, abas, simulação de log) |

Precedência: quando uma página precisar de algo que o contrato não cobre, o componente novo nasce dentro da página, e só entra no `base.css` depois de ser usado em uma segunda página. Nada de página sobrescreve token.

---

## 1. Princípios

**Problema antes de solução.** Toda seção de projeto abre pelo problema, em linguagem de quem não conhece a ferramenta. O termo técnico vem depois, na nota técnica ou nas etiquetas de termos.

**Duas camadas de leitura.** O texto em serifa é para qualquer leitor. O texto em mono carrega metadado, dado, código e vocabulário técnico. Quem quer só a história lê a serifa; quem quer a engenharia abre o acordeão.

**Demonstrar em vez de afirmar.** Quando um comportamento do sistema pode ser mostrado, ele vira simulação interativa, sempre marcada com a etiqueta `simulação`.

**Registro honesto.** Decisões desfeitas aparecem, marcadas em `--flag`. O que não foi construído aparece como `off`, e não é escondido.

**Uma ousadia só.** O único movimento automático é a entrada do hero. Todo o resto do movimento responde a uma ação do leitor.

---

## 2. Cor

Oito tokens, dois temas. Nenhuma página declara cor fora desta tabela.

| token | claro | escuro | papel |
|---|---|---|---|
| `--paper` | `#E4E7E3` | `#151B19` | fundo da página |
| `--panel` | `#EDEFEC` | `#1C2321` | superfície elevada: simulação, aba, widget |
| `--panel-deep` | `#D9DDD8` | `#111716` | superfície rebaixada: código, estado "antes" |
| `--ink` | `#16201C` | `#DCE3DE` | texto principal, valor em destaque |
| `--ink-soft` | `#5A6560` | `#8B9891` | texto secundário, rótulo, lede |
| `--rule` | `#BFC6C0` | `#2C3633` | fio, borda, item desligado ou inexistente |
| `--accent` | `#0F4C42` | `#79C4B0` | link, estado atual, seleção, acerto |
| `--flag` | `#9C4A2F` | `#D4785C` | decisão desfeita, alerta, falha |
| `--on-accent` | `var(--panel)` | `#101614` | texto sobre fundo `--accent` |

Regras de uso:

- `--accent` significa "isto é o atual, o escolhido ou o que deu certo". Não serve para decorar.
- `--flag` significa "isto foi desfeito ou deu errado". Aparece em no máximo um tipo de elemento por seção.
- `--rule` como cor de texto indica ausência (etapa não construída, prefixo "termos", seta em repouso).
- Hierarquia de superfície: `--paper` < `--panel` < nada acima. Não existe terceiro nível de elevação e não existe sombra.
- Transparência só em controles fixos, via `color-mix(in srgb, var(--paper) 85–88%, transparent)` com `backdrop-filter: blur(9px)`.

---

## 3. Tipografia

Duas famílias, com papéis que não se misturam.

| família | fonte | uso |
|---|---|---|
| `--serif` | Newsreader (opsz 6–72, pesos 300–600) | títulos, texto corrido, perguntas, títulos de acordeão |
| `--mono` | JetBrains Mono (400, 500) | marcadores, navegação, rótulos, dados, código, notas técnicas, botões |

Carregamento (idêntico em todas as páginas):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Escala em serifa

Base: `body` 17px (16px abaixo de 520px), `line-height: 1.62`.

| elemento | tamanho | peso |
|---|---|---|
| `h1` | `clamp(1.95rem, 5.2vw, 3rem)` | 400, `max-width: 22ch` |
| `h2` | `clamp(1.4rem, 3.6vw, 1.85rem)` | 500 |
| `h3`, `--fs-lg` | `1.06rem` | 500 |
| `--fs-xl` (pergunta central) | `1.14rem` | 400 |
| `--fs-md` (problema, título de acordeão) | `1.02rem` | 400/500 |
| corpo | `1rem` | 400 |
| `--fs-sm` (dentro de acordeão, aba, linha do tempo) | `.95rem` | 400 |

Títulos: `line-height: 1.2`, `letter-spacing: -.012em`.

### Escala em mono

| token | tamanho | onde |
|---|---|---|
| `--fs-mono-2xs` | `.6rem` | etiqueta `simulação`, prefixo `termos` |
| `--fs-mono-xs` | `.64rem` | botões, escala do slider, código, etiquetas de termo, data da linha do tempo |
| `--fs-mono-sm` | `.68rem` | índice, navegação entre seções, log, tabela, nota técnica, status |
| `--fs-mono-md` | `.72rem` | marcador de seção, voltar, rodapé, CTA, número de etapa |
| `--fs-mono-lg` | `.85rem` | `h4` em mono, valor numérico em painel |
| `--fs-mono-display` | `1.5rem` | número em destaque do readout |

Nota de migração: a página do CVM usa onze tamanhos mono entre `.58rem` e `.74rem`. A escala acima consolida em seis, com diferença máxima de `.02rem` para cada valor original. Ao migrar a página do CVM para o `base.css`, basta remover o `<style>` embutido; a variação visual fica abaixo do perceptível.

### Regras tipográficas

- Rótulos em mono são sempre em caixa baixa (`o problema`, `em curso`, `próxima`). Nada em caixa alta.
- Números em tabela, log e readout usam `font-variant-numeric: tabular-nums`.
- Negrito dentro de mono (`<b>`) só troca a cor para `--ink` e o peso para 500; serve para o termo técnico principal da frase.
- Texto corrido nunca passa de `--col` (31.5rem, por volta de 65 caracteres).
- `text-wrap: balance` em títulos e rótulos; `text-wrap: pretty` em parágrafos. Sem hifenização.

---

## 4. Espaço, medida e grade

| token | valor | uso |
|---|---|---|
| `--col` | `31.5rem` | largura máxima de texto de leitura e de componentes de conteúdo |
| `--col-wide` | `62rem` | largura de blocos de dado: tabela, matriz, gráfico. Aplicada por bloco com a classe `.wide`, ou à página inteira pelo perfil relatório |
| `--row-key` | `132px` | coluna de rótulo do `.row`; uma página pode aumentar sem tocar no componente |
| `--page-max` | `1040px` | largura máxima da `.shell` |
| `--gutter` | `clamp(1.15rem, 4vw, 3rem)` | margem lateral |
| `--rail-w` | `186px` | coluna do índice lateral |
| `--rail-gap` | `3.6rem` | espaço entre índice e conteúdo |
| `--space-section` | `3.6rem` | padding vertical de cada `section` |
| `--space-block` | `1.6rem` | distância entre texto e o componente que o segue |
| `--space-inner` | `1rem` | padding interno de painel |

Grade: uma coluna até 999px; a partir de 1000px, `186px | 1fr` com o índice fixo à esquerda. Conteúdo alinhado à esquerda, sempre. Nada centralizado, exceto o texto dentro das pílulas de `.chain`.

Pontos de quebra (só estes quatro):

| largura | o que muda |
|---|---|
| `≤ 520px` | corpo 16px, hero mais baixo, `.ask` menor, painéis de `.diff` mais compactos |
| `≥ 560px` | `.prob` vira duas colunas |
| `≥ 640px` | `.row` vira duas colunas (132px + 1fr) |
| `≥ 1000px` | aparece o índice lateral, some a `.railbar` |

---

## 5. Forma

- `--radius: 2px` em tudo que tem borda. Círculos só no marcador da linha do tempo e no polegar do slider.
- Borda padrão: `1px solid var(--rule)`. Borda de ênfase: `2px`, só à esquerda (`.ask`, `.tech-note`) ou como divisória do comparador.
- Sem sombra, sem gradiente, sem imagem decorativa.
- Separação entre seções por fio superior (`border-top`), nunca por mudança de fundo.

---

## 6. Movimento

| token / regra | valor |
|---|---|
| `--step` | `220ms`, transição de cor, borda e fundo em hover e seleção |
| `--ease-out` | `cubic-bezier(.2,.7,.3,1)` |
| entrada do hero (`.reveal`) | `.6s`, deslocamento de 9px, atraso escalonado de `.06s` a `.27s` |
| linha de log (`slidein`) | `.3s`, atraso de 45ms a 70ms por linha |
| troca de aba (`fadein`) | `--step` |

Regras: `.reveal` só no hero. Nenhuma seção entra animada ao rolar. `prefers-reduced-motion: reduce` zera tudo, inclusive `scroll-behavior`.

---

## 7. Componentes

Cada componente abaixo existe no `base.css`. O markup mostrado é o mínimo obrigatório.

### 7.1 Estrutura da página

Do topo para baixo: a faixa de navegação do site (`.sitenav`), os controles fixos, a barra de progresso, e a `.shell` com índice, conteúdo e rodapé. A `.sitenav`, a `.tema`, a `.topo` e a `.railbar` ficam fora da `.shell`.

```html
<nav class="sitenav" aria-label="Navegação do site">
  <ul>
    <li><a href="/" data-nav="inicio">início</a></li>
    <li><a href="/projeto-cvm/" data-nav="cvm">CVM</a></li>
    <li><a href="/projeto-databricks-skills/" data-nav="skills">skills</a></li>
    <li><a href="/genie-skills-eval/" data-nav="avaliacao">avaliação</a></li>
  </ul>
</nav>

<button class="tema" id="tema" type="button" aria-label="Alternar tema"></button>
<button class="topo" id="topo" type="button"><span>&#8593;</span> topo</button>

<div class="railbar">
  <span id="railLabel" data-padrao="o projeto">o projeto</span>
  <span class="bar"><i id="railFill"></i></span>
</div>

<div class="shell">
  <nav class="index" aria-label="Seções da página">
    <ol>
      <li><a href="#secao"><span class="num">01</span> rótulo</a></li>
      <li class="gap"></li>
      <li><a href="#outra"><span class="num">··</span> rótulo</a></li>
    </ol>
  </nav>
  <main>
    <!-- primeira seção começa com a trilha, ver 7.1-bis -->
    <!-- sections -->
    <footer>...</footer>
  </main>
</div>
```

Numeração no índice: `01`, `02`... só quando as seções formam uma sequência real (etapas de um pipeline). Seções que não são etapa usam `··`. O `li.gap` separa o bloco sequencial do bloco transversal.

### 7.1-bis Navegação do site, trilha e rodapé

Estes três são iguais em todas as páginas (a trilha é o único que cada página declara por si) e dão a sensação de site único. As duas navegações contam coisas diferentes: a faixa diz para onde se pode ir; a trilha diz onde se está.

**Faixa de navegação do site (`.sitenav`).** Lista os quatro destinos fixos, na mesma ordem em toda página: início · CVM · skills · avaliação. A escolha é editorial, não estrutural: a avaliação aparece na faixa mesmo sendo um aprofundamento de skills, por ser peça de destaque do portfólio. Cada `<a>` traz um `data-nav`; o `base.js` acende o atual lendo `data-atual` no `<body>`:

```html
<body data-atual="cvm">
```

Só isto muda por página. Um destino sem correspondência (uma página fora dos quatro) deixa a faixa sem item aceso, o que é aceitável.

**Trilha (`.trilha`).** O caminho hierárquico da página, no lugar do antigo `.back`. É o primeiro elemento do `main`, dentro da primeira seção. O último item é a página atual, sem link, marcado com `aria-current="page"`:

```html
<nav class="trilha" aria-label="Trilha">
  <a href="/">início</a>
  <span class="sep">/</span>
  <a href="/projeto-databricks-skills/">skills</a>
  <span class="sep">/</span>
  <span aria-current="page">a avaliação</span>
</nav>
```

Por página: a home não tem trilha (é a raiz); a CVM tem `início / pipeline da CVM`; skills tem `início / skills`; a avaliação tem `início / skills / a avaliação`. Quem chega de fora, direto numa página funda, vê o caminho inteiro e sobe por ele, mesmo sem ter passado pelos níveis acima. A trilha reflete a estrutura real, ainda que a faixa seja editorial.

**Rodapé (`footer`).** Só ícones, sem texto visível, herdando a cor do tema. Cada link leva um `aria-label`, porque um ícone sozinho não se anuncia a um leitor de tela. Os três SVG (LinkedIn, GitHub, envelope) estão em 7.1-ter, para copiar:

```html
<footer>
  <p class="redes">
    <a href="https://www.linkedin.com/in/1pedroosilva/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><!-- svg linkedin --></a>
    <a href="https://github.com/1pedroosilva" target="_blank" rel="noopener noreferrer" aria-label="GitHub"><!-- svg github --></a>
    <a href="mailto:1pedro.osilva@gmail.com" aria-label="E-mail"><!-- svg envelope --></a>
  </p>
  <p class="nota">São Paulo, Brasil.</p>
</footer>
```

A `.nota` é opcional, para uma linha de fecho. Como não usamos montagem automática, a faixa e o rodapé são idênticos por virem deste modelo; ao mudar um deles, muda-se em cada página. Com poucas páginas, isso é barato; se o site crescer muito, revê-se a decisão.

### 7.1-ter Ícones do rodapé (SVG para copiar)

```html
<!-- LinkedIn -->
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>

<!-- GitHub -->
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.44 9.8 8.21 11.39.6.11.82-.26.82-.58 0-.29-.01-1.24-.02-2.25-3.34.73-4.04-1.42-4.04-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.5.99.11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.53.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.87.12 3.18.77.84 1.23 1.91 1.23 3.22 0 4.61-2.81 5.62-5.49 5.92.43.37.82 1.1.82 2.22 0 1.61-.02 2.9-.02 3.29 0 .32.22.7.83.58A12 12 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>

<!-- Envelope -->
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 4h20a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm10 9.13L2.4 6.5H2v.28l10 6.9 10-6.9V6.5h-.4L12 13.13zM2 8.6V18h20V8.6l-10 6.9-10-6.9z"/></svg>
```

O `viewBox` é `0 0 24 24` nos três, para o tamanho sair uniforme. A cor vem de `fill:currentColor`, então segue o tema sem ajuste.

### 7.2 Hero

```html
<section class="hero" id="inicio">
  <nav class="trilha reveal" aria-label="Trilha">
    <a href="/">início</a>
    <span class="sep">/</span>
    <span aria-current="page">pipeline da CVM</span>
  </nav>
  <p class="marker reveal"><b>1.01</b> &nbsp;projeto</p>
  <h1 class="reveal">Título da página</h1>
  <p class="pstatus reveal">&#9679; <b>em curso</b> &nbsp;·&nbsp; complemento</p>
  <p class="ask reveal">A pergunta que o projeto responde.</p>
</section>
```

A trilha (7.1-bis) abre o hero, no lugar do antigo `.back`. `.marker` leva o código da página no portfólio em `<b>`. `.pstatus` aceita três estados: `em curso`, `concluído`, `pausado`. `.ask` é uma pergunta, não um resumo.

### 7.3 Cabeçalho de seção

Seção comum:

```html
<p class="marker">rótulo curto</p>
<h2>Título</h2>
<p class="lede">Parágrafo de abertura.</p>
```

Toda seção com `id` começa com as setas de navegação sequencial (7.3-bis), logo depois do `marker` ou do `stage`.

Seção que é etapa de sequência:

```html
<div class="stage"><span class="n">01</span><h2>Captura</h2></div>
<nav class="navsec" aria-label="Navegação entre seções"></nav>
<p class="q"><em>o problema</em> Descrição do problema.</p>
```

O rótulo do `.q` é `o problema` para etapa construída e `o que seria` para etapa ainda não construída.

### 7.3-bis Setas de navegação sequencial

Duas setas de ícone, no início de cada seção com `id`, para pular à seção anterior ou à seguinte. É o único mecanismo de navegação sequencial do site, igual em celular e desktop; substituiu a antiga navegação com palavras (`.passo`). O "voltar ao topo" fica com o botão `.topo`, e o salto para qualquer seção fica com o índice lateral, então as setas só precisam de anterior e próxima.

A página escreve apenas o contêiner vazio, no início de cada seção; o `base.js` preenche as duas setas a partir da ordem das seções, desativa a de cima na primeira e a de baixo na última, e põe o rótulo de acessibilidade com o nome da seção de destino.

```html
<section id="minha-secao">
  <p class="marker">rótulo</p>
  <nav class="navsec" aria-label="Navegação entre seções"></nav>
  <!-- conteúdo -->
</section>
```

O hero não recebe `.navsec` (é o ponto de partida). Seções sem `id` são ignoradas pela navegação.

### 7.4 Mapa de etapas

```html
<div class="chain">
  <a href="#captura"><span class="dot">&#9679;</span> 01 captura <span class="ar">&#8595;</span></a>
  <a class="off" href="#entrega"><span class="dot">&#9675;</span> 04 entrega <span class="ar">&#8595;</span></a>
</div>
<p class="hint"><span style="color:var(--rule)">&#9675;</span> ainda não construída</p>
```

Círculo cheio (`&#9679;`) para construído, vazio (`&#9675;`) com `.off` para não construído. Sempre com a legenda `.hint` quando houver algum `.off`.

### 7.5 Etiquetas de termos

```html
<div class="temas"><em>termos</em><span>termo um</span><span>termo dois</span></div>
```

Lista de vocabulário técnico da seção, para quem procura palavra-chave. Entre dois e cinco termos. Fica logo depois do componente principal da seção.

### 7.6 Acordeão

```html
<div class="acc">
  <details class="first">
    <summary><h4>como funciona</h4></summary>
    <div class="dbody">
      <p>Explicação em linguagem comum.</p>
      <p class="tech-note">Versão técnica, com o termo principal em <b>negrito</b>.</p>
    </div>
  </details>
</div>
```

O primeiro `details` leva `.first` para ganhar o fio superior. Título do acordeão em caixa baixa, como pergunta ou tema curto.

### 7.7 Nota técnica e código

`.tech-note` é sempre o último parágrafo do bloco que explica. `.code` mostra trecho real do repositório, com o caminho do arquivo:

```html
<div class="code">
  <div class="file">pasta/<b>arquivo.py</b></div>
<pre><span class="cm"># comentário</span>
codigo <span class="kw">palavra</span>(<span class="st">"texto"</span>)</pre>
</div>
```

Três classes de realce, e só elas: `.cm` comentário, `.kw` palavra-chave, `.st` string.

### 7.8 Simulação

Todo componente interativo que ilustra comportamento do sistema fica dentro de `.sim` e leva a etiqueta `simulação`.

```html
<div class="sim">
  <div class="simhead">o que está sendo simulado <span class="tag">simulação</span></div>
  <div class="btns" id="grupoBtns">
    <button type="button" aria-pressed="true">cenário 1</button>
    <button type="button" aria-pressed="false">cenário 2</button>
  </div>
  <div class="log" id="grupoLog"></div>
</div>
```

```html
<script>
Base.simulacaoLog('#grupoBtns button', '#grupoLog', [
  {ln:[['01','etapa concluída','mut'],['02','falhou aqui','bad']], sum:'resumo com <b>destaque</b>'},
  {ln:[['01','etapa concluída','hit']], sum:'outro resumo'}
]);
</script>
```

Estados de linha do log: `mut` (neutro, nada aconteceu), `hit` (ação bem-sucedida), `bad` (falha ou risco). O `.sum` fecha com a consequência, e o `<b>` marca a parte que importa.

Variantes do corpo da simulação:

- **controle deslizante com leitura**: `input[type=range]` + `.scale` (dois extremos) + `.readout` com `.meta` e `.big`, dentro de `<div class="sim-body">`.
- **comparador antes/depois**: `.diff` com `.pane.b` (antes, `--panel-deep`) e `.pane.a` (depois, recortado por `clip-path` conforme o slider). Use `.warn` para a frase que mostra o erro.
- **tabela vinculada**: `tr[data-on="true"]` destaca a linha correspondente ao estado atual.

### 7.9 Abas

```html
<div class="tabs" role="tablist" aria-label="Descrição do grupo">
  <button type="button" role="tab" data-tab="um" aria-selected="true">um</button>
  <button type="button" role="tab" data-tab="dois" aria-selected="false">dois</button>
</div>
<div class="tabbody">
  <div class="tabpanel" role="tabpanel" data-tabpanel="um">
    <h4>Título</h4>
    <p class="one">resumo em uma linha</p>
    <p>Texto.</p>
  </div>
  <div class="tabpanel" role="tabpanel" data-tabpanel="dois" hidden>...</div>
</div>
```

O `base.js` cuida de clique e das setas do teclado. Cada painel segue a ordem título, `.one`, texto, `.tech-note`, `.temas`.

### 7.10 Linha do tempo de decisões

```html
<ul class="tl">
  <li data-undo="true">
    <details>
      <summary><span class="d">20 set</span><h4>O que decidi, em primeira pessoa</h4></summary>
      <div class="dbody">
        <p>Contexto e motivo.</p>
        <p class="tech-note">O que mudou tecnicamente.</p>
      </div>
    </details>
  </li>
</ul>
```

`data-undo="true"` para decisão que desfez uma escolha anterior (marcador em `--flag`). Ordem: da mais recente para a mais antiga. Data no formato `dd mmm`, mês em três letras minúsculas.

### 7.11 Linhas chave/valor, lista de problemas, chamada para ação

- `.rows` > `.row` > `.k` + `.v`: pendências, fichas técnicas, metadados. Dentro de `.v`, um `<small>` vira sublinha de apoio, em texto menor e suave.
- `.probs` > `a.prob` > `.t` + `.g`: lista navegável de itens com um rótulo curto à direita.
- `.go` > `a.main` (uma por página, ação principal) + `a` secundários. Links externos com `target="_blank" rel="noopener noreferrer"`.

---

## 7-bis. Perfis de página

Toda página parte da mesma base (cor, tipografia, estrutura, controles fixos). O perfil só decide quais componentes e larguras ela habilita. São três.

**Projeto** é o padrão, e não precisa declarar nada. Coluna de leitura estreita (`--col`), hero de projeto, as etapas e simulações. É o que a página da CVM usa.

**Perfil** é a home: um cartão de identidade com vitrine dos projetos. Usa o hero de perfil (§7-bis.1), o mapa de trabalho (§7-bis.3) e, no celular, a navegação em abas (§7-bis.4). Marca-se ligando as abas no `main`:

```html
<main data-abas-mobile>
```

**Relatório** é a página de análise com muitos dados, como a avaliação das skills. A página inteira passa a usar a coluna larga, declarando o perfil no `main`:

```html
<main data-perfil="relatorio">
```

Nesse perfil, `--col` já vale `--col-wide` para a página toda, então tabelas, matrizes e o placar ocupam a largura de dado sem cada bloco precisar da classe `.wide`. O texto corrido continua legível porque os parágrafos mantêm o próprio limite. Fora do perfil relatório, um bloco largo isolado (uma tabela dentro de uma página de projeto) recebe a classe `.wide`.

### 7-bis.1 Hero de perfil

```html
<section class="hero" id="topo">
  <p class="role reveal">Engenharia de dados · Databricks</p>
  <h1 class="reveal">Pedro Oliveira</h1>
  <p class="stmt reveal">Frase-manifesto de uma a três linhas.</p>
  <p class="links reveal">
    <a href="...">linkedin</a><a href="...">github</a><a href="mailto:...">e-mail</a>
  </p>
  <!-- opcional: mapa de trabalho, §7-bis.3 -->
</section>
```

`.role` é o papel profissional em mono, na cor de acento. `.stmt` é o texto de abertura, maior que o corpo. Difere do hero de projeto, que abre com `.back`, `.marker`, `.pstatus` e `.ask`.

### 7-bis.2 Subtítulo do hero de projeto

Uma linha em mono logo abaixo do `h1`, para explicar um termo do título:

```html
<h1 class="reveal">Skills para o Genie Code</h1>
<p class="sub reveal">o agente de IA para engenharia de dados da Databricks</p>
```

### 7-bis.3 Mapa de trabalho

Grade de cartões que apontam para outras páginas, um em destaque com `.forte`:

```html
<nav class="mapa reveal" aria-label="O trabalho">
  <a class="mp" href="/projeto-x/">
    <span class="et">investigar</span>
    <span class="tt">Título do projeto</span>
    <span class="ds">Uma frase sobre o que é.</span>
  </a>
  <a class="mp forte" href="/destaque/">
    <span class="et">evidência</span>
    <span class="tt">O projeto em destaque</span>
    <span class="ds">A frase do que se destaca.</span>
  </a>
</nav>
```

`.et` é a etiqueta de verbo (investigar, construir, evidência), `.tt` o título em acento, `.ds` a descrição. O cartão `.forte` ganha fundo de painel e uma seta no título.

### 7-bis.4 Navegação em abas no celular

Uma barra `.atalhos` que, no desktop, some (a navegação é o índice lateral), e no celular vira abas: cada clique troca a seção visível em vez de rolar. Depende de `data-abas-mobile` no `main` e é ligada pelo `base.js`.

```html
<nav class="atalhos" aria-label="Seções da página">
  <a href="#stack">stack</a>
  <a href="#trajetoria">experiência</a>
  <a class="fora" href="/outra-pagina/">avaliação &#8599;</a>
</nav>
```

Um link para outra página leva `.fora` (cor de acento) e não participa da troca de abas.

---

## 7-ter. Componentes de ilustração e de dado

### 7-ter.1 Prancha

Ilustração de abertura com legenda e troca automática entre tema claro e escuro. Fornecer as duas imagens; a de tema escuro pode ter `alt` vazio, por ser decorativa equivalente.

```html
<figure class="prancha reveal">
  <img class="clara" src="/prancha.png" width="1200" height="630" decoding="async" alt="descrição">
  <img class="escura" src="/prancha-dark.png" width="1200" height="630" decoding="async" alt="">
  <figcaption>Legenda da ilustração.</figcaption>
</figure>
```

### 7-ter.2 Braços de experimento

Tronco comum e dois braços paralelos (por exemplo, com e sem tratamento). O braço em foco recebe `.on`.

```html
<div class="bracos">
  <p class="comum">o que os dois braços têm em comum</p>
  <div class="par">
    <div class="arm on"><p class="ak">braço A</p><p class="av">o que muda no A</p></div>
    <div class="arm"><p class="ak">braço B</p><p class="av">o que muda no B</p></div>
  </div>
</div>
```

### 7-ter.3 Rede interativa

Grafo SVG cujos nós, ao receberem foco, realçam os vizinhos e preenchem um cartão de leitura ao lado. Todo o dado (posições, arestas, textos) mora na página; o `base.js` só liga o comportamento.

Estrutura mínima: um `.rede` com o `<svg>` dentro, cada nó um `<g class="nd" data-no="id">` contendo `.dot`, `text`, `.halo` e uma área de clique `.hit`; cada aresta uma linha `.ed` com `data-a` e `data-b`. Ao lado, o cartão `.redecard` com `.rcdom`, um `h3`, um `.rctxt` e um `.rcdica`. A página chama:

```html
<script>
Base.rede({
  svg: '#minhaRede',
  card: { dom:'#rcDom', titulo:'#rcTit', texto:'#rcTxt', dica:'#rcDica' },
  inicial: 'no-1',
  nos: {
    'no-1': { dominio:'domínio', titulo:'Título', texto:'Descrição.', dica:'dica opcional', vizinhos:['no-2'] }
  }
});
</script>
```

### 7-ter.4 Placar

Cartão de resultado numérico, versão do readout com moldura, para destacar um número-chave de um relatório.

```html
<div class="placar">
  <div class="plcab">o que este número mede</div>
  <div class="corpo">
    <span class="meta">leitura antes do número</span>
    <span class="big">+38%</span>
    <span class="meta">leitura depois do número</span>
  </div>
</div>
```

### 7-ter.5 Matriz de células

Grade de células, algumas clicáveis, para representar sessões, execuções ou uma tabela cruzada. Cabeçalho em `.mcab`, cada fila em `.lin`, cada célula em `.cel` (com `.head` para rótulo, `a.cel`/`button.cel` para célula navegável). Como as colunas variam por página, defina `grid-template-columns` no HTML da página ou num `<style>` local. A seleção liga-se por:

```html
<script>
Base.matriz('.matriz a.cel', function(cel){ /* abre o detalhe de cel.dataset... */ });
</script>
```

O leitor de transcrição que a página de avaliação usa para abrir cada sessão fica na própria página, fora do contrato, até uma segunda página precisar dele.

---

## 8. Esqueleto obrigatório do `<head>`

Toda página começa assim. Os campos entre chaves mudam por página.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{Título da página} · Pedro Oliveira</title>

<meta name="robots" content="index, follow">
<meta name="author" content="Pedro Oliveira">
<meta name="description" content="{descrição de uma a duas frases}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="https://1pedroosilva.github.io/{caminho}/">

<meta property="og:type" content="article">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="https://1pedroosilva.github.io/{caminho}/">
<meta property="og:title" content="{título}">
<meta property="og:description" content="{a pergunta do .ask}">
<meta property="og:image" content="https://1pedroosilva.github.io/og.png">
<meta name="twitter:card" content="summary_large_image">

<meta name="color-scheme" content="light dark">
<script>
(function(){
  var t=null;
  try{t=localStorage.getItem('tema');}catch(e){}
  if(!t) t = matchMedia('(prefers-color-scheme: dark)').matches ? 'escuro' : 'claro';
  document.documentElement.dataset.tema=t;
})();
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/base.css">
</head>
```

E no fim do `<body>`:

```html
<script src="/assets/base.js"></script>
```

A tag `<body>` declara o destino atual da faixa de navegação, que o `base.js` acende: `<body data-atual="cvm">` (valores: `inicio`, `cvm`, `skills`, `avaliacao`). A faixa `.sitenav` é o primeiro elemento do `<body>`, antes dos controles fixos (ver 7.1).

O script de tema fica inline no `<head>` de propósito: ele precisa rodar antes da primeira pintura para a página não piscar no tema errado. A chave no `localStorage` é `tema`, com os valores `claro` e `escuro`.

Páginas de projeto acrescentam JSON-LD `SoftwareSourceCode` com `name`, `description`, `url`, `codeRepository`, `programmingLanguage`, `runtimePlatform` e `author`.

---

## 9. Escrita

A voz da página faz parte do sistema tanto quanto a cor.

- Português brasileiro, primeira pessoa do singular nas decisões ("Troquei", "Descobri"), terceira pessoa na descrição do sistema ("A captura grava").
- Frases de título em caixa de frase: só a primeira letra e nomes próprios em maiúscula.
- Rótulos em mono: caixa baixa, sem ponto final, de uma a quatro palavras.
- Cada seção de projeto responde, nesta ordem: qual é o problema, o que acontece se ninguém resolver, como foi resolvido, qual é o termo técnico.
- Número concreto em vez de adjetivo ("quinhentas e quarenta companhias", não "a maioria").
- Sem travessão longo. Use vírgula, dois-pontos ou ponto.
- O que é ilustrativo leva a etiqueta `simulação`. O que é trecho real de código leva o caminho do arquivo.
- Pendências são ditas como fato, com o motivo de ainda estarem abertas.

---

## 10. Acessibilidade

- Foco visível em tudo: `outline: 2px solid var(--accent)`, `outline-offset: 3px`.
- Grupos de botões alternáveis usam `aria-pressed`; abas usam `role="tablist"`, `role="tab"`, `role="tabpanel"` e `aria-selected`.
- Todo `input[type=range]` e todo botão sem texto visível tem `aria-label`.
- Estado nunca depende só de cor: `.off` troca também o símbolo, `tr[data-on]` ganha o `▸`, `.bad` vem com texto que descreve a falha.
- Contraste mínimo AA para `--ink-soft` sobre `--paper` e `--panel` nos dois temas. Ao propor cor nova, conferir antes de entrar no contrato.
- Tabela larga fica dentro de `.table-wrap` para rolar sozinha no celular.

---

## 11. Fora do contrato

- Cor fora dos oito tokens, inclusive tons intermediários "só desta vez".
- Sombra, gradiente, `border-radius` acima de 2px, ícone decorativo.
- Terceira família tipográfica, ou peso de Newsreader fora de 300–600.
- Texto em caixa alta.
- Animação de entrada fora do hero, ou animação que roda sem ação do leitor.
- Numeração `01 / 02 / 03` em conteúdo que não é sequência.
- Componente de simulação sem a etiqueta `simulação`.

---

## 12. Checklist de página nova

1. Perfil escolhido (projeto, perfil ou relatório) e declarado no `main` quando não for projeto.
2. `<head>` copiado do §8, com título, descrição, canonical e OG preenchidos.
3. `base.css` e `base.js` carregados; nenhum `<style>` redefinindo token.
4. Hero conforme o perfil: de projeto (`.back`, `.marker`, `h1`, `.pstatus`, `.ask`) ou de perfil (`.role`, `h1`, `.stmt`, `.links`).
5. Índice lateral e `.railbar` com os mesmos rótulos, na mesma ordem das seções.
6. Cada seção de projeto abre pelo problema e fecha com `.temas`, quando houver vocabulário técnico.
7. Toda simulação marcada; todo código com caminho de arquivo; todo bloco de dado em `--col-wide` (classe `.wide` ou perfil relatório).
8. Conferida nos dois temas, em 375px e em 1280px, e com `prefers-reduced-motion` ativo.
9. Navegação completa só com teclado.

---

## 13. Como o contrato muda

Enquanto a 1.0 está em construção, acréscimos e ajustes entram sem trocar o número: o contrato ainda está sendo formado. A primeira versão estável é marcada quando as páginas usarem o contrato de fato e o conjunto tiver sido revisado funcionando.

A partir daí, mudança de token ou de componente compartilhado entra por commit próprio, com a versão do cabeçalho incrementada: o segundo número para adição que não quebra página existente (`1.0` → `1.1`), o primeiro para mudança que exige revisar páginas já feitas (`1.x` → `2.0`). A mensagem do commit diz o que mudou e quais páginas precisam ser revisadas.
