# 📝 PEDIDO DE ORIGEM · [Projeto]

*O que foi pedido, nas palavras de quem pediu (EEEMIAD ch. 08 §1 passo 2). O Plan é uma leitura deste arquivo e pode errar; a [matriz pedido × arco](matriz-pedido-arco.md) é o que permite ver o erro.*

```yaml
solicitante: [nome ou papel de quem pede]
decide: [quem aprova o Plan, ratifica ADRs e fecha done@gate]
registrado_em: AAAA-MM-DD
```

> [!IMPORTANT]
> **Não resuma e não corrija.** Cole o texto como foi escrito (mensagem, e-mail, ata). Se o pedido foi verbal, escreva o que foi dito e marque *(verbal, AAAA-MM-DD)*. Não registre senha, dado pessoal nem dado de produção: escreva *(omitido)*.

## 1. O pedido

> [Cole aqui o pedido, literalmente.]

## 2. Fase de perguntas

Responda antes do primeiro ADR. Pergunta sem resposta fica com **"em aberto"**, nunca com um palpite. Um agente pode fazer estas perguntas por você e anotar as respostas aqui.

| # | Pergunta | Resposta (palavras de quem decide) | Data |
|---|---|---|---|
| Q1 | Quem vai usar o sistema e para fazer o quê? | em aberto | |
| Q2 | O que o sistema **não pode** fazer de jeito nenhum (perder dado, aceitar registro incompleto, expor dado pessoal…)? | em aberto | |
| Q3 | Que tecnologia (linguagem, framework, banco) deve ou não deve ser usada? | em aberto | |
| Q4 | Onde vai rodar (máquina local, servidor, nuvem, container, orquestrador)? | em aberto | |
| Q5 | Precisa de login? Agora ou numa versão futura? Com que provedor? | em aberto | |
| Q6 | Existem dados reais? São privados? Podem ser usados só como forma para gerar dados de teste? | em aberto | |
| Q7 | Com que outros sistemas precisa conversar? | em aberto | |
| Q8 | O que fica **fora** desta versão? | em aberto | |
| Q9 | Que insumos existem (layout de banco, telas, protótipo, template de UX, sistema antigo) e onde estão? | em aberto | |
| Q10 | Existe meta de desempenho, volume ou prazo? | em aberto | |
| Q11 | Adotar divisão de tarefas por nível de contexto (ch. 08 §6)? Sem resposta = não. | em aberto | |

## 3. Pedidos posteriores

Todo pedido novo durante o projeto entra aqui com data, nas palavras de quem pediu, e ganha uma linha na matriz.

| Data | Pedido (literal) |
|---|---|
| | |
