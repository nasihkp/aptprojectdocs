import os, sys

slides_data = [
    # P01
    {
        'num': '01',
        'title': r'MGDA: Provenance Graph Threat Detection \& Attack Scenario Reconstruction',
        'author': r'Mengjiao Cui, Zhengwei Jiang, Shuai Li, Chunyan Ma, Kai Zhang, Peian Yang, and Huamin Feng',
        'year': '2025',
        'journal': r'Computer Networks (Elsevier)',
        'problem': r'Detecting stealthy APTs in audit logs without labeled attack data while scaling to large provenance graphs.',
        'method': r'MGDA masked graph autoencoder reconstructs normal features and structure; flags anomalies via latent KNN distance and traces causal subgraphs.',
        'dataset': r'DARPA TC (CADETS, THEIA, TRACE), StreamSpot, and Unicorn Wget.',
        'result': r'Achieved 99.85\% F1 on StreamSpot and 99.98\% recall on TRACE with 100x faster training than ShadeWatcher.',
        'advs': [
            r'Self-supervised training on normal logs removes need for attack labels.',
            r'Achieved 99.98\% recall and 99.26\% precision on DARPA TRACE.',
            r'Fast training in 14 minutes on TRACE (100x speedup over ShadeWatcher).'
        ],
        'diss': [
            r'Scenario reconstruction relies on predefined expert rules rather than deep learning.',
            r'Uses only node and edge types, omitting payload data semantics.',
            r'KNN anomaly scoring scales quadratically on dense subgraphs.'
        ]
    },
    # P02
    {
        'num': '02',
        'title': r'Commander: Robust Cross-Machine Multi-Phase APT Detection via Provenance',
        'author': r'Qi Liu, Kaibin Bao, and Veit Hagenmeyer',
        'year': '2025',
        'journal': r'Journal of Information Security and Applications (Elsevier)',
        'problem': r'Provenance IDSs suffer dependency explosion and fail to track lateral movement across machines.',
        'method': r'Modular detector with parallel evasion filters, logon-session graph partitioning, cross-machine causal stitching, and ICS threat scoring.',
        'dataset': r'AVIATOR dataset emulating MITRE Sandworm and OilRig across IT and ICS networks.',
        'result': r'Achieved 100\% precision and recall (0 false alarms), tracing attacks into physical ICS controllers.',
        'advs': [
            r'Successfully tracks multi-phase lateral movement across distributed hosts.',
            r'Session-based execution partitioning eliminates graph dependency explosion.',
            r'Native industrial control support with parsers for Siemens and Hitachi hardware.'
        ],
        'diss': [
            r'Strictly requires Windows Active Directory domain controller authentication logs.',
            r'Relies on manual rule engineering for preliminary evasion detectors.',
            r'Cross-machine causal stitching took up to 575s on complex Sandworm data.'
        ]
    },
    # P03
    {
        'num': '03',
        'title': r'Threat Detection in CPS Through Spatio-Temporal Anomaly Detection Using GAT',
        'author': r'Roberto Canonico, Francesco Lista, Annalisa Navarro, Giancarlo Sperl{\'\i}, and Andrea Vignali',
        'year': '2025',
        'journal': r'Computers \& Security (Elsevier)',
        'problem': r'CPS anomaly detectors ignore multi-sensor temporal interactions and incur high memory overhead.',
        'method': r'Top-$K$ correlation graph pruning + Spatio-Temporal GAT with 1D temporal convolutions and joint prediction-reconstruction loss.',
        'dataset': r'Secure Water Treatment (SWaT) testbed (496,800 train and 449,919 test samples).',
        'result': r'Slashed graph memory footprint by 77.8\% and training time by 21\%, achieving 99.31\% attack precision.',
        'advs': [
            r'Top-$K$ correlation graph pruning slashes memory usage by 77.8\%.',
            r'Achieved 99.31\% precision on attack traffic, cutting false alarms by 46.6\%.',
            r'Jointly extracts spatial multi-sensor attention and 1D temporal convolutions.'
        ],
        'diss': [
            r'Moderate recall of 71.68\%, missing subtle multi-point sensor manipulations.',
            r'Performance is highly sensitive to correlation sparsity parameter $K$.',
            r'Evaluated on only a single physical water treatment testbed (SWaT).'
        ]
    },
    # P04
    {
        'num': '04',
        'title': r'EdgeFence: Federated Temporal GNNs for Adversarial Malware Detection in Edge Networks',
        'author': r'Osei Isaac, Benjamin Appiah, Daniel Commey, Kwabena Owusu-Agyemang, Michael Asante, and Benjamin Hayfrom Acquah',
        'year': '2026',
        'journal': r'International Journal of Information Security (Springer)',
        'problem': r'Edge devices have strict compute limits and cannot centrally pool private logs, facing adversarial evasion.',
        'method': r'Federated Temporal GNNs (FTGNN) on dynamic system call interaction graphs with FedAvg and adversarial training.',
        'dataset': r'CIC-IDS2018 and IoT-23 datasets with 7:3 benign-to-malicious ratio under federated simulation.',
        'result': r'Achieved 0.961 accuracy and 0.986 AUC while preserving data privacy and resisting graph evasion.',
        'advs': [
            r'Preserves privacy by sharing model parameters via FedAvg instead of raw logs.',
            r'Captures time-evolving system call sequences and process interaction graphs.',
            r'Hardened against evasion attacks through integrated adversarial graph perturbations.'
        ],
        'diss': [
            r'Suffers a slight accuracy trade-off compared to centralized model training.',
            r'Non-IID edge data distributions and graph heterogeneity slow global convergence.',
            r'Generating adversarial perturbations increases local edge training latency.'
        ]
    },
    # P05
    {
        'num': '05',
        'title': r'SHIELD: APT Detection and Intelligent Explanation Using Large Language Models',
        'author': r'Parth Atulbhai Gandhi, Prasanna N. Wudali, Yonatan Amaru, Akansha Shukla, Yuval Elovici, and Asaf Shabtai',
        'year': '2026',
        'journal': r'Engineering Applications of Artificial Intelligence (Elsevier)',
        'problem': r'Provenance graph alerts overwhelm analysts, and supervised models suffer from concept drift.',
        'method': r'Unsupervised pipeline combining LOF outlier filtering, Louvain community clustering, off-the-shelf LLMs (Llama-3.1), and a temporal correlation engine.',
        'dataset': r'DARPA CADETS, THEIA, CLEARSCOPE, DARPA OpTC, Public Arena, and Blind Eagle.',
        'result': r'Achieved 100\% precision on CADETS, cut alert workload by 95.58\%, and generated plain-English MITRE narratives.',
        'advs': [
            r'Achieved 100\% precision on DARPA CADETS, reducing alert workload by 95.58\%.',
            r'Generates clear, plain-English attack narratives mapped to MITRE ATT\&CK stages.',
            r'Concept drift immune by using off-the-shelf LLMs without model retraining.'
        ],
        'diss': [
            r'Running local 8B/70B LLMs requires high-end GPU hardware (48 GB VRAM).',
            r'15-minute sliding window introduces an operational detection delay.',
            r'Risk of LLM hallucinations requiring strict multi-stage prompt validation.'
        ]
    },
    # P06
    {
        'num': '06',
        'title': r'From Logs to Tactics: Unsupervised APT Reconstruction with MITRE Meta-Alerts',
        'author': r'Francesco Ferazza, Cosimo Melella, Konstantinos Mersinas, Ricardo Lugo, and Rain Ottis',
        'year': '2026',
        'journal': r'International Journal of Information Security (Springer)',
        'problem': r'SOC analysts face cognitive fatigue from thousands of fragmented EDR/syslog alerts lacking labels.',
        'method': r'Graph Convolutional Autoencoders for sequence extraction, GPT-3.5 summarization, S-BERT + HDBSCAN clustering into meta-alerts, and hybrid ontology-BERT mapping.',
        'dataset': r'Real-world NATO Crossed Swords 2024 (XS24) exercise telemetry (Linux syslog and SentinelOne EDR).',
        'result': r'Slashed alert triage volume by 97.8\% and achieved an 87\% F1-score on automated MITRE ATT\&CK mapping.',
        'advs': [
            r'Slashes alert volume by 97.8\% (from 925 alerts to 20 meta-alerts) with 100\% threat coverage.',
            r'Hybrid ontology and BERT mapping engine attains 87\% F1-score on MITRE ATT\&CK.',
            r'Unsupervised design requires no ground-truth labels for operational deployment.'
        ],
        'diss': [
            r'Relies on external commercial LLM APIs (GPT-3.5), incurring recurring cost.',
            r'Multi-stage pipeline creates processing delays unsuitable for inline prevention.',
            r'Modest campaign reconstruction recall (0.66 recall), missing some multi-host transitions.'
        ]
    },
    # P07
    {
        'num': '07',
        'title': r'A Novel Hybrid Intrusion Detection Method Integrating Anomaly and Misuse Detection',
        'author': r'Gisung Kim, Seungmin Lee, and Sehun Kim',
        'year': '2014',
        'journal': r'Expert Systems with Applications (Elsevier)',
        'problem': r'Misuse detection misses unknown attacks, while standalone anomaly detection has high false alarms.',
        'method': r'Hierarchical framework: C4.5 Decision Tree filters known attacks and partitions normal data into sub-clusters; individual 1-Class SVMs profile each leaf.',
        'dataset': r'NSL-KDD benchmark dataset (KDDTrain+ and KDDTest+).',
        'result': r'Boosted unknown attack detection by $\sim$10\% at low false alarm rates ($<$10\%) and reduced training time by 26.2\%.',
        'advs': [
            r'Boosts unknown attack detection by $\sim$10\% while maintaining low false alarms ($<$10\%).',
            r'Decomposing normal traffic via tree leaves allows 1-Class SVMs to form tight boundaries.',
            r'Cuts training time by 26.2\% and testing time by 28.2\% with fewer support vectors.'
        ],
        'diss': [
            r'C4.5 tree splitting is guided by information gain rather than geometric clustering.',
            r'Extreme data imbalance across sub-models: 87\% of normal data fell into a single leaf.',
            r'Evaluated only on legacy NSL-KDD tabular data; lacks graph or temporal capabilities.'
        ]
    },
    # P08
    {
        'num': '08',
        'title': r'Self-Supervised Graph Neural Networks for Network Intrusion Detection in Cloud-Edge',
        'author': r'Haiyang Diao, Xiang Li, Wan Zhang, Yan Sibyl Yu, Ye Wang, and Jing Zhang',
        'year': '2026',
        'journal': r'Journal of Cloud Computing (Springer)',
        'problem': r'Supervised NIDS require costly packet labeling, while standard GNNs treat all connections uniformly.',
        'method': r'SSGMHAN uses multi-head node-edge attention, dynamic attention-based edge pruning, and self-supervised contrastive learning via optimal transport loss.',
        'dataset': r'NF-BoT-IoT, NF-BoT-IoT-v2, and NF-ToN-IoT NetFlow benchmark datasets.',
        'result': r'Achieved 97.46\% F1-score on NF-BoT-IoT-v2 without labels and cut training time by 64.1\% via edge pruning.',
        'advs': [
            r'Self-supervised contrastive learning trains effectively on unlabeled NetFlow traffic.',
            r'Dynamic edge pruning strips structural graph noise, slashing training time by 64.1\%.',
            r'Ultra-fast batch inference latency of 5.41 ms, well suited for edge gateways.'
        ],
        'diss': [
            r'Fails on extreme minority attack classes (0\% F1-score on data theft flows).',
            r'Computing optimal transport loss during training increases CPU and memory overhead.',
            r'Frequent misclassification between similar flood categories (DoS vs. DDoS).'
        ]
    },
    # P09
    {
        'num': '09',
        'title': r'GraphShield: Advanced Dynamic Graph-Based Malware Detection Using GNNs',
        'author': r'Eslam Amer, Shaker El-Sappagh, Tamer Abuhamad, Bander Ali Saleh Al-Rimy, and Alaa Mohasseb',
        'year': '2025',
        'journal': r'Expert Systems with Applications (Elsevier)',
        'problem': r'Polymorphic and fileless malware alter execution order to evade static signatures and linear models.',
        'method': r'GraphShield converts dynamic API traces into behavioral graphs via BERT clustering and Markov transition matrices; classifies via GIN-CNN autoencoders with GNNExplainer.',
        'dataset': r'Large dataset of 500,000 samples (300,000 train, 200,000 test) collected between 2023 and 2024.',
        'result': r'Achieved 99.51\% F1-score and 0.9993 AUC, reducing false positive rate to 0.28\% with explainable subgraphs.',
        'advs': [
            r'Achieved 99.51\% accuracy and 0.9993 AUC on a large 200,000-sample holdout test set.',
            r'Reduced false positive rate to 0.28\%, a 99.4\% reduction over deep sequential models.',
            r'Integrated GNNExplainer isolates specific malicious API call subgraphs for analysts.'
        ],
        'diss': [
            r'Heavy preprocessing overhead in BERT clustering and graph construction hinders inline speed.',
            r'Requires dynamic execution in controlled sandboxes, introducing evasion risks and delays.',
            r'Blind to direct kernel system calls or in-memory attacks that bypass API hooking.'
        ]
    },
    # P10
    {
        'num': '10',
        'title': r'Cyber Security Attack Recognition on Cloud Networks Based on GCN and GraphSAGE',
        'author': r'Fargana Abdullayeva and Suleyman Suleymanzade',
        'year': '2024',
        'journal': r'Results in Control and Optimization (Elsevier)',
        'problem': r'Traditional IDSs evaluate cloud flows in isolation, and standard full-graph GCNs exhaust memory on large datasets.',
        'method': r'Cloud network flow graph modeling (IP nodes, flow edges with 80 features) comparing ConvGCN against inductive GraphSAGE with mini-batch neighborhood sampling.',
        'dataset': r'Simulated cloud topology from CSE-CIC-IDS2018 (498 IP nodes, 2,952 flow edges, 3 classes).',
        'result': r'GraphSAGE achieved 97.74\% accuracy and 0.98 F1-score, outperforming standard GCN (80.15\%) without memory bottlenecks.',
        'advs': [
            r'GraphSAGE attained 97.74\% accuracy and 0.98 F1-score, outperforming GCN by 17.6\%.',
            r'Inductive mini-batch sampling avoids loading full graphs, scaling to new cloud VMs.',
            r'Captures topological relationships across concurrent network flows to spot DDoS attacks.'
        ],
        'diss': [
            r'Evaluated on a very small network topology (only 498 nodes and 2,952 edges).',
            r'Performs node-level classification instead of edge-level, risking misclassifying shared gateways.',
            r'Standard GCN baseline performed poorly (80.15\% accuracy), showing architecture sensitivity.'
        ]
    },
    # P11
    {
        'num': '11',
        'title': r'FTG-Net-E: Hierarchical Ensemble Graph Neural Network for DDoS Attack Detection',
        'author': r'Rana Abu Bakar, Lorenzo De Marinis, Filippo Cugini, and Francesco Paolucci',
        'year': '2024',
        'journal': r'Computer Networks (Elsevier)',
        'problem': r'ML/DL DDoS detection systems rely on stateful statistical features that overfit to specific datasets.',
        'method': r'FTG-Net-E uses two-level Flow-to-Traffic Graphs (packet-level Flow Graphs nested inside endpoint Traffic Graphs) classified by an ensemble of GCNs via bagging and boosting.',
        'dataset': r'Evaluated on CIC-IDS2017 and CSE-CIC-IDS2018 benchmark datasets.',
        'result': r'Achieved 99.67\% accuracy and 100\% recall relying exclusively on graph topology without stateful features; trained in 10 minutes.',
        'advs': [
            r'Relies purely on structural graph topology, completely eliminating stateful feature overhead.',
            r'State-of-the-art detection with 99.67\% accuracy and 100\% recall on DDoS attack traffic.',
            r'Fast training: trained 8.3M parameters in 10 minutes (6x faster than CNN-based LUCID).'
        ],
        'diss': [
            r'Sensitive to time-slot window size; larger windows (50s) increase detection latency to $\sim$100 ms.',
            r'Creating and storing nested two-level graphs creates memory overhead at backbone scales.',
            r'Tested exclusively on volumetric DDoS floods; unverified on stealthy host-level APTs.'
        ]
    },
    # P12
    {
        'num': '12',
        'title': r'Intelligent Intrusion Detection for Cyber-Physical Systems Using GAN-LSTM',
        'author': r'Md Shakil Siddique, Md. Ashikur Rahman Khan, Ishtiaq Ahammad, Nishu Nath, Joysri Rani Das, and Fardowsi Rahman',
        'year': '2025',
        'journal': r'Franklin Open (Elsevier)',
        'problem': r'CPS generate multivariate sensor time-series where rare attacks are overwhelmed by normal data, causing severe class imbalance.',
        'method': r'Hybrid GAN-LSTM: LSTM generator synthesizes realistic minority attack sequences, while an LSTM discriminator trains on temporal patterns, using joint reconstruction-discrimination loss.',
        'dataset': r'Secure Water Treatment (SWaT) and Water Distribution (WADI) industrial datasets.',
        'result': r'Achieved 87\% accuracy and 99\% recall on SWaT, and 91\% accuracy with 97\% precision on WADI, outperforming MAD-GAN by 14\%--45\%.',
        'advs': [
            r'Attained 99\% recall on SWaT, detecting virtually all physical and cyber manipulation attacks.',
            r'High precision (93\% on SWaT, 97\% on WADI) prevents costly false-alarm shutdowns.',
            r'Resolves class imbalance by generating realistic synthetic minority attack sequences.'
        ],
        'diss': [
            r'Recall dropped to 75\% on the multi-stage WADI dataset, missing 25\% of stealthy intrusions.',
            r'Adversarial GAN-LSTM training is intensive and adds 50--200 ms inference latency.',
            r'Relies on a static anomaly decision threshold ($\tau$) that struggles on overlapping feature spaces.'
        ]
    },
    # P13
    {
        'num': '13',
        'title': r'Knowledge Graph Visualization and Anomaly Detection Using Graph Neural Networks',
        'author': r'Ali Yilmaz, Resul Das, Mehmet Ozdem, and Berk Canberk',
        'year': '2026',
        'journal': r'Computer Networks (Elsevier)',
        'problem': r'Intrusion detection research lacks standardized benchmarks comparing GNN models, and lacks interactive visual tools for attack propagation analysis.',
        'method': r'Unified benchmarking framework evaluating standardized two-layer GCN, GAT, GIN, and GraphSAGE models using 5-fold cross-validation, integrated with a D3.js directed attack visualizer.',
        'dataset': r'UNSW-NB15 (primary multi-class), CIC-DDoS2019, and CSE-CIC-IDS2018 datasets.',
        'result': r'GraphSAGE and GIN achieved top performance (F1 $>$ 0.969, ROC-AUC $>$ 0.99 on UNSW-NB15, and $>$ 0.9935 accuracy on CSE-CIC-IDS2018) with interactive attack visualization.',
        'advs': [
            r'Standardized, reproducible benchmark of four core GNN models under identical splits.',
            r'Interactive D3.js visualization dynamically maps attacker-target relationships and flow propagation.',
            r'High discriminative accuracy: GraphSAGE and GIN attained F1 $>$ 0.969 and ROC-AUC $>$ 0.99.'
        ],
        'diss': [
            r'Models network traffic as static aggregated graphs, missing dynamic time-evolving topology changes.',
            r'Macro-F1 dropped significantly on rare attack classes with low support (e.g., SQL Injection).',
            r'Full-batch graph processing creates memory and computational bottlenecks on large enterprise networks.'
        ]
    },
    # P14
    {
        'num': '14',
        'title': r'Robust, Efficient Detection of Network Intrusion Attacks: A Large Language Model Approach',
        'author': r'Giancarlo Iannizzotto, Andrea Nucita, and Andrea Siragusa',
        'year': '2026',
        'journal': r'Computer Networks (Elsevier)',
        'problem': r'Traditional NIDS suffer severe accuracy collapse on unseen network topologies with zero IP overlap, and deep learning models require heavy GPU memory.',
        'method': r'LLM-NIRED tokenizes structured flow telemetry into text prompts; fine-tunes Mistral-7B-v0.1 via QLoRA with 4-bit NF4 quantization, and evaluates a lightweight TinyLLM (TinyMistral-6x248M).',
        'dataset': r'CIC-IDS-2017, UNSW-NB15, NSL-KDD, CIDDS-001/002, and XOR-encrypted traffic. Tested on Raspberry Pi 5.',
        'result': r'Maintained 98.9\%--99.1\% accuracy on zero-overlap external networks where BERT baselines dropped to 47.4\%; deployed TinyLLM on a Raspberry Pi 5 with 868 MB VRAM.',
        'advs': [
            r'Exceptional cross-network generalization: maintained 98.92\% accuracy on networks with 0\% overlap.',
            r'Achieved 99.92\% accuracy on XOR-encrypted payloads and hashed IPs by analyzing flow metadata.',
            r'Single-stage architecture requires only 4.7 GB VRAM (868 MB for TinyLLM), avoiding complex embedding pipelines.'
        ],
        'diss': [
            r'High inference latency ($\sim$311 ms on GPU, $\sim$2s on Raspberry Pi 5) prevents inline line-rate filtering.',
            r'Black-box classification outputs binary prediction tokens without explainable diagnostic indicators.',
            r'Feature extraction pipeline ignores critical TLS/SSL handshake attributes (e.g., JA3/JA4 fingerprints).'
        ]
    },
    # P15
    {
        'num': '15',
        'title': r'Detection of Advanced Persistent Threat: A Genetic Programming Approach',
        'author': r'Abdullah Al Mamun, Harith Al-Sahaf, Ian Welch, and Masood Mansoori',
        'year': '2024',
        'journal': r'Applied Soft Computing (Elsevier)',
        'problem': r'Multi-stage APTs operate stealthily across long lifecycles; static ML models struggle with extreme class imbalance and fail to classify specific stages of the attack lifecycle.',
        'method': r'Genetic Programming Classifier (GPC) evolves tree-structured mathematical computer programs using basic arithmetic operators and flow features, maximizing Balanced Accuracy.',
        'dataset': r'DAPT-2020 dataset (129,223 normal samples vs. only 15 exfiltration samples, plus reconnaissance, foothold, and lateral movement).',
        'result': r'Achieved 79.75\% balanced accuracy in multi-class APT lifecycle stage detection (outperforming DT, SVM, MLP, RF, and OCSVM) with 0.0003 ms per-sample test latency.',
        'advs': [
            r'Outperformed traditional classifiers in multi-class stage detection, achieving 79.75\% balanced accuracy.',
            r'High sensitivity to stealthy intrusions, achieving 93.51\% recall on malicious flows under extreme class imbalance.',
            r'Ultra-fast test inference latency of 0.0003 ms per sample due to compact mathematical decision trees.'
        ],
        'diss': [
            r'Low precision in binary classification (37.89\%) with a 5.97\% false alarm rate, causing alert clutter.',
            r'Slow training process: evolving genetic programming trees took $\sim$17.6 minutes (vs. 8s for RF).',
            r'Arithmetic terminal nodes cannot directly process non-numerical or categorical network attributes.'
        ]
    },
    # P16
    {
        'num': '16',
        'title': r'Dynamic Cyber Deception Using AI-Driven Adaptive Honeypot Networks',
        'author': r'Mohammed Alshehri',
        'year': '2026',
        'journal': r'Ain Shams Engineering Journal (Elsevier)',
        'problem': r'Traditional static honeypots are quickly identified and avoided by advanced adversaries during reconnaissance, failing to divert multi-stage APTs or collect dynamic intelligence.',
        'method': r'ASD-TGXAI proactive closed-loop deception combining ASREF (Swarm + RL + Differential Evolution) for sub-second decoy adaptation with TGXAI-Net (Transformers + GNNs + SHAP/LRP) threat modeling.',
        'dataset': r'Dionaea honeypot logs (27,574 connections), Financial Sector dataset, and Industrial IoT network logs.',
        'result': r'Reconfigured honeypot personalities within 180--220 ms, neutralized threats in 200 ms, achieved 98\% detection accuracy, and extended attacker engagement to 18.6 minutes.',
        'advs': [
            r'Neutralizes threats in 200 ms and adapts decoy services in 180--220 ms.',
            r'Sustained 98\% detection accuracy with low false alarm rates (0.02).',
            r'Extended attacker engagement to 18.6 minutes, gathering 420 MB threat telemetry.'
        ],
        'diss': [
            r'High overhead: consumes $\sim$90\% system resources (22\% CPU, 18\% GPU, 9.2 GB RAM).',
            r'Sub-second adaptation cycles ($\sim$500 ms) risk revealing decoy quirks.',
            r'Complex multi-module architecture complicates operational enterprise deployment.'
        ]
    }
]

def make_slide(p):
    adv_items = [r'\textbullet~' + a for a in p['advs']]
    adv_str = r'\par\vspace{1.5pt}'.join(adv_items)
    
    dis_items = [r'\textbullet~' + d for d in p['diss']]
    dis_str = r'\par\vspace{1.5pt}'.join(dis_items)

    slide = f'''%% ------ P{p['num']} -----------------------------------------------------------
\\begin{{frame}}[t]{{{p['title']}}}
\\vspace{{-0.30em}}
{{\\footnotesize\\setlength{{\\tabcolsep}}{{3.5pt}}\\renewcommand{{\\arraystretch}}{{1.10}}
\\begin{{tabularx}}{{\\textwidth}}{{|L{{3.10cm}}|Y|L{{5.70cm}}|}}
\\hline\\lrhdr\\hline
\\begin{{minipage}}[t]{{\\linewidth}}\\fontsize{{7.2pt}}{{9.2pt}}\\raggedright\\selectfont
\\textbf{{Author:}}\\par
{p['author']}\\par\\vspace{{4pt}}
\\textbf{{Year:}} {p['year']}\\par\\vspace{{4pt}}
\\textbf{{Journal:}}\\par
{p['journal']}
\\end{{minipage}}
&
\\begin{{minipage}}[t]{{\\linewidth}}\\fontsize{{7.2pt}}{{9.0pt}}\\raggedright\\selectfont
\\textbf{{Problem:}} {p['problem']}\\par\\vspace{{2.5pt}}
\\textbf{{Method:}} {p['method']}\\par\\vspace{{2.5pt}}
\\textbf{{Dataset:}} {p['dataset']}\\par\\vspace{{2.5pt}}
\\textbf{{Key Result:}} {p['result']}
\\end{{minipage}}
&
\\begin{{minipage}}[t]{{\\linewidth}}\\fontsize{{7.2pt}}{{9.0pt}}\\raggedright\\selectfont
\\textcolor{{strengthGreen}}{{\\textbf{{Advantages:}}}}\\par\\vspace{{1.5pt}}
{adv_str}\\par\\vspace{{3.5pt}}
\\textcolor{{limitRed}}{{\\textbf{{Disadvantages:}}}}\\par\\vspace{{1.5pt}}
{dis_str}
\\end{{minipage}} \\\\\\hline
\\end{{tabularx}}}}
\\end{{frame}}
'''
    return slide

with open('main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# Update \lrhdr to say Summary and Advantages & Disadvantages
old_lrhdr = r'''\newcommand{\lrhdr}{%
  \rowcolor{prismNavy}%
  {\scriptsize\textcolor{white}{\textbf{Citation}}} &
  {\scriptsize\textcolor{white}{\textbf{Paper Summary}}} &
  {\scriptsize\textcolor{white}{\textbf{Key Advantages \& Disadvantages}}} \\}'''

new_lrhdr = r'''\newcommand{\lrhdr}{%
  \rowcolor{prismNavy}%
  {\scriptsize\textcolor{white}{\textbf{Citation}}} &
  {\scriptsize\textcolor{white}{\textbf{Summary}}} &
  {\scriptsize\textcolor{white}{\textbf{Advantages \& Disadvantages}}} \\}'''

if old_lrhdr in text:
    text = text.replace(old_lrhdr, new_lrhdr)

# Set frametitle font size to 9.2pt/11.0pt so all long titles are completely visible and clean
old_ft = r'''    \vbox to 1.22cm{%
      \vfill%
      \raggedright\fontsize{9.5pt}{11.5pt}\selectfont\textbf{\insertframetitle}%
      \vfill%
    }%'''

new_ft = r'''    \vbox to 1.22cm{%
      \vfill%
      \raggedright\fontsize{9.2pt}{11.0pt}\selectfont\textbf{\insertframetitle}%
      \vfill%
    }%'''

if old_ft in text:
    text = text.replace(old_ft, new_ft)

all_slides = '\n'.join([make_slide(p) for p in slides_data])

start_marker = r'\section{Literature Review}'
end_marker = r'\section{Research Gap}'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Error: Could not find markers!')
    sys.exit(1)

new_text = text[:start_idx + len(start_marker)] + '\n\n' + all_slides + '\n%% ======================================================================\n%%  SECTION 5: RESEARCH GAPS\n%% ======================================================================\n' + text[end_idx:]

with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Successfully updated main.tex!')
