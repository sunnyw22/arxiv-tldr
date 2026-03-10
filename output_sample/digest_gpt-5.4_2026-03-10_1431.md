# Research Radar Digest
*Generated: 2026-03-10 14:31 UTC*

> Papers from 2026-03-10 to latest

## Search Summary

| Parameter | Value |
|-----------|-------|
| Paper date range | 2026-03-10 |
| Total papers fetched | 972 |
| Papers shown | 18 |
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
**Expanded to:** [machine learning, deep learning, particle physics, particle reconstruction, track reconstruction, vertex reconstruction, tagging, triggers, CERN, ATLAS, CMS, HL-LHC, LHC, future collider, tracking detector, silicon tracker, track finding, track fitting, Kalman filter, combinatorial Kalman filter, vertexing, primary vertex, secondary vertex, flavor tagging, jet tagging, trigger menu, Level-1 trigger, HLT, graph neural network, GNN, geometric deep learning, point cloud, hit clustering, pattern recognition, particle flow, pileup mitigation]

## Pipeline Stats

- **Sources:** 972 from arXiv, 0 from INSPIRE
- **After dedup:** 972 unique papers
- **Keyword filter:** 176 passed, 784 rejected
- **LLM scored:** 13 papers
- **Final digest:** 18 papers

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses your active project or core methods. Must-read. |
| 7-8 | Same subfield with relevant methods or insights. Likely useful. |
| 4-6 | Adjacent field or tangentially related technique. Might be interesting. |
| 1-3 | Different field or minimal overlap with your work. |

---

## 1. Characterization and upgrade of a quantum graph neural network for charged particle tracking

**Relevance: 9/10** | Published: 2026-03-10 | Source: arXiv | Categories: quant-ph, cs.LG, hep-ex

**Authors:** Matteo Argenton, Laura Cappelli, Concezio Bozzi

<details>
<summary>Abstract</summary>

arXiv:2603.08667v1 Announce Type: cross 
Abstract: In the forthcoming years the LHC experiments are going to be upgraded to benefit from the substantial increase of the LHC instantaneous luminosity, which will lead to larger, denser events, and, consequently, greater complexity in reconstructing charged particle tracks, motivating frontier research in new technologies. Quantum machine learning models are being investigated as potential new approaches to high energy physics (HEP) tasks. We characterize and upgrade a quantum graph neural network (QGNN) architecture for charged particle track reconstruction on a simulated high luminosity dataset. The model operates on a set of event graphs, each built from the hits generated in tracking detector layers by particles produced in proton collisions, performing a classification of the possible hit connections between adjacent layers. In this approach the QGNN is designed as a hybrid architecture, interleaving classical feedforward networks with parametrized quantum circuits. We characterize the interplay between the classical and quantum components. We report on the principal upgrades to the original design, and present new evidence of improved training behavior, specifically in terms of convergence toward the final trained configuration.

</details>

**From the paper:** This paper studies charged particle tracking on simulated high-luminosity collision data using a quantum graph neural network that classifies hit connections between adjacent detector layers. The architecture is hybrid, combining classical feedforward networks with parametrized quantum circuits, and the authors analyze the interplay between the classical and quantum components. The abstract reports upgrades to the original design and presents evidence of improved training behavior, especially better convergence to the final trained configuration.

**Gpt-5.4 - Assessment:** It connects very directly to the researcher's interests in machine learning, graph neural networks, particle tracking, and collider reconstruction for LHC upgrades. The problem formulation—edge classification on detector-hit graphs for track building—is exactly in the tracking pipeline space, so even if the quantum component is not immediately deployable, the architectural choices and training observations could inform future track-reconstruction studies. Because it is framed around high-luminosity conditions, it is especially relevant for work aimed at HL-LHC or future collider tracking challenges.

[Read paper](https://arxiv.org/abs/2603.08667)
 | [PDF](https://arxiv.org/pdf/2603.08667)

---

## 2. End-to-end Differentiable Calibration and Reconstruction for Optical Particle Detectors

**Relevance: 8/10** | Published: 2026-03-10 | Source: arXiv | Categories: hep-ex, cs.LG, physics.ins-det

**Authors:** Omar Alterkait, C\'esar Jes\'us-Valls, Ryo Matsumoto, Patrick de Perio, Kazuhiro Terao

<details>
<summary>Abstract</summary>

arXiv:2602.24129v2 Announce Type: replace 
Abstract: Large-scale homogeneous detectors with optical readouts are widely used in particle detection, with Cherenkov and scintillator neutrino detectors as prominent examples. Analyses in experimental physics rely on high-fidelity simulators to translate sensor-level information into physical quantities of interest. This task critically depends on accurate calibration, which aligns simulation behavior with real detector data, and on tracking, which infers particle properties from optical signals. We present the first end-to-end differentiable optical particle detector simulator, enabling simultaneous calibration and reconstruction through gradient-based optimization. Our approach unifies simulation, calibration, and tracking, which are traditionally treated as separate problems, within a single differentiable framework. We demonstrate that it achieves smooth and physically meaningful gradients across all key stages of light generation, propagation, and detection while maintaining computational efficiency. We show that gradient-based calibration and reconstruction greatly simplify existing analysis pipelines while matching or surpassing the performance of conventional non-differentiable methods in both accuracy and speed. Moreover, the framework's modularity allows straightforward adaptation to diverse detector geometries and target materials, providing a flexible foundation for experiment design and optimization. The results demonstrate the readiness of this technique for adoption in current and future optical detector experiments, establishing a new paradigm for simulation and reconstruction in particle physics.

</details>

**From the paper:** This paper introduces an end-to-end differentiable simulator for optical particle detectors that unifies simulation, calibration, and tracking within a single gradient-based framework. The method provides differentiable treatment of light generation, propagation, and detection while remaining computationally efficient. The abstract claims that gradient-based calibration and reconstruction match or exceed conventional non-differentiable methods in both accuracy and speed, and that the framework is modular across detector geometries and materials.

**Gpt-5.4 - Assessment:** This strongly connects to your interests in machine learning for particle reconstruction because it reframes calibration and reconstruction as a differentiable end-to-end optimization problem inside a physics detector pipeline. Even though the detector class is optical rather than ATLAS/CMS tracking, the core ideas—differentiable simulation, joint calibration/reconstruction, and gradient-based inference—are highly transferable to future reconstruction systems and detector-ML co-design. For advanced work on reconstruction at CERN or future colliders, this is the sort of methodological paper that can broaden your toolbox.

[Read paper](https://arxiv.org/abs/2602.24129)
 | [PDF](https://arxiv.org/pdf/2602.24129)

---

## 3. End-to-end optimisation of HEP triggers

**Relevance: 8/10** | Published: 2026-03-10 | Source: arXiv | Categories: hep-ex

**Authors:** Noah Clarke Hall, Ioannis Xiotidis, Nikos Konstantinidis, David W. Miller

<details>
<summary>Abstract</summary>

arXiv:2603.08428v1 Announce Type: new 
Abstract: High-energy physics experiments face extreme data rates, requiring real-time trigger systems to reduce event throughput while preserving sensitivity to rare processes. Trigger systems are typically constructed as modular chains of sequentially optimised algorithms, including machine learning models. Each algorithm is optimised for a specific local objective with no guarantee of overall optimality. We instead formulate trigger design as a constrained end-to-end optimisation problem, treating all stages- including data encoding, denoising, clustering, and calibration- as components of a single differentiable system trained against a unified physics objective. The framework jointly optimises performance while incorporating physics and deployment constraints. We demonstrate this approach on a hardware multi-jet trigger inspired by the ATLAS High-Luminosity Large Hadron Collider design. Using Higgs boson pair production as a benchmark, we observe x2-4 improvement in true-positive rate at fixed false-positive rate, while preserving interpretable intermediate physics objects and monotonic calibration constraints. These results highlight end-to-end optimisation as a practical paradigm for next-generation real-time event selection systems.

</details>

**From the paper:** This paper reformulates HEP trigger design as a constrained end-to-end optimization problem rather than a sequence of separately optimized modules. The proposed differentiable framework jointly optimizes stages including data encoding, denoising, clustering, and calibration under physics and deployment constraints. On a hardware multi-jet trigger inspired by the ATLAS HL-LHC design and benchmarked with Higgs boson pair production, the abstract reports a 2-4x improvement in true-positive rate at fixed false-positive rate while preserving interpretable intermediate objects and monotonic calibration constraints.

**Gpt-5.4 - Assessment:** It directly connects to the researcher's interests in machine learning, triggers, CERN experiments, and reconstruction pipelines. Even though the example is a multi-jet trigger rather than track reconstruction, the central idea—joint optimization across traditionally separate detector-processing stages—could be highly transferable to tracking or vertexing chains, especially for real-time or resource-constrained environments. The emphasis on differentiability, constraints, and deployment realism also matches the practical demands of collider ML systems.

[Read paper](https://arxiv.org/abs/2603.08428)
 | [PDF](https://arxiv.org/pdf/2603.08428)

---

## 4. Search for long-lived charginos and $\tau$-sleptons using final states with a disappearing track in $pp$ collisions at $\sqrt{s} = 13$ TeV with the ATLAS detector

**Relevance: 8/10** | Published: 2026-03-10 | Source: arXiv | Categories: hep-ex

**Authors:** ATLAS Collaboration

<details>
<summary>Abstract</summary>

arXiv:2603.08315v1 Announce Type: new 
Abstract: This paper reports a search for decays of long-lived charginos or $\tau$-sleptons to final states containing a short disappearing track, a single high-energy jet, and missing transverse momentum. The search uses 137 fb$^{-1}$ of data from 13 TeV proton-proton collisions recorded by the ATLAS detector during Run 2 of the LHC. Multiple search regions are defined, all requiring the presence of a track reconstructed from either three or four measurements in the innermost layers of the ATLAS detector. Regions with tracks having only three measurements are further characterised by the absence or presence of a low-energy charged pion reconstructed using a dedicated algorithm, leveraging machine learning. Data-driven methods are used to estimate the background contributions in the search regions. No significant excesses are found and 95% CL lower limits are placed on the masses of charginos and $\tau$-sleptons in the lifetime range $0.01{-}10$ ns. Observed (expected) mass limits of up to 225 GeV (250 GeV) are set for pure-higgsino charginos in scenarios with lifetimes below 0.03 ns, where the electroweakino mass splitting is entirely due to loop corrections involving the Standard Model bosons, and up to 720 GeV (840 GeV) for charginos with a lifetime of around 1 ns. For wino production, charginos with masses up to 880 GeV (1020 GeV) are excluded for lifetimes of around 1 ns. For $\tau$-sleptons with lifetimes of around 1 ns, masses are excluded up to 320 GeV (390 GeV) in Constrained Minimal Supersymmetric Standard Model scenarios and 300 GeV (380 GeV) in Gauge-Mediated Supersymmetry-Breaking scenarios.

</details>

**From the paper:** This paper searches for long-lived charginos and tau-sleptons in 13 TeV ATLAS Run 2 data using final states with a short disappearing track, a high-energy jet, and missing transverse momentum. The analysis defines multiple search regions requiring tracks reconstructed from three or four innermost-layer measurements, and for three-hit tracks it further uses a dedicated machine-learning-based algorithm to identify low-energy charged pions. No significant excess is observed, and the paper reports 95% CL mass limits across lifetimes from 0.01 to 10 ns, with exclusions reaching up to 880 GeV for winos and 720 GeV for charginos around 1 ns.

**Gpt-5.4 - Assessment:** This connects directly to your interests in ATLAS, particle reconstruction, track reconstruction, and ML in collider experiments. The most relevant aspect is the handling of extremely short track signatures built from only three or four measurements, plus the use of a dedicated ML algorithm in a reconstruction-adjacent task; that is closely aligned with challenges in sparse-hit tracking and exotic-signature reconstruction. Even though it is not a methods paper, it provides a concrete high-value use case where reconstruction performance at the detector limit materially impacts physics reach.

[Read paper](https://arxiv.org/abs/2603.08315)
 | [PDF](https://arxiv.org/pdf/2603.08315)

---

## 5. Photon reconstruction using the Hough transform in imaging calorimeters

**Relevance: 7/10** | Published: 2026-03-10 | Source: arXiv | Categories: physics.ins-det, hep-ex

**Authors:** Yang Zhang (Institute of High Energy Physics, Beijing, China, University of Chinese Academy of Sciences, Beijing *et al.* (44 authors)

<details>
<summary>Abstract</summary>

arXiv:2508.20728v3 Announce Type: replace-cross 
Abstract: Photon reconstruction in calorimeters represents a crucial challenge in particle physics experiments, especially in high-density environments where shower overlapping probabilities become significant. We present an energy-core-based photon reconstruction method. It is achieved through extending the application of the Hough transform to exploit the energy-core structure of photon showers. The method, validated through simulations of the CEPC crystal electromagnetic calorimeter, achieves a reconstruction efficiency of nearly 100% for photons with energies exceeding 2 GeV and a separation efficiency approaching 100% for two 5 GeV photons, when the distance between them reaches the granularity limit of the calorimeter. This energy-core-based photon reconstruction method, integrated with an energy splitting technique, enhances the performance of photon measurement and provides a promising tool for imaging calorimeters, particularly those requiring high precision in photon detection in complex event topologies with high multiplicity.

</details>

**From the paper:** This paper presents an energy-core-based photon reconstruction method that extends the Hough transform to exploit the energy-core structure of photon showers in imaging calorimeters. Using CEPC crystal electromagnetic calorimeter simulations, it reports nearly 100% reconstruction efficiency for photons above 2 GeV and near-100% separation efficiency for two 5 GeV photons at the calorimeter granularity limit. The method is combined with an energy splitting technique to improve photon measurement in high-density topologies.

**Gpt-5.4 - Assessment:** It connects directly to your reconstruction interests in collider detectors, especially if you work broadly across particle-flow-style reconstruction, calorimeter object building, or future-collider detector concepts. Although it is not an ML method and not focused on tracks or vertices, it tackles a core reconstruction problem—separating nearby objects in dense environments—that is highly relevant to modern collider experiments. The algorithmic framing and performance claims could inform comparative baselines or hybrid reconstruction pipelines.

[Read paper](https://arxiv.org/abs/2508.20728)
 | [PDF](https://arxiv.org/pdf/2508.20728)

---

## 6. Hadronic decay branching ratio measurements of the Higgs boson at future colliders using the Holistic Approach

**Relevance: 7/10** | Published: 2026-03-10 | Source: arXiv | Categories: hep-ex

**Authors:** Jianfeng Jiang, Yongfeng Zhu, Chao Yang, Manqi Ruan

<details>
<summary>Abstract</summary>

arXiv:2602.09354v2 Announce Type: replace 
Abstract: Accurately measuring the properties of the Higgs boson is one of the primary physics objectives of the high-energy frontier. By incorporating the inclusive information of all reconstructed particles to identify the signal events, referred to as the holistic approach, we estimate the relative statistical uncertainty for the Higgs hadronic decay modes $H \to b\bar{b}$, $c\bar{c}$, $gg$, $WW^{*} \to 4q$, and $ZZ^{*} \to 4q$ at the Circular Electron--Positron Collider (CEPC) operating as a Higgs factory with an integrated luminosity of 21.6~ab$^{-1}$. In the $Z(\mu^{+}\mu^{-})H$ and $Z(\nu\bar{\nu})H$ channels, the relative statistical uncertainties for these decay modes are projected to range from 0.36\% to 5.21\% and 0.16\% to 2.52\%, respectively. Compared to the CEPC Snowmass results, the holistic approach boosts the measurement precision by a factor of two to four. The scaling behavior, specifically the dependence of the anticipated accuracy on the training dataset size, is observed and analyzed. The precision of these leading Higgs decay modes, especially the $H \to b\bar{b}$ mode, is asymptotically approaching the statistical limit. The scaling behavior could also be applied to monitor the robustness and to quantify the uncertainties of the holistic approach.

</details>

**From the paper:** This work studies hadronic Higgs decay branching-ratio measurements at the CEPC using a 'holistic approach' that incorporates inclusive information from all reconstructed particles to identify signal events. It evaluates the precision for H→bb¯, cc¯, gg, WW*→4q, and ZZ*→4q in Z(μ+μ−)H and Z(νν¯)H channels with 21.6 ab−1. The abstract reports projected relative statistical uncertainties from 0.36% to 5.21% and 0.16% to 2.52%, respectively, claims improvements by factors of two to four over CEPC Snowmass results, and discusses observed scaling with training dataset size.

**Gpt-5.4 - Assessment:** This connects strongly to your interests in machine learning, tagging, and collider reconstruction because it uses all reconstructed-particle information for classification in a future collider setting. While it is downstream of track finding, it is directly in the event-reconstruction/identification pipeline and may offer ideas for particle-level representations, end-to-end reconstruction strategies, and data-scaling behavior relevant to ML systems for future CERN-like experiments.

[Read paper](https://arxiv.org/abs/2602.09354)
 | [PDF](https://arxiv.org/pdf/2602.09354)

---

## 7. GNN For Muon Particle Momentum estimation

**Relevance: 6/10** | Published: 2026-03-10 | Source: arXiv | Categories: physics.data-an, cs.LG, hep-ex

**Authors:** Vishak K Bhat, Eric A. F. Reinhardt, Sergei Gleyzer

<details>
<summary>Abstract</summary>

arXiv:2603.06675v1 Announce Type: cross 
Abstract: Due to a high rate of overall data generation relative to data generation of interest, the CMS experiment at the Large Hadron Collider uses a combination of hardware- and software-based triggers to select data for capture. Accurate momentum calculation is crucial for improving the efficiency of the CMS trigger systems, enabling better classification of low- and high- momentum particles and reducing false triggers. This paper explores the use of Graph Neural Networks (GNNs) for the momentum estimation task. We present two graph construction methods and apply a GNN model to leverage the inherent graph structure of the data. In this paper firstly, we show that the GNN outperforms traditional models like TabNet in terms of Mean Absolute Error (MAE), demonstrating its effectiveness in capturing complex dependencies within the data. Secondly we show that the dimension of the node feature is crucial for the efficiency of GNN.

</details>

**From the paper:** This paper addresses momentum estimation for muons in the CMS trigger context, motivated by the need for accurate momentum calculation to improve trigger efficiency and reduce false triggers. The authors construct graphs using two different methods and apply a graph neural network, comparing it with traditional models such as TabNet. According to the abstract, the GNN achieves better mean absolute error than TabNet, and node-feature dimensionality is found to be important for GNN efficiency.

**Gpt-5.4 - Assessment:** It is relevant through the overlap with CMS, trigger systems, and ML for online reconstruction-related tasks in collider experiments. While not about track finding itself, momentum estimation is tightly coupled to trigger performance and could offer transferable ideas on graph construction and feature design for detector-object inference. For someone implementing ML in reconstruction pipelines, it may be useful as a neighboring application rather than a direct blueprint.

[Read paper](https://arxiv.org/abs/2603.06675)
 | [PDF](https://arxiv.org/pdf/2603.06675)

---

## 8. Learning the Standard Model Manifold: Bayesian Latent Diffusion for Collider Anomaly Detection

**Relevance: 6/10** | Published: 2026-03-10 | Source: arXiv | Categories: physics.data-an, hep-ex

**Authors:** Jigar Patel, Tommaso Dorigo

<details>
<summary>Abstract</summary>

arXiv:2603.06754v1 Announce Type: cross 
Abstract: We propose a physics-informed anomaly detection framework for collider data based on a Bayesian latent diffusion model. Our method combines a probabilistic encoder with diffusion dynamics in the latent space, allowing for stable and flexible density estimation while explicitly enforcing physics constraints, such as mass decorrelation and regularization of latent correlations. We train and test the model on simulated LHC jet data and evaluate its performance using seed-averaged ROC curves together with discovery-oriented metrics. Through a series of ablation studies, we show that the diffusion process, Bayesian regularization, and physics-motivated loss terms each contribute in a complementary way: they help stabilize training and improve generalization, even when the gains in peak performance are moderate. Overall, our results emphasize the importance of incorporating both uncertainty estimates and physics consistency when building reliable anomaly detection methods for new Physics searches in high-energy physics.

</details>

**From the paper:** This paper proposes a physics-informed anomaly detection method for collider data based on a Bayesian latent diffusion model. The approach uses a probabilistic encoder and latent-space diffusion while enforcing physics constraints such as mass decorrelation and latent-correlation regularization, and it is evaluated on simulated LHC jet data. The abstract states that diffusion, Bayesian regularization, and physics-motivated losses improve training stability and generalization, with moderate gains in peak performance.

**Gpt-5.4 - Assessment:** This is directly within ML for collider physics and may be useful if you care about uncertainty-aware generative modeling, weakly supervised searches, or physics-constrained latent representations. While it is not about track or vertex reconstruction, the ideas of uncertainty estimation, inductive physics constraints, and stable generative training are relevant to detector-level ML development at CERN experiments. It is more adjacent than central, but substantially closer to your interests than generic ML papers.

[Read paper](https://arxiv.org/abs/2603.06754)
 | [PDF](https://arxiv.org/pdf/2603.06754)

---

## 9. SCL-GNN: Towards Generalizable Graph Neural Networks via Spurious Correlation Learning

**Relevance: 6/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, cs.AI

**Authors:** Yuxiang Zhang, Enyan Dai

<details>
<summary>Abstract</summary>

arXiv:2603.08270v1 Announce Type: new 
Abstract: Graph Neural Networks (GNNs) have demonstrated remarkable success across diverse tasks. However, their generalization capability is often hindered by spurious correlations between node features and labels in the graph. Our analysis reveals that GNNs tend to exploit imperceptible statistical correlations in training data, even when such correlations are unreliable for prediction. To address this challenge, we propose the Spurious Correlation Learning Graph Neural Network (SCL-GNN), a novel framework designed to enhance generalization on both Independent and Identically Distributed (IID) and Out-of-Distribution (OOD) graphs. SCL-GNN incorporates a principled spurious correlation learning mechanism, leveraging the Hilbert-Schmidt Independence Criterion (HSIC) to quantify correlations between node representations and class scores. This enables the model to identify and mitigate irrelevant but influential spurious correlations effectively. Additionally, we introduce an efficient bi-level optimization strategy to jointly optimize modules and GNN parameters, preventing overfitting. Extensive experiments on real-world and synthetic datasets demonstrate that SCL-GNN consistently outperforms state-of-the-art baselines under various distribution shifts, highlighting its robustness and generalization capabilities.

</details>

**From the paper:** The paper addresses poor GNN generalization caused by spurious correlations between node features and labels. It proposes SCL-GNN, which uses HSIC to quantify correlations between node representations and class scores, together with a bi-level optimization strategy to identify and mitigate spurious correlations while avoiding overfitting. Experiments on synthetic and real-world datasets reportedly show consistent gains over state-of-the-art baselines on both IID and OOD graphs.

**Gpt-5.4 - Assessment:** Graph neural networks are increasingly used in particle tracking and related reconstruction tasks, where distribution shift and simulation-specific shortcuts are real concerns. A framework explicitly designed to suppress spurious correlations in node/graph representations could be relevant for improving robustness of graph-based tracking, hit association, or particle-flow style models. The limitation is that the paper is generic and does not discuss detector geometry, sparse high-energy physics graphs, or reconstruction-specific objectives.

[Read paper](https://arxiv.org/abs/2603.08270)
 | [PDF](https://arxiv.org/pdf/2603.08270)

---

## 10. LoRA-Ensemble: Efficient Uncertainty Modelling for Self-Attention Networks

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG

**Authors:** Dominik J. M\"uhlematter, Michelle Halbheer, Alexander Becker, Dominik Narnhofer, Helge Aasen *et al.* (7 authors)

<details>
<summary>Abstract</summary>

arXiv:2405.14438v5 Announce Type: replace 
Abstract: Numerous real-world decisions rely on machine learning algorithms and require calibrated uncertainty estimates. However, modern methods often yield overconfident, uncalibrated predictions. The dominant approach to quantifying the uncertainty inherent in the model is to train an ensemble of separate predictors and measure their empirical variance. In an explicit implementation, the ensemble has a high computational cost and memory footprint, especially if the base model itself is already large, like modern transformers. This motivates efforts to develop implicit ensemble methods that emulate the ensemble without explicitly instantiating all its members. We introduce LoRA-Ensemble, a parameter-efficient ensembling method for self-attention networks. It is based on Low-Rank Adaptation (LoRA), originally developed for efficient LLM fine-tuning, and extends it into an implicit ensembling scheme, where all ensemble members share the same, pre-trained self-attention network, but have individual low-rank matrices for the attention projections. The resulting method not only outperforms state-of-the-art implicit techniques like BatchEnsemble, but even matches or exceeds the accuracy of an Explicit Ensemble, while at the same time achieving superior calibration.

</details>

**From the paper:** This paper studies calibrated uncertainty estimation for self-attention networks. It introduces LoRA-Ensemble, an implicit ensemble method in which ensemble members share a pretrained self-attention backbone and differ through individual low-rank LoRA matrices applied to attention projections. According to the abstract, the method outperforms BatchEnsemble and matches or exceeds explicit ensembles in accuracy while also improving calibration.

**Gpt-5.4 - Assessment:** Uncertainty estimation is important in particle-physics ML when deploying models for tagging, trigger decisions, or ambiguous reconstruction tasks, especially if you are using transformer-style architectures. A parameter-efficient ensemble could be useful if you want better-calibrated confidence scores without training many full models. Still, because the paper is architecture-level and not tied to tracks, vertices, detector hits, or collider data, its relevance is moderate rather than direct.

[Read paper](https://arxiv.org/abs/2405.14438)
 | [PDF](https://arxiv.org/pdf/2405.14438)

---

## 11. OTAD: An Optimal Transport-Induced Robust Model for Agnostic Adversarial Attack

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, cs.AI, math.OC, stat.ML

**Authors:** Kuo Gai, Sicong Wang, Shihua Zhang

<details>
<summary>Abstract</summary>

arXiv:2408.00329v2 Announce Type: replace-cross 
Abstract: Deep neural networks (DNNs) are vulnerable to small adversarial perturbations of the inputs, posing a significant challenge to their reliability and robustness. Empirical methods such as adversarial training can defend against particular attacks but remain vulnerable to more powerful attacks. Alternatively, Lipschitz networks provide certified robustness to unseen perturbations but lack sufficient expressive power. To harness the advantages of both approaches, we design a novel two-step Optimal Transport induced Adversarial Defense (OTAD) model that can fit the training data accurately while preserving the local Lipschitz continuity. First, we train a DNN with a regularizer derived from optimal transport theory, yielding a discrete optimal transport map linking data to its features. By leveraging the map's inherent regularity, we interpolate the map by solving the convex integration problem (CIP) to guarantee the local Lipschitz property. OTAD is extensible to diverse architectures of ResNet and Transformer, making it suitable for complex data. For efficient computation, the CIP can be solved through training neural networks. OTAD opens a novel avenue for developing reliable and secure deep learning systems through the regularity of optimal transport maps. Empirical results demonstrate that OTAD can outperform other robust models on diverse datasets.

</details>

**From the paper:** This paper presents OTAD, a two-step adversarial defense framework that combines a regularizer derived from optimal transport with interpolation of the resulting transport map through a convex integration problem to guarantee local Lipschitz continuity. The approach is designed to preserve expressive power while improving robustness and is said to extend to ResNet and Transformer architectures. The abstract reports that OTAD outperforms other robust models on diverse datasets.

**Gpt-5.4 - Assessment:** For collider ML, especially tagging or trigger-related classifiers, robustness to distribution shifts or adversarial-like perturbations can matter, and the paper offers a principled route combining regularization with local Lipschitz control. However, it does not address detector geometry, graph/event data, or reconstruction outputs, so the connection to your particle tracking pipeline is methodological rather than direct.

[Read paper](https://arxiv.org/abs/2408.00329)
 | [PDF](https://arxiv.org/pdf/2408.00329)

---

## 12. The Role of Feature Interactions in Graph-based Tabular Deep Learning

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, stat.ML

**Authors:** Elias Dubbeldam, Reza Mohammadi, Marit Schoonhoven, S. Ilker Birbil

<details>
<summary>Abstract</summary>

arXiv:2510.04543v2 Announce Type: replace-cross 
Abstract: Accurate predictions on tabular data rely on capturing complex, dataset-specific feature interactions. Attention-based methods and graph neural networks, referred to as graph-based tabular deep learning (GTDL), aim to improve predictions by modeling these interactions as a graph. In this work, we analyze how these methods model the feature interactions. Current GTDL approaches primarily focus on optimizing predictive accuracy, often neglecting the accurate modeling of the underlying graph structure. Using synthetic datasets with known ground-truth graph structures, we find that current GTDL methods fail to recover meaningful feature interactions, as their edge recovery is close to random. This suggests that the attention mechanism and message-passing schemes used in GTDL do not effectively capture feature interactions. Furthermore, when we impose the true interaction structure, we find that the predictive accuracy improves. This highlights the need for GTDL methods to prioritize accurate modeling of the graph structure, as it leads to better predictions.

</details>

**From the paper:** This paper evaluates graph-based tabular deep learning methods with a focus on whether they actually recover meaningful feature interaction structures. Using synthetic datasets with known ground-truth graphs, the authors find that current methods recover edges at near-random levels, indicating that existing attention and message-passing schemes do not effectively capture interactions. They further report that imposing the true interaction structure improves predictive accuracy.

**Gpt-5.4 - Assessment:** Your work likely touches graph neural networks or attention mechanisms in particle tracking, where learned relational structure is often assumed to reflect meaningful detector or hit interactions. This paper is relevant because it cautions that graph-based models may achieve predictive gains without recovering true interaction structure, which is useful when designing or interpreting GNN-based reconstruction models.

[Read paper](https://arxiv.org/abs/2510.04543)
 | [PDF](https://arxiv.org/pdf/2510.04543)

---

## 13. Enhancing low energy reconstruction and classification in KM3NeT/ORCA with transformers

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: hep-ex, astro-ph.IM, cs.AI

**Authors:** Iv\'an Moz\'un Mateo (on behalf of the KM3NeT collaboration)

<details>
<summary>Abstract</summary>

arXiv:2511.18999v2 Announce Type: replace 
Abstract: The current KM3NeT/ORCA neutrino telescope, still under construction, has not yet reached its full potential in neutrino reconstruction capability. When training any deep learning model, no explicit information about the physics or the detector is provided, thus they remain unknown to the model. This study leverages the strengths of transformers by incorporating attention masks inspired by the physics and detector design, making the model understand both the telescope design and the neutrino physics measured on it. The study also shows the efficacy of transformers on retaining valuable information between detectors when doing fine-tuning from one configurations to another.

</details>

**From the paper:** This paper studies low-energy reconstruction and classification in the KM3NeT/ORCA neutrino telescope using transformers. The model incorporates attention masks inspired by detector design and neutrino physics so that the architecture reflects both the instrument layout and the measured processes. The abstract states that the study demonstrates the usefulness of transformers for reconstruction/classification and for retaining information when fine-tuning between detector configurations.

**Gpt-5.4 - Assessment:** It is relevant at the methodological level because it shows how detector geometry and physics priors can be embedded into a deep-learning architecture through structured attention masks. That idea could transfer to collider reconstruction problems, including tracking, where inductive bias from detector layout is often crucial. Still, the detector type and reconstruction problem are quite different from LHC charged-particle tracking, so this is more a source of architectural inspiration than a directly usable result.

[Read paper](https://arxiv.org/abs/2511.18999)
 | [PDF](https://arxiv.org/pdf/2511.18999)

---

## 14. How the Graph Construction Technique Shapes Performance in IoT Botnet Detection

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.NI, cs.CR, cs.LG

**Authors:** Hassan Wasswa, Hussein Abbass, Timothy Lynar

<details>
<summary>Abstract</summary>

arXiv:2603.06654v1 Announce Type: cross 
Abstract: The increasing incidence of IoT-based botnet attacks has driven interest in advanced learning models for detection. Recent efforts have focused on leveraging attention mechanisms to model long-range feature dependencies and Graph Neural Networks (GNNs) to capture relationships between data instances. Since GNNs require graph-structured input, tabular NetFlow data must be transformed accordingly. This study evaluates how the choice of the method for constructing the graph-structured dataset impacts the classification performance of a GNN model. Five methods--k-Nearest Neighbors, Mutual Nearest Neighbors, Shared Nearest Neighbor, Gabriel Graph, and epsilon-radius Graph--were evaluated in this research. To reduce the computational burden associated with high-dimensional data, a Variational Autoencoder (VAE) is employed to project the original features into a lower-dimensional latent space prior to graph generation. Subsequently, a Graph Attention Network (GAT) is trained on each graph to classify traffic in the N-BaIoT dataset into three categories: Normal, Mirai, and Gafgyt. The results indicate that using Gabriel graph achieves the highest detection performance with an accuracy of 97.56% while SNN recorded the lowest performance with an accuracy as low as 78.56%.

</details>

**From the paper:** This paper investigates how different graph construction methods influence GNN-based IoT botnet detection from tabular NetFlow data. It uses a variational autoencoder to embed features into a lower-dimensional latent space, then constructs graphs using five methods and trains a graph attention network for three-class classification on the N-BaIoT dataset. The abstract reports that the Gabriel graph gives the best accuracy at 97.56%, while the shared nearest neighbor graph performs worst at 78.56%.

**Gpt-5.4 - Assessment:** For graph-based tracking and reconstruction, graph construction is often a central design choice because it controls edge density, efficiency, and how much geometric prior enters the model. This paper is useful as a reminder that preprocessing choices can dominate downstream GNN performance, and its comparison of graph construction strategies could inspire analogous ablations for hit graphs or candidate association graphs. Still, the data modality and task are quite different from collider reconstruction, so the transfer is conceptual rather than direct.

[Read paper](https://arxiv.org/abs/2603.06654)
 | [PDF](https://arxiv.org/pdf/2603.06654)

---

## 15. Not All Neighbors Matter: Understanding the Impact of Graph Sparsification on GNN Pipelines

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, cs.DB

**Authors:** Yuhang Song, Naima Abrar Shami, Romaric Duvignau, Vasiliki Kalavri

<details>
<summary>Abstract</summary>

arXiv:2603.06952v1 Announce Type: new 
Abstract: As graphs scale to billions of nodes and edges, graph Machine Learning workloads are constrained by the cost of multi-hop traversals over exponentially growing neighborhoods. While various system-level and algorithmic optimizations have been proposed to accelerate Graph Neural Network (GNN) pipelines, data management and movement remain the primary bottlenecks at scale. In this paper, we explore whether graph sparsification, a well-established technique that reduces edges to create sparser neighborhoods, can serve as a lightweight pre-processing step to address these bottlenecks while preserving accuracy on node classification tasks.
  We develop an extensible experimental framework that enables systematic evaluation of how different sparsification methods affect the performance and accuracy of GNN models. We conduct the first comprehensive study of GNN training and inference on sparsified graphs, revealing several key findings. First, sparsification often preserves or even improves predictive performance. As an example, random sparsification raises the accuracy of the GAT model by 6.8% on the PubMed graph. Second, benefits increase with scale, substantially accelerating both training and inference. Our results show that the K-Neighbor sparsifier improves model serving performance on the Products graph by 11.7x with only a 0.7% accuracy drop. Importantly, we find that the computational overhead of sparsification is quickly amortized, making it practical for very large graphs.

</details>

**From the paper:** This paper studies whether graph sparsification can be used as a lightweight preprocessing step to reduce the cost of GNN pipelines on large graphs while preserving node-classification accuracy. It introduces an experimental framework to evaluate multiple sparsification methods and measures their impact on training, inference, and predictive performance. The authors report that sparsification often preserves or improves accuracy and can substantially accelerate computation, including an 11.7x serving speedup on the Products graph with only a 0.7% accuracy drop.

**Gpt-5.4 - Assessment:** Your work likely intersects with GNN-based tracking or reconstruction, where neighborhood growth and graph size are practical bottlenecks. This paper could be useful if you are considering graph pruning, edge filtering, or candidate-neighborhood reduction before message passing in track-building or hit-association graphs. However, because it focuses on generic node-classification benchmarks rather than particle-physics reconstruction graphs, transfer to your setting is plausible but not demonstrated.

[Read paper](https://arxiv.org/abs/2603.06952)
 | [PDF](https://arxiv.org/pdf/2603.06952)

---

## 16. Latent Autoencoder Ensemble Kalman Filter for Data assimilation

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, cs.NA, math.NA, stat.ME, stat.ML

**Authors:** Xin T. Tong, Yanyan Wang, Liang Yan

<details>
<summary>Abstract</summary>

arXiv:2603.06752v1 Announce Type: cross 
Abstract: The ensemble Kalman filter (EnKF) is widely used for data assimilation in high-dimensional systems, but its performance often deteriorates for strongly nonlinear dynamics due to the structural mismatch between the Kalman update and the underlying system behavior. In this work, we propose a latent autoencoder ensemble Kalman filter (LAE-EnKF) that addresses this limitation by reformulating the assimilation problem in a learned latent space with linear and stable dynamics. The proposed method learns a nonlinear encoder--decoder together with a stable linear latent evolution operator and a consistent latent observation mapping, yielding a closed linear state-space model in the latent coordinates. This construction restores compatibility with the Kalman filtering framework and allows both forecast and analysis steps to be carried out entirely in the latent space. Compared with existing autoencoder-based and latent assimilation approaches that rely on unconstrained nonlinear latent dynamics, the proposed formulation emphasizes structural consistency, stability, and interpretability. We provide a theoretical analysis of learning linear dynamics on low-dimensional manifolds and establish generalization error bounds for the proposed latent model. Numerical experiments on representative nonlinear and chaotic systems demonstrate that the LAE-EnKF yields more accurate and stable assimilation than the standard EnKF and related latent-space methods, while maintaining comparable computational cost and data-driven.

</details>

**From the paper:** This paper proposes a latent autoencoder ensemble Kalman filter (LAE-EnKF) for data assimilation in high-dimensional nonlinear systems. The method learns an encoder-decoder, stable linear latent dynamics, and a latent observation map so that forecast and analysis can be performed consistently in latent space within a linear state-space framework. The authors provide theoretical analysis and generalization bounds, and report more accurate and stable assimilation than standard EnKF and related latent-space approaches on nonlinear and chaotic systems at comparable computational cost.

**Gpt-5.4 - Assessment:** The paper connects to your ML interests through representation learning, latent-space inference, and stable state estimation in high-dimensional settings. Those ideas could be useful for sequential detector-state estimation, track-building under partial observations, or hybrid learned-filter approaches, but the paper is still outside the specific domain of collider particle reconstruction and gives no direct HEP implementation.

[Read paper](https://arxiv.org/abs/2603.06752)
 | [PDF](https://arxiv.org/pdf/2603.06752)

---

## 17. NEST: Network- and Memory-Aware Device Placement For Distributed Deep Learning

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, cs.DC, stat.ML

**Authors:** Irene Wang, Vishnu Varma Venkata, Arvind Krishnamurthy, Divya Mahajan

<details>
<summary>Abstract</summary>

arXiv:2603.06798v1 Announce Type: cross 
Abstract: The growing scale of deep learning demands distributed training frameworks that jointly reason about parallelism, memory, and network topology. Prior works often rely on heuristic or topology-agnostic search, handling communication and memory separately. Without per-device memory awareness, these methods typically ensure feasibility post hoc by sharding parameters and activations across many devices, increasing synchronization, inflating communication, and underutilizing compute-limiting scalability and efficiency on real datacenter networks. We present NEST, a network-, compute-, and memory-aware device placement framework that unifies model parallelism, topology modeling, and memory feasibility via structured dynamic programming. NEST's DP operates on operator graphs with tensor and expert parallel configurations, explicit allreduce latencies across hierarchical or arbitrary networks, and memory/compute profiles. By factoring parallelism across tensor, pipeline, data, and expert dimensions, NEST defines a principled search space for hybrid strategies while jointly optimizing co-location, network latency, and memory feasibility. Evaluations across diverse hardware and networks show NEST achieves up to 2.43 times higher throughput, better memory efficiency, and improved scalability over state-of-the-art baselines, providing a foundation for co-designing parallelization strategies and datacenter interconnects for next-generation AI infrastructure. The source code of NEST is available at: https://github.com/scai-tech/Nest

</details>

**From the paper:** This paper studies device placement for distributed deep learning when parallelism, memory constraints, compute, and network topology must be optimized jointly. It introduces NEST, a structured dynamic-programming framework that models operator graphs, multiple parallelism dimensions, explicit communication latencies, and memory feasibility. The abstract reports up to 2.43x higher throughput, improved memory efficiency, and better scalability than state-of-the-art baselines across different hardware and network settings.

**Gpt-5.4 - Assessment:** It connects to your machine learning and deep learning interests at the systems level, especially if you train large reconstruction or tagging models across multi-GPU or multi-node setups. For collider-ML workloads, better placement and memory-aware parallelization could reduce training bottlenecks for graph, transformer, or sequence models used in tracking and reconstruction. However, the contribution is infrastructure-oriented rather than specific to HEP reconstruction algorithms.

[Read paper](https://arxiv.org/abs/2603.06798)
 | [PDF](https://arxiv.org/pdf/2603.06798)

---

## 18. Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts

**Relevance: 5/10** | Published: 2026-03-10 | Source: arXiv | Categories: cs.LG, stat.ML

**Authors:** Yuxuan Han, Meng-Hao Guo, Zhengning Liu, Wenguang Chen, Shi-Min Hu

<details>
<summary>Abstract</summary>

arXiv:2603.07169v1 Announce Type: cross 
Abstract: Optimizing GPU kernels manually is a challenging and time-consuming task. With the rapid development of LLMs, automated GPU kernel optimization is gradually becoming a tangible reality. However, current LLM-driven automated optimization methods narrowly focus on machine learning applications, such as PyTorch operator optimization, while overlooking broader domains like sparse matrix operations in scientific computing. Extending to these broader applications brings new challenges for the benchmark and algorithm. Therefore, developing a general-purpose automated kernel optimization method becomes our primary focus. In this paper, we address the absence of systematic evaluation for multi-scenario settings by introducing MSKernelBench, which spans multiple scenarios, including fundamental algebraic operations, common LLM kernels, sparse matrix operators, and scientific computing routines, each supporting both FP32 and BF16 precision. Building on this benchmark, we introduce CUDAMaster, a multi-agent, hardware-aware system for kernel optimization that leverages profiling information and automatically constructs the full compilation and execution toolchain. Experimental results demonstrate that CUDAMaster achieves significant speedups across most operators, outperforming Astra by about 35%. In several cases, its performance matches or surpasses that of highly optimized, closed-source libraries such as cuBLAS. A demo showcasing the original and optimized code for each operator is available at https://hanyx2021.github.io/MSKernelBenchDemo/.

</details>

**From the paper:** This paper focuses on automated optimization of CUDA kernels across multiple application scenarios beyond standard ML operators. It introduces MSKernelBench, a benchmark covering algebraic operations, LLM kernels, sparse matrix operators, and scientific computing routines, and proposes CUDAMaster, a multi-agent hardware-aware optimization system using profiling and automated toolchain construction. The abstract states that CUDAMaster outperforms Astra by about 35% and in some cases matches or exceeds highly optimized closed-source libraries such as cuBLAS.

**Gpt-5.4 - Assessment:** It connects to your ML and particle-physics computing interests if your reconstruction pipeline depends on custom CUDA kernels, sparse operators, or high-throughput inference/training. This could be relevant for accelerating graph construction, message passing, detector-data preprocessing, or trigger-side kernels on GPUs. However, the paper is about kernel optimization methodology, not reconstruction physics or detector-specific ML methods.

[Read paper](https://arxiv.org/abs/2603.07169)
 | [PDF](https://arxiv.org/pdf/2603.07169)

---

<details>
<summary>All fetched papers (972 total)</summary>

- [First inclusive triple-differential measurement of the muon-antineutrino charged-current cross section using the NOvA Near Detector](https://arxiv.org/abs/2603.06718)
- [AI Agents, Language, Deep Learning and the Next Revolution in Science](https://arxiv.org/abs/2603.07940)
- [An improved measurement of $\eta^\prime\rightarrow e^{+}e^{-}\omega$](https://arxiv.org/abs/2603.08120)
- [Search for long-lived charginos and $\tau$-sleptons using final states with a disappearing track in $pp$ collisions at $\sqrt{s} = 13$ TeV with the ATLAS detector](https://arxiv.org/abs/2603.08315) **[ranked]**
- [Search for decays of the Higgs boson into pair-produced pseudoscalar particles decaying into $\tau^+\tau^-\tau^+\tau^-$ using $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector](https://arxiv.org/abs/2603.08323)
- [End-to-end optimisation of HEP triggers](https://arxiv.org/abs/2603.08428) **[ranked]**
- [Amplitude Analysis of Singly Cabibbo-Suppressed Decay $\Lambda^{+}_{c}\to p K^{+} K^{-}$](https://arxiv.org/abs/2603.08469)
- [Improved branching-fraction measurements of $B^0_{(s)} \to K_S^0 h^+ h^{'-}$ decays and first observation of $B^0_(s) \to K_S^0 K^+ K^-$](https://arxiv.org/abs/2603.08621)
- [GNN For Muon Particle Momentum estimation](https://arxiv.org/abs/2603.06675) **[ranked]**
- [Learning the Standard Model Manifold: Bayesian Latent Diffusion for Collider Anomaly Detection](https://arxiv.org/abs/2603.06754) **[ranked]**
- [First Optical Observation of Negative Ion Drift at Surface Pressure](https://arxiv.org/abs/2603.06837)
- [Lepton Mixing from a Lattice Flavon Model: A Two-Branch Octant-delta Prediction](https://arxiv.org/abs/2603.06934)
- [Studying the QCD phase diagram using pressure derivatives from lattice QCD](https://arxiv.org/abs/2603.07140)
- [Characterization of the Low Energy Excess using a NUCLEUS $Al_2O_3$ detector](https://arxiv.org/abs/2603.07687)
- [Physics-Informed Global Extraction of the Universal Small-$x$ Dipole Amplitude](https://arxiv.org/abs/2603.08008)
- [Broad frequency tuning of a Nb$_{3}$Sn superconducting microwave cavity for dark matter searches](https://arxiv.org/abs/2603.08175)
- [Radiative corrections to the nucleon isovector $g_V$ and $g_A$](https://arxiv.org/abs/2603.08596)
- [Characterization and upgrade of a quantum graph neural network for charged particle tracking](https://arxiv.org/abs/2603.08667) **[ranked]**
- [A Method for On-Orbit Calibration of the VLAST-P Electromagnetic Calorimeter](https://arxiv.org/abs/2511.07944)
- [Enhancing low energy reconstruction and classification in KM3NeT/ORCA with transformers](https://arxiv.org/abs/2511.18999) **[ranked]**
- [Hadronic decay branching ratio measurements of the Higgs boson at future colliders using the Holistic Approach](https://arxiv.org/abs/2602.09354) **[ranked]**
- [End-to-end Differentiable Calibration and Reconstruction for Optical Particle Detectors](https://arxiv.org/abs/2602.24129) **[ranked]**
- [Catani's generalization of collinear factorization breaking](https://arxiv.org/abs/2402.14749)
- [Les Houches 2023 -- Physics at TeV Colliders: Report on the Standard Model Precision Wishlist](https://arxiv.org/abs/2504.06689)
- [Photon reconstruction using the Hough transform in imaging calorimeters](https://arxiv.org/abs/2508.20728) **[ranked]**
- [Tribute to Henry Primakoff: Chiral Perturbation Theory Tests via Primakoff Reactions](https://arxiv.org/abs/2509.04649)
- [A Differentiable Surrogate Model for the Generation of Radio Pulses from In-Ice Neutrino Interactions](https://arxiv.org/abs/2509.10274)
- [Observation of charmonium sequential suppression in heavy-ion collisions at the Relativistic Heavy Ion Collider](https://arxiv.org/abs/2509.12842)
- [Scattering of non-relativistic finite-size particles and puffy dark matter direct detection](https://arxiv.org/abs/2510.10641)
- [Muon trident process at far-forward LHC detectors](https://arxiv.org/abs/2510.18943)
- [Constraining $A\to ZH$ with $H\to t\bar t$ in the Low-Mass Region](https://arxiv.org/abs/2510.23714)
- [Flavored QCD axion and Modular invariance](https://arxiv.org/abs/2511.06355)
- [Double Bangs at IceCube as a Window to the Neutrino Mass Origin](https://arxiv.org/abs/2511.07541)
- [Precision Higgs Boson Probe of Type-II Seesaw Models](https://arxiv.org/abs/2512.07532)
- [Two body nonleptonic decays of $\Omega_{b}\rightarrow \Omega_{c}$ beyond tree level](https://arxiv.org/abs/2601.00657)
- [Conceptual Design of a Novel Highly Granular Crystal Electromagnetic Calorimeter for Future Higgs Factories](https://arxiv.org/abs/2602.09836)
- [Alternative classical Lagrangians for the Standard-Model Extension](https://arxiv.org/abs/2603.06714)
- [Quantum and Thermal Fluctuations of Cherenkov Radiation from HQET](https://arxiv.org/abs/2603.06784)
- [The meV frontier of neutrinoless double beta decay in the JUNO era](https://arxiv.org/abs/2603.06787)
- [Vacuum Birefringence, Ellipticity, and the Anomalous Magnetic Moment of a Photon](https://arxiv.org/abs/2603.07010)
- [Conformal versus non-conformal two-Higgs-doublet model: phase transitions and gravitational waves](https://arxiv.org/abs/2603.07189)
- [Alternative framework for the left-right symmetric model including vector-like fermions](https://arxiv.org/abs/2603.07608)
- [Impact of chirality imbalance and nonlocal interactions on the QCD biased axionic domainwall interpretation of NANOGrav 15 year data](https://arxiv.org/abs/2603.07739)
- [Schwinger effect in QCD and nuclear physics](https://arxiv.org/abs/2603.07847)
- [Rephasing invariant structure of Dirac CP phase and basis independent reduction of unitarity constraints for mixing matrices](https://arxiv.org/abs/2603.08071)
- [Heavy mesons with dynamical gluon on the light front](https://arxiv.org/abs/2603.08114)
- [Formalizing the stability of the two Higgs doublet model potential into Lean: identifying an error in the literature](https://arxiv.org/abs/2603.08139)
- [Probing the CP Property of ALP-photon Interactions at Future Lepton Colliders](https://arxiv.org/abs/2603.08144)
- [Nonminimal Lorentz Violation in Atomic and Molecular Spectroscopy Experiments](https://arxiv.org/abs/2603.08298)
- [Connecting baryon light-front wave functions to quasi-transverse-momentum-dependent correlators in lattice QCD](https://arxiv.org/abs/2603.08405)
- [The Dark Photon: a 2026 Perspective](https://arxiv.org/abs/2603.08430)
- [Precise Predictions for Hadronic Higgs Decays](https://arxiv.org/abs/2603.08517)
- [Cobimaximal mixing pattern from a $\Delta(27)$ inverse seesaw model](https://arxiv.org/abs/2603.08625)
- [Flash from the Past: New Gamma-Ray Constraints on Light CP-even Scalar from SN1987A](https://arxiv.org/abs/2603.08695)
- [Thermalization of Neutrinos in a Neutron Star Merger Simulation](https://arxiv.org/abs/2603.06788)
- [Enhanced Neutrino Cooling from Parity-Doubled Nucleons in Neutron Star Cooling Simulations](https://arxiv.org/abs/2603.06789)
- [Higher-order hadronic vacuum polarization contribution to the muon $g-2$ from lattice QCD](https://arxiv.org/abs/2603.06806)
- [General Hamiltonian Approach to the $\mathbf{N}$-Body Finite-Volume Formalism: Extracting the $\mathbf{\omega}$ Resonance Parameters from Lattice QCD](https://arxiv.org/abs/2603.07205)
- [Nuclear Deformation Effects on Charmonium Suppression in Au+Au and U+U Collisions](https://arxiv.org/abs/2603.07547)
- [Thermal and chemical response from entanglement entropy](https://arxiv.org/abs/2603.07635)
- [BPS vortex from nonpolynomial scalar QED in a $\mathds{C}\mathrm{P}^1$-Maxwell theory](https://arxiv.org/abs/2603.07803)
- [Gravitational waves in metric-affine bumblebee gravity](https://arxiv.org/abs/2603.08310)
- [Effects of fermions in one-loop propagators in the Curci-Ferrari-Delbourgo-Jarvis gauge](https://arxiv.org/abs/2603.08460)
- [Circular stable orbits in $f(R)$ realistic static and spherically-symmetric spacetimes](https://arxiv.org/abs/2603.08637)
- [Black Hole Mergers as the Fastest Photon Ring Scramblers](https://arxiv.org/abs/2603.08643)
- [Multimessenger Characterization of High-Energy Neutrino Emission from the Brightest Neutrino-Active Galactic Nuclei](https://arxiv.org/abs/2603.08684)
- [Confront a dilaton model with the LHC measurements](https://arxiv.org/abs/2501.07820)
- [Extended IDM theory with low scale seesaw mechanisms](https://arxiv.org/abs/2502.19488)
- [Compositness and wave function of shallow bound states in relation to scattering observables](https://arxiv.org/abs/2505.17657)
- [Charged lepton flavor violating decays with a pair of light dark matter and muonium invisible decay](https://arxiv.org/abs/2507.13876)
- [On CP-violation and quark masses: reducing the number of free parameters](https://arxiv.org/abs/2508.11081)
- [Exploring vector-like $B$-quark pair production at CLIC in fully hadronic final states](https://arxiv.org/abs/2510.10237)
- [Energy levels of multiscale bound states from QED energy-momentum trace](https://arxiv.org/abs/2601.11403)
- [Probing the Scalar Sector: Discovery Reach for Heavy Higgs Pairs at a $\sqrt{s} = 6$ TeV Muon Collider in the 2HDM Alignment Limit](https://arxiv.org/abs/2602.12454)
- [Update analysis of $\psi(3686)\to p\bar{p}$](https://arxiv.org/abs/2602.20526)
- [Pion and $\rho$ meson's unpolarized quark distribution functions from $q\bar{q}$ and all Fock-states within Dyson--Schwinger equations](https://arxiv.org/abs/2602.24187)
- [The effect of charm quark on the QCD chiral phase diagram](https://arxiv.org/abs/2603.04728)
- [Revisiting the Chern-Simons interaction during inflation with a non-canonical pseudo-scalar](https://arxiv.org/abs/2501.02890)
- [Polaron formation as the vertex function problem: From Dyck's paths to self-energy Feynman diagrams](https://arxiv.org/abs/2505.21054)
- [Elliptic flow of deuterons from simulations with hybrid model](https://arxiv.org/abs/2510.07897)
- [Grand Unification Higgs-$\mathcal{R}^2$ Inflation: Complementarity between Proton Decay and CMB Observables](https://arxiv.org/abs/2511.05673)
- [Discovering gravitational waveform distortions from lensing: a deep dive into GW231123](https://arxiv.org/abs/2512.16916)
- [Hyperon-Induced Inhomogeneous Pion Condensation and Moat Regimes in Neutron Star Cores](https://arxiv.org/abs/2602.23433)
- [New axion bounds derived from the 100-parsec Gaia DR3 white dwarf luminosity function](https://arxiv.org/abs/2603.00901)
- [Modified Teukolsky formalism: Null testing and numerical benchmarking](https://arxiv.org/abs/2603.01456)
- [CREDO: Epistemic-Aware Conformalized Credal Envelopes for Regression](https://arxiv.org/abs/2603.06826)
- [Bilateral Trade Under Heavy-Tailed Valuations: Minimax Regret with Infinite Variance](https://arxiv.org/abs/2603.06851)
- [Fairness May Backfire: When Leveling-Down Occurs in Fair Machine Learning](https://arxiv.org/abs/2603.06901)
- [Post-Training with Policy Gradients: Optimality and the Base Model Barrier](https://arxiv.org/abs/2603.06957)
- [Masked Unfairness: Hiding Causality within Zero ATE](https://arxiv.org/abs/2603.06984)
- [Deep Generative Spatiotemporal Engression for Probabilistic Forecasting of Epidemics](https://arxiv.org/abs/2603.07108)
- [Probabilistic Inference and Learning with Stein's Method](https://arxiv.org/abs/2603.07467)
- [Beyond Data Splitting: Full-Data Conformal Prediction by Differential Privacy](https://arxiv.org/abs/2603.07522)
- [An Interpretable Generative Framework for Anomaly Detection in High-Dimensional Financial Time Series](https://arxiv.org/abs/2603.07864)
- [Robust Transfer Learning with Side Information](https://arxiv.org/abs/2603.07921)
- [Local Constrained Bayesian Optimization](https://arxiv.org/abs/2603.07965)
- [Beyond ReinMax: Low-Variance Gradient Estimators for Discrete Latent Variables](https://arxiv.org/abs/2603.08257)
- [Posterior Sampling Reinforcement Learning with Gaussian Processes for Continuous Control: Sublinear Regret Bounds for Unbounded State Spaces](https://arxiv.org/abs/2603.08287)
- [Unifying On- and Off-Policy Variance Reduction Methods](https://arxiv.org/abs/2603.08370)
- [Generative Adversarial Regression (GAR): Learning Conditional Risk Scenarios](https://arxiv.org/abs/2603.08553)
- [Momentum SVGD-EM for Accelerated Maximum Marginal Likelihood Estimation](https://arxiv.org/abs/2603.08676)
- [Structural Causal Bottleneck Models](https://arxiv.org/abs/2603.08682)
- [Khatri-Rao Clustering for Data Summarization](https://arxiv.org/abs/2603.06602)
- [Latent Autoencoder Ensemble Kalman Filter for Data assimilation](https://arxiv.org/abs/2603.06752) **[ranked]**
- [NEST: Network- and Memory-Aware Device Placement For Distributed Deep Learning](https://arxiv.org/abs/2603.06798) **[ranked]**
- [Kernel Methods for Some Transport Equations with Application to Learning Kernels for the Approximation of Koopman Eigenfunctions: A Unified Approach via Variational Methods, Green's Functions and the Method of Characteristics](https://arxiv.org/abs/2603.06872)
- [Combinatorial Allocation Bandits with Nonlinear Arm Utility](https://arxiv.org/abs/2603.07005)
- [Fr\'echet regression of multivariate distributions with nonparanormal transport](https://arxiv.org/abs/2603.07014)
- [Combining Adam and its Inverse Counterpart to Enhance Generalization of Deep Learning Optimizers](https://arxiv.org/abs/2603.07122)
- [Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts](https://arxiv.org/abs/2603.07169) **[ranked]**
- [Conditional Rank-Rank Regression via Deep Conditional Transformation Models](https://arxiv.org/abs/2603.07230)
- [Variational Flow Maps: Make Some Noise for One-Step Conditional Generation](https://arxiv.org/abs/2603.07276)
- [Adversarial Latent-State Training for Robust Policies in Partially Observable Domains](https://arxiv.org/abs/2603.07313)
- [A Distributed Gaussian Process Model for Multi-Robot Mapping](https://arxiv.org/abs/2603.07351)
- [Tree-Based Predictive Models for Noisy Input Data](https://arxiv.org/abs/2603.07409)
- [Cost-Driven Representation Learning for Linear Quadratic Gaussian Control: Part II](https://arxiv.org/abs/2603.07437)
- [Reject, Resample, Repeat: Understanding Parallel Reasoning in Language Model Inference](https://arxiv.org/abs/2603.07887)
- [Bayesian Transformer for Probabilistic Load Forecasting in Smart Grids](https://arxiv.org/abs/2603.07899)
- [RL unknotter, hard unknots and unknotting number](https://arxiv.org/abs/2603.07955)
- [Amortizing Maximum Inner Product Search with Learned Support Functions](https://arxiv.org/abs/2603.08001)
- [Explainable Condition Monitoring via Probabilistic Anomaly Detection Applied to Helicopter Transmissions](https://arxiv.org/abs/2603.08130)
- [Are We Winning the Wrong Game? Revisiting Evaluation Practices for Long-Term Time Series Forecasting](https://arxiv.org/abs/2603.08156)
- [Towards plausibility in time series counterfactual explanations](https://arxiv.org/abs/2603.08349)
- [Beyond the Markovian Assumption: Robust Optimization via Fractional Weyl Integrals in Imbalanced Data](https://arxiv.org/abs/2603.08377)
- [Decoupling Distance and Networks: Hybrid Graph Attention-Geostatistical Methods for Spatio-temporal Risk Mapping](https://arxiv.org/abs/2603.08393)
- [Efficient Credal Prediction through Decalibration](https://arxiv.org/abs/2603.08495)
- [Breaking the Bias Barrier in Concave Multi-Objective Reinforcement Learning](https://arxiv.org/abs/2603.08518)
- [Impact of Connectivity on Laplacian Representations in Reinforcement Learning](https://arxiv.org/abs/2603.08558)
- [Mini-batch Estimation for Deep Cox Models: Statistical Foundations and Practical Guidance](https://arxiv.org/abs/2408.02839)
- [Reinforcement Learning for Individual Optimal Policy from Heterogeneous Data](https://arxiv.org/abs/2505.09496)
- [Synthetic data for ratemaking: imputation-based methods vs adversarial networks and autoencoders](https://arxiv.org/abs/2509.02171)
- [Empirical PAC-Bayes bounds for Markov chains](https://arxiv.org/abs/2509.20985)
- [An Orthogonal Learner for Individualized Outcomes in Markov Decision Processes](https://arxiv.org/abs/2509.26429)
- [Wasserstein Gradient Flows for Scalable and Regularized Barycenter Computation](https://arxiv.org/abs/2510.04602)
- [Bayesian neural networks with interpretable priors from Mercer kernels](https://arxiv.org/abs/2510.23745)
- [Topological Spatial Graph Coarsening](https://arxiv.org/abs/2512.24327)
- [Sparse Offline Reinforcement Learning with Corruption Robustness](https://arxiv.org/abs/2512.24768)
- [From Mice to Trains: Amortized Bayesian Inference on Graph Data](https://arxiv.org/abs/2601.02241)
- [Synthetic Augmentation in Imbalanced Learning: When It Helps, When It Hurts, and How Much to Add](https://arxiv.org/abs/2601.16120)
- [The Partition Principle Revisited: Non-Equal Volume Designs Achieve Minimal Expected Star Discrepancy](https://arxiv.org/abs/2603.00202)
- [Online Neural Networks for Change-Point Detection](https://arxiv.org/abs/2010.01388)
- [Cost-Driven Representation Learning for Linear Quadratic Gaussian Control: Part I](https://arxiv.org/abs/2212.14511)
- [Nuisance Function Tuning and Sample Splitting for Optimally Estimating a Doubly Robust Functional](https://arxiv.org/abs/2212.14857)
- [A Robust Multi-Item Auction Design with Statistical Learning](https://arxiv.org/abs/2302.00941)
- [OTAD: An Optimal Transport-Induced Robust Model for Agnostic Adversarial Attack](https://arxiv.org/abs/2408.00329) **[ranked]**
- [Variational Learning of Gaussian Process Latent Variable Models through Stochastic Gradient Annealed Importance Sampling](https://arxiv.org/abs/2408.06710)
- [BNEM: A Boltzmann Sampler Based on Bootstrapped Noised Energy Matching](https://arxiv.org/abs/2409.09787)
- [Adaptive Transfer Clustering: A Unified Framework](https://arxiv.org/abs/2410.21263)
- [The Exploration of Error Bounds in Classification with Noisy Labels](https://arxiv.org/abs/2501.15163)
- [Active Advantage-Aligned Online Reinforcement Learning with Offline Data](https://arxiv.org/abs/2502.07937)
- [Adaptive Replication Strategies in Trust-Region-Based Bayesian Optimization of Stochastic Functions](https://arxiv.org/abs/2504.20527)
- [Online Decision-Focused Learning](https://arxiv.org/abs/2505.13564)
- [Faster Gradient Methods for Highly-Smooth Stochastic Bilevel Optimization](https://arxiv.org/abs/2509.02937)
- [Fast reconstruction of degenerate populations of conductance-based neuron models from spike times](https://arxiv.org/abs/2509.12783)
- [GDR-learners: Orthogonal Learning of Generative Models for Potential Outcomes](https://arxiv.org/abs/2509.22953)
- [Overlap-Adaptive Regularization for Conditional Average Treatment Effect Estimation](https://arxiv.org/abs/2509.24962)
- [The Role of Feature Interactions in Graph-based Tabular Deep Learning](https://arxiv.org/abs/2510.04543) **[ranked]**
- [Shortcut Invariance: Targeted Jacobian Regularization in Disentangled Latent Space](https://arxiv.org/abs/2511.19525)
- [Beyond Additivity: Sparse Isotonic Shapley Regression toward Nonlinear Explainability](https://arxiv.org/abs/2512.03112)
- [Scalable multitask Gaussian processes for complex mechanical systems with functional covariates](https://arxiv.org/abs/2602.20640)
- [vLLM Hook v0: A Plug-in for Programming Model Internals on vLLM](https://arxiv.org/abs/2603.06588)
- [How Attention Sinks Emerge in Large Language Models: An Interpretability Perspective](https://arxiv.org/abs/2603.06591)
- [FuzzingRL: Reinforcement Fuzz-Testing for Revealing VLM Failures](https://arxiv.org/abs/2603.06600)
- [Switchable Activation Networks](https://arxiv.org/abs/2603.06601)
- [Scale Dependent Data Duplication](https://arxiv.org/abs/2603.06603)
- [Know When You're Wrong: Aligning Confidence with Correctness for LLM Error Detection](https://arxiv.org/abs/2603.06604)
- [Structure-Aware Set Transformers: Temporal and Variable-Type Attention Biases for Asynchronous Clinical Time Series](https://arxiv.org/abs/2603.06605)
- [LegoNet: Memory Footprint Reduction Through Block Weight Clustering](https://arxiv.org/abs/2603.06606)
- [Valid Feature-Level Inference for Tabular Foundation Models via the Conditional Randomization Test](https://arxiv.org/abs/2603.06609)
- [CapTrack: Multifaceted Evaluation of Forgetting in LLM Post-Training](https://arxiv.org/abs/2603.06610)
- [Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness](https://arxiv.org/abs/2603.06612)
- [OptiRoulette Optimizer: A New Stochastic Meta-Optimizer for up to 5.3x Faster Convergence](https://arxiv.org/abs/2603.06613)
- [Correlation Analysis of Generative Models](https://arxiv.org/abs/2603.06614)
- [Annealed Co-Generation: Disentangling Variables via Progressive Pairwise Modeling](https://arxiv.org/abs/2603.06615)
- [RACER: Risk-Aware Calibrated Efficient Routing for Large Language Models](https://arxiv.org/abs/2603.06616)
- [Evo: Autoregressive-Diffusion Large Language Models with Evolving Balance](https://arxiv.org/abs/2603.06617)
- [Distilling and Adapting: A Topology-Aware Framework for Zero-Shot Interaction Prediction in Multiplex Biological Networks](https://arxiv.org/abs/2603.06618)
- [Not all tokens are needed(NAT): token efficient reinforcement learning](https://arxiv.org/abs/2603.06619)
- [Reward Under Attack: Analyzing the Robustness and Hackability of Process Reward Models](https://arxiv.org/abs/2603.06621)
- [From ARIMA to Attention: Power Load Forecasting Using Temporal Deep Learning](https://arxiv.org/abs/2603.06622)
- [Advances in GRPO for Generation Models: A Survey](https://arxiv.org/abs/2603.06623)
- [Pavement Missing Condition Data Imputation through Collective Learning-Based Graph Neural Networks](https://arxiv.org/abs/2603.06625)
- [Grouter: Decoupling Routing from Representation for Accelerated MoE Training](https://arxiv.org/abs/2603.06626)
- [Leakage Safe Graph Features for Interpretable Fraud Detection in Temporal Transaction Networks](https://arxiv.org/abs/2603.06632)
- [A new Uncertainty Principle in Machine Learning](https://arxiv.org/abs/2603.06634)
- [Graph Property Inference in Small Language Models: Effects of Representation and Inference Strategy](https://arxiv.org/abs/2603.06635)
- [SmartBench: Evaluating LLMs in Smart Homes with Anomalous Device States and Behavioral Contexts](https://arxiv.org/abs/2603.06636)
- [HEARTS: Benchmarking LLM Reasoning on Health Time Series](https://arxiv.org/abs/2603.06638)
- [SR-TTT: Surprisal-Aware Residual Test-Time Training](https://arxiv.org/abs/2603.06642)
- [Trust Aware Federated Learning for Secure Bone Healing Stage Interpretation in e-Health](https://arxiv.org/abs/2603.06646)
- [HURRI-GAN: A Novel Approach for Hurricane Bias-Correction Beyond Gauge Stations using Generative Adversarial Networks](https://arxiv.org/abs/2603.06649)
- [Geodesic Gradient Descent: A Generic and Learning-rate-free Optimizer on Objective Function-induced Manifolds](https://arxiv.org/abs/2603.06651)
- [ERP-RiskBench: Leakage-Safe Ensemble Learning for Financial Risk](https://arxiv.org/abs/2603.06671)
- [One step further with Monte-Carlo sampler to guide diffusion better](https://arxiv.org/abs/2603.06685)
- [Scaling Agentic Capabilities, Not Context: Efficient Reinforcement Finetuning for Large Toolspaces](https://arxiv.org/abs/2603.06713)
- [From Statistical Fidelity to Clinical Consistency: Scalable Generation and Auditing of Synthetic Patient Trajectories](https://arxiv.org/abs/2603.06720)
- [ProtAlign: Contrastive learning paradigm for Sequence and structure alignment](https://arxiv.org/abs/2603.06722)
- [Bi Directional Feedback Fusion for Activity Aware Forecasting of Indoor CO2 and PM2.5](https://arxiv.org/abs/2603.06724)
- [Regression Models Meet Foundation Models: A Hybrid-AI Approach to Practical Electricity Price Forecasting](https://arxiv.org/abs/2603.06726)
- [Safe Transformer: An Explicit Safety Bit For Interpretable And Controllable Alignment](https://arxiv.org/abs/2603.06727)
- [Orion: Characterizing and Programming Apple's Neural Engine for LLM Training and Inference](https://arxiv.org/abs/2603.06728)
- [Don't Freeze, Don't Crash: Extending the Safe Operating Range of Neural Navigation in Dense Crowds](https://arxiv.org/abs/2603.06729)
- [Rank-Factorized Implicit Neural Bias: Scaling Super-Resolution Transformer with FlashAttention](https://arxiv.org/abs/2603.06738)
- [Heterogeneous Decentralized Diffusion Models](https://arxiv.org/abs/2603.06741)
- [Improved Constrained Generation by Bridging Pretrained Generative Models](https://arxiv.org/abs/2603.06742)
- [Stabilizing Reinforcement Learning for Diffusion Language Models](https://arxiv.org/abs/2603.06743)
- [Enhancing Instruction Following of LLMs via Activation Steering with Dynamic Rejection](https://arxiv.org/abs/2603.06745)
- [Property-driven Protein Inverse Folding With Multi-Objective Preference Alignment](https://arxiv.org/abs/2603.06748)
- [Implementation of Quantum Implicit Neural Representation in Deterministic and Probabilistic Autoencoders for Image Reconstruction/Generation Tasks](https://arxiv.org/abs/2603.06755)
- [Learning Unbiased Cluster Descriptors for Interpretable Imbalanced Concept Drift Detection](https://arxiv.org/abs/2603.06757)
- [Enhancing SHAP Explainability for Diagnostic and Prognostic ML Models in Alzheimer Disease](https://arxiv.org/abs/2603.06758)
- [Diversity-Aware Adaptive Collocation for Physics-Informed Neural Networks via Sparse QUBO Optimization and Hybrid Coresets](https://arxiv.org/abs/2603.06761)
- [Metalearning traffic assignment for network disruptions with graph convolutional neural networks](https://arxiv.org/abs/2603.06763)
- [Failure Detection in Chemical Processes using Symbolic Machine Learning: A Case Study on Ethylene Oxidation](https://arxiv.org/abs/2603.06767)
- [Gauge Freedom and Metric Dependence in Neural Representation Spaces](https://arxiv.org/abs/2603.06774)
- [HGT-Scheduler: Deep Reinforcement Learning for the Job Shop Scheduling Problem via Heterogeneous Graph Transformers](https://arxiv.org/abs/2603.06777)
- [SpatialMAGIC: A Hybrid Framework Integrating Graph Diffusion and Spatial Attention for Spatial Transcriptomics Imputation](https://arxiv.org/abs/2603.06780)
- [xaitimesynth: A Python Package for Evaluating Attribution Methods for Time Series with Synthetic Ground Truth](https://arxiv.org/abs/2603.06781)
- [Physics-Informed Diffusion Model for Generating Synthetic Extreme Rare Weather Events Data](https://arxiv.org/abs/2603.06782)
- [Optimistic Policy Regularization](https://arxiv.org/abs/2603.06793)
- [Multi-Agent Reinforcement Learning with Submodular Reward](https://arxiv.org/abs/2603.06810)
- [Joint 3D Gravity and Magnetic Inversion via Rectified Flow and Ginzburg-Landau Guidance](https://arxiv.org/abs/2603.06829)
- [Contextual Counterfactual Credit Assignment for Multi-Agent Reinforcement Learning in LLM Collaboration](https://arxiv.org/abs/2603.06859)
- [IGLU: The Integrated Gaussian Linear Unit Activation Function](https://arxiv.org/abs/2603.06861)
- [Stochastic Attention via Langevin Dynamics on the Modern Hopfield Energy](https://arxiv.org/abs/2603.06875)
- [Physics-informed AI Accelerated Retention Analysis of Ferroelectric Vertical NAND: From Day-Scale TCAD to Second-Scale Surrogate Model](https://arxiv.org/abs/2603.06881)
- [Single-pass Possibilistic Clustering with Damped Window Footprints](https://arxiv.org/abs/2603.06889)
- [Learning From Design Procedure To Generate CAD Programs for Data Augmentation](https://arxiv.org/abs/2603.06894)
- [XGenBoost: Synthesizing Small and Large Tabular Datasets with XGBoost](https://arxiv.org/abs/2603.06904)
- [NerVE: Nonlinear Eigenspectrum Dynamics in LLM Feed-Forward Networks](https://arxiv.org/abs/2603.06922)
- [Swimba: Switch Mamba Model Scales State Space Models](https://arxiv.org/abs/2603.06938)
- [Physics-Consistent Neural Networks for Learning Deformation and Director Fields in Microstructured Media with Loss-Based Validation Criteria](https://arxiv.org/abs/2603.06939)
- [Joint MDPs and Reinforcement Learning in Coupled-Dynamics Environments](https://arxiv.org/abs/2603.06946)
- [Not All Neighbors Matter: Understanding the Impact of Graph Sparsification on GNN Pipelines](https://arxiv.org/abs/2603.06952) **[ranked]**
- [Chart-RL: Generalized Chart Comprehension via Reinforcement Learning with Verifiable Rewards](https://arxiv.org/abs/2603.06958)
- [Learning Quadruped Walking from Seconds of Demonstration](https://arxiv.org/abs/2603.06961)
- [Conditional Unbalanced Optimal Transport Maps: An Outlier-Robust Framework for Conditional Generative Modeling](https://arxiv.org/abs/2603.06972)
- [NePPO: Near-Potential Policy Optimization for General-Sum Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2603.06977)
- [Diffusion Controller: Framework, Algorithms and Parameterization](https://arxiv.org/abs/2603.06981)
- [RESCHED: Rethinking Flexible Job Shop Scheduling from a Transformer-based Architecture with Simplified States](https://arxiv.org/abs/2603.07020)
- [Resource-Adaptive Federated Text Generation with Differential Privacy](https://arxiv.org/abs/2603.07027)
- [Interpretable Maximum Margin Deep Anomaly Detection](https://arxiv.org/abs/2603.07073)
- [Entropy-Aware On-Policy Distillation of Language Models](https://arxiv.org/abs/2603.07079)
- [Dreamer-CDP: Improving Reconstruction-free World Models Via Continuous Deterministic Representation Prediction](https://arxiv.org/abs/2603.07083)
- [Countdown-Code: A Testbed for Studying The Emergence and Generalization of Reward Hacking in RLVR](https://arxiv.org/abs/2603.07084)
- [Agentic Planning with Reasoning for Image Styling via Offline RL](https://arxiv.org/abs/2603.07148)
- [Spectral Conditioning of Attention Improves Transformer Performance](https://arxiv.org/abs/2603.07162)
- [Shaping Parameter Contribution Patterns for Out-of-Distribution Detection](https://arxiv.org/abs/2603.07195)
- [A Dual-Graph Spatiotemporal GNN Surrogate for Nonlinear Response Prediction of Reinforced Concrete Beams under Four-Point Bending](https://arxiv.org/abs/2603.07201)
- [wDPO: Winsorized Direct Preference Optimization for Robust LLM Alignment](https://arxiv.org/abs/2603.07211)
- [Margin in Abstract Spaces](https://arxiv.org/abs/2603.07221)
- [Unlocking Data Value in Finance: A Study on Distillation and Difficulty-Aware Training](https://arxiv.org/abs/2603.07223)
- [LightMedSeg: Lightweight 3D Medical Image Segmentation with Learned Spatial Anchors](https://arxiv.org/abs/2603.07228)
- [Retrieval-Augmented Generation for Predicting Cellular Responses to Gene Perturbation](https://arxiv.org/abs/2603.07233)
- [Rethinking Deep Research from the Perspective of Web Content Distribution Matching](https://arxiv.org/abs/2603.07241)
- [LF2L: Loss Fusion Horizontal Federated Learning Across Heterogeneous Feature Spaces Using External Datasets Effectively: A Case Study in Second Primary Cancer Prediction](https://arxiv.org/abs/2603.07249)
- [Turning Time Series into Algebraic Equations: Symbolic Machine Learning for Interpretable Modeling of Chaotic Time Series](https://arxiv.org/abs/2603.07261)
- [Adaptive Double-Booking Strategy for Outpatient Scheduling Using Multi-Objective Reinforcement Learning](https://arxiv.org/abs/2603.07270)
- [Spectral Discovery of Continuous Symmetries via Generalized Fourier Transforms](https://arxiv.org/abs/2603.07299)
- [AutoResearch-RL: Perpetual Self-Evaluating Reinforcement Learning Agents for Autonomous Neural Architecture Discovery](https://arxiv.org/abs/2603.07300)
- [Retrieval-Augmented Multi-scale Framework for County-Level Crop Yield Prediction Across Large Regions](https://arxiv.org/abs/2603.07305)
- [ShakyPrepend: A Multi-Group Learner with Improved Sample Complexity](https://arxiv.org/abs/2603.07319)
- [Norm-Hierarchy Transitions in Representation Learning: When and Why Neural Networks Abandon Shortcuts](https://arxiv.org/abs/2603.07323)
- [Learning Concept Bottleneck Models from Mechanistic Explanations](https://arxiv.org/abs/2603.07343)
- [Learning Clinical Representations Under Systematic Distribution Shift](https://arxiv.org/abs/2603.07348)
- [Latent Generative Models with Tunable Complexity for Compressed Sensing and other Inverse Problems](https://arxiv.org/abs/2603.07357)
- [N-Tree Diffusion for Long-Horizon Wildfire Risk Forecasting](https://arxiv.org/abs/2603.07361)
- [Scaling Laws in the Tiny Regime: How Small Models Change Their Mistakes](https://arxiv.org/abs/2603.07365)
- [Learning to Reflect: Hierarchical Multi-Agent Reinforcement Learning for CSI-Free mmWave Beam-Focusing](https://arxiv.org/abs/2603.07370)
- [ConfHit: Conformal Generative Design with Oracle Free Guarantees](https://arxiv.org/abs/2603.07371)
- [Sparsity and Out-of-Distribution Generalization](https://arxiv.org/abs/2603.07388)
- [Feed m Birds with One Scone: Accelerating Multi-task Gradient Balancing via Bi-level Optimization](https://arxiv.org/abs/2603.07389)
- [Deterministic Fuzzy Triage for Legal Compliance Classification and Evidence Retrieval](https://arxiv.org/abs/2603.07390)
- [Generalizing Linear Autoencoder Recommenders with Decoupled Expected Quadratic Loss](https://arxiv.org/abs/2603.07402)
- [Context Channel Capacity: An Information-Theoretic Framework for Understanding Catastrophic Forgetting](https://arxiv.org/abs/2603.07415)
- [DualSpec: Accelerating Deep Research Agents via Dual-Process Action Speculation](https://arxiv.org/abs/2603.07416)
- [OrthoFormer: Instrumental Variable Estimation in Transformer Hidden States via Neural Control Functions](https://arxiv.org/abs/2603.07431)
- [Data Agent: Learning to Select Data via End-to-End Dynamic Optimization](https://arxiv.org/abs/2603.07433)
- [Discrete Tokenization Unlocks Transformers for Calibrated Tabular Forecasting](https://arxiv.org/abs/2603.07448)
- [Contact-Guided 3D Genome Structure Generation of E. coli via Diffusion Transformers](https://arxiv.org/abs/2603.07472)
- [Interpretable-by-Design Transformers via Architectural Stream Independence](https://arxiv.org/abs/2603.07482)
- [Enhanced Random Subspace Local Projections for High-Dimensional Time Series Analysis](https://arxiv.org/abs/2603.07500)
- [A Unified Framework for Knowledge Transfer in Bidirectional Model Scaling](https://arxiv.org/abs/2603.07506)
- [Online Continual Learning for Anomaly Detection in IoT under Data Distribution Shifts](https://arxiv.org/abs/2603.07507)
- [A Unified View of Drifting and Score-Based Models](https://arxiv.org/abs/2603.07514)
- [Reinforcement learning-based dynamic cleaning scheduling framework for solar energy system](https://arxiv.org/abs/2603.07518)
- [One-for-All Model Initialization with Frequency-Domain Knowledge](https://arxiv.org/abs/2603.07523)
- [Neural Dynamics-Informed Pre-trained Framework for Personalized Brain Functional Network Construction](https://arxiv.org/abs/2603.07524)
- [Generative prediction of laser-induced rocket ignition with dynamic latent space representations](https://arxiv.org/abs/2603.07525)
- [Obliviator Reveals the Cost of Nonlinear Guardedness in Concept Erasure](https://arxiv.org/abs/2603.07529)
- [ECG Classification on PTB-XL: A Data-Centric Approach with Simplified CNN-VAE](https://arxiv.org/abs/2603.07558)
- [Constraints Matrix Diffusion based Generative Neural Solver for Vehicle Routing Problems](https://arxiv.org/abs/2603.07568)
- [TS-MLLM: A Multi-Modal Large Language Model-based Framework for Industrial Time-Series Big Data Analysis](https://arxiv.org/abs/2603.07572)
- [TT-Sparse: Learning Sparse Rule Models with Differentiable Truth Tables](https://arxiv.org/abs/2603.07606)
- [Compression as Adaptation: Implicit Visual Representation with Diffusion Foundation Models](https://arxiv.org/abs/2603.07615)
- [Helix: Evolutionary Reinforcement Learning for Open-Ended Scientific Problem Solving](https://arxiv.org/abs/2603.07642)
- [Partial Differential Equations in the Age of Machine Learning: A Critical Synthesis of Classical, Machine Learning, and Hybrid Methods](https://arxiv.org/abs/2603.07655)
- [Beyond Surrogates: A Quantitative Analysis for Inter-Metric Relationships](https://arxiv.org/abs/2603.07671)
- [Global Convergence of Average Reward Constrained MDPs with Neural Critic and General Policy Parameterization](https://arxiv.org/abs/2603.07698)
- [Step-Size Decay and Structural Stagnation in Greedy Sparse Learning](https://arxiv.org/abs/2603.07703)
- [Reverse Distillation: Consistently Scaling Protein Language Model Representations](https://arxiv.org/abs/2603.07710)
- [Hide and Find: A Distributed Adversarial Attack on Federated Graph Learning](https://arxiv.org/abs/2603.07743)
- [Uncertainty-Gated Generative Modeling](https://arxiv.org/abs/2603.07753)
- [Using GPUs And LLMs Can Be Satisfying for Nonlinear Real Arithmetic Problems](https://arxiv.org/abs/2603.07764)
- [Breaking Training Bottlenecks: Effective and Stable Reinforcement Learning for Coding Models](https://arxiv.org/abs/2603.07777)
- [ProgAgent:A Continual RL Agent with Progress-Aware Rewards](https://arxiv.org/abs/2603.07784)
- [Vision Transformers that Never Stop Learning](https://arxiv.org/abs/2603.07787)
- [Neural Precoding in Complex Projective Spaces](https://arxiv.org/abs/2603.07811)
- [Gradient Iterated Temporal-Difference Learning](https://arxiv.org/abs/2603.07833)
- [Guess & Guide: Gradient-Free Zero-Shot Diffusion Guidance](https://arxiv.org/abs/2603.07860)
- [Slumbering to Precision: Enhancing Artificial Neural Network Calibration Through Sleep-like Processes](https://arxiv.org/abs/2603.07867)
- [Designing probabilistic AI monsoon forecasts to inform agricultural decision-making](https://arxiv.org/abs/2603.07893)
- [LeJOT-AutoML: LLM-Driven Feature Engineering for Job Execution Time Prediction in Databricks Cost Optimization](https://arxiv.org/abs/2603.07897)
- [DyQ-VLA: Temporal-Dynamic-Aware Quantization for Embodied Vision-Language-Action Models](https://arxiv.org/abs/2603.07904)
- [Semantic Risk Scoring of Aggregated Metrics: An AI-Driven Approach for Healthcare Data Governance](https://arxiv.org/abs/2603.07924)
- [ELLMob: Event-Driven Human Mobility Generation with Self-Aligned LLM Framework](https://arxiv.org/abs/2603.07946)
- [PSTNet: Physically-Structured Turbulence Network](https://arxiv.org/abs/2603.07957)
- [\$OneMillion-Bench: How Far are Language Agents from Human Experts?](https://arxiv.org/abs/2603.07980)
- [MJ1: Multimodal Judgment via Grounded Verification](https://arxiv.org/abs/2603.07990)
- [FedMomentum: Preserving LoRA Training Momentum in Federated Fine-Tuning](https://arxiv.org/abs/2603.08014)
- [Capacity-Aware Mixture Law Enables Efficient LLM Data Optimization](https://arxiv.org/abs/2603.08022)
- [GCGNet: Graph-Consistent Generative Network for Time Series Forecasting with Exogenous Variables](https://arxiv.org/abs/2603.08032)
- [Stabilized Fine-Tuning with LoRA in Federated Learning: Mitigating the Side Effect of Client Size and Rank via the Scaling Factor](https://arxiv.org/abs/2603.08058)
- [Adversarial Domain Adaptation Enables Knowledge Transfer Across Heterogeneous RNA-Seq Datasets](https://arxiv.org/abs/2603.08062)
- [Deterministic Differentiable Structured Pruning for Large Language Models](https://arxiv.org/abs/2603.08065)
- [Hybrid Quantum Neural Network for Multivariate Clinical Time Series Forecasting](https://arxiv.org/abs/2603.08072)
- [Tiny Autoregressive Recursive Models](https://arxiv.org/abs/2603.08082)
- [EAGLE-Pangu: Accelerator-Safe Tree Speculative Decoding on Ascend NPUs](https://arxiv.org/abs/2603.08088)
- [Invisible Safety Threat: Malicious Finetuning for LLM via Steganography](https://arxiv.org/abs/2603.08104)
- [Model-based Offline RL via Robust Value-Aware Model Learning with Implicitly Differentiable Adaptive Weighting](https://arxiv.org/abs/2603.08118)
- [Mitigating Homophily Disparity in Graph Anomaly Detection: A Scalable and Adaptive Approach](https://arxiv.org/abs/2603.08137)
- [DARC: Disagreement-Aware Alignment via Risk-Constrained Decoding](https://arxiv.org/abs/2603.08145)
- [Training event-based neural networks with exact gradients via Differentiable ODE Solving in JAX](https://arxiv.org/abs/2603.08146)
- [C$^2$FG: Control Classifier-Free Guidance via Score Discrepancy Analysis](https://arxiv.org/abs/2603.08155)
- [Learning Hierarchical Knowledge in Text-Rich Networks with Taxonomy-Informed Representation Learning](https://arxiv.org/abs/2603.08159)
- [AutoAdapt: An Automated Domain Adaptation Framework for LLMs](https://arxiv.org/abs/2603.08181)
- [SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization](https://arxiv.org/abs/2603.08185)
- [Sequential Service Region Design with Capacity-Constrained Investment and Spillover Effect](https://arxiv.org/abs/2603.08188)
- [Distributional Regression with Tabular Foundation Models: Evaluating Probabilistic Predictions via Proper Scoring Rules](https://arxiv.org/abs/2603.08206)
- [Revisiting Gradient Staleness: Evaluating Distance Metrics for Asynchronous Federated Learning Aggregation](https://arxiv.org/abs/2603.08211)
- [Wiener Chaos Expansion based Neural Operator for Singular Stochastic Partial Differential Equations](https://arxiv.org/abs/2603.08219)
- [Fibration Policy Optimization](https://arxiv.org/abs/2603.08239)
- [Optimising antibiotic switching via forecasting of patient physiology](https://arxiv.org/abs/2603.08242)
- [FedPrism: Adaptive Personalized Federated Learning under Non-IID Data](https://arxiv.org/abs/2603.08252)
- [Airborne Magnetic Anomaly Navigation with Neural-Network-Augmented Online Calibration](https://arxiv.org/abs/2603.08265)
- [SCL-GNN: Towards Generalizable Graph Neural Networks via Spurious Correlation Learning](https://arxiv.org/abs/2603.08270) **[ranked]**
- [TA-RNN-Medical-Hybrid: A Time-Aware and Interpretable Framework for Mortality Risk Prediction](https://arxiv.org/abs/2603.08278)
- [PolyFormer: learning efficient reformulations for scalable optimization under complex physical constraints](https://arxiv.org/abs/2603.08283)
- [Minor First, Major Last: A Depth-Induced Implicit Bias of Sharpness-Aware Minimization](https://arxiv.org/abs/2603.08290)
- [Rethinking Attention Output Projection: Structured Hadamard Transforms for Efficient Transformers](https://arxiv.org/abs/2603.08343)
- [A Recipe for Stable Offline Multi-agent Reinforcement Learning](https://arxiv.org/abs/2603.08399)
- [Geometrically Constrained Outlier Synthesis](https://arxiv.org/abs/2603.08413)
- [Meta-RL with Shared Representations Enables Fast Adaptation in Energy Systems](https://arxiv.org/abs/2603.08418)
- [SYNAPSE: Framework for Neuron Analysis and Perturbation in Sequence Encoding](https://arxiv.org/abs/2603.08424)
- [Grow, Assess, Compress: Adaptive Backbone Scaling for Memory-Efficient Class Incremental Learning](https://arxiv.org/abs/2603.08426)
- [LycheeCluster: Efficient Long-Context Inference with Structure-Aware Chunking and Hierarchical KV Indexing](https://arxiv.org/abs/2603.08453)
- [Data-Driven Priors for Uncertainty-Aware Deterioration Risk Prediction with Multimodal Data](https://arxiv.org/abs/2603.08459)
- [Reasoning as Compression: Unifying Budget Forcing via the Conditional Information Bottleneck](https://arxiv.org/abs/2603.08462)
- [MUSA-PINN: Multi-scale Weak-form Physics-Informed Neural Networks for Fluid Flow in Complex Geometries](https://arxiv.org/abs/2603.08465)
- [NN-OpInf: an operator inference approach using structure-preserving composable neural networks](https://arxiv.org/abs/2603.08488)
- [Echo2ECG: Enhancing ECG Representations with Cardiac Morphology from Multi-View Echos](https://arxiv.org/abs/2603.08505)
- [Oracle-Guided Soft Shielding for Safe Move Prediction in Chess](https://arxiv.org/abs/2603.08506)
- [Towards Effective and Efficient Graph Alignment without Supervision](https://arxiv.org/abs/2603.08526)
- [Drift-to-Action Controllers: Budgeted Interventions with Online Risk Certificates](https://arxiv.org/abs/2603.08578)
- [DualFlexKAN: Dual-stage Kolmogorov-Arnold Networks with Independent Function Control](https://arxiv.org/abs/2603.08583)
- [Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control](https://arxiv.org/abs/2603.08588)
- [Don't Look Back in Anger: MAGIC Net for Streaming Continual Learning with Temporal Dependence](https://arxiv.org/abs/2603.08600)
- [Integral Formulas for Vector Spherical Tensor Products](https://arxiv.org/abs/2603.08630)
- [Grow, Don't Overwrite: Fine-tuning Without Forgetting](https://arxiv.org/abs/2603.08647)
- [Divide and Predict: An Architecture for Input Space Partitioning and Enhanced Accuracy](https://arxiv.org/abs/2603.08649)
- [Group Entropies and Mirror Duality: A Class of Flexible Mirror Descent Updates for Machine Learning](https://arxiv.org/abs/2603.08651)
- [Context-free Self-Conditioned GAN for Trajectory Forecasting](https://arxiv.org/abs/2603.08658)
- [How Far Can Unsupervised RLVR Scale LLM Training?](https://arxiv.org/abs/2603.08660)
- [A New Lower Bound for the Random Offerer Mechanism in Bilateral Trade using AI-Guided Evolutionary Search](https://arxiv.org/abs/2603.08679)
- [Split Federated Learning Architectures for High-Accuracy and Low-Delay Model Training](https://arxiv.org/abs/2603.08687)
- [Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting](https://arxiv.org/abs/2603.08707)
- [XInsight: Integrative Stage-Consistent Psychological Counseling Support Agents for Digital Well-Being](https://arxiv.org/abs/2603.06583)
- [Isotonic Layer: A Universal Framework for Generic Recommendation Debiasing](https://arxiv.org/abs/2603.06589)
- [Hierarchical Latent Structures in Data Generation Process Unify Mechanistic Phenomena across Scale](https://arxiv.org/abs/2603.06592)
- [Hierarchical Embedding Fusion for Retrieval-Augmented Code Generation](https://arxiv.org/abs/2603.06593)
- [Multi-Agent DRL for V2X Resource Allocation: Disentangling Challenges and Benchmarking Solutions](https://arxiv.org/abs/2603.06607)
- [Scaling Strategy, Not Compute: A Stand-Alone, Open-Source StarCraft II Benchmark for Accessible Reinforcement Learning Research](https://arxiv.org/abs/2603.06608)
- [A Novel Approach for Testing Water Safety Using Deep Learning Inference of Microscopic Images of Unincubated Water Samples](https://arxiv.org/abs/2603.06611)
- [GraphSkill: Documentation-Guided Hierarchical Retrieval-Augmented Coding for Complex Graph Reasoning](https://arxiv.org/abs/2603.06620)
- [Exploration Space Theory: Formal Foundations for Prerequisite-Aware Location-Based Recommendation](https://arxiv.org/abs/2603.06624)
- [T-REX: Transformer-Based Category Sequence Generation for Grocery Basket Recommendation](https://arxiv.org/abs/2603.06631)
- [RECAP: Local Hebbian Prototype Learning as a Self-Organizing Readout for Reservoir Dynamics](https://arxiv.org/abs/2603.06639)
- [Roots Beneath the Cut: Uncovering the Risk of Concept Revival in Pruning-Based Unlearning for Diffusion Models](https://arxiv.org/abs/2603.06640)
- [Quantum Deep Learning: A Comprehensive Review](https://arxiv.org/abs/2603.06644)
- [How the Graph Construction Technique Shapes Performance in IoT Botnet Detection](https://arxiv.org/abs/2603.06654) **[ranked]**
- [Approximate Nearest Neighbor Search for Modern AI: A Projection-Augmented Graph Approach](https://arxiv.org/abs/2603.06660)
- [EnsAug: Augmentation-Driven Ensembles for Human Motion Sequence Analysis](https://arxiv.org/abs/2603.06661)
- [HyperTokens: Controlling Token Dynamics for Continual Video-Language Understanding](https://arxiv.org/abs/2603.06662)
- [Unmixing microinfrared spectroscopic images of cross-sections of historical oil paintings](https://arxiv.org/abs/2603.06673)
- [XAI and Few-shot-based Hybrid Classification Model for Plant Leaf Disease Prognosis](https://arxiv.org/abs/2603.06676)
- [Chart Deep Research in LVLMs via Parallel Relative Policy Optimization](https://arxiv.org/abs/2603.06677)
- [High-Resolution Image Reconstruction with Unsupervised Learning and Noisy Data Applied to Ion-Beam Dynamics for Particle Accelerators](https://arxiv.org/abs/2603.06689)
- [Soft Equivariance Regularization for Invariant Self-Supervised Learning](https://arxiv.org/abs/2603.06693)
- [On the Generalization Capacities of MLLMs for Spatial Intelligence](https://arxiv.org/abs/2603.06704)
- [Uncertainty-Aware Solar Flare Regression](https://arxiv.org/abs/2603.06712)
- [PolyBlocks: A Compiler Infrastructure for AI Chips and Programming Frameworks](https://arxiv.org/abs/2603.06731)
- [Calibrated Credit Intelligence: Shift-Robust and Fair Risk Scoring with Bayesian Uncertainty and Gradient Boosting](https://arxiv.org/abs/2603.06733)
- [Prediction of Steady-State Flow through Porous Media Using Machine Learning Models](https://arxiv.org/abs/2603.06762)
- [Best-of-Tails: Bridging Optimism and Pessimism in Inference-Time Alignment](https://arxiv.org/abs/2603.06797)
- [Symmetry-Constrained Language-Guided Program Synthesis for Discovering Governing Equations from Noisy and Partial Observations](https://arxiv.org/abs/2603.06869)
- [A Dynamic Self-Evolving Extraction System](https://arxiv.org/abs/2603.06915)
- [CN-CBF: Composite Neural Control Barrier Function for Safe Robot Navigation in Dynamic Environments](https://arxiv.org/abs/2603.06921)
- [How Private Are DNA Embeddings? Inverting Foundation Model Representations of Genomic Sequences](https://arxiv.org/abs/2603.06950)
- [A SISA-based Machine Unlearning Framework for Power Transformer Inter-Turn Short-Circuit Fault Localization](https://arxiv.org/abs/2603.06962)
- [Topology-Aware Reinforcement Learning over Graphs for Resilient Power Distribution Networks](https://arxiv.org/abs/2603.06964)
- [Adaptive Discovery of Interpretable Audio Attributes with Multimodal LLMs for Low-Resource Classification](https://arxiv.org/abs/2603.06991)
- [Can Safety Emerge from Weak Supervision? A Systematic Analysis of Small Language Models](https://arxiv.org/abs/2603.07017)
- [TEA-Time: Transporting Effects Across Time](https://arxiv.org/abs/2603.07018)
- [The Talking Robot: Distortion-Robust Acoustic Models for Robot-Robot Communication](https://arxiv.org/abs/2603.07072)
- [VLN-Cache: Enabling Token Caching for VLN Models with Visual/Semantic Dynamics Awareness](https://arxiv.org/abs/2603.07080)
- [Statistical Contraction for Chance-Constrained Trajectory Optimization of Non-Gaussian Stochastic Systems](https://arxiv.org/abs/2603.07092)
- [Towards Objective Gastrointestinal Auscultation: Automated Segmentation and Annotation of Bowel Sound Patterns](https://arxiv.org/abs/2603.07215)
- [Fast and Flexible Audio Bandwidth Extension via Vocos](https://arxiv.org/abs/2603.07285)
- [StructSAM: Structure- and Spectrum-Preserving Token Merging for Segment Anything Models](https://arxiv.org/abs/2603.07307)
- [Shutdown Safety Valves for Advanced AI](https://arxiv.org/abs/2603.07315)
- [Explainable and Hardware-Efficient Jamming Detection for 5G Networks Using the Convolutional Tsetlin Machine](https://arxiv.org/abs/2603.07336)
- [AgrI Challenge: A Data-Centric AI Competition for Cross-Team Validation in Agricultural Vision](https://arxiv.org/abs/2603.07356)
- [Domain-Specific Quality Estimation for Machine Translation in Low-Resource Scenarios](https://arxiv.org/abs/2603.07372)
- [Generalization in Online Reinforcement Learning for Mobile Agents](https://arxiv.org/abs/2603.07432)
- [Few Tokens, Big Leverage: Preserving Safety Alignment by Constraining Safety Tokens during Fine-tuning](https://arxiv.org/abs/2603.07445)
- [Dial: A Knowledge-Grounded Dialect-Specific NL2SQL System](https://arxiv.org/abs/2603.07449)
- [SLNet: A Super-Lightweight Geometry-Adaptive Network for 3D Point Cloud Recognition](https://arxiv.org/abs/2603.07454)
- [The Dual-Stream Transformer: Channelized Architecture for Interpretable Language Modeling](https://arxiv.org/abs/2603.07461)
- [Trusting What You Cannot See: Auditable Fine-Tuning and Inference for Proprietary AI](https://arxiv.org/abs/2603.07466)
- [Towards Lightweight Adaptation of Speech Enhancement Models in Real-World Environments](https://arxiv.org/abs/2603.07471)
- [Pushing Bistatic Wireless Sensing toward High Accuracy at the Sub-Wavelength Scale](https://arxiv.org/abs/2603.07492)
- [DreamSAC: Learning Hamiltonian World Models via Symmetry Exploration](https://arxiv.org/abs/2603.07545)
- [COOL-MC: Verifying and Explaining RL Policies for Multi-bridge Network Maintenance](https://arxiv.org/abs/2603.07546)
- [GRD-Net: Generative-Reconstructive-Discriminative Anomaly Detection with Region of Interest Attention Module](https://arxiv.org/abs/2603.07566)
- [Revisiting the LiRA Membership Inference Attack Under Realistic Assumptions](https://arxiv.org/abs/2603.07567)
- [A Systematic Comparison of Training Objectives for Out-of-Distribution Detection in Image Classification](https://arxiv.org/abs/2603.07571)
- [Integration of deep generative Anomaly Detection algorithm in high-speed industrial line](https://arxiv.org/abs/2603.07577)
- [Analysis-Driven Procedural Generation of an Engine Sound Dataset with Embedded Control Annotations](https://arxiv.org/abs/2603.07584)
- [Models as Lego Builders: Assembling Malice from Benign Blocks via Semantic Blueprints](https://arxiv.org/abs/2603.07590)
- [Shorter Thoughts, Same Answers: Difficulty-Scaled Segment-Wise RL for CoT Compression](https://arxiv.org/abs/2603.07598)
- [MetaSort: An Accelerated Approach for Non-uniform Compression and Few-shot Classification of Neural Spike Waveforms](https://arxiv.org/abs/2603.07602)
- [MAS-H2: A Hierarchical Multi-Agent System for Holistic Cloud-Native Autoscaling](https://arxiv.org/abs/2603.07607)
- [SMAT: Staged Multi-Agent Training for Co-Adaptive Exoskeleton Control](https://arxiv.org/abs/2603.07618)
- [Accelerating Diffusion Models for Generative AI Applications with Silicon Photonics](https://arxiv.org/abs/2603.07626)
- [Exoskeleton Control through Learning to Reduce Biological Joint Moments in Simulations](https://arxiv.org/abs/2603.07629)
- [Evaluating Synthetic Data for Baggage Trolley Detection in Airport Logistics](https://arxiv.org/abs/2603.07645)
- [Compressed Proximal Federated Learning for Non-Convex Composite Optimization on Heterogeneous Data](https://arxiv.org/abs/2603.07654)
- [Mitigating the Memory Bottleneck with Machine Learning-Driven and Data-Aware Microarchitectural Techniques](https://arxiv.org/abs/2603.07683)
- [Scalable Training of Mixture-of-Experts Models with Megatron Core](https://arxiv.org/abs/2603.07685)
- [Deep Incentive Design with Differentiable Equilibrium Blocks](https://arxiv.org/abs/2603.07705)
- [A Lightweight MPC Bidding Framework for Brand Auction Ads](https://arxiv.org/abs/2603.07721)
- [Lindbladian Learning with Neural Differential Equations](https://arxiv.org/abs/2603.07778)
- [Scaling Data Difficulty: Improving Coding Models via Reinforcement Learning on Fresh and Challenging Problems](https://arxiv.org/abs/2603.07779)
- [Toward Global Intent Inference for Human Motion by Inverse Reinforcement Learning](https://arxiv.org/abs/2603.07797)
- [Learning embeddings of non-linear PDEs: the Burgers' equation](https://arxiv.org/abs/2603.07812)
- [Fusion Complexity Inversion: Why Simpler Cross View Modules Outperform SSMs and Cross View Attention Transformers for Pasture Biomass Regression](https://arxiv.org/abs/2603.07819)
- [Transferable Optimization Network for Cross-Domain Image Reconstruction](https://arxiv.org/abs/2603.07831)
- [Viewpoint-Agnostic Grasp Pipeline using VLM and Partial Observations](https://arxiv.org/abs/2603.07866)
- [Hospitality-VQA: Decision-Oriented Informativeness Evaluation for Vision-Language Models](https://arxiv.org/abs/2603.07868)
- [Toward Unified Multimodal Representation Learning for Autonomous Driving](https://arxiv.org/abs/2603.07874)
- [VLM-SubtleBench: How Far Are VLMs from Human-Level Subtle Comparative Reasoning?](https://arxiv.org/abs/2603.07888)
- [SMGI: A Structural Theory of General Artificial Intelligence](https://arxiv.org/abs/2603.07896)
- [Revisiting Unknowns: Towards Effective and Efficient Open-Set Active Learning](https://arxiv.org/abs/2603.07898)
- [NaviDriveVLM: Decoupling High-Level Reasoning and Motion Planning for Autonomous Driving](https://arxiv.org/abs/2603.07901)
- [Rel-MOSS: Towards Imbalanced Relational Deep Learning on Relational Databases](https://arxiv.org/abs/2603.07916)
- [Scaling Machine Learning Interatomic Potentials with Mixtures of Experts](https://arxiv.org/abs/2603.07977)
- [SmartThinker: Progressive Chain-of-Thought Length Calibration for Efficient Large Language Model Reasoning](https://arxiv.org/abs/2603.08000)
- [CDRRM: Contrast-Driven Rubric Generation for Reliable and Interpretable Reward Modeling](https://arxiv.org/abs/2603.08035)
- [DC-W2S: Dual-Consensus Weak-to-Strong Training for Reliable Process Reward Modeling in Biological Reasoning](https://arxiv.org/abs/2603.08095)
- [Tau-BNO: Brain Neural Operator for Tau Transport Model](https://arxiv.org/abs/2603.08108)
- [SaiVLA-0: Cerebrum--Pons--Cerebellum Tripartite Architecture for Compute-Aware Vision-Language-Action](https://arxiv.org/abs/2603.08124)
- [Foley-Flow: Coordinated Video-to-Audio Generation with Masked Audio-Visual Alignment and Dynamic Conditional Flows](https://arxiv.org/abs/2603.08126)
- [TRIAGE: Type-Routed Interventions via Aleatoric-Epistemic Gated Estimation in Robotic Manipulation and Adaptive Perception -- Don't Treat All Uncertainty the Same](https://arxiv.org/abs/2603.08128)
- [Outlier-robust Autocovariance Least Square Estimation via Iteratively Reweighted Least Square](https://arxiv.org/abs/2603.08158)
- [Covenant-72B: Pre-Training a 72B LLM with Trustless Peers Over-the-Internet](https://arxiv.org/abs/2603.08163)
- [Is continuous CoT better suited for multi-lingual reasoning?](https://arxiv.org/abs/2603.08177)
- [ALOOD: Exploiting Language Representations for LiDAR-based Out-of-Distribution Object Detection](https://arxiv.org/abs/2603.08180)
- [The Struggle Between Continuation and Refusal: A Mechanistic Analysis of the Continuation-Triggered Jailbreak in LLMs](https://arxiv.org/abs/2603.08234)
- [FlowTouch: View-Invariant Visuo-Tactile Prediction](https://arxiv.org/abs/2603.08255)
- [Towards a more efficient bias detection in financial language models](https://arxiv.org/abs/2603.08267)
- [Graph-Instructed Neural Networks for parametric problems with varying boundary conditions](https://arxiv.org/abs/2603.08304)
- [Concept-Guided Fine-Tuning: Steering ViTs away from Spurious Correlations to Improve Robustness](https://arxiv.org/abs/2603.08309)
- [Sign Identifiability of Causal Effects in Stationary Stochastic Dynamical Systems](https://arxiv.org/abs/2603.08311)
- [Beyond Attention Heatmaps: How to Get Better Explanations for Multiple Instance Learning Models in Histopathology](https://arxiv.org/abs/2603.08328)
- [Electrocardiogram Classification with Transformers Using Koopman and Wavelet Features](https://arxiv.org/abs/2603.08339)
- [Leaderboard Incentives: Model Rankings under Strategic Post-Training](https://arxiv.org/abs/2603.08371)
- [Revealing Behavioral Plasticity in Large Language Models: A Token-Conditional Perspective](https://arxiv.org/abs/2603.08398)
- [IronEngine: Towards General AI Assistant](https://arxiv.org/abs/2603.08425)
- [A prospective clinical feasibility study of a conversational diagnostic AI in an ambulatory primary care clinic](https://arxiv.org/abs/2603.08448)
- [The Boiling Frog Threshold: Criticality and Blindness in World Model-Based Anomaly Detection Under Gradual Drift](https://arxiv.org/abs/2603.08455)
- [Adaptive Entropy-Driven Sensor Selection in a Camera-LiDAR Particle Filter for Single-Vessel Tracking](https://arxiv.org/abs/2603.08457)
- [Integrating Lagrangian Neural Networks into the Dyna Framework for Reinforcement Learning](https://arxiv.org/abs/2603.08468)
- [STRIDE: Structured Lagrangian and Stochastic Residual Dynamics via Flow Matching](https://arxiv.org/abs/2603.08478)
- [X-AVDT: Audio-Visual Cross-Attention for Robust Deepfake Detection](https://arxiv.org/abs/2603.08483)
- [Pareto-Optimal Anytime Algorithms via Bayesian Racing](https://arxiv.org/abs/2603.08493)
- [The Neural Compass: Probabilistic Relative Feature Fields for Robotic Search](https://arxiv.org/abs/2603.08544)
- [Interactive World Simulator for Robot Policy Training and Evaluation](https://arxiv.org/abs/2603.08546)
- [Trust via Reputation of Conviction](https://arxiv.org/abs/2603.08575)
- [PostTrainBench: Can LLM Agents Automate LLM Post-Training?](https://arxiv.org/abs/2603.08640)
- [Retrieval-Augmented Gaussian Avatars: Improving Expression Generalization](https://arxiv.org/abs/2603.08645)
- [Benchmarking Language Modeling for Lossless Compression of Full-Fidelity Audio](https://arxiv.org/abs/2603.08683)
- [Agentic Critical Training](https://arxiv.org/abs/2603.08706)
- [A White-Box SVM Framework and its Swarm-Based Optimization for Supervision of Toothed Milling Cutter through Characterization of Spindle Vibrations](https://arxiv.org/abs/2112.08421)
- [Automated Reinforcement Learning: An Overview](https://arxiv.org/abs/2201.05000)
- [Explainable classification of astronomical uncertain time series](https://arxiv.org/abs/2210.00869)
- [Remaining-data-free Machine Unlearning by Suppressing Sample Contribution](https://arxiv.org/abs/2402.15109)
- [Survey of Computerized Adaptive Testing: A Machine Learning Perspective](https://arxiv.org/abs/2404.00712)
- [LoRA-Ensemble: Efficient Uncertainty Modelling for Self-Attention Networks](https://arxiv.org/abs/2405.14438) **[ranked]**
- [Fast Explanations via Policy Gradient-Optimized Explainer](https://arxiv.org/abs/2405.18664)
- [From Model Explanation to Data Misinterpretation: A Cautionary Analysis of Post Hoc Explainers in Business Research](https://arxiv.org/abs/2408.16987)
- [Neural delay differential equations: learning non-Markovian closures for partially known dynamical systems](https://arxiv.org/abs/2410.02843)
- [Open-World Reinforcement Learning over Long Short-Term Imagination](https://arxiv.org/abs/2410.03618)
- [How Learning Dynamics Drive Adversarially Robust Generalization?](https://arxiv.org/abs/2410.07719)
- [Transformers as Implicit State Estimators: In-Context Learning in Dynamical Systems](https://arxiv.org/abs/2410.16546)
- [Puppet-CNN: Continuous Parameter Dynamics for Input-Adaptive Convolutional Networks](https://arxiv.org/abs/2411.12876)
- [Finite Sample Bounds for Non-Parametric Regression: Optimal Sample Efficiency and Space Complexity](https://arxiv.org/abs/2412.14744)
- [Efficient Semi-Supervised Adversarial Training via Latent Clustering-Based Data Reduction](https://arxiv.org/abs/2501.10466)
- [GRADIEND: Feature Learning within Neural Networks Exemplified through Biases](https://arxiv.org/abs/2502.01406)
- [An Efficient Local Search Approach for Polarized Community Discovery in Signed Networks](https://arxiv.org/abs/2502.02197)
- [Controllable Sequence Editing for Biological and Clinical Trajectories](https://arxiv.org/abs/2502.03569)
- [Mitigating Unintended Memorization with LoRA in Federated Learning for LLMs](https://arxiv.org/abs/2502.05087)
- [Language in the Flow of Time: Time-Series-Paired Texts Weaved into a Unified Temporal Narrative](https://arxiv.org/abs/2502.08942)
- [Go Beyond Your Means: Unlearning with Per-Sample Gradient Orthogonalization](https://arxiv.org/abs/2503.02312)
- [Characterizing Nonlinear Dynamics via Smooth Prototype Equivalences](https://arxiv.org/abs/2503.10336)
- [MUSS: Multilevel Subset Selection for Relevance and Diversity](https://arxiv.org/abs/2503.11126)
- [More Bang for the Buck: Process Reward Modeling with Entropy-Driven Uncertainty](https://arxiv.org/abs/2503.22233)
- [A Champion-level Vision-based Reinforcement Learning Agent for Competitive Racing in Gran Turismo 7](https://arxiv.org/abs/2504.09021)
- [Structural Inference: Interpreting Small Language Models with Susceptibilities](https://arxiv.org/abs/2504.18274)
- [StablePCA: Distributionally Robust Learning of Shared Representations from Multi-Source Data](https://arxiv.org/abs/2505.00940)
- [Distilled Circuits: A Mechanistic Study of Internal Restructuring in Knowledge Distillation](https://arxiv.org/abs/2505.10822)
- [Ready2Unlearn: A Learning-Time Approach for Preparing Models with Future Unlearning Readiness](https://arxiv.org/abs/2505.10845)
- [FreeKV: Boosting KV Cache Retrieval for Efficient LLM Inference](https://arxiv.org/abs/2505.13109)
- [The Cell Must Go On: Agar.io for Continual Reinforcement Learning](https://arxiv.org/abs/2505.18347)
- [X-MethaneWet: A Cross-scale Global Wetland Methane Emission Benchmark Dataset for Advancing Science Discovery with AI](https://arxiv.org/abs/2505.18355)
- [VISTA: Vision-Language Inference for Training-Free Stock Time-Series Analysis](https://arxiv.org/abs/2505.18570)
- [OCN: Effectively Utilizing Higher-Order Common Neighbors for Better Link Prediction](https://arxiv.org/abs/2505.19719)
- [LoFT: Low-Rank Adaptation That Behaves Like Full Fine-Tuning](https://arxiv.org/abs/2505.21289)
- [Rethinking Continual Learning with Progressive Neural Collapse](https://arxiv.org/abs/2505.24254)
- [Adaptive Correction for Ensuring Conservation Laws in Neural Operators](https://arxiv.org/abs/2505.24579)
- [Leveraging chaotic transients in the training of artificial neural networks](https://arxiv.org/abs/2506.08523)
- [Co-LoRA: Collaborative Model Personalization on Heterogeneous Multi-Modal Clients](https://arxiv.org/abs/2506.11024)
- [Efficient Algorithms for Logistic Contextual Slate Bandits with Bandit Feedback](https://arxiv.org/abs/2506.13163)
- [Sharpness-Aware Machine Unlearning](https://arxiv.org/abs/2506.13715)
- [Adaptive Batch-Wise Sample Scheduling for Direct Preference Optimization](https://arxiv.org/abs/2506.17252)
- [Adopting a human developmental visual diet yields robust, shape-based AI vision](https://arxiv.org/abs/2507.03168)
- [Noisy PDE Training Requires Bigger PINNs](https://arxiv.org/abs/2507.06967)
- [Flow Matching Meets Biology and Life Science: A Survey](https://arxiv.org/abs/2507.17731)
- [Weak-to-Strong Generalization with Failure Trajectories: A Tree-based Approach to Elicit Optimal Policy in Strong Models](https://arxiv.org/abs/2507.18858)
- [Exposing the Illusion of Fairness: Auditing Vulnerabilities to Distributional Manipulation Attacks](https://arxiv.org/abs/2507.20708)
- [Beyond Benchmarks: Dynamic, Automatic And Systematic Red-Teaming Agents For Trustworthy Medical Language Models](https://arxiv.org/abs/2508.00923)
- [CauKer: Classification Time Series Foundation Models Can Be Pretrained on Synthetic Data](https://arxiv.org/abs/2508.02879)
- [GraphProp: Training the Graph Foundation Models using Graph Properties](https://arxiv.org/abs/2508.04594)
- [Time-Scale Coupling Between States and Parameters in Recurrent Neural Networks](https://arxiv.org/abs/2508.12121)
- [Constraint Learning in Multi-Agent Dynamic Games from Demonstrations of Local Nash Interactions](https://arxiv.org/abs/2508.19945)
- [CbLDM: A Diffusion Model for recovering nanostructure from atomic pair distribution function](https://arxiv.org/abs/2509.01370)
- [Entropy-Driven Curriculum for Multi-Task Training in Human Mobility Prediction](https://arxiv.org/abs/2509.01613)
- [AEGIS: Authentic Edge Growth In Sparsity for Link Prediction in Edge-Sparse Bipartite Knowledge Graphs](https://arxiv.org/abs/2509.22017)
- [CLAD-Net: Continual Activity Recognition in Multi-Sensor Wearable Systems](https://arxiv.org/abs/2509.23077)
- [Generative Evolutionary Meta-Solver (GEMS): Scalable Surrogate-Free Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2509.23462)
- [FS-KAN: Permutation Equivariant Kolmogorov-Arnold Networks via Function Sharing](https://arxiv.org/abs/2509.24472)
- [Cold-Start Active Correlation Clustering](https://arxiv.org/abs/2509.25376)
- [Feedback Control for Small Budget Pacing](https://arxiv.org/abs/2509.25429)
- [Double projection for reconstructing dynamical systems: between stochastic and deterministic regimes](https://arxiv.org/abs/2510.01089)
- [Tree-based Dialogue Reinforced Policy Optimization for Red-Teaming Attacks](https://arxiv.org/abs/2510.02286)
- [The Ends Justify the Thoughts: RL-Induced Motivated Reasoning in LLM CoTs](https://arxiv.org/abs/2510.17057)
- [Explainable Heterogeneous Anomaly Detection in Financial Networks via Adaptive Expert Routing](https://arxiv.org/abs/2510.17088)
- [Reinforcing Numerical Reasoning in LLMs for Tabular Prediction via Structural Priors](https://arxiv.org/abs/2510.17385)
- [Robustness Verification of Graph Neural Networks Via Lightweight Satisfiability Testing](https://arxiv.org/abs/2510.18591)
- [A Unified Framework for Zero-Shot Reinforcement Learning](https://arxiv.org/abs/2510.20542)
- [SwiftTS: A Swift Selection Framework for Time Series Pre-trained Models via Multi-task Meta-Learning](https://arxiv.org/abs/2510.23051)
- [Continual Low-Rank Adapters for LLM-based Generative Recommender Systems](https://arxiv.org/abs/2510.25093)
- [Balancing Interpretability and Performance in Motor Imagery EEG Classification: A Comparative Study of ANFIS-FBCSP-PSO and EEGNet](https://arxiv.org/abs/2511.00369)
- [Towards Efficient Federated Learning of Networked Mixture-of-Experts for Mobile Edge Computing](https://arxiv.org/abs/2511.01743)
- [FATE: A Formal Benchmark Series for Frontier Algebra of Multiple Difficulty Levels](https://arxiv.org/abs/2511.02872)
- [Distributionally Robust Self Paced Curriculum Reinforcement Learning](https://arxiv.org/abs/2511.05694)
- [Adaptive Multi-view Graph Contrastive Learning via Fractional-order Neural Diffusion Networks](https://arxiv.org/abs/2511.06216)
- [Improving Conditional VAE with Non-Volume Preserving transformations](https://arxiv.org/abs/2511.08946)
- [Tight Robustness Certification Through the Convex Hull of $\ell_0$ Attacks](https://arxiv.org/abs/2511.10576)
- [Angular Gradient Sign Method: Uncovering Vulnerabilities in Hyperbolic Networks](https://arxiv.org/abs/2511.12985)
- [Towards Realistic Guarantees: A Probabilistic Certificate for SmoothLLM](https://arxiv.org/abs/2511.18721)
- [Automating Deception: Scalable Multi-Turn LLM Jailbreaks](https://arxiv.org/abs/2511.19517)
- [CRAwDAD: Causal Reasoning Augmentation with Dual-Agent Debate](https://arxiv.org/abs/2511.22854)
- [AltNet: Addressing the Plasticity-Stability Dilemma in Reinforcement Learning](https://arxiv.org/abs/2512.01034)
- [MSPT: Efficient Large-Scale Physical Modeling via Parallelized Multi-Scale Attention](https://arxiv.org/abs/2512.01738)
- [Dual Randomized Smoothing: Beyond Global Noise Variance](https://arxiv.org/abs/2512.01782)
- [Dual-Robust Cross-Domain Offline Reinforcement Learning Against Dynamics Shifts](https://arxiv.org/abs/2512.02486)
- [Evolving Diffusion and Flow Matching Policies for Online Reinforcement Learning](https://arxiv.org/abs/2512.02581)
- [SALVE: Sparse Autoencoder-Latent Vector Editing for Mechanistic Control of Neural Networks](https://arxiv.org/abs/2512.15938)
- [Meta-RL Induces Exploration in Language Agents](https://arxiv.org/abs/2512.16848)
- [Concurrent training methods for Kolmogorov-Arnold networks: Disjoint datasets and FPGA implementation](https://arxiv.org/abs/2512.18921)
- [Latent Sculpting for Zero-Shot Generalization: A Manifold Learning Approach to Out-of-Distribution Anomaly Detection](https://arxiv.org/abs/2512.22179)
- [Network Traffic Analysis with Process Mining: The UPSIDE Case Study](https://arxiv.org/abs/2512.23718)
- [DevBench: A Realistic, Developer-Informed Benchmark for Code Generation Models](https://arxiv.org/abs/2601.11895)
- [ELSA: Efficient LLM-Centric Split Aggregation for Privacy-Aware Hierarchical Federated Learning over the Network Edge](https://arxiv.org/abs/2601.13824)
- [Continuous-Flow Data-Rate-Aware CNN Inference on FPGA](https://arxiv.org/abs/2601.19940)
- [MeanCache: From Instantaneous to Average Velocity for Accelerating Flow Matching Inference](https://arxiv.org/abs/2601.19961)
- [PASS: Certified Subset Repair for Classical and Quantum Pairwise Constrained Clustering](https://arxiv.org/abs/2601.20157)
- [Model-Free Neural State Estimation in Nonlinear Dynamical Systems: Comparing Neural and Classical Filters](https://arxiv.org/abs/2601.21266)
- [TimeSliver : Symbolic-Linear Decomposition for Explainable Time Series Classification](https://arxiv.org/abs/2601.21289)
- [Transferable Graph Condensation from the Causal Perspective](https://arxiv.org/abs/2601.21309)
- [FlowSymm: Physics Aware, Symmetry Preserving Graph Attention for Network Flow Completion](https://arxiv.org/abs/2601.22317)
- [Mem-T: Densifying Rewards for Long-Horizon Memory Agents](https://arxiv.org/abs/2601.23014)
- [In-Run Data Shapley for Adam Optimizer](https://arxiv.org/abs/2602.00329)
- [Thickening-to-Thinning: Reward Shaping via Human-Inspired Learning Dynamics for LLM Reasoning](https://arxiv.org/abs/2602.04265)
- [Hinge Regression Tree: A Newton Method for Oblique Regression Tree Splitting](https://arxiv.org/abs/2602.05371)
- [Rewards as Labels: Revisiting RLVR from a Classification Perspective](https://arxiv.org/abs/2602.05630)
- [Radial M\"untz-Sz\'asz Networks: Neural Architectures with Learnable Power Bases for Multidimensional Singularities](https://arxiv.org/abs/2602.08419)
- [SDFed: Bridging Local Global Discrepancy via Subspace Refinement and Divergence Control in Federated Prompt Learning](https://arxiv.org/abs/2602.08590)
- [Diffusion-Guided Pretraining for Brain Graph Foundation Models](https://arxiv.org/abs/2602.09437)
- [Learning Page Order in Shuffled WOO Releases](https://arxiv.org/abs/2602.11040)
- [TrasMuon: Trust-Region Adaptive Scaling for Orthogonalized Momentum Optimizers](https://arxiv.org/abs/2602.13498)
- [Benchmark Leakage Trap: Can We Trust LLM-based Recommendation?](https://arxiv.org/abs/2602.13626)
- [Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation](https://arxiv.org/abs/2602.13810)
- [Pawsterior: Variational Flow Matching for Structured Simulation-Based Inference](https://arxiv.org/abs/2602.13813)
- [Why Code, Why Now: Learnability, Computability, and the Real Limits of Machine Learning](https://arxiv.org/abs/2602.13934)
- [Accelerated Predictive Coding Networks via Direct Kolen-Pollack Feedback Alignment](https://arxiv.org/abs/2602.15571)
- [On the Power of Source Screening for Learning Shared Feature Extractors](https://arxiv.org/abs/2602.16125)
- [ModalImmune: Immunity Driven Unlearning via Self Destructive Training](https://arxiv.org/abs/2602.16197)
- [Whole-Brain Connectomic Graph Model Enables Whole-Body Locomotion Control in Fruit Fly](https://arxiv.org/abs/2602.17997)
- [RAmmStein: Regime Adaptation in Mean-reverting Markets with Stein Thresholds -- Optimal Impulse Control in Concentrated AMMs](https://arxiv.org/abs/2602.19419)
- [Benchmarking GNN Models on Molecular Regression Tasks with CKA-Based Representation Analysis](https://arxiv.org/abs/2602.20573)
- [Autoregressive Visual Decoding from EEG Signals](https://arxiv.org/abs/2602.22555)
- [CeRA: Breaking the Linear Ceiling of Low-Rank Adaptation via Manifold Expansion](https://arxiv.org/abs/2602.22911)
- [Attn-QAT: 4-Bit Attention With Quantization-Aware Training](https://arxiv.org/abs/2603.00040)
- [Personalized Multi-Agent Average Reward TD-Learning via Joint Linear Approximation](https://arxiv.org/abs/2603.02426)
- [Embedding interpretable $\ell_1$-regression into neural networks for uncovering temporal structure in cell imaging](https://arxiv.org/abs/2603.02899)
- [CGL: Advancing Continual GUI Learning via Reinforcement Fine-Tuning](https://arxiv.org/abs/2603.02951)
- [Why Adam Can Beat SGD: Second-Moment Normalization Yields Sharper Tails](https://arxiv.org/abs/2603.03099)
- [Information Routing in Atomistic Foundation Models: How Task Alignment and Equivariance Shape Linear Disentanglement](https://arxiv.org/abs/2603.03155)
- [Half the Nonlinearity Is Wasted: Measuring and Reallocating the Transformer's MLP Budget](https://arxiv.org/abs/2603.03459)
- [Test-Time Meta-Adaptation with Self-Synthesis](https://arxiv.org/abs/2603.03524)
- [Neuro-Symbolic Financial Reasoning via Deterministic Fact Ledgers and Adversarial Low-Latency Hallucination Detector](https://arxiv.org/abs/2603.04663)
- [GALACTIC: Global and Local Agnostic Counterfactuals for Time-series Clustering](https://arxiv.org/abs/2603.05318)
- [On-Policy Self-Distillation for Reasoning Compression](https://arxiv.org/abs/2603.05433)
- [When AI Levels the Playing Field: Skill Homogenization, Asset Concentration, and Two Regimes of Inequality](https://arxiv.org/abs/2603.05565)
- [Bridging Domains through Subspace-Aware Model Merging](https://arxiv.org/abs/2603.05768)
- [Empirical Asset Pricing via Ensemble Gaussian Process Regression](https://arxiv.org/abs/2212.01048)
- [Simulating Non-Markovian Open Quantum Dynamics with Neural Quantum States](https://arxiv.org/abs/2404.11093)
- [Exploring Diffusion Models' Corruption Stage in Few-Shot Fine-tuning and Mitigating with Bayesian Neural Networks](https://arxiv.org/abs/2405.19931)
- [Estimating Treatment Effects under Algorithmic Interference: A Structured Neural Networks Approach](https://arxiv.org/abs/2406.14380)
- [Reconsidering the energy efficiency of spiking neural networks](https://arxiv.org/abs/2409.08290)
- [Input-to-State Stable Coupled Oscillator Networks for Closed-form Model-based Control in Latent Space](https://arxiv.org/abs/2409.08439)
- [xTED: Cross-Domain Adaptation via Diffusion-Based Trajectory Editing](https://arxiv.org/abs/2409.08687)
- [Landscape of Policy Optimization for Finite Horizon MDPs with General State and Action](https://arxiv.org/abs/2409.17138)
- [Autoassociative Learning of Structural Representations for Modeling and Classification in Medical Imaging](https://arxiv.org/abs/2411.12070)
- [Input-Adaptive Generative Dynamics in Diffusion Models](https://arxiv.org/abs/2411.15199)
- [Exploring Embedding Priors in Prompt-Tuning for Improved Interpretability and Control](https://arxiv.org/abs/2412.18582)
- [From Pixels to Predicates: Learning Symbolic World Models via Pretrained Vision-Language Models](https://arxiv.org/abs/2501.00296)
- [Strengthening Generative Robot Policies through Predictive World Modeling](https://arxiv.org/abs/2502.00622)
- [General Coded Computing in a Probabilistic Straggler Regime](https://arxiv.org/abs/2502.00645)
- [Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis](https://arxiv.org/abs/2502.01853)
- [LaVCa: LLM-assisted Visual Cortex Captioning](https://arxiv.org/abs/2502.13606)
- [Unveiling Downstream Performance Scaling of LLMs: A Clustering-Based Perspective](https://arxiv.org/abs/2502.17262)
- [IMPACT: Intelligent Motion Planning with Acceptable Contact Trajectories via Vision-Language Models](https://arxiv.org/abs/2503.10110)
- [Estimating Item Difficulty Using Large Language Models and Tree-Based Machine Learning Algorithms](https://arxiv.org/abs/2504.08804)
- [From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review](https://arxiv.org/abs/2504.19678)
- [Healthy LLMs? Benchmarking LLM Knowledge of UK Government Public Health Information](https://arxiv.org/abs/2505.06046)
- [EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video](https://arxiv.org/abs/2505.11709)
- [Vid2World: Crafting Video Diffusion Models to Interactive World Models](https://arxiv.org/abs/2505.14357)
- [MAS-ZERO: Designing Multi-Agent Systems with Zero Supervision](https://arxiv.org/abs/2505.14996)
- [HDLxGraph: Bridging Large Language Models and HDL Repositories via HDL Graph Databases](https://arxiv.org/abs/2505.15701)
- [WikiDBGraph: A Data Management Benchmark Suite for Collaborative Learning over Database Silos](https://arxiv.org/abs/2505.16635)
- [Maximum Principle of Optimal Probability Density Control](https://arxiv.org/abs/2505.18362)
- [Stronger Enforcement of Instruction Hierarchy via Augmented Intermediate Representations](https://arxiv.org/abs/2505.18907)
- [ViTaPEs: Visuotactile Position Encodings for Cross-Modal Alignment in Multimodal Transformers](https://arxiv.org/abs/2505.20032)
- [ActivePusher: Active Learning and Planning with Residual Physics for Nonprehensile Manipulation](https://arxiv.org/abs/2506.04646)
- [MMTU: A Massive Multi-Task Table Understanding and Reasoning Benchmark](https://arxiv.org/abs/2506.05587)
- [EROICA: Online Performance Troubleshooting for Large-scale Model Training](https://arxiv.org/abs/2506.08528)
- [BemaGANv2: Discriminator Combination Strategies for GAN-based Vocoders in Long-Term Audio Generation](https://arxiv.org/abs/2506.09487)
- [From Semantic To Instance: A Semi-Self-Supervised Learning Approach](https://arxiv.org/abs/2506.16563)
- [DemoDiffusion: One-Shot Human Imitation using pre-trained Diffusion Policy](https://arxiv.org/abs/2506.20668)
- [Towards Practical Benchmarking of Data Cleaning Techniques: On Generating Authentic Errors via Large Language Models](https://arxiv.org/abs/2507.10934)
- [Let's Think in Two Steps: Mitigating Agreement Bias in MLLMs with Self-Grounded Verification](https://arxiv.org/abs/2507.11662)
- [ECHO: Frequency-aware Hierarchical Encoding for Variable-length Signals](https://arxiv.org/abs/2508.14689)
- [Behavioral Inference at Scale: The Fundamental Asymmetry Between Motivations and Belief Systems](https://arxiv.org/abs/2509.05624)
- [Synthetic Homes: An Accessible Multimodal Pipeline for Producing Residential Building Data with Generative AI](https://arxiv.org/abs/2509.09794)
- [Physics-Aware Neural Operators for Direct Inversion in 3D Photoacoustic Tomography](https://arxiv.org/abs/2509.09894)
- [MICA: Multi-Agent Industrial Coordination Assistant](https://arxiv.org/abs/2509.15237)
- [ORIC: Benchmarking Object Recognition under Contextual Incongruity in Large Vision-Language Models](https://arxiv.org/abs/2509.15695)
- [ORN-CBF: Learning Observation-conditioned Residual Neural Control Barrier Functions via Hypernetworks](https://arxiv.org/abs/2509.16614)
- [Linear probes rely on textual evidence: Results from leakage mitigation studies in language models](https://arxiv.org/abs/2509.21344)
- [Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents](https://arxiv.org/abs/2509.26354)
- [Privately Estimating Black-Box Statistics](https://arxiv.org/abs/2510.00322)
- [Stochastic Self-Organization in Multi-Agent Systems](https://arxiv.org/abs/2510.00685)
- [CroSTAta: Cross-State Transition Attention Transformer for Robotic Manipulation](https://arxiv.org/abs/2510.00726)
- [Pretraining in Actor-Critic Reinforcement Learning for Robot Locomotion](https://arxiv.org/abs/2510.12363)
- [ARM-FM: Automated Reward Machines via Foundation Models for Compositional Reinforcement Learning](https://arxiv.org/abs/2510.14176)
- [Jr. AI Scientist and Its Risk Report: Autonomous Scientific Exploration from a Baseline Paper](https://arxiv.org/abs/2511.04583)
- [Crowdsourcing the Frontier: Advancing Hybrid Physics-ML Climate Simulation via a $50,000 Kaggle Competition](https://arxiv.org/abs/2511.20963)
- [ForamDeepSlice: A High-Accuracy Deep Learning Framework for Foraminifera Species Classification from 2D Micro-CT Slices](https://arxiv.org/abs/2512.00912)
- [Two-Step Data Augmentation for Masked Face Detection and Recognition: Turning Fake Masks to Real](https://arxiv.org/abs/2512.15774)
- [ReDepth Anything: Test-Time Depth Refinement via Self-Supervised Re-lighting](https://arxiv.org/abs/2512.17908)
- [Certifying the Right to Be Forgotten: Primal-Dual Optimization for Sample and Label Unlearning in Vertical Federated Learning](https://arxiv.org/abs/2512.23171)
- [Group Cross-Correlations with Faintly Constrained Filters](https://arxiv.org/abs/2601.00045)
- [A Component-Based Survey of Interactions between Large Language Models and Multi-Armed Bandits](https://arxiv.org/abs/2601.12945)
- [Bitcoin Price Prediction using Machine Learning and Combinatorial Fusion Analysis](https://arxiv.org/abs/2602.00037)
- [Do Schwartz Higher-Order Values Help Sentence-Level Human Value Detection? A Study of Hierarchical Gating and Calibration](https://arxiv.org/abs/2602.00913)
- [LatentMem: Customizing Latent Memory for Multi-Agent Systems](https://arxiv.org/abs/2602.03036)
- [Inference-Time Backdoors via Hidden Instructions in LLM Chat Templates](https://arxiv.org/abs/2602.04653)
- [Retrieval Pivot Attacks in Hybrid RAG: Measuring and Mitigating Amplified Leakage from Vector Seeds to Graph Expansion](https://arxiv.org/abs/2602.08668)
- [Discovering Semantic Latent Structures in Psychological Scales: A Response-Free Pathway to Efficient Simplification](https://arxiv.org/abs/2602.12575)
- [LongAudio-RAG: Event-Grounded Question Answering over Multi-Hour Long Audio](https://arxiv.org/abs/2602.14612)
- [Emotion Collider: Dual Hyperbolic Mirror Manifolds for Sentiment Recovery via Anti Emotion Reflection](https://arxiv.org/abs/2602.16161)
- [Conformal Tradeoffs: Guarantees Beyond Coverage](https://arxiv.org/abs/2602.18045)
- [Latent Equivariant Operators for Robust Object Recognition: Promise and Challenges](https://arxiv.org/abs/2602.18406)
- [Characterizing MARL for Energy Control: A Multi-KPI Benchmark on the CityLearn Environment](https://arxiv.org/abs/2602.19223)
- [MrBERT: Modern Multilingual Encoders via Vocabulary, Domain, and Dimensional Adaptation](https://arxiv.org/abs/2602.21379)
- [Scaling Search Relevance: Augmenting App Store Ranking with LLM-Generated Judgments](https://arxiv.org/abs/2602.23234)
- [Lap2: Revisiting Laplace DP-SGD for High Dimensions via Majorization Theory](https://arxiv.org/abs/2602.23516)
- [How Well Do Multimodal Models Reason on ECG Signals?](https://arxiv.org/abs/2603.00312)
- [Opponent State Inference Under Partial Observability: An HMM-POMDP Framework for 2026 Formula 1 Energy Strategy](https://arxiv.org/abs/2603.01290)
- [TCG CREST System Description for the DISPLACE-M Challenge](https://arxiv.org/abs/2603.02030)
- [A Detection-Gated Pipeline for Robust Glottal Area Waveform Extraction and Clinical Pathology Assessment](https://arxiv.org/abs/2603.02087)
- [Interpretable Motion-Attentive Maps: Spatio-Temporally Localizing Concepts in Video Diffusion Transformers](https://arxiv.org/abs/2603.02919)
- [MEM: Multi-Scale Embodied Memory for Vision Language Action Models](https://arxiv.org/abs/2603.03596)
- [ZipMap: Linear-Time Stateful 3D Reconstruction via Test-Time Training](https://arxiv.org/abs/2603.04385)
- [RoboLayout: Differentiable 3D Scene Generation for Embodied Agents](https://arxiv.org/abs/2603.05522)
- [SCOPE: Scene-Contextualized Incremental Few-Shot 3D Segmentation](https://arxiv.org/abs/2603.06572)
- [Real-Time AI Service Economy: A Framework for Agentic Computing Across the Continuum](https://arxiv.org/abs/2603.05614)
- [Reasoning Models Struggle to Control their Chains of Thought](https://arxiv.org/abs/2603.05706)
- [Evolving Medical Imaging Agents via Experience-driven Self-skill Discovery](https://arxiv.org/abs/2603.05860)
- [The World Won't Stay Still: Programmable Evolution for Agent Benchmarks](https://arxiv.org/abs/2603.05910)
- [DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality](https://arxiv.org/abs/2603.05912)
- [An Interactive Multi-Agent System for Evaluation of New Product Concepts](https://arxiv.org/abs/2603.05980)
- [Agentic LLM Planning via Step-Wise PDDL Simulation: An Empirical Characterisation](https://arxiv.org/abs/2603.06064)
- [Aggregative Semantics for Quantitative Bipolar Argumentation Frameworks](https://arxiv.org/abs/2603.06067)
- [Offline Materials Optimization with CliqueFlowmer](https://arxiv.org/abs/2603.06082)
- [Conversational Demand Response: Bidirectional Aggregator-Prosumer Coordination through Agentic AI](https://arxiv.org/abs/2603.06217)
- [Artificial Intelligence for Climate Adaptation: Reinforcement Learning for Climate Change-Resilient Transport](https://arxiv.org/abs/2603.06278)
- [The EpisTwin: A Knowledge Graph-Grounded Neuro-Symbolic Architecture for Personal AI](https://arxiv.org/abs/2603.06290)
- [SAHOO: Safeguarded Alignment for High-Order Optimization Objectives in Recursive Self-Improvement](https://arxiv.org/abs/2603.06333)
- [Talk Freely, Execute Strictly: Schema-Gated Agentic AI for Flexible and Reproducible Scientific Workflows](https://arxiv.org/abs/2603.06394)
- [Boosting deep Reinforcement Learning using pretraining with Logical Options](https://arxiv.org/abs/2603.06565)
- [Can LLM Aid in Solving Constraints with Inductive Definitions?](https://arxiv.org/abs/2603.03668)
- [Exploring Human-in-the-Loop Themes in AI Application Development: An Empirical Thematic Analysis](https://arxiv.org/abs/2603.05510)
- [An Embodied Companion for Visual Storytelling](https://arxiv.org/abs/2603.05511)
- [From Toil to Thought: Designing for Strategic Exploration and Responsible AI in Systematic Literature Reviews](https://arxiv.org/abs/2603.05514)
- [Traversal-as-Policy: Log-Distilled Gated Behavior Trees as Externalized, Verifiable Policies for Safe, Robust, and Efficient Agents](https://arxiv.org/abs/2603.05517)
- [Molecular Representations for AI in Chemistry and Materials Science: An NLP Perspective](https://arxiv.org/abs/2603.05525)
- [Omni-C: Compressing Heterogeneous Modalities into a Single Dense Encoder](https://arxiv.org/abs/2603.05528)
- [Towards Neural Graph Data Management](https://arxiv.org/abs/2603.05529)
- [On the Reliability of AI Methods in Drug Discovery: Evaluation of Boltz-2 for Structure and Binding Affinity Prediction](https://arxiv.org/abs/2603.05532)
- [JAWS: Enhancing Long-term Rollout of Neural Operators via Spatially-Adaptive Jacobian Regularization](https://arxiv.org/abs/2603.05538)
- [VDCook:DIY video data cook your MLLMs](https://arxiv.org/abs/2603.05539)
- [Human-Data Interaction, Exploration, and Visualization in the AI Era: Challenges and Opportunities](https://arxiv.org/abs/2603.05542)
- [EigenData: A Self-Evolving Multi-Agent Platform for Function-Calling Data Synthesis, Auditing, and Repair](https://arxiv.org/abs/2603.05553)
- [Towards Efficient and Stable Ocean State Forecasting: A Continuous-Time Koopman Approach](https://arxiv.org/abs/2603.05560)
- [Model Change for Description Logic Concepts](https://arxiv.org/abs/2603.05562)
- [CBR-to-SQL: Rethinking Retrieval-based Text-to-SQL using Case-based Reasoning in the Healthcare Domain](https://arxiv.org/abs/2603.05569)
- [PRISM: Personalized Refinement of Imitation Skills for Manipulation via Human Instructions](https://arxiv.org/abs/2603.05574)
- [Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent](https://arxiv.org/abs/2603.05578)
- [Spatiotemporal Heterogeneity of AI-Driven Traffic Flow Patterns and Land Use Interaction: A GeoAI-Based Analysis of Multimodal Urban Mobility](https://arxiv.org/abs/2603.05581)
- [On the Value of Tokeniser Pretraining in Physics Foundation Models](https://arxiv.org/abs/2603.05598)
- [DreamCAD: Scaling Multi-modal CAD Generation using Differentiable Parametric Surfaces](https://arxiv.org/abs/2603.05607)
- [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621)
- [Adversarial Batch Representation Augmentation for Batch Correction in High-Content Cellular Screening](https://arxiv.org/abs/2603.05622)
- [Post Fusion Bird's Eye View Feature Stabilization for Robust Multimodal 3D Detection](https://arxiv.org/abs/2603.05623)
- [Relational Semantic Reasoning on 3D Scene Graphs for Open World Interactive Object Search](https://arxiv.org/abs/2603.05642)
- [The Fragility Of Moral Judgment In Large Language Models](https://arxiv.org/abs/2603.05651)
- [The DSA's Blind Spot: Algorithmic Audit of Advertising and Minor Profiling on TikTok](https://arxiv.org/abs/2603.05653)
- [When Rubrics Fail: Error Enumeration as Reward in Reference-Free RL Post-Training for Virtual Try-On](https://arxiv.org/abs/2603.05659)
- [SecureRAG-RTL: A Retrieval-Augmented, Multi-Agent, Zero-Shot LLM-Driven Framework for Hardware Vulnerability Detection](https://arxiv.org/abs/2603.05689)
- [Longitudinal Lesion Inpainting in Brain MRI via 3D Region Aware Diffusion](https://arxiv.org/abs/2603.05693)
- [Autonomous Algorithm Discovery for Ptychography via Evolutionary LLM Reasoning](https://arxiv.org/abs/2603.05696)
- [The Rise of AI in Weather and Climate Information and its Impact on Global Inequality](https://arxiv.org/abs/2603.05710)
- [Cultural Perspectives and Expectations for Generative AI: A Global Survey Approach](https://arxiv.org/abs/2603.05723)
- [LTLGuard: Formalizing LTL Specifications with Compact Language Models and Lightweight Symbolic Reasoning](https://arxiv.org/abs/2603.05728)
- [Revisiting the (Sub)Optimality of Best-of-N for Inference-Time Alignment](https://arxiv.org/abs/2603.05739)
- [TML-Bench: Benchmark for Data Science Agents on Tabular ML Tasks](https://arxiv.org/abs/2603.05764)
- [Depth Charge: Jailbreak Large Language Models from Deep Safety Attention Heads](https://arxiv.org/abs/2603.05772)
- [Knowing without Acting: The Disentangled Geometry of Safety Mechanisms in Large Language Models](https://arxiv.org/abs/2603.05773)
- [PVminerLLM: Structured Extraction of Patient Voice from Patient-Generated Text using Large Language Models](https://arxiv.org/abs/2603.05776)
- [Balancing Domestic and Global Perspectives: Evaluating Dual-Calibration and LLM-Generated Nudges for Diverse News Recommendation](https://arxiv.org/abs/2603.05780)
- [Visual Words Meet BM25: Sparse Auto-Encoder Visual Word Scoring for Image Retrieval](https://arxiv.org/abs/2603.05781)
- [Proof-of-Guardrail in AI Agents and What (Not) to Trust from It](https://arxiv.org/abs/2603.05786)
- [StreamWise: Serving Multi-Modal Generation in Real-Time at Scale](https://arxiv.org/abs/2603.05800)
- [Ambiguity Collapse by LLMs: A Taxonomy of Epistemic Risks](https://arxiv.org/abs/2603.05801)
- [Margin and Consistency Supervision for Calibrated and Robust Vision Models](https://arxiv.org/abs/2603.05812)
- [Lexara: A User-Centered Toolkit for Evaluating Large Language Models for Conversational Visual Analytics](https://arxiv.org/abs/2603.05832)
- [Evaluating LLM Alignment With Human Trust Models](https://arxiv.org/abs/2603.05839)
- [Remote Sensing Image Classification Using Deep Ensemble Learning](https://arxiv.org/abs/2603.05844)
- [Computational Pathology in the Era of Emerging Foundation and Agentic AI -- International Expert Perspectives on Clinical Integration and Translational Readiness](https://arxiv.org/abs/2603.05884)
- [Reconstruct! Don't Encode: Self-Supervised Representation Reconstruction Loss for High-Intelligibility and Low-Latency Streaming Neural Audio Codec](https://arxiv.org/abs/2603.05887)
- [Lost in Stories: Consistency Bugs in Long Story Generation by LLMs](https://arxiv.org/abs/2603.05890)
- [Reference-guided Policy Optimization for Molecular Optimization via LLM Reasoning](https://arxiv.org/abs/2603.05900)
- [LUMINA: LLM-Guided GPU Architecture Exploration via Bottleneck Analysis](https://arxiv.org/abs/2603.05904)
- [CORE-Seg: Reasoning-Driven Segmentation for Complex Lesions via Reinforcement Learning](https://arxiv.org/abs/2603.05911)
- [Stock Market Prediction Using Node Transformer Architecture Integrated with BERT Sentiment Analysis](https://arxiv.org/abs/2603.05917)
- [BlackMirror: Black-Box Backdoor Detection for Text-to-Image Models via Instruction-Response Deviation](https://arxiv.org/abs/2603.05921)
- [RAC: Rectified Flow Auto Coder](https://arxiv.org/abs/2603.05925)
- [Addressing the Ecological Fallacy in Larger LMs with Human Context](https://arxiv.org/abs/2603.05928)
- [Facial Expression Recognition Using Residual Masking Network](https://arxiv.org/abs/2603.05937)
- [XAI for Coding Agent Failures: Transforming Raw Execution Traces into Actionable Insights](https://arxiv.org/abs/2603.05941)
- [Energy-Driven Adaptive Visual Token Pruning for Efficient Vision-Language Models](https://arxiv.org/abs/2603.05950)
- [Who We Are, Where We Are: Mental Health at the Intersection of Person, Situation, and Large Language Models](https://arxiv.org/abs/2603.05953)
- [Domain-Adaptive Model Merging across Disconnected Modes](https://arxiv.org/abs/2603.05957)
- [Skeleton-to-Image Encoding: Enabling Skeleton Representation Learning via Vision-Pretrained Models](https://arxiv.org/abs/2603.05963)
- [Imagine How To Change: Explicit Procedure Modeling for Change Captioning](https://arxiv.org/abs/2603.05969)
- [Technical Report: Automated Optical Inspection of Surgical Instruments](https://arxiv.org/abs/2603.05987)
- [TADPO: Reinforcement Learning Goes Off-road](https://arxiv.org/abs/2603.05995)
- [MM-ISTS: Cooperating Irregularly Sampled Time Series Forecasting with Multimodal Vision-Text LLMs](https://arxiv.org/abs/2603.05997)
- [Restoring Linguistic Grounding in VLA Models via Train-Free Attention Recalibration](https://arxiv.org/abs/2603.06001)
- [Demystifying KAN for Vision Tasks: The RepKAN Approach](https://arxiv.org/abs/2603.06002)
- [MASFactory: A Graph-centric Framework for Orchestrating LLM-Based Multi-Agent Systems with Vibe Graphing](https://arxiv.org/abs/2603.06007)
- [Sensitivity-Aware Retrieval-Augmented Intent Clarification](https://arxiv.org/abs/2603.06025)
- [Probing Visual Concepts in Lightweight Vision-Language Models for Automated Driving](https://arxiv.org/abs/2603.06054)
- [TempoSyncDiff: Distilled Temporally-Consistent Diffusion for Low-Latency Audio-Driven Talking Head Generation](https://arxiv.org/abs/2603.06057)
- [Evaluating Austrian A-Level German Essays with Large Language Models for Automated Essay Scoring](https://arxiv.org/abs/2603.06066)
- [Text-Driven Emotionally Continuous Talking Face Generation](https://arxiv.org/abs/2603.06071)
- [Lifelong Embodied Navigation Learning](https://arxiv.org/abs/2603.06073)
- [StreamVoiceAnon+: Emotion-Preserving Streaming Speaker Anonymization via Frame-Level Acoustic Distillation](https://arxiv.org/abs/2603.06079)
- [Experiences Build Characters: The Linguistic Origins and Functional Impact of LLM Personality](https://arxiv.org/abs/2603.06088)
- [Making Implicit Premises Explicit in Logical Understanding of Enthymemes](https://arxiv.org/abs/2603.06114)
- [A Hazard-Informed Data Pipeline for Robotics Physical Safety](https://arxiv.org/abs/2603.06130)
- [A Causal Graph Approach to Oppositional Narrative Analysis](https://arxiv.org/abs/2603.06135)
- [Partial Policy Gradients for RL in LLMs](https://arxiv.org/abs/2603.06138)
- [Place-it-R1: Unlocking Environment-aware Reasoning Potential of MLLM for Video Object Insertion](https://arxiv.org/abs/2603.06140)
- [Predictive Coding Graphs are a Superset of Feedforward Neural Networks](https://arxiv.org/abs/2603.06142)
- [VLM-RobustBench: A Comprehensive Benchmark for Robustness of Vision-Language Models](https://arxiv.org/abs/2603.06148)
- [Ensemble Graph Neural Networks for Probabilistic Sea Surface Temperature Forecasting via Input Perturbations](https://arxiv.org/abs/2603.06153)
- [Do Compact SSL Backbones Matter for Audio Deepfake Detection? A Controlled Study with RAPTOR](https://arxiv.org/abs/2603.06164)
- [Reflective Flow Sampling Enhancement](https://arxiv.org/abs/2603.06165)
- [Contrastive-to-Self-Supervised: A Two-Stage Framework for Script Similarity Learning](https://arxiv.org/abs/2603.06180)
- [CRIMSON: A Clinically-Grounded LLM-Based Metric for Generative Radiology Report Evaluation](https://arxiv.org/abs/2603.06183)
- [Whisper-CD: Accurate Long-Form Speech Recognition using Multi-Negative Contrastive Decoding](https://arxiv.org/abs/2603.06193)
- [MAPO: Mixed Advantage Policy Optimization for Long-Horizon Multi-Turn Dialogue](https://arxiv.org/abs/2603.06194)
- [FlashPrefill: Instantaneous Pattern Discovery and Thresholding for Ultra-Fast Long-Context Prefilling](https://arxiv.org/abs/2603.06199)
- [Cut to the Chase: Training-free Multimodal Summarization via Chain-of-Events](https://arxiv.org/abs/2603.06213)
- [TaPD: Temporal-adaptive Progressive Distillation for Observation-Adaptive Trajectory Forecasting in Autonomous Driving](https://arxiv.org/abs/2603.06231)
- [GazeMoE: Perception of Gaze Target with Mixture-of-Experts](https://arxiv.org/abs/2603.06256)
- [Learning to Solve Orienteering Problem with Time Windows and Variable Profits](https://arxiv.org/abs/2603.06260)
- [HiPP-Prune: Hierarchical Preference-Conditioned Structured Pruning for Vision-Language Models](https://arxiv.org/abs/2603.06270)
- [Agentic retrieval-augmented reasoning reshapes collective reliability under model variability in radiology question answering](https://arxiv.org/abs/2603.06271)
- [Looking Through Glass Box](https://arxiv.org/abs/2603.06272)
- [Stem: Rethinking Causal Information Flow in Sparse Attention](https://arxiv.org/abs/2603.06274)
- [Learning Where the Physics Is: Probabilistic Adaptive Sampling for Stiff PDEs](https://arxiv.org/abs/2603.06287)
- [DEX-AR: A Dynamic Explainability Method for Autoregressive Vision-Language Models](https://arxiv.org/abs/2603.06302)
- [From Entropy to Calibrated Uncertainty: Training Language Models to Reason About Uncertainty](https://arxiv.org/abs/2603.06317)
- [Structured Exploration vs. Generative Flexibility: A Field Study Comparing Bandit and LLM Architectures for Personalised Health Behaviour Interventions](https://arxiv.org/abs/2603.06330)
- [AI End-to-End Radiation Treatment Planning Under One Second](https://arxiv.org/abs/2603.06338)
- [K-MaT: Knowledge-Anchored Manifold Transport for Cross-Modal Prompt Learning in Medical Imaging](https://arxiv.org/abs/2603.06340)
- [MoEless: Efficient MoE LLM Serving via Serverless Computing](https://arxiv.org/abs/2603.06350)
- [Dynamic Chunking Diffusion Transformer](https://arxiv.org/abs/2603.06351)
- [CLAIRE: Compressed Latent Autoencoder for Industrial Representation and Evaluation -- A Deep Learning Framework for Smart Manufacturing](https://arxiv.org/abs/2603.06361)
- [ESAA-Security: An Event-Sourced, Verifiable Architecture for Agent-Assisted Security Audits of AI-Generated Code](https://arxiv.org/abs/2603.06365)
- [Kinetic-based regularization: Learning spatial derivatives and PDE applications](https://arxiv.org/abs/2603.06380)
- [Prompt Group-Aware Training for Robust Text-Guided Nuclei Segmentation](https://arxiv.org/abs/2603.06384)
- [Physical Simulator In-the-Loop Video Generation](https://arxiv.org/abs/2603.06408)
- [A Reference Architecture of Reinforcement Learning Frameworks](https://arxiv.org/abs/2603.06413)
- [CLoPA: Continual Low Parameter Adaptation of Interactive Segmentation for Medical Image Annotation](https://arxiv.org/abs/2603.06426)
- [Abductive Reasoning with Syllogistic Forms in Large Language Models](https://arxiv.org/abs/2603.06428)
- [Prosodic Boundary-Aware Streaming Generation for LLM-Based TTS with Streaming Text Input](https://arxiv.org/abs/2603.06444)
- [Do Foundation Models Know Geometry? Probing Frozen Features for Continuous Physical Measurement](https://arxiv.org/abs/2603.06459)
- [PONTE: Personalized Orchestration for Natural Language Trustworthy Explanations](https://arxiv.org/abs/2603.06485)
- [NOBLE: Accelerating Transformers with Nonlinear Low-Rank Branches](https://arxiv.org/abs/2603.06492)
- [COLD-Steer: Steering Large Language Models via In-Context One-step Learning Dynamics](https://arxiv.org/abs/2603.06495)
- [Artificial Intelligence for Detecting Fetal Orofacial Clefts and Advancing Medical Education](https://arxiv.org/abs/2603.06522)
- [RAMoEA-QA: Hierarchical Specialization for Robust Respiratory Audio Question Answering](https://arxiv.org/abs/2603.06542)
- [LiveSense: A Real-Time Wi-Fi Sensing Platform for Range-Doppler on COTS Laptop](https://arxiv.org/abs/2603.06545)
- [SUREON: A Benchmark and Vision-Language-Model for Surgical Reasoning](https://arxiv.org/abs/2603.06570)
- [Fly360: Omnidirectional Obstacle Avoidance within Drone View](https://arxiv.org/abs/2603.06573)
- [BEVLM: Distilling Semantic Knowledge from LLMs into Bird's-Eye View Representations](https://arxiv.org/abs/2603.06576)
- [Mean-based incomplete pairwise comparisons method with the reference values](https://arxiv.org/abs/2207.10783)
- [Transforming Agency. On the mode of existence of Large Language Models](https://arxiv.org/abs/2407.10735)
- [Position: Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces!](https://arxiv.org/abs/2504.09762)
- [Mitigating Content Effects on Reasoning in Language Models through Fine-Grained Activation Steering](https://arxiv.org/abs/2505.12189)
- [VisioMath: Benchmarking Figure-based Mathematical Reasoning in LMMs](https://arxiv.org/abs/2506.06727)
- [Discerning What Matters: A Multi-Dimensional Assessment of Moral Competence in LLMs](https://arxiv.org/abs/2506.13082)
- [ContextBench: Modifying Contexts for Targeted Latent Activation](https://arxiv.org/abs/2506.15735)
- [Sysformer: Safeguarding Frozen Large Language Models with Adaptive System Prompts](https://arxiv.org/abs/2506.15751)
- [A Multi-Agent System Enables Versatile Information Extraction from the Chemical Literature](https://arxiv.org/abs/2507.20230)
- [PepEDiff: Zero-Shot Peptide Binder Design via Protein Embedding Diffusion](https://arxiv.org/abs/2601.13327)
- [Knowledge Graphs are Implicit Reward Models: Path-Derived Signals Enable Compositional Reasoning](https://arxiv.org/abs/2601.15160)
- [Localizing and Correcting Errors for LLM-based Planners](https://arxiv.org/abs/2602.00276)
- [Uncertainty Quantification in LLM Agents: Foundations, Emerging Challenges, and Opportunities](https://arxiv.org/abs/2602.05073)
- [From Features to Actions: Explainability in Traditional and Agentic AI Systems](https://arxiv.org/abs/2602.06841)
- [MERIT Feedback Elicits Better Bargaining in LLM Negotiators](https://arxiv.org/abs/2602.10467)
- [The Consensus Trap: Dissecting Subjectivity and the "Ground Truth" Illusion in Data Annotation](https://arxiv.org/abs/2602.11318)
- [How Well Does Agent Development Reflect Real-World Work?](https://arxiv.org/abs/2603.01203)
- [Multimodal Mixture-of-Experts with Retrieval Augmentation for Protein Active Site Identification](https://arxiv.org/abs/2603.01511)
- [MOOSEnger -- a Domain-Specific AI Agent for the MOOSE Ecosystem](https://arxiv.org/abs/2603.04756)
- [SEA-TS: Self-Evolving Agent for Autonomous Code Generation of Time Series Forecasting Algorithms](https://arxiv.org/abs/2603.04873)
- [A Cognitive Explainer for Fetal ultrasound images classifier Based on Medical Concepts](https://arxiv.org/abs/2201.07798)
- [RAG-Driver: Generalisable Driving Explanations with Retrieval-Augmented In-Context Learning in Multi-Modal Large Language Model](https://arxiv.org/abs/2402.10828)
- [Estimation of Energy-dissipation Lower-bounds for Neuromorphic Learning-in-memory](https://arxiv.org/abs/2402.14878)
- [Make VLM Recognize Visual Hallucination on Cartoon Character Image with Pose Information](https://arxiv.org/abs/2403.15048)
- [Algorithmic Collusion by Large Language Models](https://arxiv.org/abs/2404.00806)
- [Predictive Coding Networks and Inference Learning: Tutorial and Survey](https://arxiv.org/abs/2407.04117)
- [FALCON: Future-Aware Learning with Contextual Object-Centric Pretraining for UAV Action Recognition](https://arxiv.org/abs/2409.18300)
- [SpecFuse: Ensembling Large Language Models via Next-Segment Prediction](https://arxiv.org/abs/2412.07380)
- [Transforming Science with Large Language Models: A Survey on AI-assisted Scientific Discovery, Experimentation, Content Generation, and Evaluation](https://arxiv.org/abs/2502.05151)
- [Conditioning LLMs to Generate Code-Switched Text](https://arxiv.org/abs/2502.12924)
- [Generative Predictive Control: Flow Matching Policies for Dynamic and Difficult-to-Demonstrate Tasks](https://arxiv.org/abs/2502.13406)
- [FragFM: Hierarchical Framework for Efficient Molecule Generation via Fragment-Level Discrete Flow Matching](https://arxiv.org/abs/2502.15805)
- [Aligning Compound AI Systems via System-level DPO](https://arxiv.org/abs/2502.17721)
- [Adversarial Robustness of Partitioned Quantum Classifiers](https://arxiv.org/abs/2502.20403)
- [FindAnything: Open-Vocabulary and Object-Centric Mapping for Robot Exploration in Any Environment](https://arxiv.org/abs/2504.08603)
- [From Tokenizer Bias to Backbone Capability: A Controlled Study of LLMs for Time Series Forecasting](https://arxiv.org/abs/2504.08818)
- [The Malicious Technical Ecosystem: Exposing Limitations in Technical Governance of AI-Generated Non-Consensual Intimate Images of Adults](https://arxiv.org/abs/2504.17663)
- [Federated Learning: A Survey on Privacy-Preserving Collaborative Intelligence](https://arxiv.org/abs/2504.17703)
- [HCT-QA: A Benchmark for Question Answering on Human-Centric Tables](https://arxiv.org/abs/2504.20047)
- [FourierSpecNet: Neural Collision Operator Approximation Inspired by the Fourier Spectral Method for Solving the Boltzmann Equation](https://arxiv.org/abs/2504.20408)
- [RM-R1: Reward Modeling as Reasoning](https://arxiv.org/abs/2505.02387)
- [Software Development Life Cycle Perspective: A Survey of Benchmarks for Code Large Language Models and Agents](https://arxiv.org/abs/2505.05283)
- [Maximizing Asynchronicity in Event-based Neural Networks](https://arxiv.org/abs/2505.11165)
- [AdAEM: An Adaptively and Automated Extensible Measurement of LLMs' Value Difference](https://arxiv.org/abs/2505.13531)
- [KramaBench: A Benchmark for AI Systems on Data-to-Insight Pipelines over Data Lakes](https://arxiv.org/abs/2506.06541)
- [Iterative Quantum Feature Maps](https://arxiv.org/abs/2506.19461)
- [SPARC: Concept-Aligned Sparse Autoencoders for Cross-Model and Cross-Modal Interpretability](https://arxiv.org/abs/2507.06265)
- [Bridging MOOCs, Smart Teaching, and AI: A Decade of Evolution Toward a Unified Pedagogy](https://arxiv.org/abs/2507.14266)
- [ExDD: Explicit Dual Distribution Learning for Surface Defect Detection via Diffusion Synthesis](https://arxiv.org/abs/2507.15335)
- [MAP: Mitigating Hallucinations in Large Vision-Language Models with Map-Level Attention Processing](https://arxiv.org/abs/2508.01653)
- [VLMQ: Token Saliency-Driven Post-Training Quantization for Vision-language Models](https://arxiv.org/abs/2508.03351)
- [SGDFuse: SAM-Guided Diffusion Model for High-Fidelity Infrared and Visible Image Fusion](https://arxiv.org/abs/2508.05264)
- [A Geometric Perspective on the Difficulties of Learning GNN-based SAT Solvers](https://arxiv.org/abs/2508.21513)
- [Performance Assessment Strategies for Language Model Applications in Healthcare](https://arxiv.org/abs/2509.08087)
- [Reasoned Safety Alignment: Ensuring Jailbreak Defense via Answer-Then-Check](https://arxiv.org/abs/2509.11629)
- [Better Late Than Never: Meta-Evaluation of Latency Metrics for Simultaneous Speech-to-Text Translation](https://arxiv.org/abs/2509.17349)
- [LikePhys: Evaluating Intuitive Physics Understanding in Video Diffusion Models via Likelihood Preference](https://arxiv.org/abs/2510.11512)
- [Phys2Real: Fusing VLM Priors with Interactive Online Adaptation for Uncertainty-Aware Sim-to-Real Manipulation](https://arxiv.org/abs/2510.11689)
- [CanvasMAR: Improving Masked Autoregressive Video Prediction With Canvas](https://arxiv.org/abs/2510.13669)
- [Just-In-Time Objectives: A General Approach for Specialized AI Interactions](https://arxiv.org/abs/2510.14591)
- [Think with 3D: Geometric Imagination Grounded Spatial Reasoning from Limited Views](https://arxiv.org/abs/2510.18632)
- [Automated Coding of Communication Data Using ChatGPT: Consistency Across Subgroups](https://arxiv.org/abs/2510.20584)
- [Shoot First, Ask Questions Later? Building Rational Agents that Explore and Act Like People](https://arxiv.org/abs/2510.20886)
- [LA-MARRVEL: A Knowledge-Grounded, Language-Aware LLM Framework for Clinically Robust Rare Disease Gene Prioritization](https://arxiv.org/abs/2511.02263)
- [The Persistence of Cultural Memory: Investigating Multimodal Iconicity in Diffusion Models](https://arxiv.org/abs/2511.11435)
- [Diffusion Fine-Tuning via Reparameterized Policy Gradient of the Soft Q-Function](https://arxiv.org/abs/2512.04559)
- [XR-DT: Extended Reality-Enhanced Digital Twin for Safe Motion Planning via Human-Aware Model Predictive Path Integral Control](https://arxiv.org/abs/2512.05270)
- [Whatever Remains Must Be True: Filtering Drives Reasoning in LLMs, Shaping Diversity](https://arxiv.org/abs/2512.05962)
- [Exploiting Spatiotemporal Properties for Efficient Event-Driven Human Pose Estimation](https://arxiv.org/abs/2512.06306)
- [A-3PO: Accelerating Asynchronous LLM Training with Staleness-aware Proximal Policy Approximation](https://arxiv.org/abs/2512.06547)
- [Data-Driven Global Sensitivity Analysis for Engineering Design Based on Individual Conditional Expectations](https://arxiv.org/abs/2512.11946)
- [Understanding and Improving Hyperbolic Deep Reinforcement Learning](https://arxiv.org/abs/2512.14202)
- [Agent Tools Orchestration Leaks More: Dataset, Benchmark, and Mitigation](https://arxiv.org/abs/2512.16310)
- [CASA: Cross-Attention over Self-Attention for Efficient Vision-Language Fusion](https://arxiv.org/abs/2512.19535)
- [CARE What Fails: Contrastive Anchored-REflection for Verifiable Multimodal](https://arxiv.org/abs/2512.19554)
- [LLMTM: Benchmarking and Optimizing LLMs for Temporal Motif Analysis in Dynamic Graphs](https://arxiv.org/abs/2512.22266)
- [Window-based Membership Inference Attacks Against Fine-tuned Large Language Models](https://arxiv.org/abs/2601.02751)
- [Classroom AI: Large Language Models as Grade-Specific Teachers](https://arxiv.org/abs/2601.06225)
- [Purification Before Fusion: Toward Mask-Free Speech Enhancement for Robust Audio-Visual Speech Recognition](https://arxiv.org/abs/2601.12436)
- [SpatialMem: Metric-Aligned Long-Horizon Video Memory for Language Grounding and QA](https://arxiv.org/abs/2601.14895)
- [Neural Signals Generate Clinical Notes in the Wild](https://arxiv.org/abs/2601.22197)
- [Accelerating Scientific Research with Gemini: Case Studies and Common Techniques](https://arxiv.org/abs/2602.03837)
- [Towards Autonomous Mathematics Research](https://arxiv.org/abs/2602.10177)
- [Why Human Guidance Matters in Collaborative Vibe Coding](https://arxiv.org/abs/2602.10473)
- [DataChef: Cooking Up Optimal Data Recipes for LLM Adaptation via Reinforcement Learning](https://arxiv.org/abs/2602.11089)
- [SWE-MiniSandbox: Container-Free Reinforcement Learning for Building Software Engineering Agents](https://arxiv.org/abs/2602.11210)
- [Peak + Accumulation: A Proxy-Level Scoring Formula for Multi-Turn LLM Attack Detection](https://arxiv.org/abs/2602.11247)
- [An Adaptive Model Selection Framework for Demand Forecasting under Horizon-Induced Degradation to Support Business Strategy and Operations](https://arxiv.org/abs/2602.13939)
- [IntelliAsk: Learning to Ask High-Quality Research Questions via RLVR](https://arxiv.org/abs/2602.15849)
- [The Compute ICE-AGE: Invariant Compute Envelope under Addressable Graph Evolution](https://arxiv.org/abs/2602.16736)
- [FLoRG: Federated Fine-tuning with Low-rank Gram Matrices and Procrustes Alignment](https://arxiv.org/abs/2602.17095)
- [The Cascade Equivalence Hypothesis: When Do Speech LLMs Behave Like ASR$\rightarrow$LLM Pipelines?](https://arxiv.org/abs/2602.17598)
- [Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization](https://arxiv.org/abs/2602.23008)
- [Modality Collapse as Mismatched Decoding: Information-Theoretic Limits of Multimodal LLMs](https://arxiv.org/abs/2602.23136)
- [CoME: Empowering Channel-of-Mobile-Experts with Informative Hybrid-Capabilities Reasoning](https://arxiv.org/abs/2602.24142)
- [Theory of Code Space: Do Code Agents Understand Software Architecture?](https://arxiv.org/abs/2603.00601)
- [Reparameterized Tensor Ring Functional Decomposition for Multi-Dimensional Data Recovery](https://arxiv.org/abs/2603.01034)
- [MatRIS: Toward Reliable and Efficient Pretrained Machine Learning Interatomic Potentials](https://arxiv.org/abs/2603.02002)
- ["When to Hand Off, When to Work Together": Expanding Human-Agent Co-Creative Collaboration through Concurrent Interaction](https://arxiv.org/abs/2603.02050)
- [Kiwi-Edit: Versatile Video Editing via Instruction and Reference Guidance](https://arxiv.org/abs/2603.02175)
- [Whisper-RIR-Mega: A Paired Clean-Reverberant Speech Benchmark for ASR Robustness to Room Acoustics](https://arxiv.org/abs/2603.02252)
- [Rigidity-Aware Geometric Pretraining for Protein Design and Conformational Ensembles](https://arxiv.org/abs/2603.02406)
- [Fine-Tuning and Evaluating Conversational AI for Agricultural Advisory](https://arxiv.org/abs/2603.03294)
- [Fragile Thoughts: How Large Language Models Handle Chain-of-Thought Perturbations](https://arxiv.org/abs/2603.03332)
- [Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion](https://arxiv.org/abs/2603.03485)
- [Large-Language-Model-Guided State Estimation for Partially Observable Task and Motion Planning](https://arxiv.org/abs/2603.03704)
- [Measuring AI R&D Automation](https://arxiv.org/abs/2603.03992)
- [Simulating Meaning, Nevermore! Introducing ICR: A Semiotic-Hermeneutic Metric for Evaluating Meaning in LLM Text Summaries](https://arxiv.org/abs/2603.04413)
- [vLLM Semantic Router: Signal Driven Decision Routing for Mixture-of-Modality Models](https://arxiv.org/abs/2603.04444)
- [RoboPocket: Improve Robot Policies Instantly with Your Phone](https://arxiv.org/abs/2603.05504)

</details>

*Model: openai/gpt-5.4 | LLM Usage: 6 calls, 20,370 prompt tokens, 13,014 completion tokens, 33,384 total tokens, estimated cost: $0.246135*
