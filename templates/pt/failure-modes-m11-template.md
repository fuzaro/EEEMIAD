# 🧯 MATRIZ M11 · Modos de Falha e Postura de Degradação

*Anexo obrigatório de toda spec contratual: o que acontece quando a dependência cai*

```yaml
component: [nome]
spec_reference: specs/[componente].md
governing_adr: ADR-[XXX]
```

---

## 1. Doutrina

1. **Decisões de segurança são fail-closed.** Sob qualquer dúvida de autenticação, autorização ou parsing de permissão, a máquina nega, e loga alto.
2. **Evidência de algo que já aconteceu é fail-open com buffer durável.** Falha no pipeline de auditoria jamais descarta o registro; retém até o downstream voltar (R7).
3. **Tri-estado na resposta.** `inválido` (401), `negado` (403) e `não consegui verificar` (503) são estados distintos; colapsá-los é a assinatura da família (R1).
4. **Cada linha tem um teste de injeção de falha.** Linha sem teste é intenção, não postura.
5. **Entrega com evidência obrigatória é um terceiro caso.** Quando a operação entrega um artefato cuja emissão precisa ficar registrada (certificado, etiqueta, relatório oficial), a evidência precede a entrega: falha ao registrar → nada é entregue (fail-closed na evidência); falha ao produzir depois de registrar → erro, e o registro é mantido e anotado, porque a tentativa aconteceu.

## 2. Matriz por interface

| Operação | Condição de erro | Classe | Postura | Resposta / ação | Log e telemetria | Teste |
|---|---|---|---|:---:|---|---|
| `POST /v1/items` | credencial ausente | dura | **Fail-closed** | `401` | evento de segurança com origem | `test_items_missing_bearer_401` |
| `POST /v1/items` | serviço de autorização indisponível | transiente | **Fail-closed** | `503` | retry com backoff; nunca aceita sem verificar | `test_items_authz_down_503` |
| `POST /v1/items` | timeout da política (> limite declarado na spec) | transiente | **Fail-closed** | `403` | nega por mundo fechado | `test_items_policy_timeout_denies` |
| `POST /v1/audit` | armazenamento indisponível | transiente | **Fail-open com buffer durável** | `202` | evento na fila persistente; alerta | `test_audit_store_down_buffers` |
| `GET /v1/items/{id}` | identidade derivada falha | dura | **Fail-closed** | `401` | nunca cai em identidade padrão | `test_items_identity_resolution_fails_closed` |
| `POST /v1/items/{id}/certificate` | registro de emissão indisponível | transiente | **Fail-closed na evidência** | `503`, nada entregue | erro com causa | `test_certificate_not_issued_when_record_fails` |
| `POST /v1/items/{id}/certificate` | geração falha após o registro | dura | **Erro, registro mantido** | `500` | registro anotado `render_failed` | `test_certificate_render_failure_keeps_record` |

## 3. Sumidouros de evidência (a metade que costuma faltar)

| Sumidouro | Falha | Postura | Buffer | Prova de que nada se perdeu |
|---|---|---|---|---|
| log de auditoria | banco indisponível | FO-durável | fila persistente | contagem emitida = gravada + bufferizada (par discordável) |
| intent-log de shadow | disco cheio | FO-durável | rotação com alerta | idem |
