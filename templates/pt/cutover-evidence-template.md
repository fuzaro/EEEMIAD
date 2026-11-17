# 🚦 EVIDÊNCIA DE CUT-OVER · [Arco] · [off → enforce]

*Registro de uma virada de flag: o pré-voo respondido, o artefato exercitado e a reprodução ao vivo, cada linha com comando e resultado*

```yaml
arc_id: ARC-[XXX]
flag: [NOME_DA_FLAG]
transition: [off → shadow | shadow → enforce | enforce → shadow]
environment: [nome do ambiente]
artifact: [imagem@tag ou pacote@versão]
code_commit: [sha curto do código no artefato]
flip_commit: [sha do commit que muda manifesto + ledger]
decided_by: [papel que decide]
date: YYYY-MM-DD
```

---

> [!IMPORTANT]
> Uma linha sem comando e saída observada é inferência e não conta. Nível de prova (R15) declarado em cada seção.

## 1. Pré-voo respondido (ch. 04, Fase 7)

| # | Pergunta | Comando | Saída observada |
|---|---|---|---|
| 1 | Efeitos colaterais além do alvo | | |
| 2 | Reversível? (se NÃO → parar) | | |
| 3 | Rollback ensaiado, com tempo medido | | |
| 4 | Precondição de estado na fonte (tabelas, grants, variáveis, registry acessível pelos nós) | | |
| 5 | Composição: outros gates mudados nesta janela e produto exercitado | | |
| 6 | Mecanismo `enforce` existe (verificação sintática) | | |
| 7 | Estado do destino coberto pelos testes? (vazio, recém-migrado, dados antigos fora da regra nova, volume) Se não, bateria rodada a partir desse estado | | |

## 2. Artefato de deploy exercitado (nível 3b)

O artefato **que vai para produção**, não o processo de teste.

| Verificação | Comando | Resultado |
|---|---|---|
| Boot sem erro e com as flags esperadas | | |
| Health publica flags = ledger | | |
| Caminho feliz da propriedade | | |
| Vizinho que deve seguir barrado (R2) | | |

## 3. Reprodução ao vivo (nível 4)

Modo: **leitura** | **escrita** (escrita em ambiente com dado de negócio só com dado marcado como teste e removível; senão, a escrita fica provada em 3b e este nível vale só para leitura).

| Caso | Requisição | Esperado | Observado |
|---|---|---|---|
| **Propriedade** | | | |
| **Refutação** (o caso que, se passasse, refutaria o arco) | | barrado | |

## 4. Flip e ledger

- Commit único que muda manifesto e ledger: `[sha]`
- Valor explícito no manifesto: `[FLAG]="[valor]"` em `[arquivo:linha]`
- Health depois do flip: `[saída]`

## 5. Janela de observação

- Início: `YYYY-MM-DD HH:MM` · tamanho declarado: `[N oportunidades reais]`
- Consulta de critério de saída: `[comando]` → `[total, divergentes]`

## 6. Decisão

`done@[tier]`, nível de prova `[3b | 4]`, decidido por `[papel]` em `YYYY-MM-DD`. Aposentadoria da flag: depois da janela, com prova de zero consumidores.
