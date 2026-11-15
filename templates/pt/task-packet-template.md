# 📦 PACOTE DE TAREFA · [ID]

*Unidade de despacho da divisão por nível de contexto: uma tarefa fechada, com entradas, saída e gate declarados*

> [!NOTE]
> Usado **apenas** quando o operador aceitou a divisão por nível de contexto na fase de perguntas ([08 §6](../../docs/pt/08-guia-de-aplicacao.md#6-divisão-de-tarefas-por-nível-de-contexto-opcional)). Quem escreve o pacote é o nível de sistema; quem executa e quem confere não o alteram.

```yaml
packet_id: [ARC-XXX-T01]
arc: ARC-[XXX]
level: local          # local | modulo | sistema (regra de classificação em 08 §6)
written_by: [papel/agente do nível de sistema]
executor: [papel/agente que executa]
checker: [papel/agente que confere; nunca o mesmo autor do executor]
executes_at: here       # here | <sessão remota>: onde estão o terreno e a credencial (08 §7)
action: read-only       # read-only | write (escrita exige autorização do operador na sessão que age)
escalate_after: 2     # falhas no gate antes de subir um nível
```

---

## 1. Objetivo (uma frase, verificável)

> *"[O que passa a existir ou mudar, em termos observáveis.]"*

## 2. Entradas permitidas

| Arquivo | Trecho | Por quê |
|---|---|---|
| `specs/[componente].md` | §[n] | contrato |
| `[caminho]` | `[símbolo ou linhas]` | ponto de alteração |

Nada fora desta lista é lido pelo executor. Se a tarefa exigir outra leitura, ela não é deste nível: devolva com o motivo.

## 3. Leituras proibidas

- Para quem confere: a implementação e o raciocínio do executor. Recebe só este pacote, a saída e o gate.
- [outras, ex.: dados reais, segredos]

## 4. Contrato de saída

| Saída | Forma | Onde |
|---|---|---|
| [arquivo/trecho/relatório] | [formato exato] | [caminho] |

## 5. Gate (o veredito é deste comando, não de leitura)

```bash
[comando que decide]
```

Resultado esperado: `[saída ou código de saída]`.

> [!IMPORTANT]
> **Tarefa sem gate mecânico não pode ser nível local.** Sem comando que decida, quem confere precisaria reler o trabalho, e isso recria a autoria única.

## 6. Condição de refutação

> *"[Observação que, se ocorrer, mostra que a tarefa não foi cumprida mesmo com o gate verde.]"*

## 7. Registro (preenchido por quem confere)

| Campo | Valor |
|---|---|
| Gate na primeira tentativa | passou / falhou |
| Tentativas | [n] |
| Escalonado para | — / [nível] |
| Veredito | APROVADO · DEVOLVIDO ([motivo]) · ESCALONADO |
| Custo (se a ferramenta informar) | [tokens / tempo] |
