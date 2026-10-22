# Comprehensive Slide-by-Slide Technical Reference & Keyword Glossary

**Project Title:** CYBER ATTACK PREDICTION PLATFORM USING SPATIO-TEMPORAL GRAPH NEURAL NETWORKS  
**Subtitle:** Dual-Tier Conventional and APT Threat Detection via ST-GNN (GAT+GRU+VGAE), Federated Privacy (TenSEAL CKKS) & MITRE ATT&CK Mapping  
**Department:** Department of Computer Science & Engineering, College of Engineering, Karunagappally  
**Academic Batch:** B.Tech Computer Science and Engineering  
**Project Group:** Group 14  
**Project Members:**
1. Muhammed Nasih K P (KNP23CS074)
2. Sumayya Ershad (KNP23CS107)
3. Najmunniza N (LKNP20CS056)
4. K.S. Mahadev (KNP23CS066)

**Project Guide:** Mrs. SYAMA S R, Assistant Professor, Dept. of CSE  
**Date of Current Milestone:** September 2026 (Requirement Analysis & Feasibility Phase)

---

## 1. Synthesis of the Three Research Papers into Our Do-able System

Our project synthesizes three peer-reviewed foundations into a feasible, production-ready system:

1. **MGDA (Cui et al., Elsevier *Computer Networks*, 2025):**
   - *Core Contribution Adopted:* Semantic-preserving provenance graph construction from OS kernel audit logs (DARPA TC CADETS/THEIA). Event compression merging consecutive read/write operations without state changes (cutting volume by >80%). Unsupervised anomaly detection on benign baselines without requiring labeled attack samples.
2. **Commander (Liu et al., Elsevier *Journal of Information Security and Applications*, 2025):**
   - *Core Contribution Adopted:* Cross-machine multi-phase APT tracking and session-based execution partitioning to halt dependency explosion. Resistance against cyber persistence (registry run keys, cron jobs) and session hijacking (token impersonation, pass-the-hash).
3. **EdgeFence (Isaac et al., Springer *International Journal of Information Security*, 2026):**
   - *Core Contribution Adopted:* Distributed temporal graph snapshots ($G_t = (V_t, E_t, X_t)$) over sliding windows, lightweight Temporal Graph Neural Networks, and Federated Learning across distributed endpoints so raw audit logs never leave host nodes.
4. **Our Innovative Project Enhancements:**
   - **ST-VGAE (Spatio-Temporal Variational Graph Autoencoder):** GAT captures spatial entity relationships (Process, File, Socket); GRU captures multi-window sequence progression; VGAE models the benign latent distribution $\mathcal{N}(\mu, \sigma^2)$ and flags zero-days via adjacency reconstruction error $\|\mathbf{A} - \hat{\mathbf{A}}\|_F^2$.
   - **TenSEAL CKKS Homomorphic Encryption:** Encrypts local weight gradients $\Delta \mathbf{w}_i$ before sending them to the central aggregation server. The server performs homomorphic FedAvg ($[[\Delta \mathbf{w}]] = \sum \frac{N_i}{N} [[\Delta \mathbf{w}_i]]$) without ever decrypting weights, eliminating gradient inversion risks.
   - **Automated Causal Forensics & MITRE ATT&CK Attribution:** Bidirectional $k$-hop BFS extracts causal attack DAGs from high-outlier seed processes, matched against MITRE ATT&CK tactics (Initial Access, Persistence, Lateral Movement, Exfiltration) for SOC analysts.

---

## 2. Complete Presentation Structure (37 Slides)

### Slide 1: Title Slide
- Project Title, Group 14 members, Guide Mrs. SYAMA S R, CEK College Logo.

### Slide 2: Presentation Overview / Roadmap
- Part I: Foundations & Literature (Slides 3 to 22).
- Part II: Architecture & Engineering (Slides 23 to 37).

### Slide 3: 1. Introduction (Shortened & Cohesive)
- **Advanced Persistent Threats (APTs):** Low-and-slow, multi-stage cyber intrusions lasting weeks/months.
- **Loss of Context in Flat Logs:** Conventional tools flatten logs into tables, losing process-to-file cause-and-effect links.
- **Dynamic Provenance Graphs:** Directed property graphs connecting Processes, Files, and Network Sockets.
- **Spatio-Temporal Deep Learning:** GAT + GRU + VGAE enables self-supervised zero-day detection without attack labels.
- **Federated Privacy (TenSEAL CKKS):** Multi-host collaborative defense without sharing raw private logs.
- **Automated Attribution:** Extracted attack subgraphs mapped to MITRE ATT&CK tactics.

### Slide 4: 2. Project Objectives (Single Cohesive Paragraph)
- Design and develop an intelligent, privacy-preserving cyber attack prediction and investigation platform detecting stealthy APTs and zero-days across enterprise networks.
- Methods integrated: Provenance graphs with semantic compression (DARPA TC), unsupervised ST-VGAE anomaly detection, TenSEAL CKKS homomorphic federated learning, and causal attack subgraph reconstruction with MITRE ATT&CK mapping.

### Slide 5: 3. Problem Statement
- Traditional security systems struggle to detect stealthy, multi-stage cyberattacks that mimic normal system activities. Existing approaches often fail to capture complex behavioral relationships and temporal patterns in system logs.
- Proposes a spatio-temporal graph-based anomaly detection framework using GAT, GRU, and VGAE to detect suspicious activities, reconstruct potential attack paths, and map threats to the MITRE ATT&CK framework while preserving data privacy.

### Slides 6 to 21: 4. Literature Review (16 Papers Preserved Verbatim)
- [P01] MGDA (Cui et al., 2025)
- [P02] Commander (Liu et al., 2025)
- [P03] Canonico et al. (2025)
- [P04] EdgeFence (Isaac et al., 2026)
- [P05] SHIELD (Gandhi et al., 2026)
- [P06] Ferazza et al. (2026)
- [P07] Kim et al. (2014)
- [P08] Diao et al. (2026)
- [P09] GraphShield (Amer et al., 2025)
- [P10] Abdullayeva & Suleymanzade (2024)
- [P11] FTG-Net-E (Abu Bakar et al., 2024)
- [P12] Siddique et al. (2025)
- [P13] Yilmaz et al. (2026)
- [P14] Iannizzotto et al. (2026)
- [P15] Al Mamun et al. (2024)
- [P16] Alshehri (2026)

### Slide 22: Research Gaps & Proposed Solutions
- **1. Separate Defenses for Network and Host:** Integrated platform uniting network filtering with deep host provenance graph analysis.
- **2. Graph Explosion and Loss of Causal Context:** Semantics-preserving log compression and session partitioning preserving $Process \rightarrow File \rightarrow Socket$ chains.
- **3. Heavy Dependence on Labeled Attack Data:** Unsupervised ST-VGAE (GAT + GRU + VGAE) detecting zero-day anomalies via reconstruction error.
- **4. Privacy Bottlenecks and Alert Overload:** TenSEAL CKKS Homomorphic Encryption for federated learning and automated MITRE ATT&CK mapping.

### Slide 23: 5a. System Design Principles: Features, Libraries & Datasets
- **Features:** Node attributes (Process, File, Socket), binary path entropy, command-line hashes; Edge types (`fork`, `execve`, `read`, `write`, `connect`).
- **Software Libraries:** PyTorch 2.x, PyTorch Geometric (PyG), TenSEAL, NetworkX, FastAPI.
- **Datasets:** DARPA Transparent Computing (CADETS, THEIA, OpTC).

### Slide 24: 5b. System Design Principles: Neo4j Graph Database & Storage Architecture
- **Neo4j Graph Database:** Native directed property graph for sub-second recursive Cypher traversal during backward/forward causal attack reconstruction.
- **Relational Metadata Store (SQLite / PostgreSQL):** Time-series anomaly scores, host agent inventory, and federated round telemetry.

### Slide 25: 6. Workflow Diagram (TikZ)
- High-level end-to-end operational pipeline from raw DARPA TC logs to real-time SOC alerting.

### Slide 26: 7. Proposed Methods (4 Core Pillars)
- Method 1: Provenance Graph Construction & Compression (Semantic merging + session partitioning).
- Method 2: Spatio-Temporal VGAE (GAT + GRU + VGAE).
- Method 3: Privacy-Preserving TenSEAL CKKS Federated Learning.
- Method 4: Causal Attack Reconstruction & MITRE ATT&CK Mapping.

### Slide 27: 8. Model Responsibilities and Inference Flow
- **Mathematical Formulations:** GAT spatial attention ($\alpha_{ij}$), GRU temporal recurrence ($\mathbf{s}_t$), VGAE Gaussian latent sampling ($\mathbf{Z}_t \sim \mathcal{N}(\mu, \sigma^2)$) and adjacency reconstruction ($\hat{\mathbf{A}}_t$).
- **Inference Flow:** Streaming windowing $\rightarrow$ forward pass $\rightarrow$ reconstruction loss $\rightarrow$ threshold evaluation $\rightarrow$ seed extraction.

### Slide 28: 9. Dataset Preparation & Model Training
- **Data Acquisition & Normalization:** Standardizing DARPA TC logs into `(subject, relation, object, timestamp)`.
- **Training Strategy:** Self-supervised training strictly on benign operational periods. Composite loss $\mathcal{L} = \mathcal{L}_{\text{recon}} + \beta \mathcal{L}_{\text{KL}}$.

### Slide 29: 10. System Architecture Diagram (TikZ)
- 4-layer modular architecture:
  1. Host Data Ingestion & Provenance Construction Layer
  2. Edge / Endpoint ST-VGAE AI Detection Engine Layer
  3. Privacy-Preserving Collaborative Federated Orchestration Layer
  4. Threat Intelligence, Causal Attribution & SOC Dashboard Layer

### Slide 30: 11. Flowchart Diagram (TikZ with Proper Arrows)
- Decision-tree flowchart tracing log ingestion, ST-VGAE forward pass, threshold decision, seed extraction, bidirectional BFS, noise pruning, MITRE ATT&CK matching, and alert dispatch.

### Slide 31: 12. Database Schema (Graph & Relational)
- **Neo4j Graph Schema:** `:Process`, `:File`, `:Socket` nodes with `[:FORK]`, `[:EXEC]`, `[:READ]`, `[:WRITE]`, `[:CONNECT]` relationships.
- **Relational Schema:** `hosts`, `anomalies`, `attack_subgraphs`, and `federated_rounds` tables.

### Slide 32: 13. Algorithmic Comparison: Base Papers vs. Our Project
- **EdgeFence (Isaac et al., 2026):** Federated GNN over temporal edge graphs. *Limitation:* Relies on supervised attack labels and transmits plaintext gradient updates $\Delta \mathbf{w}_i$ vulnerable to gradient inversion. *Our Solution:* Unsupervised reconstruction objective + TenSEAL CKKS homomorphic ciphertext aggregation.
- **MGDA (Cui et al., 2025):** Masked autoencoder with contextual backward/forward BFS. *Limitation:* Single-host scope without cross-window temporal recurrence; non-standard heuristic TTP labels. *Our Solution:* Multi-window dynamic seed nodes + Neo4j bidirectional BFS + automated MITRE ATT\&CK Enterprise Matrix mapping.
- **Commander (Liu et al., 2025):** Whole-network provenance with logon session partitioning and Cpd persistence rules. *Limitation:* Purely rule-based heuristics tied to Windows Active Directory; fails on novel zero-day attacks. *Our Solution:* Integrate logon-session execution boundaries into Algorithm 2's BFS traversal to halt dependency explosion while detecting zero-days via ST-VGAE anomaly scores.
- **Synthesis:** Unifies EdgeFence's federated temporal framework, MGDA's contextual causal tracing, and Commander's logon session partitioning into two robust algorithms.

### Slide 33: Algorithm 1: Privacy-Preserving Federated ST-VGAE Training via TenSEAL CKKS
- **Purpose & Lineage:** Upgrades EdgeFence by eliminating labeled data requirements and encrypting parameter updates so the aggregation server never decrypts client weights.
- **Key Steps:** Local ST-VGAE training on normal benign graphs $\rightarrow$ CKKS encryption $[[\Delta \mathbf{w}_k]] \leftarrow \text{Enc}(\Delta \mathbf{w}_k, pk)$ $\rightarrow$ Homomorphic server aggregation $[[\Delta \mathbf{w}]] \leftarrow \sum \frac{|\mathcal{D}_k|}{|\mathcal{D}|} [[\Delta \mathbf{w}_k]]$ $\rightarrow$ Client decryption with private key $sk$.

### Slide 34: Algorithm 2: Causal Attack Subgraph Reconstruction & MITRE ATT&CK Attribution
- **Purpose & Lineage:** Combines MGDA's bidirectional search and Commander's session-partitioned pruning with standardized MITRE ATT&CK technique mapping.
- **Key Steps:** Anomaly score thresholding ($S(v) > \tau$) $\rightarrow$ Extract seed nodes $\mathcal{V}_{\text{seed}}$ $\rightarrow$ Backward BFS for root cause (within execution session) $\rightarrow$ Forward BFS for lateral impact $\rightarrow$ Noise pruning $\rightarrow$ Semantic rule matching $\rightarrow$ Attack DAG mapped to MITRE ATT&CK tactics & techniques.

### Slide 35: Project Work Plan & Gantt Chart
- **Status as of October 2026:**
  - Phase 1 (Problem Formulation & Literature Review): **$\checkmark$ Completed**
  - Phase 2 (Dataset Preprocessing & Graph Modeling): **$\checkmark$ Completed**
  - Phase 3 (System Architecture & Graph Schema Design): **$\blacktriangleright$ In Progress (Now)**
  - Phase 4 (ST-VGAE Model Development): Upcoming (Nov--Dec 2026)
  - Phase 5 (Federated Learning & Homomorphic Encryption): Upcoming (Jan--Feb 2027)
  - Phase 6 (Attack Reconstruction & SOC Dashboard): Upcoming (Mar 2027)
  - Phase 7 (Testing, Validation & Thesis Defense): Upcoming (Apr--May 2027)

### Slide 36: References
- Citations [1] to [8] covering foundational provenance graph frameworks and detection methodologies.

### Slide 37: References
- Citations [9] to [16] covering graph neural network defenses, anomaly detection, and deception networks.

### Slide 38: Thank You & Viva Voce Discussion
- Professional closing slide with Group 14 members, guide Mrs. SYAMA S R, and college department affiliation.
