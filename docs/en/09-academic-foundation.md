# 09. Academic and Epistemological Foundations
## Theoretical Underpinnings of Evolutionary Empirical Engineering

---

### 1. Epistemology of Software Engineering under Stochastic Compilers

Software engineering with Large Language Models (LLMs) represents a fundamental paradigm shift. For the first time, the compiler materializing executable code is not a deterministic finite-state automaton, but a **high-dimensional autoregressive estimator**:

$$P(W_t \mid W_{<t}) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}} V\right)$$

This stochastic nature introduces **compliant hallucination** and **erroneous self-consistency** (Wang et al., 2022; Fuzaro, 2026). When the same stochastic agent authors the specification, writes the code, and generates the tests, the joint probability of undetected failure does not converge to zero; it hits an empirically measured ceiling:

$$p_0 \approx 0.616$$

To break through this ceiling, EEEMIAD grounds itself in five classical formal disciplines:

---

### 2. Property Graph Theory and Extensional Modeling
*(Angles et al., 2017; Robinson et al., 2015)*

The methodology leverages Frege’s classical distinction between **intension (*Sinn*)** and **extension (*Bedeutung*)**:
- **Language Models operate in the intensional domain:** Fluid contextual understanding and semantic inference, yet prone to discourse illusion.
- **Property Graphs operate in the extensional domain:** Explicit sets of vertices ($V$), typed edges ($E$), and property maps ($\lambda: V \cup E \to \mathcal{P}(\text{Key} \times \text{Value})$).

$$\mathcal{G} = (V, E, \Sigma_V, \Sigma_E, \lambda)$$

In EEEMIAD:
- Decidability of structural compliance queries is polynomial: $\mathcal{O}(|V| + |E|)$.
- By modeling engineering artifacts as a property graph, the methodology enforces **Rules-as-Constraints**: no probabilistic inference can bypass an `:ENFORCES_INVARIANT` edge.

---

### 3. Peircean Pragmatism and Popperian Defeasibility
*(Peirce, 1878; Popper, 1959)*

Operational truth in EEEMIAD reflects Charles Sanders Peirce’s pragmatic theory of truth:
> *"The opinion which is fated to be ultimately agreed to by all who investigate, is what we mean by the truth."*

From this, two corolários emerge:

#### Defeasibility of DONE
Reflecting Karl Popper’s falsificationism, a passing test suite never proves that code is correct in the absolute; it merely proves that **no defect was discovered by battery $B$ up to time $t$**:

$$\text{DONE} \equiv \neg \exists d \in \mathcal{D}_{\text{known}} : \text{Violates}(d, \mathcal{S})$$

All DONE claims are strictly **defeasible**.

#### Rule R2 and Disagreeable Pairs
The mandate that every measurement must carry a counter-balancing companion is rooted in the Neyman-Pearson hypothesis testing framework: an isolated measurement with no negative control provides zero statistical power against confirmation bias.

---

### 4. Statistical Decision Theory and Bayesian Calibration
*(Wilson, 1927; Sutton & Barto, 2018; Agrawal & Goyal, 2012)*

In the 4R judgment plane, naive arithmetic averages are discarded in favor of Bayesian inference with conjugate Beta priors:

$$\text{Posterior} \sim \text{Beta}(\alpha_0 + \text{successes}, \;\beta_0 + \text{failures})$$

To resolve cold-start bias, evaluations calculate the **Wilson Score Lower Bound** at 95% confidence:

$$W = \frac{\hat{p} + \frac{z^2}{2n} - z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

Where $\hat{p}$ is the sample ratio, $n$ is the count of genuine opportunities (Rule R5), and $z = 1.96$. Newly instantiated agents receive conservative scores until empirical evidence accumulates.

---

### 5. Formal Verification and Axiomatic Semantics
*(Hoare, 1969; Dijkstra, 1976)*

Service contracts in EEEMIAD (§7 Explicit Contract Registry) map to **Hoare Triples**:

$$\{P\} \; C \; \{Q\}$$

Where $P$ is the state precondition verified at source, $C$ is sandboxed execution, and $Q$ is the postcondition certified by independent verifiers. This converts stochastic generation into a bounded, verifiable compilation process.
