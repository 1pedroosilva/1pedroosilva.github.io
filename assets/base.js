/* ==========================================================================
   base.js · comportamentos compartilhados do design system
   Carregar no fim do <body>: <script src="/assets/base.js"></script>
   O script de tema que evita o flash fica INLINE no <head> (ver contrato §8).
   ========================================================================== */
(function(){

  /* tema: botão .tema#tema */
  const btema = document.getElementById('tema');
  function pintaTema(t){
    document.documentElement.dataset.tema = t;
    if(btema){
      btema.textContent = t === 'escuro' ? 'claro' : 'escuro';
      btema.setAttribute('aria-pressed', String(t === 'escuro'));
    }
    try{ localStorage.setItem('tema', t); }catch(e){}
  }
  pintaTema(document.documentElement.dataset.tema || 'claro');
  if(btema) btema.addEventListener('click', () =>
    pintaTema(document.documentElement.dataset.tema === 'escuro' ? 'claro' : 'escuro'));

  /* botão de topo: .topo#topo, aparece depois de 700px de rolagem */
  const btopo = document.getElementById('topo');
  if(btopo) btopo.addEventListener('click', () => scrollTo({top:0, behavior:'smooth'}));

  /* faixa de navegação do site: acende o destino atual. a página informa
     qual é em <body data-atual="cvm">, e cada <a> traz data-nav="cvm". */
  const atual = document.body.dataset.atual;
  if(atual){
    document.querySelectorAll('.sitenav a[data-nav]').forEach(a =>
      a.setAttribute('aria-current', a.dataset.nav === atual ? 'page' : 'false'));
  }

  /* setas de navegação sequencial: em cada .navsec, gera anterior e próxima
     a partir da ordem das seções com id. A página só coloca <nav class="navsec">
     no início de cada seção; o resto é automático. Nos extremos, a seta que
     não se aplica fica apagada. */
  const navs = [...document.querySelectorAll('.navsec')];
  if(navs.length){
    const setaCima  = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>';
    const setaBaixo = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
    navs.forEach(nav => {
      const sec = nav.closest('section');
      if(!sec) return;
      const irmas = [...document.querySelectorAll('main section[id]')].filter(s => !s.classList.contains('hero'));
      const i = irmas.indexOf(sec);
      const ant = i > 0 ? irmas[i - 1] : null;
      const prox = i < irmas.length - 1 ? irmas[i + 1] : null;
      const rotulo = s => (s.querySelector('h2, h1')?.textContent || s.id).trim();
      nav.innerHTML =
        (ant
          ? '<a href="#' + ant.id + '" aria-label="Seção anterior: ' + rotulo(ant) + '">' + setaCima + '</a>'
          : '<span class="off" aria-hidden="true">' + setaCima + '</span>') +
        (prox
          ? '<a href="#' + prox.id + '" aria-label="Próxima seção: ' + rotulo(prox) + '">' + setaBaixo + '</a>'
          : '<span class="off" aria-hidden="true">' + setaBaixo + '</span>');
    });
  }

  /* índice lateral + barra de progresso */
  const links = [...document.querySelectorAll('.index a')];
  const label = document.getElementById('railLabel');
  const fill  = document.getElementById('railFill');
  if(links.length){
    const obs = new IntersectionObserver(es => {
      es.forEach(en => {
        if(!en.isIntersecting) return;
        const id = en.target.id;
        links.forEach(a => a.setAttribute('aria-current', String(a.getAttribute('href') === '#' + id)));
        const hit = links.find(a => a.getAttribute('href') === '#' + id);
        if(label) label.textContent = hit ? hit.textContent.trim().replace(/^\S+\s/, '') : (label.dataset.padrao || '');
      });
    }, {rootMargin:'-40% 0px -50% 0px'});
    document.querySelectorAll('main section[id]').forEach(s => obs.observe(s));
  }
  addEventListener('scroll', () => {
    const max = document.body.scrollHeight - innerHeight;
    if(fill) fill.style.width = (max > 0 ? (scrollY / max) * 100 : 0) + '%';
    if(btopo) btopo.classList.toggle('on', scrollY > 700);
  }, {passive:true});

  /* abas: [role=tablist] com botões data-tab e painéis data-tabpanel no mesmo bloco */
  document.querySelectorAll('[role="tablist"]').forEach(lista => {
    const botoes = [...lista.querySelectorAll('[role="tab"]')];
    const escopo = lista.parentElement;
    const paineis = [...escopo.querySelectorAll('[data-tabpanel]')];
    function ativa(b, foco){
      paineis.forEach(p => { p.hidden = p.dataset.tabpanel !== b.dataset.tab; });
      botoes.forEach(o => {
        const on = o === b;
        o.setAttribute('aria-selected', String(on));
        o.tabIndex = on ? 0 : -1;
      });
      if(foco) b.focus();
    }
    botoes.forEach((b, i) => {
      b.addEventListener('click', () => ativa(b));
      b.addEventListener('keydown', e => {
        if(e.key === 'ArrowRight') ativa(botoes[(i + 1) % botoes.length], true);
        if(e.key === 'ArrowLeft')  ativa(botoes[(i - 1 + botoes.length) % botoes.length], true);
      });
    });
    const inicial = botoes.find(b => b.getAttribute('aria-selected') === 'true') || botoes[0];
    if(inicial) ativa(inicial);
  });

  /* modo de abas no celular: main[data-abas-mobile] com uma .atalhos e
     seções irmãs identificadas por id. No desktop tudo aparece; no mobile
     só a seção da aba corrente. Ativa por atributo, para páginas de projeto
     não herdarem esse comportamento sem querer. */
  const palcoAbas = document.querySelector('main[data-abas-mobile]');
  if(palcoAbas){
    const mq = matchMedia('(max-width:999px)');
    const abas = [...palcoAbas.querySelectorAll('.atalhos a[href^="#"]')];
    const secoes = [...palcoAbas.querySelectorAll('section[id]:not(.hero)')];
    const lb = document.getElementById('railLabel');
    let atual = abas.length ? abas[0].getAttribute('href').slice(1) : null;
    function aplica(){
      if(mq.matches){
        secoes.forEach(s => { s.hidden = s.id !== atual; });
        abas.forEach(a => a.setAttribute('aria-current', String(a.getAttribute('href') === '#' + atual)));
        const alvo = abas.find(a => a.getAttribute('href') === '#' + atual);
        if(alvo && lb) lb.textContent = alvo.textContent.trim();
      } else {
        secoes.forEach(s => { s.hidden = false; });
        abas.forEach(a => a.removeAttribute('aria-current'));
      }
    }
    abas.forEach(a => a.addEventListener('click', e => {
      if(!mq.matches) return;
      e.preventDefault();
      atual = a.getAttribute('href').slice(1);
      aplica();
      const sec = secoes.find(s => s.id === atual);
      const barra = (document.querySelector('.railbar')?.offsetHeight || 0)
                  + (palcoAbas.querySelector('.atalhos')?.offsetHeight || 0);
      const y = sec.getBoundingClientRect().top + scrollY - barra;
      scrollTo({top:Math.max(0,y), behavior:'auto'});
    }));
    mq.addEventListener('change', aplica);
    aplica();
  }

  window.Base = {
    /* simulação de log: grupo de botões, alvo .log, dados [{ln:[[rótulo,texto,estado]], sum}] */
    simulacaoLog(grupo, alvo, dados, atraso = 45){
      const botoes = [...document.querySelectorAll(grupo)];
      const log = document.querySelector(alvo);
      function pinta(i){
        const d = dados[i];
        log.innerHTML = d.ln.map((l, k) =>
          '<div class="ln ' + l[2] + '" style="animation-delay:' + (k * atraso) + 'ms">' +
          '<span class="y">' + l[0] + '</span><span class="s">' + l[1] + '</span></div>'
        ).join('') + '<span class="sum">' + d.sum + '</span>';
        botoes.forEach((b, k) => b.setAttribute('aria-pressed', String(k === i)));
      }
      botoes.forEach((b, k) => b.addEventListener('click', () => pinta(k)));
      pinta(0);
    },

    /* rede SVG interativa. cfg: {svg, card:{dom,titulo,texto,dica}, nos:{id:{dominio,titulo,texto,dica,vizinhos:[]}}}.
       Cada nó no SVG é um <g class="nd" data-no="id">. Passar o mouse realça os vizinhos;
       clicar fixa a seleção e preenche o cartão. Toda a informação vem da página. */
    rede(cfg){
      const svg = document.querySelector(cfg.svg);
      if(!svg) return;
      const nds = [...svg.querySelectorAll('.nd')];
      const eds = [...svg.querySelectorAll('.ed')];
      const wrap = svg.closest('.rede');
      const card = cfg.card || {};
      const el = s => s ? document.querySelector(s) : null;
      const cDom = el(card.dom), cTit = el(card.titulo), cTxt = el(card.texto), cDica = el(card.dica);
      function vizinhos(id){ return (cfg.nos[id] && cfg.nos[id].vizinhos) || []; }
      function realca(id){
        const grupo = new Set([id, ...vizinhos(id)]);
        wrap.classList.add('ativa');
        nds.forEach(n => n.classList.toggle('on', grupo.has(n.dataset.no)));
        eds.forEach(e => {
          const a = e.dataset.a, b = e.dataset.b;
          e.classList.toggle('on', (a === id && grupo.has(b)) || (b === id && grupo.has(a)));
        });
      }
      function limpa(){
        wrap.classList.remove('ativa');
        nds.forEach(n => n.classList.remove('on'));
        eds.forEach(e => e.classList.remove('on'));
      }
      function escreve(id){
        const d = cfg.nos[id]; if(!d) return;
        if(cDom) cDom.textContent = d.dominio || '';
        if(cTit) cTit.textContent = d.titulo || '';
        if(cTxt) cTxt.textContent = d.texto || '';
        if(cDica){ cDica.textContent = d.dica || ''; cDica.hidden = !d.dica; }
      }
      function seleciona(id){
        nds.forEach(n => n.classList.toggle('sel', n.dataset.no === id));
        escreve(id); realca(id);
      }
      nds.forEach(n => {
        const id = n.dataset.no;
        n.setAttribute('tabindex','0');
        n.addEventListener('mouseenter', () => { if(!svg.querySelector('.nd.sel')) realca(id); });
        n.addEventListener('mouseleave', () => { if(!svg.querySelector('.nd.sel')) limpa(); });
        n.addEventListener('click', () => seleciona(id));
        n.addEventListener('keydown', e => { if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); seleciona(id); } });
      });
      if(cfg.inicial) seleciona(cfg.inicial);
    },

    /* seleção simples numa matriz de células: grupo de a.cel/button.cel,
       callback recebe o elemento clicado. Marca .sel na célula ativa. */
    matriz(grupo, aoSelecionar){
      const cels = [...document.querySelectorAll(grupo)];
      cels.forEach(c => c.addEventListener('click', e => {
        if(c.tagName === 'A' && c.getAttribute('href')?.startsWith('#')) e.preventDefault();
        cels.forEach(o => o.classList.toggle('sel', o === c));
        if(aoSelecionar) aoSelecionar(c);
      }));
    }
  };
})();
