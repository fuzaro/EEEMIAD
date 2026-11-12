# 05. As Dez Regras do Refinamento Empírico (R1 a R10)
## A Anatomia da "Família da Resposta Plausível"

---

### 1. O Diagnóstico: A Família da Resposta Plausível

> **Definição:**  
> Uma computação que devolve um valor **bem-formado, válido e tipado** para uma pergunta que **não foi feita**, tornando-se **indistinguível da resposta correta**.

O defeito nunca é um erro de sintaxe ou uma exceção óbvia. O defeito é o valor ser **certo para outra pergunta**. Por essa razão, atravessa revisões de código humanas e passa por testes automatizados superficiais: **porque parece resposta**.

#### As 11 Ocorrências Empíricas Históricas por Camada:
1. **Camada de Código:** Portão de segurança alimentado com `subject` escolhido pelo chamador na requisição (o portão validava a permissão com sucesso, mas sobre o sujeito forjado).
2. **Camada de Código:** `check` de autorização contra relação inexistente que retornava `deny` idêntico a um `deny` legítimo.
3. **Camada de Código:** Retorno de `status=success` com contagem sintética de `tokens_used=142` mascarando falha de transporte.
4. **Camada de Dados:** `quality_score=0.8` fixo constante gravado em 6.301 registros sendo lido como medição viva real.
5. **Camada de Dados:** Atributo `prior_source="kin"` anotado sobre dados de andaime/mock, afirmando aprendizado onde havia apenas placeholder.
6. **Camada de Dados:** `anchored:false` gravado sobre segmento vazio (uma afirmação sem sujeito real).
7. **Camada de Especificação:** Declaração de `authorized ANN: Real` em documento de especificação para funcionalidade ainda não codificada.
8. **Camada de Testes:** Teste de perímetro de segurança passando 100% verde porque media a divergência de um shadow desativado.
9. **Camada de Testes:** Teste passando verde pela causa errada: a fixture de teste nunca escreveu a tupla no banco.
10. **Camada de ADR:** ADR-011 justificando o bloqueio de segurança "com base em evidências da Fase 1" e admitindo no parágrafo seguinte que a métrica "não estava instrumentada".
11. **Camada de Instrumentos:** As próprias métricas de monitoramento construídas para detectar anomalias continham denominadores diluídos que convertiam cenários não-exercitados em provas falsas de segurança.

---

### 2. O Decálogo de Regras Operacionais (R1 a R10)

#### R1 — Booleano num domínio de três estados é a assinatura da família
Toda vez que um campo precisa representar *"ausência de sujeito"* ou *"estado desconhecido"* e possui apenas `true` e `false`, o valor `false` converte-se em mentira:
- `allowed:false` para credencial inválida (confunde recusa de política com falha de infraestrutura).
- `success:false` para falha de transporte.
- **Remediação:** Exigir domínios ternários explícitos: `real | curated | unknown` ou `permit | deny | unauthenticated`.

#### R2 — Toda medição carrega um par que precisa concordar (Pares Discordáveis)
Foi o **par de valores** que denunciou o engano em todos os casos reais observados, nunca um valor isolado:
- `t0` versus `pos_estanque`.
- Probe com literal versus controle com bearer inválido.
- `occurred_at` versus `recorded_at`.
> **Regra de Ouro:** *Medida sem companheira discordável não é medida; é mera afirmação.*

#### R3 — Evidência de existência não é evidência de alcance
- Endpoint implementado no código $\ne$ rota alcançável pela rede.
- Mint de token aberto $\ne$ credencial aceita pelo serviço a jusante.
- Teste respondendo na porta local `127.0.0.1` $\ne$ tráfego roteável entre contêineres na malha.

#### R4 — Antes de ler séries temporais em produção, nomeie o processo gerador
Quedas bruscas de taxa de sucesso ou janelas de silêncio podem ser meros reflexos da periodicidade de jobs em batch ou de rotações de shards de modelo. Nenhum p-valor ou desvio padrão em ambiente de agentes é válido sem o calendário do processo gerador ao lado.

#### R5 — Taxa de corrida se normaliza por oportunidades reais, não por total de operações
Se o denominador de uma métrica inclui milhares de operações de preenchimento trivial, uma taxa de falha de `0/793` parece estatisticamente segura, quando na verdade o caminho crítico de segurança só foi exercitado **2 vezes**. Normalizar sempre por oportunidades reais de confronto.

#### R6 — Não-exercitado $\ne$ passou
Portão que não rodou não foi aprovado. Zero defeitos sob amostra insuficiente é apenas **resultado inconclusivo**, nunca evidência de estabilidade.

#### R7 — Fail-Closed protege decisão; Fail-Open protege evidência
- Quando o componente decide **autorização de acesso**, o modo de falha deve ser estritamente **Fail-Closed** (bloquear por segurança).
- Quando o componente guarda a **integridade da trilha de auditoria de algo que já aconteceu**, o modo Fail-Closed destrói a evidência (recusar a escrita do log apaga a prova do evento que ocorreu no mundo real). O log deve adotar **Fail-Open com buffer durável**.

#### R8 — Asserção sobre código é sintática (AST), nunca textual
A prosa em docstrings e comentários engana ferramentas de busca textual (*grep/regex*):
- Um comentário contendo `REVOKE admin` parece uma revogação ativa para uma busca textual.
- Uma docstring citando `is_platform_admin` parece uma chamada de método.
> **Mandato:** Verificações automáticas de código operam exclusivamente sobre a **Árvore Sintática Abstrata (AST)**.

#### R9 — Corrigir uma premissa exige varrer todas as decisões que se apoiavam nela
Se uma emenda altera uma premissa topológica (ex.: "agora existem dois bancos em vez de um"), o autor é obrigado a auditar e atualizar todas as decisões e especificações que foram deduzidas a partir da premissa anterior.

#### R10 — Numa auditoria que não converge, ordene por taxa de degradação
Quando a lista de pendências for imensa, ordenar por "severidade teórica" gera paralisia analítica. Deve-se ordenar por **o que piora enquanto espera**: bancos que acumulam dados corrompidos a cada minuto ou logs que mentem a cada execução de tarefa têm prioridade absoluta sobre refatorações cosméticas.
