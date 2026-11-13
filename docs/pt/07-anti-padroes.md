# ⚠️ 07 · Catálogo de Anti-padrões

*As armadilhas medidas e nomeadas da engenharia de software com IA*

---

## 1. Por que um catálogo

Nomear a forma uma vez vale mais que consertar onze instâncias. Cada entrada abaixo foi **observada e medida** antes de receber nome; o catálogo cresce por evidência, não por analogia.

## 2. Anti-padrões de decisão e documento

### §6.1 · Ratify-and-write
- **Sintoma:** propor uma decisão no mesmo documento que a declara aprovada. Sintoma verbal: *"decisões já tomadas, este plano só escreve o rationale"*.
- **Remédio:** minutas nascem `PROPOSED`; a ratificação é artefato separado que cita evidência, SHA e nível de prova. Quem propõe não ratifica.

### §6.5 · Spec que prescreve o que já existe
- **Sintoma:** "propõe-se construir" para algo entregue há meses. Confunde plano com realidade.
- **Remédio:** sweep da Fase 8 sincroniza tempo verbal e status (`Active / Living`).

### §6.6 · Inversão de hierarquia
- **Sintoma:** o código diverge da spec; altera-se a spec para perdoar o atalho.
- **Remédio:** reconciliação ascendente ([03](03-hierarquia-da-verdade.md)). O código nunca vence por já estar no ar.

### §6.8 · Capitulação à camada conveniente
- **Sintoma:** ao auditar um drift, aceitar a primeira explicação fácil ("a docstring dizia X") sem verificar se uma ADR acima revogou a cláusula. Um lado capitula, emite *mea culpa*, e o drift real fica mascarado de "engano".
- **Remédio:** toda claim de reconciliação declara sua camada autoritativa e confirma contra a **mais alta** que fala do assunto.

### Arquitetura decidida implicitamente em plano de implementação
- **Sintoma:** protocolo ou topologia aparecem como pressuposição num plano, sem ADR própria. A implementação fixa o desenho antes do debate.
- **Remédio:** toda decisão que restringe alternativas futuras tem ADR.

## 3. Anti-padrões de release e operação

### §6.2 · Release composta com risco heterogêneo
- **Sintoma:** refatoração cosmética e migração destrutiva sob a mesma tag. O revisor aprova pela trivialidade da primeira e ignora o risco da segunda.
- **Remédio:** homogeneidade de risco: mudanças destrutivas ou de segurança trafegam sozinhas.

### §6.3 · Idempotente como falsa segurança
- **Sintoma:** um script rotulado "idempotente" executa rotação de chave ou migração irreversível como efeito colateral.
- **Remédio:** idempotência significa *estado final convergente*, não "seguro para rerodar" nem "reversível". O pré-voo enumera os efeitos de **cada passo**, não do wrapper. "Idempotente" é bandeira amarela.

### §6.4 · Soft gate sem critério de promoção
- **Sintoma:** gate introduzido em modo não bloqueante sem data, volume amostral ou métrica que o torne bloqueante. Vira débito perpétuo.
- **Remédio:** toda flag em `shadow` nasce com gate de saída declarado no charter.

### §6.7 · Estado crítico fora da fonte (config-as-state)
- **Sintoma:** flag, job ou postura que governa comportamento vivendo só no runtime ou na memória do operador. Um redeploy reverte em silêncio.
- **Remédio:** *se governa comportamento, vive na fonte versionada*, inclusive o flip de cut-over desde o commit do cut-over.

### Composição de flips não exercitada
- **Sintoma:** vários gates viram na mesma janela, cada um com pré-voo do próprio chamador, nenhum com pré-voo do **produto**. O gate quebra a **pergunta**, não a resposta, e não há saída por dentro.
- **Remédio:** item de composição no pré-voo: quais outros gates mudaram, e o produto deles foi exercitado com comando e resultado.

## 4. Anti-padrões de andaime e flag

### Mock que vira medida
- **Sintoma:** valor constante produzido por stub gravado em dados de produção e lido como telemetria viva.
- **Remédio:** proveniência por atributo (`real | curated | unknown`); raio histórico medido antes do desmock.

### Fallback silencioso para stub
- **Sintoma:** falha de transporte devolve `status=success` com contagens sintéticas porque o caminho de stub assumiu.
- **Remédio:** stub atrás de flag com default desligado, valor explícito e log alto; erro honesto (`503`) quando a dependência cai.

### Flag fantasma
- **Sintoma:** flag declarada na configuração, zero consumidores no código.
- **Remédio:** sweep AST da Fase 8; a flag é removida ou ganha consumidor.

### Existência sem via
- **Sintoma:** o artefato existe e está correto, mas não há caminho dele até um consumidor. A revisão olha para dentro da peça e não vê.
- **Remédio:** critério de saída em forma de aresta; rastrear até o consumidor. Controle exposto em interface sem consumidor **fabrica confiança**.

### Colapso benigno
- **Sintoma:** dois estados distintos colapsam num mesmo observável, e o sobrevivente é o que **não exige ação**. Um parâmetro cuja semente coincide com o comportamento implementado é indetectável por observação.
- **Remédio:** só um valor **discordante** o testa. O par discordável aqui não é opcional; é a única sonda que discrimina.

## 5. Anti-padrões de medição e teste

### Teste verde pela causa errada
- **Sintoma:** a asserção passa porque a fixture nunca escreveu o dado, ou porque mede a divergência de um shadow desligado.
- **Remédio:** *probe-and-revert*: injetar o defeito exato e confirmar o vermelho antes de aceitar o verde.

### Nome que declara uma propriedade e asserção que mede outra
- **Sintoma:** teste "flag vive na fonte" cravando um valor específico. Falha num flip legítimo; passa numa flag fantasma com o valor certo.
- **Remédio:** a asserção mede a propriedade que o nome declara (R28).

### Denominador que se move com o numerador
- **Sintoma:** registro de dívida que conta só o pendente; quitar encolhe o registro e o corpus pune consertar.
- **Remédio:** denominador é o **declarado** (R29).

### Corroboração com ancestral comum
- **Sintoma:** N artefatos concordam, todos descendentes da mesma enumeração. Peso de um, aparência de N.
- **Remédio:** independência de origem antes de contar concordância.

## 6. A dialética do §11: improvisação × governança

```
          [ ZONA DA MORTE ]                      [ ZONA DA MORTE ]
    Improvisação permanente (§11a)         Governança permanente (§11b)
    · sem specs, ADRs, contratos           · cerimônias infinitas
    · o LLM improvisa a cada prompt        · auditoria que nunca converge em deploy
    · o humano vira depurador perpétuo     · spec tão densa quanto o código
    · colapso por alucinação e spec-rot    · alavanca de abstração = 0
                     ╲                          ╱
                      ╲   ◆ ponto de equilíbrio ╱
                       ╲  spec densa o bastante para eliminar
                          alucinação estrutural, abstrata o
                          bastante para preservar a alavanca;
                          governança executável por scripts
```

> **A EEE não busca burocracia por vaidade acadêmica.** O antídoto operacional à governança permanente é a R10 (ordenar por taxa de degradação) e a Fase 8 executada por scripts, não por reuniões.
