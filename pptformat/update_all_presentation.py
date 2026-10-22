import os, sys, re

# ==============================================================================
# DATA DEFINITIONS
# ==============================================================================

slides_data = [
    # P01
    {
        'num': '01',
        'title': r'MGDA: Provenance Graph Threat Detection \& Attack Scenario Reconstruction',
        'author': r'''Mengjiao Cui, Zhengwei Jiang, Shuai Li, Chunyan Ma, Kai Zhang, Peian Yang, and Huamin Feng''',
        'year': '2025',
        'journal': r'''Computer Networks (Elsevier)''',
        'summary': r'''Proposes \textbf{MGDA}, a self-supervised masked graph autoencoder on system provenance graphs for label-free APT detection. By learning normal behavior through masked node and edge reconstruction, anomalies are flagged via reconstruction errors, followed by causal tracing to reconstruct multi-stage attack scenarios.''',
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
        'author': r'''Qi Liu, Kaibin Bao, and Veit Hagenmeyer''',
        'year': '2025',
        'journal': r'''Journal of Information Security and Applications (Elsevier)''',
        'summary': r'''Proposes \textbf{Commander}, a cross-machine provenance analytics detector that tracks multi-phase APT lateral movement across distributed hosts. It uses logon-session partitioning to bound graph growth and prevent dependency explosion, correlating host audit logs with authentication events to trace attacker progression.''',
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
        'author': r'''Roberto Canonico, Francesco Lista, Annalisa Navarro, Giancarlo Sperl{\'\i}, and Andrea Vignali'''\i}, and Andrea Vignali',
        'year': '2025',
        'journal': r'''Computers \& Security (Elsevier)''',
        'summary': r'''Proposes an unsupervised spatio-temporal framework combining \textbf{Graph Attention Networks (GAT)} for spatial dependencies and recurrent units for temporal patterns. It detects complex cyber-physical anomalies from multivariate sensor streams via joint forecasting and reconstruction errors.''',
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
        'author': r'''Osei Isaac, Benjamin Appiah, Daniel Commey, Kwabena Owusu-Agyemang, Michael Asante, and Benjamin Hayfrom Acquah''',
        'year': '2026',
        'journal': r'''International Journal of Information Security (Springer)''',
        'summary': r'''Proposes \textbf{EdgeFence}, a federated learning framework for lightweight malware detection across distributed edge networks. Edge nodes model system call sequences as dynamic interaction graphs and locally train Temporal GNNs, sharing only model weights via FedAvg to preserve data privacy against adversarial threats.''',
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
        'author': r'''Parth Atulbhai Gandhi, Prasanna N. Wudali, Yonatan Amaru, Akansha Shukla, Yuval Elovici, and Asaf Shabtai''',
        'year': '2026',
        'journal': r'''Engineering Applications of Artificial Intelligence (Elsevier)''',
        'summary': r'''Proposes \textbf{SHIELD}, an end-to-end framework combining provenance graph anomaly detection with Large Language Models (LLMs). It isolates suspicious subgraphs from OS audit logs, prompting a fine-tuned LLM to verify attacks, generate plain-English explanations, and map activities to MITRE ATT\&CK techniques.''',
        'advs': [
            r'''Reduces false alarms and analyst workload.''',
            r'''Tracks slow-evolving attacks over long periods.''',
            r'''Provides clear and human-interpretable attack summaries.'''
        ],
        'diss': [
            r'''Requires high computational resources.''',
            r'''Can cause detection delay.''',
            r'''Depends on complete and accurate log capture.'''
        ]
    },
    # P06
    {
        'num': '06',
        'title': r'From Logs to Tactics: Unsupervised APT Reconstruction with MITRE Meta-Alerts',
        'author': r'''Francesco Ferazza, Cosimo Melella, Konstantinos Mersinas, Ricardo Lugo, and Rain Ottis''',
        'year': '2026',
        'journal': r'''International Journal of Information Security (Springer)''',
        'summary': r'''Proposes an unsupervised framework that reconstructs full-scale APT campaigns from noisy audit logs. It uses Graph Autoencoders and Sentence-BERT to generate alert embeddings, clustering them into multi-stage attack sequences and achieving an 87\% F1-score in automated MITRE ATT\&CK mapping.''',
        'advs': [
            r'''Reduces alert overload by grouping many alerts into meaningful meta-alerts.''',
            r'''Works without labelled data using an unsupervised approach.''',
            r'''Handles noisy and heterogeneous logs from different sources.'''
        ],
        'diss': [
            r'''Depends on LLM summary quality, so incorrect summaries can affect later stages.''',
            r'''Ontology-based mapping can miss paraphrased expressions.''',
            r'''Evaluation was mainly based on exercise data, so broader real-world testing is needed.'''
        ]
    },
    # P07
    {
        'num': '07',
        'title': r'A Novel Hybrid Intrusion Detection Method Integrating Anomaly and Misuse Detection',
        'author': r'''Gisung Kim, Seungmin Lee, and Sehun Kim''',
        'year': '2014',
        'journal': r'''Expert Systems with Applications (Elsevier)''',
        'summary': r'''Proposes a hierarchical dual-tier intrusion detection architecture integrating misuse and anomaly detection. A frontline Decision Tree rapidly filters known network attack signatures, while decomposed One-Class SVMs profile normal behavior to detect novel zero-day attacks with reduced overhead.''',
        'advs': [
            r'''Improves detection performance for both known and unknown attacks.''',
            r'''Reduces the training time of the anomaly detection model.''',
            r'''Uses known attack information to build more accurate normal-behavior profiles.'''
        ],
        'diss': [
            r'''C4.5 may split well-formed normal clusters.''',
            r'''Uneven data distribution reduces the expected reduction in training and testing time.''',
            r'''About 87\% of training data was concentrated in one subset, limiting the time-saving benefit.'''
        ]
    },
    # P08
    {
        'num': '08',
        'title': r'Self-Supervised Graph Neural Networks for Network Intrusion Detection in Cloud-Edge',
        'author': r'''Haiyang Diao, Xiang Li, Wan Zhang, Yan Sibyl Yu, Ye Wang, and Jing Zhang''',
        'year': '2026',
        'journal': r'''Journal of Cloud Computing (Springer)''',
        'summary': r'''Proposes a self-supervised contrastive Graph Neural Network framework for network intrusion detection in cloud-edge environments. Modeling traffic flows as IP-port communication graphs, it learns robust topological representations from unlabeled traffic via multi-head attention without requiring labeled attack data.''',
        'advs': [
            r'''Reduces the dependency on labeled data by using self-supervised contrastive learning.''',
            r'''Captures both node and edge information using multi-head attention, which helps represent different malicious traffic patterns.''',
            r'''Reduces computational cost through dynamic attention-based edge pruning, which is useful for resource-constrained edge devices.'''
        ],
        'diss': [
            r'''High training computational overhead because Wasserstein and Gromov-Wasserstein distances are computationally expensive.''',
            r'''Sensitive to extreme class imbalance, causing poor detection of minority attack classes such as Theft and Backdoor.''',
            r'''Performance varies across datasets, with lower performance on complex datasets.'''
        ]
    },
    # P09
    {
        'num': '09',
        'title': r'GraphShield: Advanced Dynamic Graph-Based Malware Detection Using GNNs',
        'author': r'''Eslam Amer, Shaker El-Sappagh, Tamer Abuhamad, Bander Ali Saleh Al-Rimy, and Alaa Mohasseb''',
        'year': '2025',
        'journal': r'''Expert Systems with Applications (Elsevier)''',
        'summary': r'''Proposes \textbf{GraphShield}, an explainable malware detection platform that converts dynamic program execution traces into behavioral interaction graphs. An attention-based GNN captures execution dependencies, while GNNExplainer highlights the exact malicious subgraphs to provide actionable explanations for analysts.''',
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
        'author': r'''Fargana Abdullayeva and Suleyman Suleymanzade''',
        'year': '2024',
        'journal': r'''Results in Control and Optimization (Elsevier)''',
        'summary': r'''Proposes modeling cloud network flows as communication graphs to classify multi-class attacks using GCN and GraphSAGE models. The inductive neighborhood sampling of GraphSAGE allows the model to generalize effectively to newly deployed virtual machines without full-graph retraining.''',
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
        'author': r'''Rana Abu Bakar, Lorenzo De Marinis, Filippo Cugini, and Francesco Paolucci''',
        'year': '2024',
        'journal': r'''Computer Networks (Elsevier)''',
        'summary': r'''Proposes \textbf{FTG-Net-E}, a hierarchical ensemble Graph Neural Network for detecting high-volume DDoS floods and volumetric network attacks. By converting traffic into Flow Traffic Graphs (FTG), a two-level ensemble processes local and global traffic topology, achieving 99.2\% detection precision.''',
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
        'author': r'''Md Shakil Siddique, Md. Ashikur Rahman Khan, Ishtiaq Ahammad, Nishu Nath, Joysri Rani Das, and Fardowsi Rahman''',
        'year': '2025',
        'journal': r'''Franklin Open (Elsevier)''',
        'summary': r'''Proposes an intrusion detection framework for cyber-physical systems combining Generative Adversarial Networks (GAN) and LSTM networks. The GAN synthesizes realistic minority-class attack samples to overcome severe data imbalance, while the LSTM captures sequential temporal patterns in industrial telemetry logs.''',
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
        'author': r'''Ali Yilmaz, Resul Das, Mehmet Ozdem, and Berk Canberk''',
        'year': '2026',
        'journal': r'''Computer Networks (Elsevier)''',
        'summary': r'''Represents network communication as a graph, where IP addresses are nodes and communication flows are edges. Applies GCN, GAT, GIN, and GraphSAGE to detect network anomalies and identify suspicious communication patterns. Provides dynamic attack-topology visualization, helping security analysts understand relationships between network entities and possible attack paths.''',
        'advs': [
            r'''Represents communication between IPs as a graph, making attack connections easier to identify.''',
            r'''GNN models such as GIN and GraphSAGE achieved strong F1 and ROC-AUC results.''',
            r'''Provides attack-topology visualization to help analysts understand attacker--target relationships.'''
        ],
        'diss': [
            r'''Mainly focuses on network-level graph analysis, not live OS-level provenance.''',
            r'''Does not fully address temporal/dynamic graph behaviour.''',
            r'''Streaming graph updates and low-latency deployment need further development.'''
        ]
    },
    # P14
    {
        'num': '14',
        'title': r'Robust, Efficient Detection of Network Intrusion Attacks: A Large Language Model Approach',
        'author': r'''Giancarlo Iannizzotto, Andrea Nucita, and Andrea Siragusa''',
        'year': '2026',
        'journal': r'''Computer Networks (Elsevier)''',
        'summary': r'''Proposes applying transformer language models to network intrusion detection by tokenizing packet byte streams and sequential flow features into discrete vocabularies. Multi-head self-attention learns contextual syntax across packet sequences, providing strong robustness against noise and obfuscation.''',
        'advs': [
            r'''Uses Transformer self-attention to capture sequential dependencies in network traffic.''',
            r'''Shows strong generalization to unseen network topologies and traffic distributions.''',
            r'''Demonstrates robustness to noisy/corrupted network traffic.'''
        ],
        'diss': [
            r'''Large Transformer models can have high memory and computational requirements.''',
            r'''Represents traffic as linear 1D token sequences, so it does not naturally capture multi-hop graph relationships.''',
            r'''Provides limited insight into host-level process execution and disk activity.'''
        ]
    },
    # P15
    {
        'num': '15',
        'title': r'Detection of Advanced Persistent Threat: A Genetic Programming Approach',
        'author': r'''Abdullah Al Mamun, Harith Al-Sahaf, Ian Welch, and Masood Mansoori''',
        'year': '2024',
        'journal': r'''Applied Soft Computing (Elsevier)''',
        'summary': r'''Proposes a multi-tree Genetic Programming (GP) evolutionary approach for detecting APTs in high-dimensional audit logs. By evolving tree-based symbolic feature extractors, it automatically constructs discriminative non-linear features, overcoming severe class imbalance without manual feature engineering.''',
        'advs': [
            r'''Automatically discovers non-linear features without manual feature engineering.''',
            r'''Useful for identifying changing and previously unseen APT patterns.''',
            r'''Evolutionary search can discover different solutions rather than relying only on fixed signatures.'''
        ],
        'diss': [
            r'''GP involves an evolutionary search over many candidate solutions, making it computationally demanding.''',
            r'''Detecting complex, multi-stage APT behaviour remains challenging.''',
            r'''Traditional/ML approaches can struggle when attacker behaviour changes significantly.'''
        ]
    },
    # P16
    {
        'num': '16',
        'title': r'Dynamic Cyber Deception Using AI-Driven Adaptive Honeypot Networks',
        'author': r'''Mohammed Alshehri''',
        'year': '2026',
        'journal': r'''Ain Shams Engineering Journal (Elsevier)''',
        'summary': r'''Proposes an AI-driven dynamic cyber deception platform that deploys adaptive honeypot networks against multi-stage APT campaigns. Using reinforcement learning, it continuously reconfigures decoy services and synthetic vulnerabilities based on attacker probing, diverting adversaries and capturing high-fidelity telemetry.''',
        'advs': [
            r'''Dynamically changes honeypot behaviour according to attacker activity.''',
            r'''Makes deception more difficult for attackers to identify.''',
            r'''Records attacker activities and helps identify their tactics and techniques.'''
        ],
        'diss': [
            r'''Effectiveness depends on attackers interacting with the honeypot environment.''',
            r'''Continuous changes may cause over-reactive or unrealistic behaviour.'''
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
{p['summary']}
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

# Read existing main.tex
with open('main.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Introduction Slide
intro_pattern = r'\\section\{Introduction\}.*?\\end\{frame\}'
new_intro = r'''\section{Introduction}

\begin{frame}{Introduction}
\vspace{0.4em}
{\small
\begin{itemize}\itemsep0.65em
  \item \textbf{Two Types of Cyber Threats:} Organizations face large, fast network attacks (like DDoS) and hidden, slow Advanced Persistent Threats (APTs) that stay inside systems for weeks.

  \item \textbf{Limits of Standard Tools:} Traditional tools look at logs as flat tables, missing how processes, files, and network connections interact over time.

  \item \textbf{Graph-Based Detection:} By representing system actions as activity graphs, Graph Neural Networks (GNNs) can track complex attack steps and detect unknown threats without labeled attack data.

  \item \textbf{Privacy-Preserving Training:} Federated learning with encryption allows multiple organizations to train models together safely without sharing raw private logs.

  \item \textbf{Clear Threat Reporting:} Mapping detected threats directly to the MITRE ATT\&CK framework gives security teams clear and simple explanations of what happened.
\end{itemize}
}
\end{frame}'''

text = re.sub(intro_pattern, new_intro, text, flags=re.DOTALL)

# 2. Update Problem Statement Slide
prob_pattern = r'\\section\{Problem Statement\}.*?\\end\{frame\}'
new_prob = r'''\section{Problem Statement}

\begin{frame}{Problem Statement}
\vspace{1.2em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=1.5em,wd=\textwidth]{block body}
\justifying\normalsize
Existing cybersecurity systems often struggle to detect both common network attacks and stealthy APTs in a single system. APTs can hide within normal activities, while high-volume attacks need fast detection, and data sharing raises privacy concerns. Our system uses network traffic and host logs with a dual-tier spatio-temporal approach to detect threats, protect sensitive data, and provide clear alerts with MITRE ATT\&CK mappings.
\end{beamercolorbox}
\end{frame}'''

text = re.sub(prob_pattern, new_prob, text, flags=re.DOTALL)

# 3. Update Objective Slide
obj_pattern = r'\\section\{Project Objective\}.*?\\end\{frame\}'
new_obj = r'''\section{Project Objective}

\begin{frame}{Project Objective}
\vspace{1.0em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=1.4em,wd=\textwidth]{block body}
\justifying\normalsize
To design and develop a privacy-preserving dual-tier cyber attack detection platform using GCN for fast detection of common network attacks and a Spatio-Temporal Graph Neural Network (ST-GAT + GRU + VGAE) for multi-stage APTs from system activity graphs. The system also uses Federated Learning with CKKS Homomorphic Encryption for secure collaboration and MITRE ATT\&CK mapping for clear and explainable threat analysis.
\end{beamercolorbox}
\end{frame}'''

text = re.sub(obj_pattern, new_obj, text, flags=re.DOTALL)

# 4. Update Research Gaps & Proposed Solutions Slide
rg_pattern = r'\\section\{Research Gap\}.*?\\end\{frame\}'
new_rg = r'''\section{Research Gap}

\begin{frame}{Research Gaps \& Proposed Solutions}
\vspace{-0.2em}
{\fontsize{7.5pt}{9.8pt}\raggedright\selectfont
\begin{itemize}\itemsep0.45em
  \item \textbf{1. Separate Defenses for Network and Host:}\\
  \textbf{Gap:} Current tools check network traffic and host logs separately, missing threats that move between them.\\
  \textbf{Solution:} We build a two-tier system: a fast GCN filters high-volume network floods, and an ST-GNN analyzes host logs for hidden APTs.

  \item \textbf{2. Graph Growth and Loss of Context:}\\
  \textbf{Gap:} System activity graphs grow too large over time, while basic machine learning flattens logs and loses cause-and-effect links.\\
  \textbf{Solution:} We build session-based streaming graphs that prune normal background noise while keeping key process-to-file relationships.

  \item \textbf{3. Dependence on Labeled Attack Data:}\\
  \textbf{Gap:} Most models need labeled attack examples, so they fail to catch new zero-day attacks.\\
  \textbf{Solution:} We train an ST-VGAE model self-supervised on normal activity, flagging any unusual behavior as a potential threat.

  \item \textbf{4. Data Privacy Risks and Alert Overload:}\\
  \textbf{Gap:} Sharing raw logs risks private data leaks, and raw anomaly scores overwhelm security analysts.\\
  \textbf{Solution:} We use encrypted federated learning to train models safely across teams and map threats directly to MITRE ATT\&CK tactics.
\end{itemize}
}
\end{frame}'''

text = re.sub(rg_pattern, new_rg, text, flags=re.DOTALL)

# 5. Update Literature Review (Paper Slides)
all_slides = '\n'.join([make_slide(p) for p in slides_data])

lit_pattern = r'\\section\{Literature Review\}.*?(?=\\section\{Research Gap\})'
new_lit = '\\section{Literature Review}\n\n' + all_slides + '\n%% ======================================================================\n%%  SECTION 5: RESEARCH GAPS\n%% ======================================================================\n'

text = re.sub(lit_pattern, new_lit, text, flags=re.DOTALL)

with open('main.tex', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated main.tex with user requested Problem Statement, Objective, Introduction, Research Gaps, and single-paragraph Paper Summaries!')
