# 🔬 05 · As Regras do Refinamento Empírico

*A anatomia da "família da resposta plausível" e as regras que dela decorrem*

---

## 1. O diagnóstico

> **Resposta plausível para a pergunta errada:** uma computação que devolve um valor **bem-formado, válido e tipado** para uma pergunta que **não foi feita**, tornando-se **indistinguível da resposta correta**.

O defeito nunca é um valor malformado. É o valor **certo para outra pergunta**. Por isso atravessa revisão humana e testes rasos: **parece resposta**.

A forma foi observada, no ecossistema de origem, em sete camadas distintas, e a camada mais instrutiva foi a última: **a família apareceu dentro dos instrumentos construídos para detectá-la**.

| Camada | Forma típica da instância |
|---|---|
| **Código** | Gate de segurança que valida corretamente a permissão sobre um sujeito **fornecido pelo próprio chamador**. Resposta de `success` com contagens sintéticas mascarando falha de transporte. Consulta de autorização contra relação inexistente que devolve `deny` idêntico ao `deny` legítimo. |
| **Dados** | Score constante gravado em milhares de registros e lido como medição. Atributo de proveniência "aprendido" sobre dado de andaime. `anchored:false` sobre segmento vazio: afirmação sem sujeito. |
| **Spec** | Capacidade marcada como "Real" para algo ainda não implementado. |
| **Corpus de teste** | Teste de perímetro verde porque medía a divergência de um shadow desligado. Teste verdadeiro **pela causa errada**: a fixture nunca escreveu a tupla. |
| **ADR** | Justificativa "com base na evidência da Fase 1" e, na mesma seção, a admissão de que a métrica "não estava instrumentada". |
| **Instrumento de medição** | Agregado sem filtro, denominador diluído, gap medido contra o antecessor em vez do irmão. |
| **Critério de saída** | Gate verde só alcançável conformando-se ao teto que suprimia a maior parte das observações. Um gate assim não erra sozinho: **ratifica** o erro que mede. |

## 2. O decálogo (R1 a R10)

### R1 · Booleano num domínio de três estados é a assinatura da família
Toda vez que um campo precisa dizer *"sem sujeito"* ou *"desconhecido"* e só tem `true`/`false`, o `false` vira mentira: `allowed:false` para credencial inválida; `success:false` para falha de transporte.
**Remédio:** domínios ternários explícitos: `real | curated | unknown`, `permit | deny | unauthenticated`, `invalid (401) | dependência indisponível (503)`.
**Corolário (R22):** o terceiro estado é **ausência de evidência**, nunca *"evidência de valor extremo"*. Cinco amostras idênticas produzem variância zero legitimamente: há evidência, e máxima; o que falta é dispersão. Coagir o extremo para "ausência" cria um falso negativo novo com o conserto do falso positivo antigo.

### R2 · Toda medição carrega um par que precisa concordar
Foi o **par** que denunciou o engano em todos os casos observados, nunca o valor isolado: tempo zero *versus* pós-estanque; sonda com credencial válida *versus* controle com credencial inválida; `occurred_at` *versus* `recorded_at`.
> *Medida sem companheira discordável não é medida; é afirmação.*

**Corolário (R27):** par que degenera em espelho **exatamente sob a falha que deveria detectar** não é par. O instrumento declara, no próprio veredito, em que regime é par e em que regime não é.

### R3 · Evidência de existência não é evidência de alcance
Endpoint implementado ≠ rota alcançável pela rede. Emissão de token aberta ≠ credencial aceita a jusante. Serviço respondendo em `127.0.0.1` ≠ tráfego roteável entre contêineres. Artefato correto **sem via até um consumidor** não é detectável inspecionando o artefato.

### R4 · Antes de ler séries temporais, nomeie o processo gerador
Quedas de taxa e janelas de silêncio podem ser reflexo da periodicidade de um job em lote ou de rotação de shards. Nenhum p-valor é válido sem o calendário do processo gerador ao lado.

### R5 · Taxa se normaliza por oportunidades reais, não por total de operações
Se o denominador inclui milhares de operações triviais, `0/793` parece seguro quando o caminho crítico foi exercitado **duas vezes**. Normalizar por oportunidades de confronto. **Inverso (R29):** denominador de um registro de dívida é o **declarado**, nunca o **pendente**; se quitar uma dívida encolhe o registro, a métrica pune consertar. *Check:* o denominador muda quando o numerador muda? Então a métrica mede a si mesma.

### R6 · Não exercitado ≠ passou
Gate que não rodou não foi aprovado. Zero defeitos sob amostra insuficiente é **resultado inconclusivo**, nunca evidência de estabilidade.

### R7 · Fail-closed protege decisão; fail-open protege evidência
Quando o componente **decide autorização**, falhar é fechar. Quando o componente guarda **a integridade do registro de algo que já aconteceu**, fechar destrói o registro: recusar a escrita não desfaz o evento, apaga a prova. O log de auditoria adota **fail-open com buffer durável**. Esta é a metade que falta em toda matriz de modos de falha que só tabela gates.

### R8 · Asserção sobre código é sintática (AST), nunca textual
Prosa engana busca textual: `REVOKE` num comentário parece revogação ativa; uma docstring citando `is_platform_admin` parece chamada. Verificações automáticas sobre estrutura operam sobre a **árvore sintática**. **Corolário (R14):** âncora é **símbolo**; linha é conveniência. Símbolo é verificável e não decai; linha decai a cada commit e o decaimento não emite sinal.

### R9 · Corrigir uma premissa exige varrer todas as decisões que se apoiavam nela
Se uma emenda altera uma premissa topológica ("agora há dois escritores em vez de um"), o autor audita e atualiza toda decisão e spec deduzida da premissa anterior, inclusive no mesmo documento.

### R10 · Numa auditoria que não converge, ordene por taxa de degradação
Ordenar por "severidade teórica" gera paralisia. Ordenar por **o que piora enquanto espera**: um corpus que degrada a cada submissão ou um log que mente a cada execução têm prioridade sobre refatorações cosméticas. É o antídoto operacional à governança permanente.

## 3. Regras de construção derivadas

As regras seguintes nasceram em arcos posteriores e governam diretamente a [construção evolutiva](06-construcao-evolutiva.md):

| Regra | Enunciado |
|---|---|
| **R11 · Propriedade, não mecanismo** | Quem decide especifica a **propriedade** e a **condição de refutação**; a consulta é de quem executa. Prescrever *como medir* já é mecanismo. |
| **R15 · Nível de ground truth** | Toda afirmação de estado declara seu nível: **1** intenção (arquivo versionado) · **2** intenção aplicada (job registrado) · **3a** estado no processo de teste · **3b** estado no artefato de deploy (a imagem ou o pacote que vai para produção) · **4** estado e efeito (reprodução ao vivo). Defeitos de empacotamento (dependência carregada dinamicamente, arquivo lido do disco) só aparecem em 3b. Afirmação sem nível é lida como 4 e costuma ser 1. O nível 4 declara também se a reprodução **lê** ou **escreve**: escrita em ambiente com dado de negócio usa dado marcado como teste e removível, ou fica de fora (a propriedade de escrita é então provada em 3b, e o nível 4 vale só para leitura). |
| **R26 · O mecanismo da fase existe** | Antes de planejar um flip, verificar sintaticamente que o caminho `enforce` **existe no código**. Nomear a fase na ADR não a constrói. |
| **R28 · O nome do teste declara a propriedade medida** | Um teste chamado "flag vive na fonte" que crava um valor específico mede **postura**, não **visibilidade**: falha num flip legítimo e passa numa flag fantasma com o valor certo. |
| **R29b · Dívida negativa em `xfail(strict)`** | Uma asserção negativa registrada como `xfail(strict=True)` é, de graça, um **detector de fechamento**: quando o defeito é consertado, ela passa a `XPASS` e denuncia a própria quitação. Dívida registra-se sempre `strict`. |
| **R30 · Quem decide também descreve** | Toda tabela, flag ou job criado sob uma ADR entra na spec no mesmo arco. Decidir sem descrever produz documentação verdadeira sobre o decidido e falsa sobre o que existe. |

## 4. Duas formas que organizam a medição

### Capacidade negativa × provisionamento negativo
- **Não alcança com o que recebe** (provisionamento): falta grant, tupla, credencial.
- **Não alcança mesmo se tentar** (capacidade): a barreira é estrutural.

Só a segunda prova um limite de segurança. Reportar a primeira como se fosse a segunda é a família com número grande.

### Critério de saída em forma de aresta, não de nó
Critério de nó (*"nenhum fail-open em gate"*) é estruturalmente incapaz de ver superfície **sem** gate. Critério de aresta: *"nenhuma execução alcança dado de tenant, mutação de autorização ou privilégio administrativo além do seu acesso autorizado, verificado de dentro do cluster"*. O segundo pega os caminhos que o primeiro não vê.
