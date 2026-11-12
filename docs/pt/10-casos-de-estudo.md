# 10. Estudos de Caso Reais do Ecossistema SolarSystems
## Evidências Empíricas, Incidentes Críticos e Resoluções Metodológicas

---

### 1. Caso 1: O Blecaute do RBAC Admin e a Regra da Composição (§5.4)

#### Contexto e Sintoma
Em agosto de 2026, a plataforma passou por uma virada de chave para ativar o modo estrito de autorização: `PLUTO_ACCESS_ADMISSION_MODE=enforce`.
Imediatamente após o deploy, o varredor automatizado de tarefas em lote (`solar-decision-table`, rodando a cada hora via cron) entrou em colapso silencioso. Durante **11 dias consecutivos**, todas as execuções falharam com HTTP 403, mascaradas no orquestrador Nomad como status `dead`. 
- **Custo Medido:** ~2.800 execuções perdidas; a taxa de tarefas em `sun.executions` caiu de ~252 por dia para **exatamente zero**.

#### Causa-Raiz
Três alterações de segurança (*flips*) foram realizadas na mesma janela operacional:
1. Ativação do lock de auditoria: `MOON_AUDIT_CHAIN_LOCK=true`.
2. Exigência de token em inferência: `NEPTUNE_TOKEN_REQUIRED=true`.
3. Ativação da admissão estrita no Pluto: `PLUTO_ACCESS_ADMISSION_MODE=enforce`.

Cada flip havia sido testado individualmente pelo seu respectivo autor e aprovado em seus testes unitários locais. Contudo, o cliente interno do Saturn, ao consultar quem era o administrador de uma conta para processar o lote, omitia o cabeçalho `Authorization`. 
> **A falha quebrou a pergunta, não a resposta.** Nenhum teste individual dos três serviços pegou o erro porque nenhum testou a **composição no nível do produto final**.

#### Resolução EEEMIAD
1. **Recuo Imediato para Shadow:** A flag foi revertida para modo `shadow` em 2026-08-18 (`commit a671908`).
2. **Instituição da Forma 1 do Pré-Voo (§5.4):** Adição obrigatória da cláusula de **Composição de Flips**:
   *"Quais OUTROS gates foram alterados nesta janela? O PRODUTO da composição foi exercitado ponta a ponta com comando e resultado comprovados?"*
3. **Reprovisionamento Conforme:** Eliminação do bypass administrativo estático e emissão da tupla relacional FGA correta para a máquina de operação (`pri_platform_ops`).

---

### 2. Caso 2: A Rota Órfã de Auditoria no Moon e o Modo de Falha M11

#### Contexto e Sintoma
Em 2026-08-03, durante uma varredura de rotina de telemetria, detectou-se que um dos endpoints centrais de gravação de auditoria do Moon estava retornando HTTP 422 em silêncio.
- **Custo Medido:** Perda de ~370 registros de auditoria em produção durante uma janela de 8 horas.

#### Causa-Raiz
Um erro sutil de ordenação de decorators no framework FastAPI vinculou uma função auxiliar de sanitização de payload no lugar do handler real de persistência em banco.
O serviço adotava **Fail-Closed inadvertido na camada de persistência de auditoria**: a requisição falhava, a tarefa prosseguia sem o log, e o registro do que ocorreu no mundo físico foi apagado.

#### Resolução EEEMIAD (Regra R7)
1. **Aplicação da Regra R7:**  
   *"Fail-Closed protege decisão de autorização; Fail-Open protege evidência histórica."*
2. **Buffer Append-Only Durável:** A gravação de auditoria foi desacoplada em fila transacional com *write-ahead log* e trava transacional por tenant (`advisory lock 64-bit`). Mesmo sob indisponibilidade momentânea do Postgres, a mensagem é preservada no JetStream e nunca descartada.
3. **Teste de Controle Negativo:** Inclusão de teste com payload corrompido que prova a emissão de alerta em canal secundário sem abortar a cadeia de custódia.

---

### 3. Caso 3: A Falácia do Ingress Interno e o Ataque C6 (ADR-042)

#### Contexto e Sintoma
Uma tarefa submetida à API externa no gateway Venus conseguia ignorar completamente o classificador de risco e os limites de quota do tenant se o corpo da requisição JSON contivesse a chave:
```json
{
  "caller_type": "internal",
  "priority": "system"
}
```

#### Causa-Raiz
O orquestrador Sun lia a identidade e a autoridade do remetente **a partir do corpo da mensagem HTTP**, presumindo que apenas serviços confiáveis da rede interna chamavam o endpoint `/v1/tasks`. 
Trata-se da clássica ocorrência da **Resposta Plausível (Instância #1)**: o portão de segurança funcionava perfeitamente e conferia as permissões, mas recebia como argumento um sujeito fornecido livremente pelo próprio atacante.

#### Resolução EEEMIAD
1. **Formalização da ADR-042:** Redigida pelo Agente Reflexivo com análise de alternativas e emendas graduais (v0.1.0 a v0.2.3).
2. **Derivação de Identidade por Token (Hop-by-Hop):** Fica terminantemente proibido ler papéis, tenants ou tipos de chamador do corpo da mensagem. A identidade é **obrigatoriamente derivada dos claims do JWT assinado via Vault Transit**.
3. **Validação Live:** O teste de reprovação adversarial provou a transição: a mesma requisição forjada passou de `HTTP 500 / Bypass silencioso` para `HTTP 403 blocked_by_classifier`.
