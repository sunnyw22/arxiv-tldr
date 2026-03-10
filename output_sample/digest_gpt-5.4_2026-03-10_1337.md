# Research Radar Digest
*Generated: 2026-03-10 13:37 UTC*

> Papers from 2026-03-08 to latest

## Search Summary

| Parameter | Value |
|-----------|-------|
| Paper date range | 2026-03-09 |
| Total papers fetched | 250 |
| Papers shown | 14 |
| arXiv categories | hep-ex, hep-ph, stat.ML, cs.LG, cs.AI |
| INSPIRE keywords | tracking, tagging, particle reconstruction, machine learning |
| INSPIRE subjects | Experiment-HEP |

## User Profile

| Field | Values |
|-------|--------|
| Topic interests | machine learning, deep learning, particle physics, particle reconstruction, track reconstruction, vertex reconstruction, tagging, triggers, CERN, ATLAS, CMS |
| Negative filters | survey only, workshop abstract |
| Project context | Implementing machine learning techniques for particle tracking and reconstruction in particle physics collider experiments related to CERN or future colliders. |
| Expertise level | advanced |

## Keyword Expansion

**Original interests:** [machine learning, deep learning, particle physics, particle reconstruction, track reconstruction, vertex reconstruction, tagging, triggers, CERN, ATLAS, CMS]
**Expanded to:** [machine learning, deep learning, particle physics, particle reconstruction, track reconstruction, vertex reconstruction, tagging, triggers, CERN, ATLAS, CMS, HL-LHC, FCC, silicon tracking, charged particle tracking, track finding, track fitting, vertexing, primary vertex, secondary vertex, b tagging, pileup mitigation, graph neural network, GNN, Kalman filter]

## Pipeline Stats

- **Sources:** 250 from arXiv, 0 from INSPIRE
- **After dedup:** 250 unique papers
- **Keyword filter:** 29 passed, 209 rejected
- **LLM scored:** 13 papers
- **Final digest:** 14 papers

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses your active project or core methods. Must-read. |
| 7-8 | Same subfield with relevant methods or insights. Likely useful. |
| 4-6 | Adjacent field or tangentially related technique. Might be interesting. |
| 1-3 | Different field or minimal overlap with your work. |

---

## 1. Characterization and upgrade of a quantum graph neural network for charged particle tracking

**Relevance: 9/10** | Published: 2026-03-09 | Source: arXiv | Categories: quant-ph, cs.LG, hep-ex

**Authors:** Matteo Argenton, Laura Cappelli, Concezio Bozzi

<details>
<summary>Abstract</summary>

In the forthcoming years the LHC experiments are going to be upgraded to benefit from the substantial increase of the LHC instantaneous luminosity, which will lead to larger, denser events, and, consequently, greater complexity in reconstructing charged particle tracks, motivating frontier research in new technologies. Quantum machine learning models are being investigated as potential new approaches to high energy physics (HEP) tasks. We characterize and upgrade a quantum graph neural network (QGNN) architecture for charged particle track reconstruction on a simulated high luminosity dataset. The model operates on a set of event graphs, each built from the hits generated in tracking detector layers by particles produced in proton collisions, performing a classification of the possible hit connections between adjacent layers. In this approach the QGNN is designed as a hybrid architecture, interleaving classical feedforward networks with parametrized quantum circuits. We characterize the interplay between the classical and quantum components. We report on the principal upgrades to the original design, and present new evidence of improved training behavior, specifically in terms of convergence toward the final trained configuration.

</details>

**From the paper:** This paper studies charged particle track reconstruction in the high-luminosity LHC setting, where denser events make hit-to-hit association more difficult. It uses a hybrid quantum graph neural network that interleaves classical feedforward networks with parameterized quantum circuits to classify candidate hit connections between adjacent detector layers. The authors characterize the interaction between the classical and quantum components, describe upgrades to the original architecture, and report improved training behavior, especially better convergence to the final trained configuration.

**Gpt-5.4 - Assessment:** This connects directly to the researcher's interests in machine learning, deep learning, graph methods, and particle track reconstruction for CERN collider experiments. The task formulation—edge classification on detector hit graphs—is highly aligned with current tracking pipelines in ATLAS/CMS-style environments, so the paper is relevant both as a tracking-method reference and as a benchmark for whether quantum-enhanced architectures offer anything beyond classical GNNs in this domain.

[Read paper](https://arxiv.org/abs/2603.08667v1)
 | [PDF](https://arxiv.org/pdf/2603.08667v1)

---

## 2. End-to-end optimisation of HEP triggers

**Relevance: 8/10** | Published: 2026-03-09 | Source: arXiv | Categories: hep-ex

**Authors:** Noah Clarke Hall, Ioannis Xiotidis, Nikos Konstantinidis, David W. Miller

<details>
<summary>Abstract</summary>

High-energy physics experiments face extreme data rates, requiring real-time trigger systems to reduce event throughput while preserving sensitivity to rare processes. Trigger systems are typically constructed as modular chains of sequentially optimised algorithms, including machine learning models. Each algorithm is optimised for a specific local objective with no guarantee of overall optimality. We instead formulate trigger design as a constrained end-to-end optimisation problem, treating all stages- including data encoding, denoising, clustering, and calibration- as components of a single differentiable system trained against a unified physics objective. The framework jointly optimises performance while incorporating physics and deployment constraints. We demonstrate this approach on a hardware multi-jet trigger inspired by the ATLAS High-Luminosity Large Hadron Collider design. Using Higgs boson pair production as a benchmark, we observe x2-4 improvement in true-positive rate at fixed false-positive rate, while preserving interpretable intermediate physics objects and monotonic calibration constraints. These results highlight end-to-end optimisation as a practical paradigm for next-generation real-time event selection systems.

</details>

**From the paper:** This paper addresses the design of high-energy physics trigger systems under extreme data-rate constraints, arguing that sequentially optimized trigger components may not be globally optimal. It formulates trigger design as a constrained end-to-end optimization problem in which stages such as encoding, denoising, clustering, and calibration are trained jointly as one differentiable system against a unified physics objective. On a hardware multi-jet trigger inspired by the ATLAS HL-LHC design and using Higgs boson pair production as a benchmark, the authors report a two- to four-fold improvement in true-positive rate at fixed false-positive rate while preserving interpretable intermediate objects and monotonic calibration constraints.

**Gpt-5.4 - Assessment:** This is directly connected to the researcher's interests in machine learning, triggers, ATLAS, and collider reconstruction workflows at CERN. Even though it is not a tracking paper, the methodological idea—joint optimization across a full physics pipeline under deployment constraints—is very relevant to reconstruction chains, where graph building, seeding, filtering, and classification are often tuned locally rather than globally.

[Read paper](https://arxiv.org/abs/2603.08428v1)
 | [PDF](https://arxiv.org/pdf/2603.08428v1)

---

## 3. Mitigating Homophily Disparity in Graph Anomaly Detection: A Scalable and Adaptive Approach

**Relevance: 6/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG

**Authors:** Yunhui Liu, Qizhuo Xie, Yinfeng Chen, Xudong Jin, Tao Zheng *et al.* (7 authors)

<details>
<summary>Abstract</summary>

Graph anomaly detection (GAD) aims to identify nodes that deviate from normal patterns in structure or features. While recent GNN-based approaches have advanced this task, they struggle with two major challenges: 1) homophily disparity, where nodes exhibit varying homophily at both class and node levels; and 2) limited scalability, as many methods rely on costly whole-graph operations. To address them, we propose SAGAD, a Scalable and Adaptive framework for GAD. SAGAD precomputes multi-hop embeddings and applies reparameterized Chebyshev filters to extract low- and high-frequency information, enabling efficient training and capturing both homophilic and heterophilic patterns. To mitigate node-level homophily disparity, we introduce an Anomaly Context-Aware Adaptive Fusion, which adaptively fuses low- and high-pass embeddings using fusion coefficients conditioned on Rayleigh Quotient-guided anomalous subgraph structures for each node. To alleviate class-level disparity, we design a Frequency Preference Guidance Loss, which encourages anomalies to preserve more high-frequency information than normal nodes. SAGAD supports mini-batch training, achieves linear time and space complexity, and drastically reduces memory usage on large-scale graphs. Theoretically, SAGAD ensures asymptotic linear separability between normal and abnormal nodes under mild conditions. Extensive experiments on 10 benchmarks confirm SAGAD's superior accuracy and scalability over state-of-the-art methods.

</details>

**From the paper:** This paper studies graph anomaly detection under varying homophily and scalability constraints. It proposes SAGAD, which uses precomputed multi-hop embeddings, reparameterized Chebyshev filters, adaptive fusion of low- and high-pass embeddings conditioned on anomalous subgraph structure, and a frequency preference guidance loss. The abstract claims linear time and space complexity, mini-batch training, theoretical asymptotic linear separability, and superior accuracy and scalability on 10 benchmark datasets.

**Gpt-5.4 - Assessment:** You work in machine learning for particle reconstruction, where graph neural networks are often used for track-building, hit association, and event-structure modeling; the paper's scalable graph filtering and adaptive fusion mechanisms may be transferable to those settings. It is not directly about collider data or reconstruction targets, but the emphasis on scalable graph processing and handling heterogeneous local structure could be useful for large detector graphs and irregular event topologies.

[Read paper](https://arxiv.org/abs/2603.08137v1)
 | [PDF](https://arxiv.org/pdf/2603.08137v1)

---

## 4. Towards Effective and Efficient Graph Alignment without Supervision

**Relevance: 6/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, cs.AI

**Authors:** Songyang Chen, Youfang Lin, Yu Liu, Shuai Zheng, Lei Zou

<details>
<summary>Abstract</summary>

Unsupervised graph alignment aims to find the node correspondence across different graphs without any anchor node pairs. Despite the recent efforts utilizing deep learning-based techniques, such as the embedding and optimal transport (OT)-based approaches, we observe their limitations in terms of model accuracy-efficiency tradeoff. By focusing on the exploitation of local and global graph information, we formalize them as the ``local representation, global alignment'' paradigm, and present a new ``global representation and alignment'' paradigm to resolve the mismatch between the two phases in the alignment process. We then propose \underline{Gl}obal representation and \underline{o}ptimal transport-\underline{b}ased \underline{Align}ment (\texttt{GlobAlign}), and its variant, \texttt{GlobAlign-E}, for better \underline{E}fficiency. Our methods are equipped with the global attention mechanism and a hierarchical cross-graph transport cost, able to capture long-range and implicit node dependencies beyond the local graph structure. Furthermore, \texttt{GlobAlign-E} successfully closes the time complexity gap between representative embedding and OT-based methods, reducing OT's cubic complexity to quadratic terms. Through extensive experiments, our methods demonstrate superior performance, with up to a 20\% accuracy improvement over the best competitor. Meanwhile, \texttt{GlobAlign-E} achieves the best efficiency, with an order of magnitude speedup against existing OT-based methods.

</details>

**From the paper:** This paper studies unsupervised graph alignment, aiming to recover node correspondences across graphs without anchor pairs. It proposes GlobAlign and a more efficient variant, GlobAlign-E, using global attention and hierarchical cross-graph optimal transport to couple representation learning and alignment, while reducing the complexity of OT-based methods from cubic to quadratic terms in the efficient variant. The abstract reports superior performance with up to 20% accuracy improvement over the best competitor and an order-of-magnitude speedup over existing OT-based methods.

**Gpt-5.4 - Assessment:** Your work likely touches graph-based ML for detector hits, tracks, or higher-level reconstruction objects, so methods for global graph representation and matching could be conceptually useful. In particular, optimal-transport-based alignment and scalable graph correspondence may inspire approaches to associating detector objects across views, bunch crossings, or reconstruction stages. It is not directly about HEP tracking, but it is close enough methodologically to merit attention if you use graph ML heavily.

[Read paper](https://arxiv.org/abs/2603.08526v1)
 | [PDF](https://arxiv.org/pdf/2603.08526v1)

---

## 5. Drift-to-Action Controllers: Budgeted Interventions with Online Risk Certificates

**Relevance: 6/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, cs.CL

**Authors:** Ismail Lamaakal, Chaymae Yahyati, Khalid El Makkaoui, Ibrahim Ouahbi, Yassine Maleh

<details>
<summary>Abstract</summary>

Deployed machine learning systems face distribution drift, yet most monitoring pipelines stop at alarms and leave the response underspecified under labeling, compute, and latency constraints. We introduce Drift2Act, a drift-to-action controller that treats monitoring as constrained decision-making with explicit safety. Drift2Act combines a sensing layer that maps unlabeled monitoring signals to a belief over drift types with an active risk certificate that queries a small set of delayed labels from a recent window to produce an anytime-valid upper bound $U_t(δ)$ on current risk. The certificate gates operation: if $U_t(δ) \le τ$, the controller selects low-cost actions (e.g., recalibration or test-time adaptation); if $U_t(δ) > τ$, it activates abstain/handoff and escalates to rollback or retraining under cooldowns. In a realistic streaming protocol with label delay and explicit intervention costs, Drift2Act achieves near-zero safety violations and fast recovery at moderate cost on WILDS Camelyon17, DomainNet, and a controlled synthetic drift stream, outperforming alarm-only monitoring, adapt-always adaptation, schedule-based retraining, selective prediction alone, and an ablation without certification. Overall, online risk certification enables reliable drift response and reframes monitoring as decision-making with safety.

</details>

**From the paper:** The paper frames model monitoring under distribution drift as constrained decision-making rather than simple alarm generation. It introduces Drift2Act, which combines unlabeled drift sensing with an active risk certificate based on a small number of delayed labels to produce an anytime-valid upper bound on current risk, and uses this certificate to choose interventions such as recalibration, adaptation, abstention, rollback, or retraining. In streaming experiments with label delay and intervention costs on Camelyon17, DomainNet, and synthetic drift, it reports near-zero safety violations and fast recovery at moderate cost, outperforming several baselines.

**Gpt-5.4 - Assessment:** For collider ML deployment, especially in triggers, tagging, or reconstruction services exposed to changing detector conditions and simulation/data mismatch, safe drift response is a real operational issue. The paper is relevant because it focuses not just on detecting drift but on deciding what action to take under constraints, with explicit risk control. That could be useful if you are thinking about robust online operation of ML-based reconstruction components or monitoring production models in experiment software.

[Read paper](https://arxiv.org/abs/2603.08578v1)
 | [PDF](https://arxiv.org/pdf/2603.08578v1)

---

## 6. Amortizing Maximum Inner Product Search with Learned Support Functions

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, stat.ML

**Authors:** Theo X. Olausson, João Monteiro, Michal Klein, Marco Cuturi

<details>
<summary>Abstract</summary>

Maximum inner product search (MIPS) is a crucial subroutine in machine learning, requiring the identification of key vectors that align best with a given query. We propose amortized MIPS: a learning-based approach that trains neural networks to directly predict MIPS solutions, amortizing the computational cost of matching queries (drawn from a fixed distribution) to a fixed set of keys. Our key insight is that the MIPS value function, the maximal inner product between a query and keys, is also known as the support function of the set of keys. Support functions are convex, 1-homogeneous and their gradient w.r.t. the query is exactly the optimal key in the database. We approximate the support function using two complementary approaches: (1) we train an input-convex neural network (SupportNet) to model the support function directly; the optimal key can be recovered via (autodiff) gradient computation, and (2) we regress directly the optimal key from the query using a vector valued network (KeyNet), bypassing gradient computation entirely at inference time. To learn a SupportNet, we combine score regression with gradient matching losses, and propose homogenization wrappers that enforce the positive 1-homogeneity of a neural network, theoretically linking function values to gradients. To train a KeyNet, we introduce a score consistency loss derived from the Euler theorem for homogeneous functions. Our experiments show that learned SupportNet or KeyNet achieve high match rates and open up new directions to compress databases with a specific query distribution in mind.

</details>

**From the paper:** This paper studies amortized maximum inner product search, where neural networks are trained to directly predict MIPS solutions for queries drawn from a fixed distribution over a fixed key set. It develops two approaches: SupportNet, which learns the support function of the key set and recovers the optimal key via gradients, and KeyNet, which directly regresses the optimal key. The abstract reports high match rates in experiments and argues that these learned models suggest new ways to compress databases tailored to a query distribution.

**Gpt-5.4 - Assessment:** The connection is methodological rather than domain-specific: particle tracking and reconstruction often involve large-scale matching, nearest-neighbor-like retrieval, or candidate scoring under tight compute budgets. If your pipeline contains repeated search over fixed candidate libraries, detector templates, or embedding memories, amortizing that search with learned predictors could be conceptually transferable, though the paper is not directly about HEP reconstruction.

[Read paper](https://arxiv.org/abs/2603.08001v1)
 | [PDF](https://arxiv.org/pdf/2603.08001v1)

---

## 7. Tau-BNO: Brain Neural Operator for Tau Transport Model

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.CE, cs.LG

**Authors:** Nuutti Barron, Heng Rao, Urmi Saha, Yu Gu, Zhenghao Liu *et al.* (9 authors)

<details>
<summary>Abstract</summary>

Mechanistic modeling provides a biophysically grounded framework for studying the spread of pathological tau protein in tauopathies like Alzheimer's disease. Existing approaches typically model tau propagation as a diffusive process on the brain's structural connectome, reproducing macroscopic patterns but neglecting microscale cellular transport and reaction mechanisms. The Network Transport Model (NTM) was introduced to fill this gap, explaining how region-level progression of tau emerges from microscale biophysical processes. However, the NTM faces a common challenge for complex models defined by large systems of partial differential equations: the inability to perform parameter inference and mechanistic discovery due to high computational burden and slow model simulations. To overcome this barrier, we propose Tau-BNO, a Brain Neural Operator surrogate framework for rapidly approximating NTM dynamics that captures both intra-regional reaction kinetics and inter-regional network transport. Tau-BNO combines a function operator that encodes kinetic parameters with a query operator that preserves initial state information, while approximating anisotropic transport through a spectral kernel that retains directionality. Empirical evaluations demonstrate high predictive accuracy ($R^2\approx$ 0.98) across diverse biophysical regimes and an 89\% performance improvement over state-of-the-art sequence models like Transformers and Mamba, which lack inherent structural priors. By reducing simulation time from hours to seconds, we show that the surrogate model is capable of producing new insights and generating new hypotheses. This framework is readily extensible to a broader class of connectome-based biophysical models, showcasing the transformative value of deep learning surrogates to accelerate analysis of large-scale, computationally intensive dynamical systems.

</details>

**From the paper:** This paper addresses the high computational cost of the Network Transport Model for tau propagation in neurodegenerative disease. It proposes Tau-BNO, a brain neural operator surrogate that encodes kinetic parameters, preserves initial state information through a query operator, and models anisotropic transport with a directional spectral kernel. The abstract reports high predictive accuracy with R^2 around 0.98, an 89% performance improvement over Transformers and Mamba, and simulation speedups from hours to seconds.

**Gpt-5.4 - Assessment:** For a researcher implementing ML in physics workflows, the paper is relevant as an example of learned surrogates for expensive mechanistic models, especially where geometry and transport structure matter. However, it does not touch particle tracking, vertexing, tagging, triggers, or collider detector reconstruction, so its value is mainly as scientific-ML inspiration rather than direct technical guidance.

[Read paper](https://arxiv.org/abs/2603.08108v1)
 | [PDF](https://arxiv.org/pdf/2603.08108v1)

---

## 8. Outlier-robust Autocovariance Least Square Estimation via Iteratively Reweighted Least Square

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: math.OC, cs.LG, eess.SP

**Authors:** Jiahong Li, Fang Deng

<details>
<summary>Abstract</summary>

The autocovariance least squares (ALS) method is a computationally efficient approach for estimating noise covariances in Kalman filters without requiring specific noise models. However, conventional ALS and its variants rely on the classic least mean squares (LMS) criterion, making them highly sensitive to measurement outliers and prone to severe performance degradation. To overcome this limitation, this paper proposes a novel outlier-robust ALS algorithm, termed ALS-IRLS, based on the iteratively reweighted least squares (IRLS) framework. Specifically, the proposed approach introduces a two-tier robustification strategy. First, an innovation-level adaptive thresholding mechanism is employed to filter out heavily contaminated data. Second, the outlier-contaminated autocovariance is formulated using an $ε$-contamination model, where the standard LMS criterion is replaced by the Huber cost function. The IRLS method is then utilized to iteratively adjust data weights based on estimation deviations, effectively mitigating the influence of residual outliers. Comparative simulations demonstrate that ALS-IRLS reduces the root-mean-square error (RMSE) of noise covariance estimates by over two orders of magnitude compared to standard ALS. Furthermore, it significantly enhances downstream state estimation accuracy, outperforming existing outlier-robust Kalman filters and achieving performance nearly equivalent to the ideal Oracle lower bound in the presence of noisy and anomalous data.

</details>

**From the paper:** This paper addresses the sensitivity of autocovariance least squares noise covariance estimation in Kalman filters to measurement outliers. It proposes ALS-IRLS, which combines adaptive innovation thresholding, an ε-contamination model with Huber loss, and iteratively reweighted least squares to robustify estimation. The abstract reports more than two orders of magnitude RMSE reduction over standard ALS and downstream state estimation performance close to an Oracle lower bound in noisy, anomalous conditions.

**Gpt-5.4 - Assessment:** Kalman filtering is foundational in many tracking pipelines, including particle track reconstruction, so robust covariance estimation under outliers could matter if you are working on filtering-based track fits or hit-assignment robustness. Still, the paper is not framed around collider detectors, combinatorial track building, vertexing, or learned reconstruction, so it is more a potentially useful adjacent methods reference than a direct match.

[Read paper](https://arxiv.org/abs/2603.08158v1)
 | [PDF](https://arxiv.org/pdf/2603.08158v1)

---

## 9. Search for long-lived charginos and $τ$-sleptons using final states with a disappearing track in $pp$ collisions at $\sqrt{s} = 13$ TeV with the ATLAS detector

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: hep-ex

**Authors:** ATLAS Collaboration

<details>
<summary>Abstract</summary>

This paper reports a search for decays of long-lived charginos or $τ$-sleptons to final states containing a short disappearing track, a single high-energy jet, and missing transverse momentum. The search uses 137 fb$^{-1}$ of data from 13 TeV proton-proton collisions recorded by the ATLAS detector during Run 2 of the LHC. Multiple search regions are defined, all requiring the presence of a track reconstructed from either three or four measurements in the innermost layers of the ATLAS detector. Regions with tracks having only three measurements are further characterised by the absence or presence of a low-energy charged pion reconstructed using a dedicated algorithm, leveraging machine learning. Data-driven methods are used to estimate the background contributions in the search regions. No significant excesses are found and 95% CL lower limits are placed on the masses of charginos and $τ$-sleptons in the lifetime range $0.01{-}10$ ns. Observed (expected) mass limits of up to 225 GeV (250 GeV) are set for pure-higgsino charginos in scenarios with lifetimes below 0.03 ns, where the electroweakino mass splitting is entirely due to loop corrections involving the Standard Model bosons, and up to 720 GeV (840 GeV) for charginos with a lifetime of around 1 ns. For wino production, charginos with masses up to 880 GeV (1020 GeV) are excluded for lifetimes of around 1 ns. For $τ$-sleptons with lifetimes of around 1 ns, masses are excluded up to 320 GeV (390 GeV) in Constrained Minimal Supersymmetric Standard Model scenarios and 300 GeV (380 GeV) in Gauge-Mediated Supersymmetry-Breaking scenarios.

</details>

**From the paper:** This paper presents an ATLAS search for long-lived charginos and tau-sleptons in Run 2 13 TeV pp collision data corresponding to 137 fb^-1. The analysis targets final states with a short disappearing track, a high-energy jet, and missing transverse momentum, and includes regions based on three- or four-hit tracks; for some three-hit cases it uses a dedicated machine-learning-assisted algorithm to reconstruct a low-energy charged pion. No significant excess is observed, and the paper sets 95% CL mass limits across several chargino and tau-slepton lifetime scenarios, with exclusions reaching up to 880 GeV for winos near 1 ns lifetime.

**Gpt-5.4 - Assessment:** It intersects with the researcher's interests in ATLAS, tracking, and reconstruction under unusual signatures, especially because disappearing tracks stress low-hit-count reconstruction and specialized algorithms. For someone developing ML methods for particle reconstruction, the main value is as an application case showing where nonstandard tracking and auxiliary ML reconstruction can matter, rather than as a methods paper to build on directly.

[Read paper](https://arxiv.org/abs/2603.08315v1)
 | [PDF](https://arxiv.org/pdf/2603.08315v1)

---

## 10. Search for decays of the Higgs boson into pair-produced pseudoscalar particles decaying into $τ^+τ^-τ^+τ^-$ using $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: hep-ex

**Authors:** ATLAS Collaboration

<details>
<summary>Abstract</summary>

A search for a pair of low-mass pseudoscalars $a$ that promptly decay into $τ$-leptons is presented using 140 fb$^{-1}$ of proton-proton collision data at $13$ TeV centre-of-mass energy recorded with the ATLAS detector at the Large Hadron Collider. The result is used to place constraints on exotic decays of the Higgs boson into four $τ$-leptons, $H\to aa\to τ^+τ^-τ^+τ^-$. This search focuses on events with either one or two $τ$-leptons decaying into hadrons and neutrinos, and the remaining three or two $τ$-leptons decaying into either electron or muon and neutrinos. No significant excess is observed above the expected Standard Model background and upper limits at the 95% confidence level on $\mathcal{B}(H\rightarrow aa\rightarrow τ^+τ^-τ^+τ^-)$ are set ranging from 0.06 to 0.23, depending on the mass $m_a$ ranging from 15 to 60 GeV.

</details>

**From the paper:** This paper presents an ATLAS search for Higgs decays of the form H→aa→τ+τ−τ+τ− using 140 fb^-1 of 13 TeV proton-proton collision data. It focuses on final states with one or two hadronic tau decays and the remaining tau decays to electrons or muons, and uses the result to constrain exotic Higgs decays into four taus over pseudoscalar masses from 15 to 60 GeV. The abstract states that no significant excess is observed and that 95% confidence level upper limits on the branching fraction are set between 0.06 and 0.23 depending on ma.

**Gpt-5.4 - Assessment:** This matters because it is directly in the ATLAS/CERN environment and involves reconstruction-heavy tau final states, which are relevant to collider analysis pipelines and may intersect with tagging and event-selection considerations. For your project, it is more useful as domain context and a potential downstream application area than as a source of new ML methods for track or vertex reconstruction.

[Read paper](https://arxiv.org/abs/2603.08323v1)
 | [PDF](https://arxiv.org/pdf/2603.08323v1)

---

## 11. Efficient Credal Prediction through Decalibration

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, stat.ML

**Authors:** Paul Hofman, Timo Löhr, Maximilian Muschalik, Yusuf Sale, Eyke Hüllermeier

<details>
<summary>Abstract</summary>

A reliable representation of uncertainty is essential for the application of modern machine learning methods in safety-critical settings. In this regard, the use of credal sets (i.e., convex sets of probability distributions) has recently been proposed as a suitable approach to representing epistemic uncertainty. However, as with other approaches to epistemic uncertainty, training credal predictors is computationally complex and usually involves (re-)training an ensemble of models. The resulting computational complexity prevents their adoption for complex models such as foundation models and multi-modal systems. To address this problem, we propose an efficient method for credal prediction that is grounded in the notion of relative likelihood and inspired by techniques for the calibration of probabilistic classifiers. For each class label, our method predicts a range of plausible probabilities in the form of an interval. To produce the lower and upper bounds of these intervals, we propose a technique that we refer to as decalibration. Extensive experiments show that our method yields credal sets with strong performance across diverse tasks, including coverage-efficiency evaluation, out-of-distribution detection, and in-context learning. Notably, we demonstrate credal prediction on models such as TabPFN and CLIP -- architectures for which the construction of credal sets was previously infeasible.

</details>

**From the paper:** The paper addresses computational barriers to constructing credal predictors, which represent epistemic uncertainty using convex sets of probability distributions. It proposes an efficient method based on relative likelihood and a calibration-inspired procedure called decalibration that outputs classwise probability intervals. The abstract states that the method performs well on coverage-efficiency evaluation, out-of-distribution detection, and in-context learning, and enables credal prediction for models such as TabPFN and CLIP.

**Gpt-5.4 - Assessment:** Reliable uncertainty estimates matter in collider ML when deciding whether to trust a classifier or reconstruction output, particularly in safety- or rate-critical systems like triggers and object tagging. This paper could be useful if you are exploring abstention, OOD detection, or uncertainty-aware decision thresholds in production ML. Its relevance is methodological rather than domain-specific, so it is a secondary read rather than a core one.

[Read paper](https://arxiv.org/abs/2603.08495v1)
 | [PDF](https://arxiv.org/pdf/2603.08495v1)

---

## 12. Don't Look Back in Anger: MAGIC Net for Streaming Continual Learning with Temporal Dependence

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, cs.AI

**Authors:** Federico Giannini, Sandro D'Andrea, Emanuele Della Valle

<details>
<summary>Abstract</summary>

Concept drift, temporal dependence, and catastrophic forgetting represent major challenges when learning from data streams. While Streaming Machine Learning and Continual Learning (CL) address these issues separately, recent efforts in Streaming Continual Learning (SCL) aim to unify them. In this work, we introduce MAGIC Net, a novel SCL approach that integrates CL-inspired architectural strategies with recurrent neural networks to tame temporal dependence. MAGIC Net continuously learns, looks back at past knowledge by applying learnable masks over frozen weights, and expands its architecture when necessary. It performs all operations online, ensuring inference availability at all times. Experiments on synthetic and real-world streams show that it improves adaptation to new concepts, limits memory usage, and mitigates forgetting.

</details>

**From the paper:** This paper studies streaming continual learning in the presence of concept drift, temporal dependence, and catastrophic forgetting. It proposes MAGIC Net, which combines recurrent neural networks with continual-learning-inspired masking over frozen weights and architecture expansion, while maintaining online inference availability. According to the abstract, experiments on synthetic and real-world streams show improved adaptation to new concepts, reduced memory usage, and mitigated forgetting.

**Gpt-5.4 - Assessment:** This connects to your machine-learning interests through online adaptation and handling nonstationarity, which can matter for detector conditions, calibration drift, and long-term deployment of trigger or reconstruction models. The masking and expansion ideas may be transferable if you are considering continuously updated inference systems in collider experiments. Still, because it is a general SCL method without any HEP structure, it is more of a technique reference than a domain-specific lead.

[Read paper](https://arxiv.org/abs/2603.08600v1)
 | [PDF](https://arxiv.org/pdf/2603.08600v1)

---

## 13. SCL-GNN: Towards Generalizable Graph Neural Networks via Spurious Correlation Learning

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG, cs.AI

**Authors:** Yuxiang Zhang, Enyan Dai

<details>
<summary>Abstract</summary>

Graph Neural Networks (GNNs) have demonstrated remarkable success across diverse tasks. However, their generalization capability is often hindered by spurious correlations between node features and labels in the graph. Our analysis reveals that GNNs tend to exploit imperceptible statistical correlations in training data, even when such correlations are unreliable for prediction. To address this challenge, we propose the Spurious Correlation Learning Graph Neural Network (SCL-GNN), a novel framework designed to enhance generalization on both Independent and Identically Distributed (IID) and Out-of-Distribution (OOD) graphs. SCL-GNN incorporates a principled spurious correlation learning mechanism, leveraging the Hilbert-Schmidt Independence Criterion (HSIC) to quantify correlations between node representations and class scores. This enables the model to identify and mitigate irrelevant but influential spurious correlations effectively. Additionally, we introduce an efficient bi-level optimization strategy to jointly optimize modules and GNN parameters, preventing overfitting. Extensive experiments on real-world and synthetic datasets demonstrate that SCL-GNN consistently outperforms state-of-the-art baselines under various distribution shifts, highlighting its robustness and generalization capabilities.

</details>

**From the paper:** This paper addresses the problem that GNNs can exploit unreliable spurious correlations between node features and labels, harming IID and out-of-distribution generalization. It proposes SCL-GNN, which uses HSIC-based spurious correlation learning and a bi-level optimization strategy to jointly optimize modules and GNN parameters. Experiments on real-world and synthetic datasets show consistent improvements over state-of-the-art baselines under various distribution shifts.

**Gpt-5.4 - Assessment:** If your tracking or reconstruction pipeline uses graph neural networks, robustness to detector- or simulation-induced spurious correlations is a concrete concern, especially for domain shifts across runs, detector conditions, or simulation-to-data transfer. The paper could therefore inform how to regularize graph models to avoid learning shortcuts tied to nonphysical features. Still, because the work is not in HEP and does not discuss detector graphs or event reconstruction, it is more a transferable ML idea than a direct match to your project.

[Read paper](https://arxiv.org/abs/2603.08270v1)
 | [PDF](https://arxiv.org/pdf/2603.08270v1)

---

## 14. Airborne Magnetic Anomaly Navigation with Neural-Network-Augmented Online Calibration

**Relevance: 5/10** | Published: 2026-03-09 | Source: arXiv | Categories: cs.LG

**Authors:** Antonia Hager, Sven Nebendahl, Alexej Klushyn, Jasper Krauser, Torleiv H. Bryne *et al.* (6 authors)

<details>
<summary>Abstract</summary>

Airborne Magnetic Anomaly Navigation (MagNav) provides a jamming-resistant and robust alternative to satellite navigation but requires the real-time compensation of the aircraft platform's large and dynamic magnetic interference. State-of-the-art solutions often rely on extensive offline calibration flights or pre-training, creating a logistical barrier to operational deployment. We present a fully adaptive MagNav architecture featuring a "cold-start" capability that identifies and compensates for the aircraft's magnetic signature entirely in-flight. The proposed method utilizes an extended Kalman filter with an augmented state vector that simultaneously estimates the aircraft's kinematic states as well as the coefficients of the physics-based Tolles-Lawson calibration model and the parameters of a Neural Network to model aircraft interferences. The Kalman filter update is mathematically equivalent to an online Natural Gradient descent, integrating superior convergence and data efficiency of state-of-the-art second-order optimization directly into the navigation filter. To enhance operational robustness, the neural network is constrained to a residual learning role, modeling only the nonlinearities uncorrected by the explainable physics-based calibration baseline. Validated on the MagNav Challenge dataset, our framework effectively bounds inertial drift using a magnetometer-only feature set. The results demonstrate navigation accuracy comparable to state-of-the-art models trained offline, without requiring prior calibration flights or dedicated maneuvers.

</details>

**From the paper:** The paper addresses airborne magnetic anomaly navigation without offline calibration flights. It proposes an extended Kalman filter with an augmented state that jointly estimates kinematics, Tolles-Lawson calibration coefficients, and neural-network parameters for residual magnetic interference modeling, with the filter update interpreted as online natural gradient descent. On the MagNav Challenge dataset, the method reportedly bounds inertial drift and reaches navigation accuracy comparable to state-of-the-art offline-trained models using only magnetometer features.

**Gpt-5.4 - Assessment:** The strongest connection is to sequential estimation under physical constraints: online calibration, hybrid physics-plus-ML modeling, and filter-based learning are all ideas that can transfer to particle detector alignment, calibration, or track-state estimation. For reconstruction projects, especially those involving learned corrections inside Kalman-style pipelines or real-time adaptation, this could spark useful design ideas even though the application domain is navigation rather than collider experiments.

[Read paper](https://arxiv.org/abs/2603.08265v1)
 | [PDF](https://arxiv.org/pdf/2603.08265v1)

---

<details>
<summary>All fetched papers (250 total)</summary>

- [Scale Space Diffusion](https://arxiv.org/abs/2603.08709v1)
- [Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting](https://arxiv.org/abs/2603.08707v1)
- [Agentic Critical Training](https://arxiv.org/abs/2603.08706v1)
- [Evaluating Financial Intelligence in Large Language Models: Benchmarking SuperInvesting AI with LLM Engines](https://arxiv.org/abs/2603.08704v1)
- [Flash from the Past: New Gamma-Ray Constraints on Light CP-even Scalar from SN1987A](https://arxiv.org/abs/2603.08695v1)
- [A Multi-Objective Optimization Approach for Sustainable AI-Driven Entrepreneurship in Resilient Economies](https://arxiv.org/abs/2603.08692v1)
- [Split Federated Learning Architectures for High-Accuracy and Low-Delay Model Training](https://arxiv.org/abs/2603.08687v1)
- [Multimessenger Characterization of High-Energy Neutrino Emission from the Brightest Neutrino-Active Galactic Nuclei](https://arxiv.org/abs/2603.08684v1)
- [Benchmarking Language Modeling for Lossless Compression of Full-Fidelity Audio](https://arxiv.org/abs/2603.08683v1)
- [Structural Causal Bottleneck Models](https://arxiv.org/abs/2603.08682v1)
- [A New Lower Bound for the Random Offerer Mechanism in Bilateral Trade using AI-Guided Evolutionary Search](https://arxiv.org/abs/2603.08679v1)
- [Momentum SVGD-EM for Accelerated Maximum Marginal Likelihood Estimation](https://arxiv.org/abs/2603.08676v1)
- [Characterization and upgrade of a quantum graph neural network for charged particle tracking](https://arxiv.org/abs/2603.08667v1) **[ranked]**
- [How Far Can Unsupervised RLVR Scale LLM Training?](https://arxiv.org/abs/2603.08660v1)
- [Context-free Self-Conditioned GAN for Trajectory Forecasting](https://arxiv.org/abs/2603.08658v1)
- [OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning](https://arxiv.org/abs/2603.08655v1)
- [CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation](https://arxiv.org/abs/2603.08652v1)
- [Group Entropies and Mirror Duality: A Class of Flexible Mirror Descent Updates for Machine Learning](https://arxiv.org/abs/2603.08651v1)
- [Divide and Predict: An Architecture for Input Space Partitioning and Enhanced Accuracy](https://arxiv.org/abs/2603.08649v1)
- [Grow, Don't Overwrite: Fine-tuning Without Forgetting](https://arxiv.org/abs/2603.08647v1)
- [Retrieval-Augmented Gaussian Avatars: Improving Expression Generalization](https://arxiv.org/abs/2603.08645v1)
- [Black Hole Mergers as the Fastest Photon Ring Scramblers](https://arxiv.org/abs/2603.08643v1)
- [PostTrainBench: Can LLM Agents Automate LLM Post-Training?](https://arxiv.org/abs/2603.08640v1)
- [UNBOX: Unveiling Black-box visual models with Natural-language](https://arxiv.org/abs/2603.08639v1)
- [Circular stable orbits in $f(R)$ realistic static and spherically-symmetric spacetimes](https://arxiv.org/abs/2603.08637v1)
- [Integral Formulas for Vector Spherical Tensor Products](https://arxiv.org/abs/2603.08630v1)
- [Cobimaximal mixing pattern from a $Δ(27)$ inverse seesaw model](https://arxiv.org/abs/2603.08625v1)
- [Improved branching-fraction measurements of $B^0_{(s)} \to K_S^0 h^+ h^{'-}$ decays and first observation of $B^0_(s) \to K_S^0 K^+ K^-$](https://arxiv.org/abs/2603.08621v1)
- [Weakly Supervised Teacher-Student Framework with Progressive Pseudo-mask Refinement for Gland Segmentation](https://arxiv.org/abs/2603.08605v1)
- [Don't Look Back in Anger: MAGIC Net for Streaming Continual Learning with Temporal Dependence](https://arxiv.org/abs/2603.08600v1) **[ranked]**
- [Radiative corrections to the nucleon isovector $g_V$ and $g_A$](https://arxiv.org/abs/2603.08596v1)
- [Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control](https://arxiv.org/abs/2603.08588v1)
- [DualFlexKAN: Dual-stage Kolmogorov-Arnold Networks with Independent Function Control](https://arxiv.org/abs/2603.08583v1)
- [Drift-to-Action Controllers: Budgeted Interventions with Online Risk Certificates](https://arxiv.org/abs/2603.08578v1) **[ranked]**
- [Trust via Reputation of Conviction](https://arxiv.org/abs/2603.08575v1)
- [MetaWorld-X: Hierarchical World Modeling via VLM-Orchestrated Experts for Humanoid Loco-Manipulation](https://arxiv.org/abs/2603.08572v1)
- [OSS-CRS: Liberating AIxCC Cyber Reasoning Systems for Real-World Open-Source Security](https://arxiv.org/abs/2603.08566v1)
- [RetroAgent: From Solving to Evolving via Retrospective Dual Intrinsic Feedback](https://arxiv.org/abs/2603.08561v1)
- [Impact of Connectivity on Laplacian Representations in Reinforcement Learning](https://arxiv.org/abs/2603.08558v1)
- [Generative Adversarial Regression (GAR): Learning Conditional Risk Scenarios](https://arxiv.org/abs/2603.08553v1)
- [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546v1)
- [The Neural Compass: Probabilistic Relative Feature Fields for Robotic Search](https://arxiv.org/abs/2603.08544v1)
- [Towards Effective and Efficient Graph Alignment without Supervision](https://arxiv.org/abs/2603.08526v1) **[ranked]**
- [Breaking the Bias Barrier in Concave Multi-Objective Reinforcement Learning](https://arxiv.org/abs/2603.08518v1)
- [Precise Predictions for Hadronic Higgs Decays](https://arxiv.org/abs/2603.08517v1)
- [Beyond Hungarian: Match-Free Supervision for End-to-End Object Detection](https://arxiv.org/abs/2603.08514v1)
- [Oracle-Guided Soft Shielding for Safe Move Prediction in Chess](https://arxiv.org/abs/2603.08506v1)
- [Echo2ECG: Enhancing ECG Representations with Cardiac Morphology from Multi-View Echos](https://arxiv.org/abs/2603.08505v1)
- [Efficient Credal Prediction through Decalibration](https://arxiv.org/abs/2603.08495v1) **[ranked]**
- [First-Order Geometry, Spectral Compression, and Structural Compatibility under Bounded Computation](https://arxiv.org/abs/2603.08494v1)
- [Pareto-Optimal Anytime Algorithms via Bayesian Racing](https://arxiv.org/abs/2603.08493v1)
- [NN-OpInf: an operator inference approach using structure-preserving composable neural networks](https://arxiv.org/abs/2603.08488v1)
- [Visual Self-Fulfilling Alignment: Shaping Safety-Oriented Personas via Threat-Related Images](https://arxiv.org/abs/2603.08486v1)
- [X-AVDT: Audio-Visual Cross-Attention for Robust Deepfake Detection](https://arxiv.org/abs/2603.08483v1)
- [STRIDE: Structured Lagrangian and Stochastic Residual Dynamics via Flow Matching](https://arxiv.org/abs/2603.08478v1)
- [R2F: Repurposing Ray Frontiers for LLM-free Object Navigation](https://arxiv.org/abs/2603.08475v1)
- [Amplitude Analysis of Singly Cabibbo-Suppressed Decay $Λ^{+}_{c}\to p K^{+} K^{-}$](https://arxiv.org/abs/2603.08469v1)
- [Integrating Lagrangian Neural Networks into the Dyna Framework for Reinforcement Learning](https://arxiv.org/abs/2603.08468v1)
- [MUSA-PINN: Multi-scale Weak-form Physics-Informed Neural Networks for Fluid Flow in Complex Geometries](https://arxiv.org/abs/2603.08465v1)
- [Reasoning as Compression: Unifying Budget Forcing via the Conditional Information Bottleneck](https://arxiv.org/abs/2603.08462v1)
- [Effects of fermions in one-loop propagators in the Curci-Ferrari-Delbourgo-Jarvis gauge](https://arxiv.org/abs/2603.08460v1)
- [Data-Driven Priors for Uncertainty-Aware Deterioration Risk Prediction with Multimodal Data](https://arxiv.org/abs/2603.08459v1)
- [Adaptive Entropy-Driven Sensor Selection in a Camera-LiDAR Particle Filter for Single-Vessel Tracking](https://arxiv.org/abs/2603.08457v1)
- [The Boiling Frog Threshold: Criticality and Blindness in World Model-Based Anomaly Detection Under Gradual Drift](https://arxiv.org/abs/2603.08455v1)
- [LycheeCluster: Efficient Long-Context Inference with Structure-Aware Chunking and Hierarchical KV Indexing](https://arxiv.org/abs/2603.08453v1)
- [A prospective clinical feasibility study of a conversational diagnostic AI in an ambulatory primary care clinic](https://arxiv.org/abs/2603.08448v1)
- [Efficient Policy Learning with Hybrid Evaluation-Based Genetic Programming for Uncertain Agile Earth Observation Satellite Scheduling](https://arxiv.org/abs/2603.08447v1)
- [The Dark Photon: a 2026 Perspective](https://arxiv.org/abs/2603.08430v1)
- [One Model Is Enough: Native Retrieval Embeddings from LLM Agent Hidden States](https://arxiv.org/abs/2603.08429v1)
- [End-to-end optimisation of HEP triggers](https://arxiv.org/abs/2603.08428v1) **[ranked]**
- [Grow, Assess, Compress: Adaptive Backbone Scaling for Memory-Efficient Class Incremental Learning](https://arxiv.org/abs/2603.08426v1)
- [IronEngine: Towards General AI Assistant](https://arxiv.org/abs/2603.08425v1)
- [SYNAPSE: Framework for Neuron Analysis and Perturbation in Sequence Encoding](https://arxiv.org/abs/2603.08424v1)
- [Human-Aware Robot Behaviour in Self-Driving Labs](https://arxiv.org/abs/2603.08420v1)
- [Meta-RL with Shared Representations Enables Fast Adaptation in Energy Systems](https://arxiv.org/abs/2603.08418v1)
- [Geometrically Constrained Outlier Synthesis](https://arxiv.org/abs/2603.08413v1)
- [Aligning to Illusions: Choice Blindness in Human and AI Feedback](https://arxiv.org/abs/2603.08412v1)
- [Connecting baryon light-front wave functions to quasi-transverse-momentum-dependent correlators in lattice QCD](https://arxiv.org/abs/2603.08405v1)
- [A Recipe for Stable Offline Multi-agent Reinforcement Learning](https://arxiv.org/abs/2603.08399v1)
- [Revealing Behavioral Plasticity in Large Language Models: A Token-Conditional Perspective](https://arxiv.org/abs/2603.08398v1)
- [Decoupling Distance and Networks: Hybrid Graph Attention-Geostatistical Methods for Spatio-temporal Risk Mapping](https://arxiv.org/abs/2603.08393v1)
- [A Hierarchical Error-Corrective Graph Framework for Autonomous Agents with LLM-Based Action Generation](https://arxiv.org/abs/2603.08388v1)
- [Beyond the Markovian Assumption: Robust Optimization via Fractional Weyl Integrals in Imbalanced Data](https://arxiv.org/abs/2603.08377v1)
- [Leaderboard Incentives: Model Rankings under Strategic Post-Training](https://arxiv.org/abs/2603.08371v1)
- [Unifying On- and Off-Policy Variance Reduction Methods](https://arxiv.org/abs/2603.08370v1)
- [M$^3$-ACE: Rectifying Visual Perception in Multimodal Math Reasoning via Multi-Agentic Context Engineering](https://arxiv.org/abs/2603.08369v1)
- [Computational modeling of early language learning from acoustic speech and audiovisual input without linguistic priors](https://arxiv.org/abs/2603.08359v1)
- [Towards plausibility in time series counterfactual explanations](https://arxiv.org/abs/2603.08349v1)
- [Rethinking Attention Output Projection: Structured Hadamard Transforms for Efficient Transformers](https://arxiv.org/abs/2603.08343v1)
- [Electrocardiogram Classification with Transformers Using Koopman and Wavelet Features](https://arxiv.org/abs/2603.08339v1)
- [Detecting Fake Reviewer Groups in Dynamic Networks: An Adaptive Graph Learning Method](https://arxiv.org/abs/2603.08332v1)
- [SPD-RAG: Sub-Agent Per Document Retrieval-Augmented Generation](https://arxiv.org/abs/2603.08329v1)
- [Beyond Attention Heatmaps: How to Get Better Explanations for Multiple Instance Learning Models in Histopathology](https://arxiv.org/abs/2603.08328v1)
- [EndoSERV: A Vision-based Endoluminal Robot Navigation System](https://arxiv.org/abs/2603.08324v1)
- [Search for decays of the Higgs boson into pair-produced pseudoscalar particles decaying into $τ^+τ^-τ^+τ^-$ using $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector](https://arxiv.org/abs/2603.08323v1) **[ranked]**
- [Agentic Neurosymbolic Collaboration for Mathematical Discovery: A Case Study in Combinatorial Design](https://arxiv.org/abs/2603.08322v1)
- [CORE-Acu: Structured Reasoning Traces and Knowledge Graph Safety Verification for Acupuncture Clinical Decision Support](https://arxiv.org/abs/2603.08321v1)
- [Human-AI Divergence in Ego-centric Action Recognition under Spatial and Spatiotemporal Manipulations](https://arxiv.org/abs/2603.08317v1)
- [Search for long-lived charginos and $τ$-sleptons using final states with a disappearing track in $pp$ collisions at $\sqrt{s} = 13$ TeV with the ATLAS detector](https://arxiv.org/abs/2603.08315v1) **[ranked]**
- [Sign Identifiability of Causal Effects in Stationary Stochastic Dynamical Systems](https://arxiv.org/abs/2603.08311v1)
- [Gravitational waves in metric-affine bumblebee gravity](https://arxiv.org/abs/2603.08310v1)
- [Concept-Guided Fine-Tuning: Steering ViTs away from Spurious Correlations to Improve Robustness](https://arxiv.org/abs/2603.08309v1)
- [Retrieval-Augmented Anatomical Guidance for Text-to-CT Generation](https://arxiv.org/abs/2603.08305v1)
- [Graph-Instructed Neural Networks for parametric problems with varying boundary conditions](https://arxiv.org/abs/2603.08304v1)
- [Nonminimal Lorentz Violation in Atomic and Molecular Spectroscopy Experiments](https://arxiv.org/abs/2603.08298v1)
- [Deconstructing Multimodal Mathematical Reasoning: Towards a Unified Perception-Alignment-Reasoning Paradigm](https://arxiv.org/abs/2603.08291v1)
- [Minor First, Major Last: A Depth-Induced Implicit Bias of Sharpness-Aware Minimization](https://arxiv.org/abs/2603.08290v1)
- [A Blockchain-based Traceability System for AI-Driven Engine Blade Inspection](https://arxiv.org/abs/2603.08288v1)
- [Posterior Sampling Reinforcement Learning with Gaussian Processes for Continuous Control: Sublinear Regret Bounds for Unbounded State Spaces](https://arxiv.org/abs/2603.08287v1)
- [PolyFormer: learning efficient reformulations for scalable optimization under complex physical constraints](https://arxiv.org/abs/2603.08283v1)
- [Evaluating LLM-Based Grant Proposal Review via Structured Perturbations](https://arxiv.org/abs/2603.08281v1)
- [TA-RNN-Medical-Hybrid: A Time-Aware and Interpretable Framework for Mortality Risk Prediction](https://arxiv.org/abs/2603.08278v1)
- [AdaCultureSafe: Adaptive Cultural Safety Grounded by Cultural Knowledge in Large Language Models](https://arxiv.org/abs/2603.08275v1)
- [How Much Do LLMs Hallucinate in Document Q&A Scenarios? A 172-Billion-Token Study Across Temperatures, Context Lengths, and Hardware Platforms](https://arxiv.org/abs/2603.08274v1)
- [SCL-GNN: Towards Generalizable Graph Neural Networks via Spurious Correlation Learning](https://arxiv.org/abs/2603.08270v1) **[ranked]**
- [SAIL: Test-Time Scaling for In-Context Imitation Learning with VLM](https://arxiv.org/abs/2603.08269v1)
- [Towards a more efficient bias detection in financial language models](https://arxiv.org/abs/2603.08267v1)
- [Airborne Magnetic Anomaly Navigation with Neural-Network-Augmented Online Calibration](https://arxiv.org/abs/2603.08265v1) **[ranked]**
- [FinToolBench: Evaluating LLM Agents for Real-World Financial Tool Use](https://arxiv.org/abs/2603.08262v1)
- [Beyond ReinMax: Low-Variance Gradient Estimators for Discrete Latent Variables](https://arxiv.org/abs/2603.08257v1)
- [FlowTouch: View-Invariant Visuo-Tactile Prediction](https://arxiv.org/abs/2603.08255v1)
- [FedPrism: Adaptive Personalized Federated Learning under Non-IID Data](https://arxiv.org/abs/2603.08252v1)
- [Optimising antibiotic switching via forecasting of patient physiology](https://arxiv.org/abs/2603.08242v1)
- [Fibration Policy Optimization](https://arxiv.org/abs/2603.08239v1)
- [Exploring Deep Learning and Ultra-Widefield Imaging for Diabetic Retinopathy and Macular Edema](https://arxiv.org/abs/2603.08235v1)
- [The Struggle Between Continuation and Refusal: A Mechanistic Analysis of the Continuation-Triggered Jailbreak in LLMs](https://arxiv.org/abs/2603.08234v1)
- [Disentangling Reasoning in Large Audio-Language Models for Ambiguous Emotion Prediction](https://arxiv.org/abs/2603.08230v1)
- [SplitAgent: A Privacy-Preserving Distributed Architecture for Enterprise-Cloud Agent Collaboration](https://arxiv.org/abs/2603.08221v1)
- [Wiener Chaos Expansion based Neural Operator for Singular Stochastic Partial Differential Equations](https://arxiv.org/abs/2603.08219v1)
- [Revisiting Gradient Staleness: Evaluating Distance Metrics for Asynchronous Federated Learning Aggregation](https://arxiv.org/abs/2603.08211v1)
- [Alignment-Aware and Reliability-Gated Multimodal Fusion for Unmanned Aerial Vehicle Detection Across Heterogeneous Thermal-Visual Sensors](https://arxiv.org/abs/2603.08208v1)
- [Distributional Regression with Tabular Foundation Models: Evaluating Probabilistic Predictions via Proper Scoring Rules](https://arxiv.org/abs/2603.08206v1)
- [MM-TS: Multi-Modal Temperature and Margin Schedules for Contrastive Learning with Long-Tail Data](https://arxiv.org/abs/2603.08202v1)
- [Sequential Service Region Design with Capacity-Constrained Investment and Spillover Effect](https://arxiv.org/abs/2603.08188v1)
- [SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization](https://arxiv.org/abs/2603.08185v1)
- [TildeOpen LLM: Leveraging Curriculum Learning to Achieve Equitable Language Representation](https://arxiv.org/abs/2603.08182v1)
- [AutoAdapt: An Automated Domain Adaptation Framework for LLMs](https://arxiv.org/abs/2603.08181v1)
- [ALOOD: Exploiting Language Representations for LiDAR-based Out-of-Distribution Object Detection](https://arxiv.org/abs/2603.08180v1)
- [Privacy-Preserving End-to-End Full-Duplex Speech Dialogue Models](https://arxiv.org/abs/2603.08179v1)
- [Is continuous CoT better suited for multi-lingual reasoning?](https://arxiv.org/abs/2603.08177v1)
- [Broad frequency tuning of a Nb$_{3}$Sn superconducting microwave cavity for dark matter searches](https://arxiv.org/abs/2603.08175v1)
- [Evolution Strategy-Based Calibration for Low-Bit Quantization of Speech Models](https://arxiv.org/abs/2603.08173v1)
- [Evidence-Driven Reasoning for Industrial Maintenance Using Heterogeneous Data](https://arxiv.org/abs/2603.08171v1)
- [An explainable hybrid deep learning-enabled intelligent fault detection and diagnosis approach for automotive software systems validation](https://arxiv.org/abs/2603.08165v1)
- [Covenant-72B: Pre-Training a 72B LLM with Trustless Peers Over-the-Internet](https://arxiv.org/abs/2603.08163v1)
- [Learning Hierarchical Knowledge in Text-Rich Networks with Taxonomy-Informed Representation Learning](https://arxiv.org/abs/2603.08159v1)
- [Outlier-robust Autocovariance Least Square Estimation via Iteratively Reweighted Least Square](https://arxiv.org/abs/2603.08158v1) **[ranked]**
- [Are We Winning the Wrong Game? Revisiting Evaluation Practices for Long-Term Time Series Forecasting](https://arxiv.org/abs/2603.08156v1)
- [C$^2$FG: Control Classifier-Free Guidance via Score Discrepancy Analysis](https://arxiv.org/abs/2603.08155v1)
- [Gradually Excavating External Knowledge for Implicit Complex Question Answering](https://arxiv.org/abs/2603.08148v1)
- [Training event-based neural networks with exact gradients via Differentiable ODE Solving in JAX](https://arxiv.org/abs/2603.08146v1)
- [DARC: Disagreement-Aware Alignment via Risk-Constrained Decoding](https://arxiv.org/abs/2603.08145v1)
- [Probing the CP Property of ALP-photon Interactions at Future Lepton Colliders](https://arxiv.org/abs/2603.08144v1)
- [Formalizing the stability of the two Higgs doublet model potential into Lean: identifying an error in the literature](https://arxiv.org/abs/2603.08139v1)
- [Mitigating Homophily Disparity in Graph Anomaly Detection: A Scalable and Adaptive Approach](https://arxiv.org/abs/2603.08137v1) **[ranked]**
- [Explainable Condition Monitoring via Probabilistic Anomaly Detection Applied to Helicopter Transmissions](https://arxiv.org/abs/2603.08130v1)
- [TRIAGE: Type-Routed Interventions via Aleatoric-Epistemic Gated Estimation in Robotic Manipulation and Adaptive Perception -- Don't Treat All Uncertainty the Same](https://arxiv.org/abs/2603.08128v1)
- [Foley-Flow: Coordinated Video-to-Audio Generation with Masked Audio-Visual Alignment and Dynamic Conditional Flows](https://arxiv.org/abs/2603.08126v1)
- [SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action](https://arxiv.org/abs/2603.08124v1)
- [An improved measurement of $η^\prime\rightarrow e^{+}e^{-}ω$](https://arxiv.org/abs/2603.08120v1)
- [Model-based Offline RL via Robust Value-Aware Model Learning with Implicitly Differentiable Adaptive Weighting](https://arxiv.org/abs/2603.08118v1)
- [UIS-Digger: Towards Comprehensive Research Agent Systems for Real-world Unindexed Information Seeking](https://arxiv.org/abs/2603.08117v1)
- [Heavy mesons with dynamical gluon on the light front](https://arxiv.org/abs/2603.08114v1)
- [Tau-BNO: Brain Neural Operator for Tau Transport Model](https://arxiv.org/abs/2603.08108v1) **[ranked]**
- [Invisible Safety Threat: Malicious Finetuning for LLM via Steganography](https://arxiv.org/abs/2603.08104v1)
- [DC-W2S: Dual-Consensus Weak-to-Strong Training for Reliable Process Reward Modeling in Biological Reasoning](https://arxiv.org/abs/2603.08095v1)
- [DSH-Bench: A Difficulty- and Scenario-Aware Benchmark with Hierarchical Subject Taxonomy for Subject-Driven Text-to-Image Generation](https://arxiv.org/abs/2603.08090v1)
- [EAGLE-Pangu: Accelerator-Safe Tree Speculative Decoding on Ascend NPUs](https://arxiv.org/abs/2603.08088v1)
- [Tiny Autoregressive Recursive Models](https://arxiv.org/abs/2603.08082v1)
- [Hybrid Quantum Neural Network for Multivariate Clinical Time Series Forecasting](https://arxiv.org/abs/2603.08072v1)
- [Rephasing invariant structure of Dirac CP phase and basis independent reduction of unitarity constraints for mixing matrices](https://arxiv.org/abs/2603.08071v1)
- [In-Context Reinforcement Learning for Tool Use in Large Language Models](https://arxiv.org/abs/2603.08068v1)
- [Deterministic Differentiable Structured Pruning for Large Language Models](https://arxiv.org/abs/2603.08065v1)
- [Adversarial Domain Adaptation Enables Knowledge Transfer Across Heterogeneous RNA-Seq Datasets](https://arxiv.org/abs/2603.08062v1)
- [ImageEdit-R1: Boosting Multi-Agent Image Editing via Reinforcement Learning](https://arxiv.org/abs/2603.08059v1)
- [Stabilized Fine-Tuning with LoRA in Federated Learning: Mitigating the Side Effect of Client Size and Rank via the Scaling Factor](https://arxiv.org/abs/2603.08058v1)
- [Speed3R: Sparse Feed-forward 3D Reconstruction Models](https://arxiv.org/abs/2603.08055v1)
- [S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis](https://arxiv.org/abs/2603.08048v1)
- [CDRRM: Contrast-Driven Rubric Generation for Reliable and Interpretable Reward Modeling](https://arxiv.org/abs/2603.08035v1)
- [Solution to the 10th ABAW Expression Recognition Challenge: A Robust Multimodal Framework with Safe Cross-Attention and Modality Dropout](https://arxiv.org/abs/2603.08034v1)
- [GCGNet: Graph-Consistent Generative Network for Time Series Forecasting with Exogenous Variables](https://arxiv.org/abs/2603.08032v1)
- [DyLLM: Efficient Diffusion LLM Inference via Saliency-based Token Selection and Partial Attention](https://arxiv.org/abs/2603.08026v1)
- [Not Like Transformers: Drop the Beat Representation for Dance Generation with Mamba-Based Diffusion Model](https://arxiv.org/abs/2603.08023v1)
- [Capacity-Aware Mixture Law Enables Efficient LLM Data Optimization](https://arxiv.org/abs/2603.08022v1)
- [Alignment--Process--Outcome: Rethinking How AIs and Humans Collaborate](https://arxiv.org/abs/2603.08017v1)
- [FedMomentum: Preserving LoRA Training Momentum in Federated Fine-Tuning](https://arxiv.org/abs/2603.08014v1)
- [PIRA-Bench: A Transition from Reactive GUI Agents to GUI-based Proactive Intent Recommendation Agents](https://arxiv.org/abs/2603.08013v1)
- [Physics-Informed Global Extraction of the Universal Small-$x$ Dipole Amplitude](https://arxiv.org/abs/2603.08008v1)
- [ViSA-Enhanced Aerial VLN: A Visual-Spatial Reasoning Enhanced Framework for Aerial Vision-Language Navigation](https://arxiv.org/abs/2603.08007v1)
- [Amortizing Maximum Inner Product Search with Learned Support Functions](https://arxiv.org/abs/2603.08001v1) **[ranked]**
- [SmartThinker: Progressive Chain-of-Thought Length Calibration for Efficient Large Language Model Reasoning](https://arxiv.org/abs/2603.08000v1)
- [Aero-Promptness: Drag-Aware Aerodynamic Manipulability for Propeller-driven Vehicles](https://arxiv.org/abs/2603.07998v1)
- [CMMR-VLN: Vision-and-Language Navigation via Continual Multimodal Memory Retrieval](https://arxiv.org/abs/2603.07997v1)
- [MJ1: Multimodal Judgment via Grounded Verification](https://arxiv.org/abs/2603.07990v1)
- [\$OneMillion-Bench: How Far are Language Agents from Human Experts?](https://arxiv.org/abs/2603.07980v1)
- [Emergence is Overrated: AGI as an Archipelago of Experts](https://arxiv.org/abs/2603.07979v1)
- [OSExpert: Computer-Use Agents Learning Professional Skills via Exploration](https://arxiv.org/abs/2603.07978v1)
- [Scaling Machine Learning Interatomic Potentials with Mixtures of Experts](https://arxiv.org/abs/2603.07977v1)
- [VORL-EXPLORE: A Hybrid Learning Planning Approach to Multi-Robot Exploration in Dynamic Environments](https://arxiv.org/abs/2603.07973v1)
- [Adaptive Collaboration with Humans: Metacognitive Policy Optimization for Multi-Agent LLMs with Continual Learning](https://arxiv.org/abs/2603.07972v1)
- [Advancing Automated Algorithm Design via Evolutionary Stagewise Design with LLMs](https://arxiv.org/abs/2603.07970v1)
- [Local Constrained Bayesian Optimization](https://arxiv.org/abs/2603.07965v1)
- [PSTNet: Physically-Structured Turbulence Network](https://arxiv.org/abs/2603.07957v1)
- [RL unknotter, hard unknots and unknotting number](https://arxiv.org/abs/2603.07955v1)
- [ELLMob: Event-Driven Human Mobility Generation with Self-Aligned LLM Framework](https://arxiv.org/abs/2603.07946v1)
- [AI Agents, Language, Deep Learning and the Next Revolution in Science](https://arxiv.org/abs/2603.07940v1)
- [SWE-Fuse: Empowering Software Agents via Issue-free Trajectory Learning and Entropy-aware RLVR Training](https://arxiv.org/abs/2603.07927v1)
- [IMSE: Intrinsic Mixture of Spectral Experts Fine-tuning for Test-Time Adaptation](https://arxiv.org/abs/2603.07926v1)
- [Semantic Risk Scoring of Aggregated Metrics: An AI-Driven Approach for Healthcare Data Governance](https://arxiv.org/abs/2603.07924v1)
- [Robust Transfer Learning with Side Information](https://arxiv.org/abs/2603.07921v1)
- [Rel-MOSS: Towards Imbalanced Relational Deep Learning on Relational Databases](https://arxiv.org/abs/2603.07916v1)
- [Ares: Adaptive Reasoning Effort Selection for Efficient LLM Agents](https://arxiv.org/abs/2603.07915v1)
- [Long-Short Term Agents for Pure-Vision Bronchoscopy Robotic Autonomy](https://arxiv.org/abs/2603.07909v1)
- [DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models](https://arxiv.org/abs/2603.07904v1)
- [NaviDriveVLM: Decoupling High-Level Reasoning and Motion Planning for Autonomous Driving](https://arxiv.org/abs/2603.07901v1)
- [EveryQuery: Zero-Shot Clinical Prediction via Task-Conditioned Pretraining over Electronic Health Records](https://arxiv.org/abs/2603.07900v1)
- [Bayesian Transformer for Probabilistic Load Forecasting in Smart Grids](https://arxiv.org/abs/2603.07899v1)
- [Revisiting Unknowns: Towards Effective and Efficient Open-Set Active Learning](https://arxiv.org/abs/2603.07898v1)
- [LeJOT-AutoML: LLM-Driven Feature Engineering for Job Execution Time Prediction in Databricks Cost Optimization](https://arxiv.org/abs/2603.07897v1)
- [SMGI: A Structural Theory of General Artificial Intelligence](https://arxiv.org/abs/2603.07896v1)
- [Designing probabilistic AI monsoon forecasts to inform agricultural decision-making](https://arxiv.org/abs/2603.07893v1)
- [A Lightweight Traffic Map for Efficient Anytime LaCAM*](https://arxiv.org/abs/2603.07891v1)
- [Visualizing Coalition Formation: From Hedonic Games to Image Segmentation](https://arxiv.org/abs/2603.07890v1)
- [VLM-SubtleBench: How Far Are VLMs from Human-Level Subtle Comparative Reasoning?](https://arxiv.org/abs/2603.07888v1)
- [Reject, Resample, Repeat: Understanding Parallel Reasoning in Language Model Inference](https://arxiv.org/abs/2603.07887v1)
- [CCR-Bench: A Comprehensive Benchmark for Evaluating LLMs on Complex Constraints, Control Flows, and Real-World Cases](https://arxiv.org/abs/2603.07886v1)
- [Toward Unified Multimodal Representation Learning for Autonomous Driving](https://arxiv.org/abs/2603.07874v1)
- [Hospitality-VQA: Decision-Oriented Informativeness Evaluation for Vision-Language Models](https://arxiv.org/abs/2603.07868v1)
- [Slumbering to Precision: Enhancing Artificial Neural Network Calibration Through Sleep-like Processes](https://arxiv.org/abs/2603.07867v1)
- [Viewpoint-Agnostic Grasp Pipeline using VLM and Partial Observations](https://arxiv.org/abs/2603.07866v1)
- [An Interpretable Generative Framework for Anomaly Detection in High-Dimensional Financial Time Series](https://arxiv.org/abs/2603.07864v1)
- [Guess & Guide: Gradient-Free Zero-Shot Diffusion Guidance](https://arxiv.org/abs/2603.07860v1)
- [SynPlanResearch-R1: Encouraging Tool Exploration for Deep Research with Synthetic Plans](https://arxiv.org/abs/2603.07853v1)
- [Intentional Deception as Controllable Capability in LLM Agents](https://arxiv.org/abs/2603.07848v1)
- [Schwinger effect in QCD and nuclear physics](https://arxiv.org/abs/2603.07847v1)
- [AI Steerability 360: A Toolkit for Steering Large Language Models](https://arxiv.org/abs/2603.07837v1)
- [DistillGuard: Evaluating Defenses Against LLM Knowledge Distillation](https://arxiv.org/abs/2603.07835v1)
- [AI Misuse in Education Is a Measurement Problem: Toward a Learning Visibility Framework](https://arxiv.org/abs/2603.07834v1)
- [Gradient Iterated Temporal-Difference Learning](https://arxiv.org/abs/2603.07833v1)
- [Transferable Optimization Network for Cross-Domain Image Reconstruction](https://arxiv.org/abs/2603.07831v1)
- [Column Generation for the Micro-Transit Zoning Problem](https://arxiv.org/abs/2603.07821v1)
- [Fusion Complexity Inversion: Why Simpler Cross View Modules Outperform SSMs and Cross View Attention Transformers for Pasture Biomass Regression](https://arxiv.org/abs/2603.07819v1)
- [HybridStitch: Pixel and Timestep Level Model Stitching for Diffusion Acceleration](https://arxiv.org/abs/2603.07815v1)
- [Learning embeddings of non-linear PDEs: the Burgers' equation](https://arxiv.org/abs/2603.07812v1)
- [Neural Precoding in Complex Projective Spaces](https://arxiv.org/abs/2603.07811v1)
- [BPS vortex from nonpolynomial scalar QED in a $\mathds{C}\mathrm{P}^1$-Maxwell theory](https://arxiv.org/abs/2603.07803v1)
- [Toward Global Intent Inference for Human Motion by Inverse Reinforcement Learning](https://arxiv.org/abs/2603.07797v1)
- [Dual-Metric Evaluation of Social Bias in Large Language Models: Evidence from an Underrepresented Nepali Cultural Context](https://arxiv.org/abs/2603.07792v1)
- [Vision Transformers that Never Stop Learning](https://arxiv.org/abs/2603.07787v1)
- [ProgAgent:A Continual RL Agent with Progress-Aware Rewards](https://arxiv.org/abs/2603.07784v1)

</details>

*Model: openai/gpt-5.4 | LLM Usage: 4 calls, 11,531 prompt tokens, 7,381 completion tokens, 18,912 total tokens, estimated cost: $0.139542*
