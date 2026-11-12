# 04. As Oito Fases Formais do Ciclo de Vida
## Da Intenção Inicial à Governança Evolutiva

---

### 1. Visão Geral das 8 Fases
O ciclo de vida da EEEMIAD divide o amadurecimento de qualquer subsistema, contrato ou funcionalidade em **oito fases progressivas**, desenhadas para prevenir a proliferação descontrolada de complexidade e código morto:

```mermaid
flowchart LR
    F1["Fase 1<br/>Exploração & Grounding"] --> F2["Fase 2<br/>Mapeamento de Contratos"]
    F2 --> F3["Fase 3<br/>Fluxo Mínimo (POC)"]
    F3 --> F4["Fase 4<br/>Refinamento Progressivo"]
    F4 --> F5["Fase 5<br/>Shadow Validation"]
    F5 --> F6["Fase 6<br/>Identificação de Padrões"]
    F6 --> F7["Fase 7<br/>Cut-over Controlado"]
    F7 --> F8["Fase 8<br/>Governança & Sweeps"]
    F8 -.->|"Feedback Longitudinal"| F1
```

---

### 2. Detalhamento Operacional de Cada Fase

#### Fase 1: Exploração e Grounding Inicial
- **Objetivo:** Investigar a viabilidade técnica e confrontar a intenção humana contra o terreno real.
- **Atividades:** Sondagens de rede, inspeção de bibliotecas externas, análise de compatibilidade de APIs.
- **Regra de Isolamento:** Proibido commitar código na árvore de produção. Todo o trabalho ocorre em arquivos temporários de rascunho (`scratch/`) ou branches de spike.

#### Fase 2: Mapeamento de Contratos e Fronteiras
- **Objetivo:** Estabelecer as interfaces explícitas antes de qualquer implementação de negócio.
- **Atividades:** Definição de Schemas Pydantic / OpenAPI, DDLs de tabelas relacionais com índices e constraints, e redação preliminar da ADR governante (`status=proposed`).
- **Critério de Saída:** Schemas aprovados e validados contra os Princípios Fundamentais.

#### Fase 3: Fluxo Mínimo Funcional (POC / Fatia Fina)
- **Objetivo:** Provar o acoplamento ponta a ponta com o mínimo de código indispensável.
- **Atividades:** Implementação da "fatia fina vertical" (*thin vertical slice*), conectando entrada, processamento e saída.
- **Disciplina:** Permitido adotar pragmatismos locais temporários (ex.: stubs mockados em memória), desde que categorizados explicitamente como tais no código.

#### Fase 4: Refinamento Progressivo (Hardening)
- **Objetivo:** Eliminar atalhos provisórios da Fase 3 e endurecer a segurança e a resiliência.
- **Atividades:** Substituição de stubs por implementações completas, inclusão de middlewares de autenticação, injeção de segredos via Vault, tratamento estrito de exceções e tabelamento formal dos modos de falha (Tabela M11).

#### Fase 5: Shadow Validation (Observação Não-Bloqueante)
- **Objetivo:** Medir o comportamento da nova funcionalidade sob carga real de produção sem interferir nas decisões do sistema.
- **Atividades:** O componente opera em modo `shadow=true`. Ele consome os payloads reais, calcula decisões, pontuações ou políticas e grava o resultado em log auditável (*intent-log*), enquanto a decisão em vigor continua sendo a do legado.
- **Janela Mínima:** Pelo menos 14 a 21 dias de coleta contínua ou no mínimo 5.000 amostras medidas com concordância comprovada.

#### Fase 6: Identificação de Padrões e Abstração Justificada
- **Objetivo:** Consolidar aprendizados e abstrair componentes comuns sob a égide do Princípio 4.
- **Regra:** Somente após observar o mesmo comportamento ou a mesma divergência em 2 ou mais fatias distintas, autoriza-se a extração de uma biblioteca compartilhada, modelo de autorização genérico ou tabela transversal.

#### Fase 7: Cut-over Controlado (Transição para Enforce)
- **Objetivo:** Virar a chave operacional de `shadow` para `enforce`.
- **Rito Mandatório:**
  1. Pré-voo de Raio de Explosão preenchido.
  2. Precondição de estado verificada na fonte (chaves, grants e tabelas existem antes do deploy).
  3. Composição de gates testada: provar que a combinação de flags não quebra o produto final.
  4. Procedimento de rollback ensaiado e cronometrado antes da virada da flag.

#### Fase 8: Governança Evolutiva e Sprint-Exit Sweeps
- **Objetivo:** Preservar a entropia zero e impedir a regeneração do *spec-rot*.
- **Rito do Sprint-Exit Sweep:**
  - Varredura exaustiva via AST contra código morto ou flags fantasma.
  - Confrontação bidirecional 1:1 entre rotas expostas em código e rotas descritas nas especificações.
  - Avaliação de conformidade das ADRs: decisões em `proposed` há mais de 30 dias são canceladas ou promovidas.
  - Re-execução da bateria canônica de fechamento por re-avaliação.
