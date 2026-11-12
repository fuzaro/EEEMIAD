# 09. Fundamentação Acadêmica e Epistemológica
## A Base Teórica da Engenharia Empírica Evolutiva

---

### 1. Epistemologia da Engenharia de Software com Modelos Estocásticos

O desenvolvimento de software assistido por Modelos de Linguagem de Grande Porte (LLMs) representa uma ruptura paradigmática na ciência da computação. Pela primeira vez na história da engenharia de software, o compilador ou transdutor semântico que gera o código-fonte executável não é um autômato determinístico finito, mas um **estimador probabilístico autorregressivo de alta dimensionalidade**:

$$P(W_t \mid W_{<t}) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}} V\right)$$

Essa natureza estocástica introduz o que a literatura recente identifica como **alucinação conforme (*compliant hallucination*)** ou **auto-consistência errônea** (Wang et al., 2022; Fuzaro, 2026). Quando o mesmo agente estocástico é encarregado de especificar o problema, codificar a solução e validar o resultado, a probabilidade conjunta de falha não-detectada não colapsa a zero; ela atinge um teto assintótico medido empiricamente:

$$p_0 \approx 0.616$$

Para superar essa barreira, a EEEMIAD ancora-se em cinco disciplinas acadêmicas formais:

---

### 2. Teoria dos Grafos de Propriedade e Modelagem Extensional
*(Angles et al., 2017; Robinson et al., 2015)*

A metodologia adota a distinção filosófica clássica de Frege entre **sentido (*Sinn*)** e **referência (*Bedeutung*)**, ou verdade intencional versus extensional:
- **Modelos de Linguagem operam no domínio intencional:** Compreensão contextual fluida, sinônimos, metáforas e inferência tácita. Contudo, são propensos a deriva e ilusão de coerência discursiva.
- **Grafos de Propriedade operam no domínio extensional:** Conjuntos explícitos de vértices ($V$), arestas direcionadas e tipadas ($E$), e funções de valoração de propriedades ($\lambda: V \cup E \to \mathcal{P}(\text{Key} \times \text{Value})$).

$$\mathcal{G} = (V, E, \Sigma_V, \Sigma_E, \lambda)$$

No modelo EEEMIAD:
- A decidibilidade de uma consulta topológica sobre a conformidade de um subsistema é estritamente polinomial: $\mathcal{O}(|V| + |E|)$.
- Ao converter a especificação em um grafo de propriedades (onde nós são `:Principle`, `:Invariant`, `:Specification`, `:Endpoint`, `:ADR`), o sistema estabelece **barreiras de restrição invioláveis (*Rules-as-Constraints*)**. Nenhuma inferência probabilística do LLM pode violar uma aresta `:ENFORCES_INVARIANT` declarada no grafo.

---

### 3. O Pragmatismo Semiótico de Peirce e a Defeasibilidade de Popper
*(Peirce, 1878; Popper, 1959)*

A definição de verdade operacional adotada pela EEEMIAD apoia-se diretamente na teoria pragmática da verdade formulada por Charles Sanders Peirce:
> *"A opinião sobre a qual existe um acordo fatal e irrevogável entre todos os que investigam é o que significamos pela verdade."*

Na EEEMIAD, a verdade não é uma declaração retórica imutável; é o **limite convergente da investigação empírica**. Daí decorrem dois corolários epistemológicos:

#### A Defeasibilidade do DONE
Inspirada no princípio de falseabilidade de Karl Popper, a metodologia postula que um teste nunca "prova" que o software está correto no absoluto; um teste prova apenas que **nenhum contra-exemplo foi encontrado pela bateria $B$ até o instante $t$**:

$$\text{DONE} \equiv \neg \exists d \in \mathcal{D}_{\text{conhecidos}} : \text{Violates}(d, \mathcal{S})$$

Todo status de conclusão é, por definição, **derrogável (*defeasible*)**: permanece válido apenas enquanto novas evidências de runtime não o refutarem.

#### A Regra R2 e os Pares Discordáveis
A exigência de que toda medição empírica carregue um par discordável deriva do princípio da prova de hipóteses concorrentes (Neyman-Pearson): uma asserção isolada sem controle negativo possui poder estatístico nulo contra o viés de confirmação.

---

### 4. Teoria da Decisão Estatística e Calibração Bayesiana
*(Wilson, 1927; Sutton & Barto, 2018; Agrawal & Goyal, 2012)*

No plano de julgamento e avaliação de reputação de agentes e modelos (Plano 4R), a metodologia abandona médias aritméticas ingênuas e adota modelagem Bayesiana com priori Beta conjugada:

$$\text{Posterior} \sim \text{Beta}(\alpha_0 + \text{sucessos}, \;\beta_0 + \text{falhas})$$

Para prevenir o problema clássico de *cold-start* (onde um modelo com 1 sucesso em 1 tentativa teria nota 1.0, superando um modelo veterano com 980 sucessos em 1.000 tentativas), o ranking utiliza o **Limite Inferior do Intervalo de Pontuação de Wilson (Wilson Lower Bound)** a 95% de confiança:

$$W = \frac{\hat{p} + \frac{z^2}{2n} - z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

Onde $\hat{p}$ é a proporção amostral observada, $n$ é o total de oportunidades reais (Regra R5) e $z = 1.96$. Esse rigor matemático assegura que agentes recém-instanciados recebam pontuações conservadoras até acumularem volume empírico suficiente.

---

### 5. Verificação Formal e Semântica Axiomática
*(Hoare, 1969; Dijkstra, 1976)*

O contrato formal de cada componente na EEEMIAD (§7 Explicit Contract Registry) ancora-se no formalismo das **Triplas de Hoare**:

$$\{P\} \; C \; \{Q\}$$

Onde $P$ é a pré-condição de estado verificada na fonte, $C$ é a execução do agente em container estanque, e $Q$ é a pós-condição atestada por verificadores independentes. 

A EEEMIAD traduz esse formalismo acadêmico para o desenvolvimento moderno de IA ao exigir que todo *Brief* contenha sua pré-condição de estado explícita e seu raio de explosão delimitado, transformando a síntese estocástica de código em um processo matematicamente cercado.
