# AGENTS.md · [Projeto]

<!--
Template de ponto de entrada (EEEMIAD ch. 08 §8.2). Salve como AGENTS.md na raiz do projeto.
Os arquivos próprios de cada ferramenta (ex.: CLAUDE.md, .cursor/rules/, .github/copilot-instructions.md,
skills e definições de agente) são adaptadores: só apontam para este arquivo e para a pasta canônica.
O gate do projeto verifica que este arquivo só cita caminhos que existem.
-->

Instruções para pessoas e para agentes de código de qualquer ferramenta. Este arquivo é o **ponto de entrada canônico**; os arquivos de cada ferramenta só apontam para cá e para `eee/`.

## O que é este repositório

[Uma frase sobre o sistema e a stack.]

## Ordem de leitura antes de agir

1. `eee/state/STATE.md`: o estado operacional (datado). Confira com o ambiente antes de agir.
2. `eee/state/decisions-operator.md`: decisões fixas do operador. Não as rediscuta.
3. O charter do arco (`specs/charters/`), o item do pedido que ele atende (`request_item`, na matriz pedido × arco), a spec que ele cita e a ADR que governa a spec. Trabalho sem item na matriz começa por registrar o pedido.
4. O procedimento do seu papel em `eee/playbooks/`.

## Hierarquia da verdade

| Camada | Onde | Regra |
|---|---|---|
| 1 · Plan | `Plan/docs/` | propósito, invariantes, orçamentos; o pedido de origem e a matriz pedido × arco |
| 2 · ADR | `Plan/decisions/` | nasce `PROPOSED`; ratificada por quem decide, em commit separado |
| 3 · Spec | `specs/` | contrato 1:1 com o código; charters em `specs/charters/` |
| 4 · Código | [`src/`, `tests/`] | segue a spec; divergência se resolve na camada de cima |

## Regras duras

1. [Dados privados: o que nunca entra no repositório.]
2. **Segredo não entra no repositório nem em mensagem.** O estado registra onde está cada credencial, nunca o valor.
3. **Escrita em ambiente compartilhado exige duas chaves:** a decisão do operador e a autorização dele na sessão que age.
4. **Teste vermelho antes do verde**, com par discordável e probe-and-revert registrados.
5. **Flag e ledger no mesmo commit.**
6. **Diário no mesmo commit:** toda mudança de estado relevante ganha uma linha em `eee/log.md`.
7. **Nível de prova declarado** (R15) em toda afirmação de estado.
8. **Humanos fecham `done@gate`.**

## Comandos

```bash
tools/gate.sh            # gate único: todos os verificadores; dependência ausente reprova
[como subir dependências de teste]
[como rodar a aplicação localmente]
```

## Mapa de `eee/`

| Caminho | Conteúdo |
|---|---|
| `eee/state/` | estado operacional, decisões do operador, ambientes |
| `eee/playbooks/` | procedimentos por papel, sem nome de ferramenta ou modelo |
| `eee/kit/` | templates do EEEMIAD copiados, com origem e versão em `eee/kit/VERSION` |
| `eee/log.md` | diário de evidências, permanente |
