# 📚 09 · Fundamentação Acadêmica e Epistemológica

*Em que literatura a EEE se apoia, e o que ela acrescenta*

---

## 1. O problema epistemológico

Pela primeira vez na engenharia de software, o "compilador" que materializa especificação em código executável não é um autômato determinístico, mas um **estimador probabilístico autorregressivo**. Isso não é uma limitação a contornar com prompts melhores; é uma propriedade do substrato que o método precisa absorver.

Duas consequências organizam a EEE:

1. **A verificação não pode ser interna ao gerador.** Um sistema que produz spec, código e teste a partir do mesmo estado tende à **autoconsistência errônea**: erros coerentes entre si passam na própria verificação. A literatura sobre autocorreção de LLMs confirma que modelos não corrigem com confiabilidade o próprio raciocínio sem sinal externo (Huang et al., 2024; Kadavath et al., 2022, sobre calibração limitada da autoavaliação).
2. **"Pronto" é uma afirmação empírica, não lógica.** Como Dijkstra observou, *testes mostram a presença de defeitos, nunca a ausência* (Dijkstra, 1970). Logo, todo DONE é derrogável.

### A medida que motivou o método

Em um laço experimental interno (112 capacidades, 28 sessões, tenant isolado, protocolo pré-registrado), a taxa de capacidades "verificadas por execução" quando o mesmo modelo escreveu spec, implementação e teste ficou em **0,51** (IC 95% 0,41–0,62). Fixar os **tipos** de valor na spec moveu a taxa para **0,62** (IC 95% 0,53–0,71), com o mecanismo confirmado pela queda da classe de erro alvo (3,7×).

O ponto metodológico não é o número: é que **0,62 é um limite superior da correção real**, porque capacidades consistentemente erradas (spec, código e teste concordando num valor errado) passam na verificação e ficam dentro do "verificado". Só autoria independente ou cega enxerga esse teto. Daí a separação de papéis ([01 §5](01-visao-geral.md#5-os-três-papéis)) e o verificador que não lê a implementação.

## 2. Verdade pragmática e derrogabilidade

**Peirce (1878)** define verdade como *a opinião destinada a ser acordada por todos os que investigam*: um limite da investigação, não um decreto. A EEE adota essa leitura operacional: a verdade de um sistema é a spec declarada, e "verificado" significa fidelidade a essa fonte, não correção absoluta.

**Popper (1959)** fornece a assimetria: uma hipótese não é confirmada por casos favoráveis; é refutada por um contraexemplo. Por isso todo charter de arco exige **condição de refutação** e todo DONE significa "nenhum contraexemplo encontrado pela bateria B até t".

A exigência do **par discordável** (R2) tem raiz no desenho experimental: uma observação sem controle não distingue a hipótese de suas alternativas (Fisher, 1935; a formalização de hipóteses concorrentes em Neyman e Pearson, 1933). O **controle negativo** é a transposição direta dessa prática para suítes de teste.

## 3. Verificação versus validação

A distinção que a EEE fixa na pilha de DONE é clássica: Boehm (1979; 1981) separa **verificação** (*"are we building the product right?"*) de **validação** (*"are we building the right product?"*). A EEE acrescenta uma consequência arquitetural: a máquina pode certificar o primeiro e é **estruturalmente incapaz** do segundo, porque a spec é verdadeira por decreto e não julga a si mesma.

Parnas e Clements (1986) lembram que o processo racional de projeto é uma ficção útil que a documentação deve **simular**: a hierarquia `Plan → ADR → Spec → Code` é essa simulação disciplinada, com a regra adicional de que a documentação só pode ser reescrita **para cima**.

## 4. Contratos e modos de falha

- **Triplas de Hoare (1969)** e a disciplina de Dijkstra (1976) fundamentam a exigência de pré e pós-condições em cada interface. A EEE traduz a tripla `{P} C {Q}` em: precondição de estado verificada na fonte, execução sob flag, pós-condição atestada por verificador independente.
- **Design by Contract (Meyer, 1992)** é o antecedente direto do *registro explícito de contratos* (princípio 10): invariantes, pré e pós-condições publicadas, não implícitas.
- **Fail-safe defaults (Saltzer e Schroeder, 1975)** sustentam a postura fail-closed em decisões de acesso. A contribuição da EEE (R7) é a **metade complementar**: quando o componente guarda evidência de algo que já aconteceu, fechar destrói a prova; o modo correto é fail-open com buffer durável.
- **Acidentes normais (Perrow, 1984)** e a engenharia de resiliência (Hollnagel, Woods e Leveson, 2006) explicam por que a **composição** de mudanças individualmente corretas produz falhas que nenhum teste unitário vê. É a origem do item "composição de flips" no pré-voo.

## 5. Construção evolutiva, andaimes e flags

- **Evo (Gilb, 1988)** e o **modelo espiral (Boehm, 1988)** formalizam a entrega em incrementos pequenos com medição a cada ciclo; a EEE herda a cadência e adiciona o critério de parada empírico (gate em oportunidades reais).
- **Mocks e stubs:** Fowler (2007) distingue *stubs* (respostas fixas) de *mocks* (verificação de interação); Meszaros (2007) sistematiza *test doubles* e os riscos de testes acoplados à implementação. A regra da EEE, *"o mock valida o cano, não a medida"*, é uma consequência operacional: dublês provam contrato de forma, não valor.
- **Feature toggles e dark launching:** Humble e Farley (2010) e Hodgson (2017) descrevem toggles de release e de operação, com o alerta de que toggles acumulam dívida se não forem aposentados. A EEE formaliza o ciclo `off → shadow → enforce → aposentada`, o ledger e o **tri-estado** como requisitos, e nomeia a patologia da **flag fantasma**.
- **Estabilidade e padrões de falha:** Nygard (2018) fundamenta *fail fast*, *circuit breaker* e a recusa de fallbacks silenciosos, de onde decorre a proibição de stub como fallback de produção.
- **Abstração só na repetição:** a regra "≥ 2 ocorrências" segue a prática *rule of three* da refatoração (Fowler, 1999) e o alerta de Brooks (1987) contra a complexidade acidental introduzida por generalizações prematuras.
- **Registros de decisão:** o formato de ADR deriva de Nygard (2011); a EEE acrescenta o ciclo `PROPOSED → ACCEPTED` com ratificação separada e a custódia medível do registro.

## 6. Engenharia de software empírica

A palavra *empírica* no nome não é retórica. Basili, Caldiera e Rombach (1994) propõem que a melhoria de processo se dê por **medição orientada a metas** (GQM) e por uma *fábrica de experiência* que transforma observações em regras reutilizáveis. É exatamente o mecanismo pelo qual o catálogo de anti-padrões e as regras R1–R30 cresceram: cada regra nasce de instâncias medidas, nunca de analogia. A *evidence-based software engineering* (Kitchenham, Dybå e Jørgensen, 2004) oferece o critério de admissão: proposições entram no método quando há evidência, e saem quando ela falta.

As patologias de medição que a EEE cataloga (denominador diluído, métrica que mede a si mesma, gate que ratifica o erro) são instâncias do que Goodhart (1975) e Strathern (1997) descrevem: quando uma medida vira alvo, deixa de ser boa medida.

## 7. Grafos de propriedade e verificação topológica

O fechamento estrutural por consulta a um grafo de propriedade (Angles et al., 2017; Robinson, Webber e Eifrem, 2015) oferece uma verificação **extensional**, decidível e barata: nós para `Principle`, `Invariant`, `ADR`, `Specification`, `Endpoint`, arestas para `GOVERNS`, `MATERIALIZES_INTO`, `VALIDATED_BY`. A consulta que detecta um déficit (por exemplo, "endpoint sem spec") é a mesma que o fecha quando retorna zero: é o fundamento do **fechamento por reavaliação**. O grafo é cego ao corpo das funções; por isso o degrau funcional existe, e por isso a tensão fidelidade × alavanca não desaparece.

## 8. Calibração estatística dos gates

Quando uma garantia opera no modo *limiar + confiança*, a EEE recusa médias ingênuas. O **limite inferior do intervalo de Wilson (1927)** evita o problema do *cold start* (um sucesso em uma tentativa não supera 980 em 1.000):

```math
W = \frac{\hat{p} + \frac{z^2}{2n} - z\sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}
```

em que `p̂` é a proporção observada, `n` o número de **oportunidades reais** (R5) e `z = 1,96` para 95%. A regra de que a janela de shadow conta oportunidades, e não dias de calendário, é a leitura operacional dessa fórmula.

## 9. Referências

- Angles, R., Arenas, M., Barceló, P., Hogan, A., Reutter, J., Vrgoč, D. (2017). *Foundations of Modern Query Languages for Graph Databases.* ACM Computing Surveys, 50(5).
- Basili, V. R., Caldiera, G., Rombach, H. D. (1994). *The Goal Question Metric Approach* e *The Experience Factory.* In: Encyclopedia of Software Engineering. Wiley.
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
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2.ª ed.). Pragmatic Bookshelf.
- Parnas, D. L., Clements, P. C. (1986). *A Rational Design Process: How and Why to Fake It.* IEEE Transactions on Software Engineering, SE-12(2).
- Peirce, C. S. (1878). *How to Make Our Ideas Clear.* Popular Science Monthly, 12.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies.* Basic Books.
- Popper, K. R. (1959). *The Logic of Scientific Discovery.* Hutchinson.
- Robinson, I., Webber, J., Eifrem, E. (2015). *Graph Databases* (2.ª ed.). O'Reilly.
- Saltzer, J. H., Schroeder, M. D. (1975). *The Protection of Information in Computer Systems.* Proceedings of the IEEE, 63(9).
- Strathern, M. (1997). *'Improving Ratings': Audit in the British University System.* European Review, 5(3).
- Wilson, E. B. (1927). *Probable Inference, the Law of Succession, and Statistical Inference.* Journal of the American Statistical Association, 22(158).

> [!NOTE]
> As medições citadas na §1 e os documentos canônicos de onde as regras foram destiladas (*A verdade, o materializador e o DONE*, 2026; *Refinamento EEE: a família da resposta plausível*, 2026) pertencem ao ecossistema de origem da metodologia e serão publicados conforme a prática de pesquisa que os produziu.
