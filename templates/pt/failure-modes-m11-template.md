# Matriz M11: Modos de Falha e Postura de Degradação
## Anexo Obrigatório para Especificações Contratuais (§7 e §11)

```yaml
service_name: [Nome do Serviço / Componente]
spec_reference: specs/[servico].md
governing_adr: ADR-[XXX]
```

---

## 1. Matriz de Modos de Falha por Interface / Endpoint

| Operação / Rota | Condição de Erro | Modo de Falha | Postura de Degradação | Código HTTP / Ação | Log & Telemetria |
|---|---|---|---|:---:|---|
| `POST /v1/tasks` | Token ausente | Falha-Dura | **Fail-Closed** | `401 Unauthorized` | Log de segurança imediato com IP de origem |
| `POST /v1/tasks` | Vault Transit indisponível | Falha-Transiente | **Fail-Closed** | `503 Service Unavailable` | Retry com backoff exponencial; não aceita sem assinar |
| `POST /v1/audit` | Banco Moon inacessível | Falha-Transiente | **Fail-Open com Buffer Durável** | `202 Accepted` | Encaminha mensagem para fila JetStream em disco (R7) |
| `POST /v1/access/check` | Timeout OpenFGA (>100ms) | Falha-Transiente | **Fail-Closed** | `403 Forbidden (Timeout)` | Nega por segurança de mundo fechado (ADR-040) |

---

## 2. Invariantes da Doutrina M11
1. **Decisões de Segurança são SEMPRE Fail-Closed:** Sob qualquer dúvida de autorização, autenticação ou parsing de permissões, a máquina nega o acesso.
2. **Preservação de Evidência Histórica é Fail-Open com Buffer Durável:** Falhas no pipeline de auditoria jamais descartam logs de eventos ocorridos; retêm os registros em buffer durável até a recuperação do downstream.
