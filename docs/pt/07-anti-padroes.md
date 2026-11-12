# 07. Catálogo de Anti-Padrões Diagnosticados
## As Armadilhas Críticas da Engenharia de Software com IA (§6 e §11)

---

### 1. A Taxonomia dos Anti-Padrões
A aplicação continuada de modelos de linguagem e agentes em sistemas de grande escala revelou uma taxonomia recorrente de patologias arquiteturais. A EEEMIAD cataloga formalmente esses anti-padrões, seus sintomas e suas remediações:

---

### 2. Os Anti-Padrões Estruturais (§6)

#### §6.1 Ratify-and-Write (Ratificação Simultânea)
- **Sintoma:** Propor uma decisão arquitetural complexa no mesmo documento que a declara aprovada, eliminando o período de contraditório e análise de alternativas.
- **Remediação:** Minutas nascem sempre com `status=proposed`. A aprovação exige uma sessão reflexiva separada ou aprovação do operador humano.

#### §6.2 Release Composta com Risco Heterogêneo
- **Sintoma:** Empacotar uma refatoração estética de documentação junto com uma migração destrutiva de banco ou rotação de credenciais sob a mesma tag de versão.
- **Risco:** O revisor aprova a release motivado pela trivialidade da primeira parte e ignora o risco sistêmico da segunda.
- **Remediação:** Princípio da homogeneidade de risco: releases destrutivas ou de segurança trafegam sozinhas e isoladas.

#### §6.3 Idempotente-como-Falsa-Segurança
- **Sintoma:** Rotular um script ou playbook como "idempotente" para tranquilizar o operador, quando o script realiza operações destrutivas ou irreversíveis (como rotação de chave primária ou rekeying de cofre).
- **Remediação:** Idempotência significa apenas *convergência para o mesmo estado final*; não significa que o script seja seguro para re-executar sem efeitos colaterais. O bloco de pré-voo (§5.4) deve enumerar os side-effects do passo individual, não do wrapper.

#### §6.4 Soft Gate sem Critério de Promoção
- **Sintoma:** Introduzir um portão de segurança em modo "não-bloqueante" (*best-effort*) sem definir a data ou a métrica exata em que ele se tornará bloqueante (*enforce*).
- **Consequência:** Torna-se débito técnico perpétuo; ninguém assume a responsabilidade de virar a chave.
- **Remediação:** Toda introdução de modo shadow carrega data-limite ou volume amostral que dispara o cut-over compulsório.

#### §6.5 Spec que Prescreve o que Já Existe
- **Sintoma:** Documentos de especificação usando verbos como "propõe-se construir" para funcionalidades que já foram entregues e estão operando há meses.
- **Remediação:** Varreduras rituais da Fase 8 sincronizam o tempo verbal e o status das especificações para `Active / Living`.

#### §6.6 Hierarchy Inversion (Inversão de Hierarquia — Anti-Padrão 10.7)
- **Sintoma:** O código diverge da especificação; em vez de corrigir o código ou emitir uma ADR formal, altera-se a especificação para perdoar o atalho do código.
- **Remediação:** Regra da Reconciliação Ascendente: a especificação e as ADRs estão acima do código. O código nunca vence a divergência por já estar no ar.

#### §6.7 Config-as-State Fora da Fonte
- **Sintoma:** Parâmetros críticos de controle, flags de segurança ou regras de autorização existindo apenas em variáveis manuais de ambiente ou na memória do cluster, sem versionamento em repositório Git.
- **Custo Medido:** Perda silenciosa de configuração após reinicialização de contêineres e divergência entre staging e produção.
- **Remediação:** *"Se governa comportamento, vive na fonte versionada no Git."*

#### §6.8 Capitulação à Camada Conveniente e Coincident-State
- **Sintoma:** Ao auditar uma divergência entre o código e uma especificação, o agente aceita a primeira explicação fácil (ex.: "a docstring dizia X, logo X está certo"), sem verificar se uma ADR de nível superior havia revogado aquela cláusula.
- **Remediação:** O reality-check deve sempre validar a claim contra a **camada mais alta** que trata do assunto na hierarquia da verdade.

---

### 3. A Dialética do §11: Improvisação vs. Governança Permanente

```
               [ ZONA DA MORTE ]
      Improvisação Permanente (§11a)
      - Sem specs, sem ADRs, sem contratos
      - O LLM improvisa a cada prompt
      - Humano vira depurador perpétuo de bugs
      - Colapso por alucinação e spec-rot
                    ▲
                    │  (A Tensão Dialética)
                    ▼
      Governança Permanente (§11b)
      - Cerimônias infinitas, burocracia paralisante
      - Auditorias que nunca convertem em deploy
      - Specs tão densas que custam o mesmo que o código
      - Alavanca de abstração = 0
               [ ZONA DA MORTE ]
```

> **O Ponto de Equilíbrio EEEMIAD:**  
> A metodologia não busca burocracia por vaidade acadêmica. A especificação deve ser **suficientemente densa para eliminar a alucinação estrutural**, mas **suficientemente abstrata para preservar a alavanca dos agentes**. Toda governança deve ser executável por scripts mecânicos e queries, desonerando a atenção humana.
