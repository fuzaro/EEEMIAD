# 📚 09 · Academic and Epistemological Foundations

*Which literature EEE rests on, and what it adds*

---

## 1. The epistemological problem

For the first time in software engineering, the "compiler" that materializes specification into executable code is not a deterministic automaton but an **autoregressive probabilistic estimator**. This is not a limitation to work around with better prompts; it is a property of the substrate that the method must absorb.

Two consequences organize EEE:

1. **Verification cannot be internal to the generator.** A system that produces spec, code and test from the same state tends to **erroneous self-consistency**: mutually coherent errors pass their own verification. The literature on LLM self-correction confirms that models do not reliably correct their own reasoning without an external signal (Huang et al., 2024; Kadavath et al., 2022, on the limited calibration of self-assessment).
2. **"Done" is an empirical claim, not a logical one.** As Dijkstra observed, *testing shows the presence of defects, never their absence* (Dijkstra, 1970). Hence every DONE is defeasible.

### The measurement that motivated the method

In an internal experimental loop (112 capabilities, 28 sessions, isolated tenant, pre-registered protocol), the rate of capabilities "verified by execution" when the same model wrote spec, implementation and test was **0.51** (95% CI 0.41–0.62). Pinning value **types** in the spec moved the rate to **0.62** (95% CI 0.53–0.71), with the mechanism confirmed by the drop of the target error class (3.7×).

The methodological point is not the number: it is that **0.62 is an upper bound of real correctness**, because consistently wrong capabilities (spec, code and test agreeing on a wrong value) pass verification and stay inside "verified". Only independent or blind authorship sees that ceiling. Hence the role separation ([01 §5](01-overview.md#5-the-three-roles)) and the verifier that does not read the implementation.

## 2. Pragmatic truth and defeasibility

**Peirce (1878)** defines truth as *the opinion fated to be agreed upon by all who investigate*: a limit of inquiry, not a decree. EEE adopts that operational reading: a system's truth is its declared spec, and "verified" means fidelity to that source, not absolute correctness.

**Popper (1959)** supplies the asymmetry: a hypothesis is not confirmed by favourable cases; it is refuted by a counter-example. Hence every arc charter requires a **refutation condition** and every DONE means "no counter-example found by battery B up to t".

The requirement of the **disagreeable pair** (R2) is rooted in experimental design: an observation without a control does not distinguish the hypothesis from its alternatives (Fisher, 1935; the formalization of competing hypotheses in Neyman and Pearson, 1933). The **negative control** is the direct transposition of that practice to test suites.

## 3. Verification versus validation

The distinction EEE fixes in the DONE stack is classical: Boehm (1979; 1981) separates **verification** (*"are we building the product right?"*) from **validation** (*"are we building the right product?"*). EEE adds an architectural consequence: the machine can certify the first and is **structurally incapable** of the second, because the spec is true by decree and does not judge itself.

Parnas and Clements (1986) remind us that the rational design process is a useful fiction that documentation must **fake**: the hierarchy `Plan → ADR → Spec → Code` is that disciplined fake, with the additional rule that documentation may only be rewritten **upwards**.

## 4. Contracts and failure modes

- **Hoare triples (1969)** and Dijkstra's discipline (1976) ground the requirement of pre- and post-conditions on every interface. EEE translates the triple `{P} C {Q}` into: state precondition verified at the source, execution under a flag, post-condition attested by an independent verifier.
- **Design by Contract (Meyer, 1992)** is the direct antecedent of the *explicit contract register* (principle 10): invariants, pre- and post-conditions published, not implicit.
- **Fail-safe defaults (Saltzer and Schroeder, 1975)** support the fail-closed posture on access decisions. EEE's contribution (R7) is the **complementary half**: when the component guards evidence of something that already happened, closing destroys the proof; the correct mode is fail-open with a durable buffer.
- **Normal accidents (Perrow, 1984)** and resilience engineering (Hollnagel, Woods and Leveson, 2006) explain why the **composition** of individually correct changes produces failures that no unit test sees. It is the origin of the "flip composition" item in the pre-flight.

## 5. Evolutionary construction, scaffolds and flags

- **Evo (Gilb, 1988)** and the **spiral model (Boehm, 1988)** formalize delivery in small increments with measurement every cycle; EEE inherits the cadence and adds the empirical stopping criterion (a gate in real opportunities).
- **Mocks and stubs:** Fowler (2007) distinguishes *stubs* (fixed responses) from *mocks* (interaction verification); Meszaros (2007) systematizes *test doubles* and the risks of tests coupled to the implementation. EEE's rule, *"the mock validates the pipe, not the measurement"*, is an operational consequence: doubles prove shape contracts, not values.
- **Feature toggles and dark launching:** Humble and Farley (2010) and Hodgson (2017) describe release and ops toggles, with the warning that toggles accumulate debt if not retired. EEE formalizes the cycle `off → shadow → enforce → retired`, the ledger and the **tri-state** as requirements, and names the pathology of the **ghost flag**.
- **Stability and failure patterns:** Nygard (2018) grounds *fail fast*, *circuit breaker* and the refusal of silent fallbacks, from which follows the prohibition of a stub as a production fallback.
- **Abstraction only on repetition:** the "≥ 2 occurrences" rule follows the *rule of three* of refactoring (Fowler, 1999) and Brooks's (1987) warning against accidental complexity introduced by premature generalization.
- **Decision records:** the ADR format derives from Nygard (2011); EEE adds the `PROPOSED → ACCEPTED` cycle with separate ratification and the measurable custody of the record.

## 6. Empirical software engineering

The word *empirical* in the name is not rhetoric. Basili, Caldiera and Rombach (1994) propose that process improvement proceed by **goal-oriented measurement** (GQM) and an *experience factory* that turns observations into reusable rules. That is exactly the mechanism by which the anti-pattern catalogue and rules R1–R30 grew: each rule is born from measured instances, never from analogy. *Evidence-based software engineering* (Kitchenham, Dybå and Jørgensen, 2004) offers the admission criterion: propositions enter the method when there is evidence, and leave when it is missing.

The measurement pathologies EEE catalogues (diluted denominator, metric that measures itself, gate that ratifies the error) are instances of what Goodhart (1975) and Strathern (1997) describe: when a measure becomes a target, it ceases to be a good measure.

## 7. Property graphs and topological verification

Structural closure by querying a property graph (Angles et al., 2017; Robinson, Webber and Eifrem, 2015) offers an **extensional**, decidable and cheap verification: nodes for `Principle`, `Invariant`, `ADR`, `Specification`, `Endpoint`, edges for `GOVERNS`, `MATERIALIZES_INTO`, `VALIDATED_BY`. The query that detects a deficit (for example, "endpoint without spec") is the same one that closes it when it returns zero: it is the foundation of **closure by re-evaluation**. The graph is blind to function bodies; that is why the functional tier exists, and why the fidelity × leverage tension does not go away.

## 8. Statistical calibration of gates

When a guarantee operates in *threshold + confidence* mode, EEE refuses naive averages. The **Wilson (1927) lower bound** avoids the *cold start* problem (one success in one attempt does not beat 980 in 1,000):

```math
W = \frac{\hat{p} + \frac{z^2}{2n} - z\sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}
```

where `p̂` is the observed proportion, `n` the number of **real opportunities** (R5) and `z = 1.96` for 95%. The rule that the shadow window counts opportunities, not calendar days, is the operational reading of that formula.

## 9. References

- Angles, R., Arenas, M., Barceló, P., Hogan, A., Reutter, J., Vrgoč, D. (2017). *Foundations of Modern Query Languages for Graph Databases.* ACM Computing Surveys, 50(5).
- Basili, V. R., Caldiera, G., Rombach, H. D. (1994). *The Goal Question Metric Approach* and *The Experience Factory.* In: Encyclopedia of Software Engineering. Wiley.
- Boehm, B. W. (1979). *Guidelines for Verifying and Validating Software Requirements and Design Specifications.* Euro IFIP 79.
- Boehm, B. W. (1981). *Software Engineering Economics.* Prentice Hall.
- Boehm, B. W. (1988). *A Spiral Model of Software Development and Enhancement.* IEEE Computer, 21(5).
- Brooks, F. P. (1987). *No Silver Bullet: Essence and Accidents of Software Engineering.* IEEE Computer, 20(4).
- Dijkstra, E. W. (1970). *Notes on Structured Programming.* EWD249.
- Dijkstra, E. W. (1976). *A Discipline of Programming.* Prentice Hall.
- Fisher, R. A. (1935). *The Design of Experiments.* Oliver and Boyd.
- Fowler, M. (1999). *Refactoring: Improving the Design of Existing Code.* Addison-Wesley.
- Fowler, M. (2007). *Mocks Aren't Stubs.* martinfowler.com.
- Gilb, T. (1988). *Principles of Software Engineering Management.* Addison-Wesley.
- Goodhart, C. (1975). *Problems of Monetary Management: The U.K. Experience.* Papers in Monetary Economics, Reserve Bank of Australia.
- Hoare, C. A. R. (1969). *An Axiomatic Basis for Computer Programming.* Communications of the ACM, 12(10).
- Hodgson, P. (2017). *Feature Toggles (aka Feature Flags).* martinfowler.com.
- Hollnagel, E., Woods, D. D., Leveson, N. (eds.) (2006). *Resilience Engineering: Concepts and Precepts.* Ashgate.
- Huang, J. et al. (2024). *Large Language Models Cannot Self-Correct Reasoning Yet.* ICLR 2024.
- Humble, J., Farley, D. (2010). *Continuous Delivery.* Addison-Wesley.
- Kadavath, S. et al. (2022). *Language Models (Mostly) Know What They Know.* arXiv:2207.05221.
- Kitchenham, B. A., Dybå, T., Jørgensen, M. (2004). *Evidence-Based Software Engineering.* ICSE 2004.
- Meszaros, G. (2007). *xUnit Test Patterns: Refactoring Test Code.* Addison-Wesley.
- Meyer, B. (1992). *Applying "Design by Contract".* IEEE Computer, 25(10).
- Neyman, J., Pearson, E. S. (1933). *On the Problem of the Most Efficient Tests of Statistical Hypotheses.* Philosophical Transactions of the Royal Society A, 231.
- Nygard, M. T. (2011). *Documenting Architecture Decisions.* cognitect.com.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.
- Parnas, D. L., Clements, P. C. (1986). *A Rational Design Process: How and Why to Fake It.* IEEE Transactions on Software Engineering, SE-12(2).
- Peirce, C. S. (1878). *How to Make Our Ideas Clear.* Popular Science Monthly, 12.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies.* Basic Books.
- Popper, K. R. (1959). *The Logic of Scientific Discovery.* Hutchinson.
- Robinson, I., Webber, J., Eifrem, E. (2015). *Graph Databases* (2nd ed.). O'Reilly.
- Saltzer, J. H., Schroeder, M. D. (1975). *The Protection of Information in Computer Systems.* Proceedings of the IEEE, 63(9).
- Strathern, M. (1997). *'Improving Ratings': Audit in the British University System.* European Review, 5(3).
- Wilson, E. B. (1927). *Probable Inference, the Law of Succession, and Statistical Inference.* Journal of the American Statistical Association, 22(158).

> [!NOTE]
> The measurements cited in §1 and the canonical documents from which the rules were distilled (*Truth, the Materializer and DONE*, 2026; *EEE Refinement: the plausible answer family*, 2026) belong to the methodology's ecosystem of origin and will be published according to the research practice that produced them.
