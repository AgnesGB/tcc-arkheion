# Migração para funcionamento Offline-First

> Documento vivo. Registra **o que** mudou, **onde** e **por quê** em cada fase da
> migração do Arkheion para funcionar offline no navegador.

## Objetivo

Hoje toda a regra de negócio (cálculos de ficha de Tormenta 20) roda no backend
Django e é acessada por requisições REST — o app só funciona 100% online. A meta
é que o app **funcione offline no navegador** e, ao voltar a ter conexão, apenas
**sincronize as alterações** com o banco.

## Estratégia: PWA (não Tauri)

O app é **mobile-first** e não deve virar executável desktop nem depender de loja
de apps. Por isso o caminho escolhido é **PWA** (Progressive Web App): o próprio
Vue vira instalável na tela inicial do celular, abre sem rede (Service Worker) e
guarda os dados localmente (IndexedDB), sincronizando com o Django quando online.

> O Tauri (sugerido inicialmente) resolve empacotamento **desktop** — que não é o
> problema aqui — e ainda exigiria toolchain nativo/publicação em loja, sem poupar
> o trabalho central de portar as regras para o cliente.

## Decisão arquitetural central

A capacidade offline **não vem da "casca"** (PWA ou Tauri): vem de mover a lógica
e os dados para o cliente. Portanto:

1. As **regras de cálculo** passam a viver num motor em TypeScript, no cliente.
2. O **cliente** vira a **fonte única de verdade** dos cálculos.
3. O **Django** passa a ser essencialmente **armazenamento** (persiste o estado
   que o app envia).

## Fases

| Fase | Descrição | Status |
|------|-----------|--------|
| 0  | Motor de regras puro em TS + testes | ✅ Concluída |
| 0b | Ligar o app (store/model) ao motor e apagar a duplicação | ✅ Concluída |
| 1  | Persistência local (IndexedDB) | ✅ Concluída |
| 2  | PWA shell (Service Worker, abrir sem rede) | ✅ Concluída |
| 3  | Fila de sincronização (outbox) → Django ao voltar online | ✅ Concluída |
| 4  | Django como "só storage" + nível offline | ✅ Concluída |

---

## Fase 0 — Motor de regras puro (✅)

### Por quê

Os cálculos estavam **duplicados e divergentes** em três lugares:

- **Django** — `arkheion/backend/models.py` (`calcularVida`, `calcularMana`,
  `PericiaTreinada.calcularValor`, peso/valor de itens). Era a fonte "oficial".
- **Store do front** — `frontend/src/stores/ficha.store.ts`
  (`vidaMaximaCalculada`, `manaMaximaCalculada`, `calcularValorPericia`). **É o
  que a tela realmente mostra.**
- **Model do front** — `frontend/src/models/ficha.model.ts` (getters
  `vidaMaxima`/`manaMaximo`, `PericiaTreinada.calcularValor`). **Código morto**
  (nenhum componente usava), e ainda por cima divergente.

Divergências reais encontradas:

- **Vida:** o Django somava Constituição **uma única vez**; o store somava CON
  **por nível**. Ex.: guerreiro com vida-base 20, vida/nível 4, CON 3, nível 3 →
  a tela mostrava **37**, mas o Django calcularia **31**.
- **Perícia:** o `calcularValor` do *model* usava `(valor-10)/2` (modificador de
  D&D, **errado para T20**) e nem somava metade do nível.

Manter isso enquanto se adiciona offline só multiplicaria os motores divergentes.
A Fase 0 cria **um** motor, testado, para ser a fonte única.

### O que foi criado

Pasta nova **`frontend/src/rules/`** — módulo **puro**, sem `axios`/`pinia`/`vue`
(recebe dados simples, devolve números; roda offline e é testável isolado):

| Arquivo | Conteúdo |
|---------|----------|
| `rules/types.ts`      | Tipos de entrada mínimos e desacoplados |
| `rules/vida.ts`       | `calcularVidaMaxima` |
| `rules/mana.ts`       | `calcularManaMaxima` |
| `rules/pericia.ts`    | `calcularValorPericia`, `bonusTreinamento` |
| `rules/inventario.ts` | `pesoTotalItem`, `valorTotalItem`, `pesoTotalInventario`, `valorTotalInventario` |
| `rules/index.ts`      | Barrel de export |
| `rules/*.spec.ts`     | 21 testes (Vitest) |

### Regras implementadas (T20 correto — por decisão da autora)

- **Vida:** no 1º nível = vida-base da 1ª classe **+ CON**; a cada nível seguinte
  (mesma classe ou multiclasse) **+ (vida/nível + CON)**. → **CON entra em todos
  os níveis.** Corrige o Django.
- **Mana:** soma de `mana_por_nivel × nível` de cada classe. `mana_base` é
  ignorado (o PM de T20 vem por nível), mantendo o comportamento atual.
- **Perícia:** `⌊nível/2⌋ + soma dos atributos-chave (valor bruto) + bônus de
  treino + bônus adicional`. Perícia que exige treino e não treinada → 0.
- **Bônus de treino:** +2 (1º–6º), +4 (7º–14º), +6 (15º–20º). Corrige a faixa do
  Django, que virava +4 já no 6º nível.
- **Inventário:** peso/valor com padrão *Composite* (kits somam recursivamente o
  conteúdo × quantidade).

> ⚠️ Conferir no livro de T20 quando possível: (1) o corte do bônus de treino no
> 6º nível; (2) o `mana_base` realmente não entrar. Se algo mudar, é ajustar uma
> constante e o teste correspondente.

### Ferramental de teste

- **Vitest** adicionado (`devDependencies`, `^4`).
- `frontend/vite.config.ts`: passou a importar de `vitest/config` e ganhou o bloco
  `test` (`environment: 'node'`, `include: ['src/**/*.spec.ts']`).
- `frontend/package.json`: scripts `test` (`vitest run`) e `test:watch` (`vitest`).

Rodar:

```bash
cd frontend && npm test
```

---

## Fase 0b — Ligar o app ao motor e apagar a duplicação (✅)

### Por quê

Na Fase 0 o motor foi criado e testado, mas **ninguém o usava**. A duplicação
divergente continuava viva. A Fase 0b aponta o código real para o motor e **remove**
as fórmulas duplicadas, tornando o motor a única fonte de verdade de fato.

### O que mudou

**1. `frontend/src/stores/ficha.store.ts`** (é o que alimenta a tela)

- Passou a importar `calcularVidaMaxima`, `calcularManaMaxima` e
  `calcularValorPericia` (como `calcularValorPericiaRegra`) de `@/rules`.
- `vidaMaximaCalculada`: os ~35 linhas de fórmula inline viraram uma extração
  simples de CON + chamada a `calcularVidaMaxima(...)`.
- `manaMaximaCalculada`: a soma inline virou chamada a `calcularManaMaxima(...)`.
- `calcularValorPericia(pericia)`: a fórmula inline (com a faixa de treino antiga)
  virou chamada a `calcularValorPericiaRegra(...)`. A assinatura pública foi
  mantida — continua gravando `pericia.valor_calculado` — para não quebrar os
  componentes que a usam.

**2. `frontend/src/models/ficha.model.ts`** (antes: código morto e divergente)

- Passou a importar `calcularVidaMaxima`, `calcularManaMaxima`,
  `calcularValorPericia` e `bonusTreinamento` de `@/rules`.
- Getters `vidaMaxima` e `manaMaximo`: agora **delegam** ao motor.
- `PericiaTreinada.calcularValor()` e `verificarTreino()`: agora **delegam** ao
  motor (usando `this.ficha?.nivel`). Isso elimina a fórmula errada de D&D que
  estava aqui.

### Impacto visível ao usuário (mudança de comportamento intencional)

- **Vida máxima na tela pode mudar** para fichas com CON ≠ 0 e mais de 1 nível,
  porque agora bate com a regra T20 (CON por nível). Isso é **correção**, não bug.
- **Valor de perícia no 6º nível** (treinada) passa de +4 para +2, também por
  correção da faixa.

### O que **não** mudou

- Assinaturas públicas do store e as props dos componentes: intactas.
- O inventário do backend existe, mas **ainda não há consumidor no frontend** — o
  `rules/inventario.ts` fica pronto para quando a tela de inventário for ligada.
- O backend Django continua com sua própria cópia dos cálculos (ainda a fonte no
  save). A unificação com o backend acontece na Fase 4.

### Verificação

- `npm test` → 21 testes passando.
- `npm run type-check` → **zero** erros nos arquivos alterados (`ficha.store.ts`,
  `ficha.model.ts`, `src/rules/*`).

> Observação: o `type-check` do projeto já acusava erros **pré-existentes** em
> outros componentes (`AtaquesModal.vue`, `HabilidadesModal.vue`,
> `SubirNivelModal.vue`, `HomeView.vue`, etc.), sem relação com esta migração.

---

## Fase 1 — Persistência local (IndexedDB) (✅)

### Por quê

Para funcionar offline, o app precisa ter os dados **no dispositivo**, não só na
memória. Sem isso, ao recarregar sem rede não há nada para mostrar. A Fase 1
introduz um banco local (IndexedDB) e faz a leitura de ficha ser **cache-first**:
mostra a cópia local na hora e atualiza pela rede quando dá.

> A capacidade de **salvar alterações offline e enviá-las depois** (fila de
> outbox) é a Fase 3. A Fase 1 cuida do armazenamento e da leitura local.

### O que foi criado

- **`dexie`** (dependência): camada ergonômica sobre o IndexedDB.
- **`fake-indexeddb`** (devDependency): IndexedDB em memória para os testes.
- **`frontend/src/db/arkheionDB.ts`**: define o banco local `arkheion` (Dexie) com
  a tabela `fichas` (`FichaLocal = { id, dados, atualizadoEm }`). `dados` guarda o
  payload cru da ficha (mesmo shape da API), para reconstruir uma `Ficha` na
  leitura. Exporta a instância única `db`.
- **`frontend/src/services/offline/ficha.local.ts`**: repositório local, espelhando
  a leitura do `fichaService`:
  - `salvarFichaLocal`, `salvarFichasLocais` — grava (upsert) no cache;
  - `buscarFichaLocal(id)` → `Ficha | null`;
  - `listarFichasLocais()` → `Ficha[]`;
  - `removerFichaLocal(id)`.
  - As fichas são normalizadas com `JSON.parse(JSON.stringify(...))` antes de
    gravar, para remover métodos/getters e a reatividade do Vue (proxies não são
    clonáveis pelo IndexedDB).
- **`frontend/src/services/offline/ficha.local.spec.ts`**: 6 testes (upsert,
  busca, listagem, remoção, payload sem id, preservação do snake_case).

### O que mudou

**`frontend/src/stores/ficha.store.ts` — `carregarFicha(id)` virou cache-first:**

1. Lê `buscarFichaLocal(id)`; se existir, já exibe (resposta instantânea, offline).
2. Tenta `fichaService.buscarPorId(id)`; se conseguir, atualiza a tela e regrava
   no cache com `salvarFichaLocal(...)`.
3. Se a rede falhar **mas** já houver cópia local, segue com ela em silêncio (não
   é erro). Só mostra erro quando não há nem local nem rede.

### Impacto visível ao usuário

- Abrir uma ficha já visitada fica **instantâneo** (vem do cache) e **funciona
  sem internet**.
- Com rede, o comportamento é o mesmo de antes, com um passo extra invisível de
  regravar o cache.

### O que **não** mudou (ainda)

- **Escritas** (treino, bônus, recursos, subir nível) continuam indo direto para
  a API e falham se estiver offline — a fila de sincronização é a Fase 3.
- A **listagem** de fichas (`listarTodas`) ainda não usa o cache; o repositório já
  tem `listarFichasLocais`/`salvarFichasLocais` prontos para isso.

### Verificação

- `npm test` → 27 testes passando (21 do motor + 6 do repositório local).
- `npm run type-check` → zero erros nos arquivos novos/alterados.

---

## Fase 2 — PWA shell (✅)

### Por quê

A Fase 1 deu os **dados** offline (IndexedDB), mas o app em si ainda não abria sem
rede: ao recarregar sem internet, o navegador não tinha o HTML/JS/CSS. A Fase 2
transforma o site num **PWA**: um Service Worker cacheia o "app shell" (para abrir
offline) e um manifesto permite **instalar o app na tela inicial** do celular,
com ícone e tela cheia — sem loja, sem executável.

### O que foi criado / mudou

- **`vite-plugin-pwa`** (devDependency): gera o Service Worker (via Workbox) e o
  manifesto no build.
- **`frontend/public/pwa-icon.svg`**: ícone quadrado do app (512×512), desenhado na
  paleta da marca (fundo vinho/marrom, "A" mostarda). Serve para `any` e
  `maskable`.
- **`frontend/vite.config.ts`**: adicionado o plugin `VitePWA(...)` com:
  - `registerType: 'autoUpdate'` — o app se atualiza sozinho quando há versão nova;
  - `manifest` — nome, cores (`theme_color #590d1c`, `background_color #24140f`),
    `display: standalone`, `orientation: portrait`, `lang: pt-BR`, ícones;
  - `workbox` — pré-cache do app shell (`**/*.{js,css,html,ico,svg,woff,woff2}`) e
    `navigateFallback: '/index.html'` (SPA: navegação offline cai no index e o Vue
    Router assume a rota);
  - `devOptions.enabled: false` — SW só no build, para não atrapalhar o HMR do dev.
- **`frontend/index.html`**: `lang="pt-BR"`, `<title>` de "Vite App" → "Arkheion —
  Fichas de Tormenta 20", `meta description`, `meta theme-color` e
  `apple-touch-icon`. (O link do manifesto e o registro do SW são injetados pelo
  próprio plugin no build.)

### Separação de responsabilidades (importante)

O backend fica em **outra origem/porta** (ex.: `:8000`/`:30080`). Como o Service
Worker só age na própria origem, ele **não intercepta as chamadas de dados** — os
dados offline continuam 100% por conta do IndexedDB (Fase 1). O SW cuida só do
"app shell" (arquivos estáticos). Sem sobreposição entre as duas camadas.

### Como testar offline

O SW é gerado só no build (não no `npm run dev`):

```bash
cd frontend
npm run build-only   # gera dist/ com sw.js, manifest.webmanifest, registerSW.js
npm run preview      # serve o build localmente
```

No navegador (DevTools → Application): conferir o "Service Worker" ativo e o
"Manifest". Depois, em Network, marcar **Offline** e recarregar — o app deve abrir.
No celular, o Chrome oferece "Adicionar à tela inicial".

### O que **não** muda (ainda)

- Continua faltando **salvar alterações offline** e reenviá-las (fila de
  sincronização) — é a Fase 3.

### Verificação

- `npm run build-only` → build OK; `PWA v1.3.0` gerou `dist/sw.js`,
  `dist/workbox-*.js`, `dist/manifest.webmanifest`, `dist/registerSW.js` e copiou
  `pwa-icon.svg`; `index.html` passou a referenciar o manifesto e o `registerSW.js`.
- `npm test` → 27 testes seguem passando (o plugin não afeta os testes).

> ⚠️ Limitação conhecida: em iOS, o `apple-touch-icon` idealmente é PNG; o SVG pode
> não ser usado como ícone de tela inicial no Safari. Se virar requisito, gerar um
> PNG 180×180 a partir do `pwa-icon.svg`.

---

## Fase 3 — Fila de sincronização (outbox) (✅)

### Por quê

Até aqui o app **lia** offline, mas toda **escrita** ia direto para a API e falhava
sem rede. A Fase 3 permite **editar a ficha offline**: cada alteração é aplicada na
hora localmente e entra numa fila (outbox); quando a conexão volta, a fila é
enviada ao Django. É a peça que fecha o ciclo offline-first.

### Como funciona (padrão outbox + escrita otimista)

1. **Otimista:** a edição é aplicada imediatamente na ficha em memória e gravada no
   IndexedDB (o valor exibido é calculado pelo motor `@/rules`, não pelo servidor).
2. **Enfileira:** a alteração vira uma `MutacaoPendente` na tabela `mutacoes`.
3. **Sincroniza:** ao voltar a ter conexão (evento `online`) — ou logo após
   enfileirar, se já online — a fila é reenviada ao backend, em ordem.

**Coalescência:** cada mutação tem uma *chave* (`tipo:fichaId[:periciaId]`). Ao
enfileirar, a anterior de mesma chave é substituída. Assim a fila guarda o **estado
final desejado** de cada campo, não cada toque — bater +1 de vida 20× offline vira
**1** item, não 20.

**Conflito = last-write-wins:** como cada mutação "seta" o valor final de um campo
e é reenviada na ordem, o servidor termina com o último valor definido pelo usuário.

**Política de falhas na sincronização:**
- *Offline* (`navigator.onLine === false`): não envia nada; tudo fica na fila.
- *Falha de rede* (sem resposta do servidor): para e mantém a fila para depois.
- *Erro do servidor* (respondeu 4xx/5xx): conta a tentativa e, após `MAX_TENTATIVAS`
  (5), descarta a mutação para não travar a fila; segue para a próxima.

### O que foi criado / mudou

- **`frontend/src/db/arkheionDB.ts`**: schema **v2** com a tabela `mutacoes`
  (`++id, chave, fichaId, criadoEm`) e o tipo `MutacaoPendente`.
- **`frontend/src/services/offline/outbox.ts`** (novo):
  - `TIPOS` — os tipos de mutação suportados offline (treino, bônus, atributo-chave,
    recursos);
  - `enfileirarMutacao` — enfileira com coalescência;
  - `contarMutacoesPendentes` — nº de pendências (para a UI);
  - `sincronizarOutbox` — reenvia a fila conforme a política acima;
  - `MANIPULADORES` — mapeia cada tipo para a chamada REST correspondente.
- **`frontend/src/services/offline/outbox.spec.ts`** (novo): 8 testes (enfileirar,
  coalescência, envio online, offline, falha de rede, parada em ordem, erro de
  servidor).
- **`frontend/src/stores/ficha.store.ts`**: as escritas viraram offline-first:
  - `atualizarTreinamento`, `atualizarBonusAdicional`, `atualizarAtributoChave`,
    `salvarRecursos` agora: aplicam local → `persistirFichaLocal()` → `registrarMutacao(...)`.
    **Sem rollback** (offline deixou de ser erro).
  - novos: `pendentesSync` (ref reativa com o nº de pendências) e `sincronizar()`,
    ambos expostos no store; listener de `online` dispara a sincronização.
  - `subirUmNivel`/`setarNivel` ganharam guarda `exigeConexao()` — ver limitação.

### Impacto visível ao usuário

- Dá para **ajustar PV/PM, treino, bônus e atributo-chave sem internet**; as
  mudanças aparecem na hora e sobem sozinhas quando a conexão volta.
- A UI pode exibir um contador de pendências via `fichaStore.pendentesSync` (ex.:
  um selo "N alterações não sincronizadas"). *A tela ainda não mostra isso — é só
  ligar o valor num componente.*

### Limitação conhecida (intencional)

**Subir de nível / setar nível continuam exigindo conexão.** Essas operações são
estruturais: o Django adiciona níveis de classe, habilidades etc. e devolve a ficha
recalculada. Replicá-las offline exigiria trazer essa lógica para o cliente — é
trabalho de uma fase futura (relacionado à Fase 4). Offline, elas mostram uma
mensagem clara em vez de falhar de forma silenciosa.

### Verificação

- `npm test` → 35 testes passando (27 anteriores + 8 da outbox).
- `npm run type-check` → zero erros nos arquivos novos/alterados.
- `npm run build-only` → build OK.

---

## Fase 4 — Django como "só storage" + nível offline (✅)

### Descoberta ao investigar o backend

A investigação dos endpoints de escrita (`arkheion/backend/views.py`) revelou que o
**Django já é, na prática, "só storage" para os dados editáveis**:

- `update-resources`, `update-pericia-treino`, `update-pericia-bonus`,
  `update-pericia-atributo` apenas **gravam o dado-fonte** (vida/mana atual, treino,
  bônus, atributo-chave). O `calcularValor()` do servidor é usado **só na resposta**
  — e o cliente já **ignora** essa resposta desde a Fase 0b (usa o motor `@/rules`).
- Nenhum desses endpoints persiste valor derivado (não existe coluna
  `valor_calculado`/`vida_maxima` no banco). Logo, **o banco só guarda dado-fonte**.
- `subir-nivel` e `setar-nivel` (nível do personagem) apenas alteram o inteiro
  `nivel` — o trabalho estrutural (níveis de classe, habilidades) está em **outros**
  endpoints, fora do fluxo de edição da ficha.

Ou seja: o grande objetivo da Fase 4 ("cliente é a fonte de verdade, backend só
persiste") **já estava atingido** para o fluxo de edição — sem precisar mexer no
Django. O que faltava era completar o **offline** para a última escrita que ainda
exigia rede: o **nível**.

### O que mudou

- **`frontend/src/services/offline/outbox.ts`**: novo tipo `TIPOS.NIVEL`. O
  manipulador envia o nível **absoluto** via `setarNivel` (não um incremento), o que
  o torna coalescível e last-write-wins.
- **`frontend/src/stores/ficha.store.ts`**:
  - novo `definirNivel(novoNivel)` — aplica o nível localmente, recalcula as
    perícias (½ do nível e o bônus de treino dependem dele), persiste no IndexedDB e
    enfileira a mutação;
  - `subirUmNivel()` agora chama `definirNivel(nivel + 1)`;
  - `setarNivel(n)` agora chama `definirNivel(n)`;
  - **removida** a guarda `exigeConexao()` da Fase 3 — nível agora funciona offline.
- **`frontend/src/services/offline/outbox.spec.ts`**: +2 testes (coalescência de
  vários "subir nível" no valor final; sincronização via `setar-nivel`).

### Resultado

**Todo o fluxo de edição da ficha agora funciona offline** (recursos, treino,
bônus, atributo-chave e nível), com sincronização automática ao voltar online.

### O que permanece online (intencional)

Operações **estruturais** continuam exigindo conexão, pois o servidor faz trabalho
não-trivial e devolve a ficha remontada: adicionar/remover classe, subir nível de
uma classe específica, adicionar/remover habilidades e ataques, criar ficha,
homebrew. São ações mais raras e de "montagem" da ficha, não de jogo.

### Recomendação de backend (não aplicada — decisão da autora)

O Django ainda **carrega** cópias das fórmulas de cálculo (`calcularVida`,
`PericiaTreinada.calcularValor`, faixa de treino) nos models — hoje usadas só para
respostas que o cliente ignora, e que **divergem** da regra T20-correta do motor
(ver Fase 0). Como são código de cálculo que ninguém mais consome de forma
autoritativa, o ideal é **alinhá-las ao motor** (ou removê-las) para que as duas
implementações não voltem a divergir silenciosamente. Isso **não foi aplicado**
porque mexe no backend do TCC (na AWS) e os testes Django precisam ser rodados no
ambiente Python — fica como passo recomendado, a critério da autora.

### Verificação

- `npm test` → 37 testes passando (35 anteriores + 2 do nível offline).
- `npm run type-check` → zero erros nos arquivos alterados.
- `npm run build-only` → build OK.

---

## Situação atual

O núcleo do **offline-first está completo**: o app instala como PWA, abre sem rede,
**lê e edita** a ficha offline (recursos, perícias e nível) e **sincroniza** as
alterações com o Django quando a conexão volta. O backend permaneceu como storage
dos dados-fonte, sem alterações.

### Extra — Selo de sincronização na UI (✅)

Implementado `frontend/src/components/fichas/SyncStatus.vue` e encaixado no topo da
`views/ficha/FichaView.vue`. Um selo (Badge) que reflete o estado offline-first:

- **offline** (via `useOnline` do `@vueuse/core`): "Offline" (ou "Offline · N
  pendentes");
- **online com pendências**: "N alterações pendentes" — **clicável** para
  sincronizar na hora (ícone gira enquanto envia);
- **online sem pendências**: "Tudo sincronizado".

Lê `fichaStore.pendentesSync` e chama `fichaStore.sincronizar()`. (Correção de
tipo pré-existente em `FichaView.vue` — `logAlteracao` — aproveitada no caminho.)

### Ideias de continuidade (opcionais)

- **Alinhar o backend** às fórmulas do motor (ver recomendação da Fase 4).
- **Operações estruturais offline:** trazer para o cliente a lógica de níveis de
  classe/habilidades, hoje ainda server-side.
