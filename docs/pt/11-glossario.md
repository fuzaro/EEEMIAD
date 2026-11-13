# 📖 11 · Glossário

*Termos da EEE em definições curtas, com o capítulo onde cada um é desenvolvido*

---

| Termo | Definição | Ver |
|---|---|---|
| **Arco** | Trecho de trabalho que leva **uma propriedade** de "não existe" a "ligada e medida", sob uma flag, abrindo com charter e fechando com gate mensurável e evidência. | [06](06-construcao-evolutiva.md) |
| **Charter** | Contrato de abertura de um arco: propriedade alvo, condição de refutação, flag, postura de falha, gate de saída, janela de observação. | [06](06-construcao-evolutiva.md), [template](../../templates/pt/arc-charter-template.md) |
| **Condição de refutação** | Observação concreta que, se ocorrer, prova que o arco **não** entregou a propriedade. Sem ela não há arco, há intenção. | [06](06-construcao-evolutiva.md), [09](09-fundamentacao-academica.md) |
| **Fatia fina (vertical)** | Implementação mínima que atravessa todas as camadas uma vez (entrada → processamento → saída), com stubs permitidos e marcados. | [04](04-fases-do-ciclo.md) |
| **Elo mínimo** | Sinônimo de fatia fina na Fase 3: o menor acoplamento ponta a ponta que prova o cano. | [04](04-fases-do-ciclo.md) |
| **Stub / Mock / Fake / Dry-run** | Dublês de teste e andaimes. Provam contrato de forma e fluxo; **não** provam valor. "O mock valida o cano, não a medida." | [06](06-construcao-evolutiva.md) |
| **Desmock** | Substituição de um stub pela implementação real, um colaborador por vez, sem mudar o contrato de forma. | [06](06-construcao-evolutiva.md) |
| **Formas verdadeiras** | Propriedade de um mock cujo retorno é reproduzível pela implementação real; critério de saída da Fase 2. | [04](04-fases-do-ciclo.md) |
| **Flag** | Âncora operacional de um arco; contrato com default neutro no código, valor explícito no deploy, domínio `off \| shadow \| enforce`, postura M11 e registro no ledger. | [06](06-construcao-evolutiva.md) |
| **Shadow** | Estado em que o componente computa a decisão e registra a divergência contra o comportamento vigente, **sem decidir**. | [04](04-fases-do-ciclo.md) |
| **Enforce** | Estado em que o componente decide; postura de falha M11 ativa. | [04](04-fases-do-ciclo.md) |
| **Cut-over** | Virada de `shadow` para `enforce`, sob pré-voo obrigatório. | [04](04-fases-do-ciclo.md) |
| **Pré-voo (raio de explosão)** | Bloco obrigatório antes de qualquer ação que toque produção: efeitos colaterais, reversibilidade, rollback ensaiado, precondição de estado, composição de flips. | [04](04-fases-do-ciclo.md), [08](08-guia-de-aplicacao.md) |
| **Composição de flips** | Pergunta do pré-voo: quais outros gates mudaram nesta janela e o **produto** deles foi exercitado. | [07](07-anti-padroes.md), [10](10-casos-ilustrativos.md) |
| **Flag fantasma** | Flag declarada na configuração com zero consumidores no código. | [06](06-construcao-evolutiva.md), [07](07-anti-padroes.md) |
| **Ledger de enforcement** | Registro vivo de cada flag: default, valor no deploy, estado, garantia, postura de falha, ADR. Muda no mesmo commit do flip. | [06](06-construcao-evolutiva.md), [template](../../templates/pt/flag-ledger-template.md) |
| **Config-as-state** | Anti-padrão: comportamento governado por estado que vive só no runtime, fora da fonte versionada. | [07](07-anti-padroes.md) |
| **M11 (matriz de modos de falha)** | Tabela que declara, por interface e condição de erro, a postura de degradação (fail-closed, fail-open com buffer durável) e a resposta esperada. | [05 R7](05-regras-do-refinamento.md), [template](../../templates/pt/failure-modes-m11-template.md) |
| **Fail-closed / Fail-open durável** | Posturas de falha: a primeira protege **decisão**; a segunda protege **evidência** de algo que já aconteceu. | [05 R7](05-regras-do-refinamento.md) |
| **Tri-estado** | Domínio de resposta que distingue `inválido` (401), `negado` (403) e `não consegui verificar` (503). Booleano aqui é a assinatura da família. | [05 R1](05-regras-do-refinamento.md) |
| **Família da resposta plausível** | Valor bem-formado e tipado para uma pergunta que não foi feita, indistinguível da resposta correta. | [05](05-regras-do-refinamento.md) |
| **Par discordável** | Segunda medida que pode **discordar** da primeira. "Medida sem companheira discordável não é medida; é afirmação." | [05 R2](05-regras-do-refinamento.md) |
| **Controle negativo** | Teste que deve **falhar** (ou barrar) para provar que a asserção positiva mede algo. Inclui o vizinho que deve seguir barrado. | [06](06-construcao-evolutiva.md) |
| **Probe-and-revert** | Injetar o defeito exato que o teste existe para pegar, confirmar o vermelho, reverter; só então aceitar o verde. | [06](06-construcao-evolutiva.md) |
| **Proof test** | Exercício deliberado, em cadência declarada, de um mecanismo de contingência cuja única manifestação orgânica é a falha que ele trata. | [04 Fase 8](04-fases-do-ciclo.md) |
| **Nível de ground truth (R15)** | 1 intenção · 2 intenção aplicada · 3 estado · 4 estado e efeito. Toda afirmação de estado declara o seu. | [05](05-regras-do-refinamento.md) |
| **Reality-check (RC)** | Medição do terreno contra o que um documento assume: âncoras verificadas por símbolo, precondições na fonte, drift reportado antes de qualquer edição. | [08](08-guia-de-aplicacao.md), [template](../../templates/pt/reality-check-template.md) |
| **Reconciliação ascendente** | Resolução de drift subindo para a camada superior (ADR de emenda), nunca ajustando a spec ao código. | [03](03-hierarquia-da-verdade.md) |
| **Inversão de hierarquia** | Anti-padrão: a spec é alterada para perdoar o atalho do código. | [03](03-hierarquia-da-verdade.md), [07](07-anti-padroes.md) |
| **Fechamento por reavaliação** | Uma tarefa fecha quando a verificação que detectou o déficit é reexecutada e retorna zero; nunca por auto-relato. | [02](02-principios.md) |
| **DONE@tier** | Degrau declarado de conclusão: `estrutural`, `funcional`, `gate`, `propósito`. "Done" pelado é proibido. | [02](02-principios.md) |
| **Modo de garantia** | Determinístico, limiar + confiança, ou forma/juízo. Limita o tier alcançável. | [02](02-principios.md) |
| **Fidelidade × alavanca** | Tensão central: spec mais densa → materialização mais fiel → menos alavanca. O alvo é o ponto em que o resíduo de improvisação é barato de verificar. | [01](01-visao-geral.md) |
| **Sprint-exit sweep (Fase 8)** | Varredura mecânica de saída de ciclo: AST por fantasmas, paridade rotas ↔ specs, custódia de ADRs, envelhecimento de `PROPOSED`, proof tests. | [04](04-fases-do-ciclo.md), [08](08-guia-de-aplicacao.md) |
| **Sino de bambu** | Metáfora do propósito: infraestrutura que desaparece quando funciona e devolve atenção ao humano. | [00](00-manifesto.md) |
