import sys, os, re, subprocess

# Define exactly 16 papers with simplified summaries, simple pros/cons, and clean citations
papers = [
    {
        'num': 1,
        'author': r'Cui, M., Jiang, Z.\ et al.',
        'title': r'MGDA: A Provenance Graph-Based Framework for Threat Detection and Attack Scenario Reconstruction',
        'journal': r'Comput. Netw.\ (Elsevier)',
        'year': '2025',
        'doi': '10.1016/j.comnet.2025.111806',
        'url': 'https://doi.org/10.1016/j.comnet.2025.111806',
        'summary': r'Proposes \textbf{MGDA}, a self-supervised masked graph autoencoder on provenance graphs that learns normal system behavior and detects APT attacks without requiring labeled attack data, reconstructing multi-stage attack scenarios on the DARPA TC benchmark.',
        'advantages': [
            r'Learns from normal behavior without needing labeled attack samples',
            r'Achieves a high 98.03\% F1-score on benchmark datasets',
            r'Reduces graph size while preserving cause-and-effect relationships'
        ],
        'disadvantages': [
            r'Reconstruction relies on fixed rules rather than deep learning',
            r'Evaluates static snapshots without tracking sliding time windows',
            r'Cannot share threat intelligence across organizations privately'
        ]
    },
    {
        'num': 2,
        'author': r'Liu, Q., Bao, K.\ \& Hagenmeyer, V.',
        'title': r'Commander: A Robust Cross-Machine Multi-Phase APT Detector via Provenance Analytics',
        'journal': r'J. Inf. Secur. Appl.\ (Elsevier)',
        'year': '2025',
        'doi': '10.1016/j.jisa.2025.104057',
        'url': 'https://doi.org/10.1016/j.jisa.2025.104057',
        'summary': r'Proposes \textbf{Commander}, a provenance-based detection system that tracks attackers moving across multiple machines and maintaining persistence, using logon-session partitioning to stop dependency explosion.',
        'advantages': [
            r'Accurately tracks lateral movement across multiple network machines',
            r'Prevents graph explosion using session-based execution partitioning',
            r'Resistant to common evasion tactics like session hijacking'
        ],
        'disadvantages': [
            r'Depends on manual rules rather than generalized neural networks',
            r'Requires custom log parsers tailored to specific industrial controllers',
            r'Lacks privacy-preserving federated training across enterprise sites'
        ]
    },
    {
        'num': 3,
        'author': r'Canonico, R., Lista, F.\ et al.',
        'title': r'Threat Detection in Reconfigurable Cyber-Physical Systems Through Spatio-Temporal Anomaly Detection Using Graph Attention Network',
        'journal': r'Comput. Secur.\ (Elsevier)',
        'year': '2025',
        'doi': '10.1016/j.cose.2025.104509',
        'url': 'https://doi.org/10.1016/j.cose.2025.104509',
        'summary': r'Proposes a spatio-temporal framework combining \textbf{Graph Attention Networks (GAT)} for spatial connections and recurrent units for temporal sequence patterns to detect anomalies in multivariate time-series data.',
        'advantages': [
            r'Attention mechanism automatically learns the most important connections',
            r'Simultaneously models spatial graph structure and time-based changes',
            r'Reduces memory usage by 77.8\% and training time by 21\%'
        ],
        'disadvantages': [
            r'Built for continuous sensor values rather than discrete OS event logs',
            r'Does not use a variational autoencoder (VGAE) for graph reconstruction',
            r'Centralized model without collaborative federated learning'
        ]
    },
    {
        'num': 4,
        'author': r'Isaac, O., Appiah, B.\ et al.',
        'title': r'EdgeFence: Federated Temporal Graph Neural Networks for Lightweight, Adversarial Malware Detection in Distributed Edge Networks',
        'journal': r'Int. J. Inf. Secur.\ (Springer)',
        'year': '2026',
        'doi': '10.1007/s10207-026-01237-x',
        'url': 'https://doi.org/10.1007/s10207-026-01237-x',
        'summary': r'Proposes \textbf{EdgeFence}, a federated learning architecture where distributed edge nodes train local Temporal Graph Neural Networks on system calls and exchange only model weights via FedAvg to maintain data privacy.',
        'advantages': [
            r'Protects data privacy by sharing model parameters instead of raw logs',
            r'Captures time-based sequence changes in system interaction graphs',
            r'Shows high resistance against adversarial evasion and poisoning attacks'
        ],
        'disadvantages': [
            r'Sends unencrypted model updates, vulnerable to gradient leakage',
            r'Tested on mobile/edge malware rather than enterprise OS audit logs',
            r'Uses supervised classification that cannot detect unknown zero-day attacks'
        ]
    },
    {
        'num': 5,
        'author': r'Gandhi, P.\ A., Wudali, P.\ N.\ et al.',
        'title': r'SHIELD: Advanced Persistent Threats Detection and Intelligent Explanation Using Large Language Models',
        'journal': r'Eng. Appl. Artif. Intell.\ (Elsevier)',
        'year': '2026',
        'doi': '10.1016/j.engappai.2026.115443',
        'url': 'https://doi.org/10.1016/j.engappai.2026.115443',
        'summary': r'Proposes \textbf{SHIELD}, combining provenance graph anomaly detection with Large Language Models (LLMs) to isolate suspicious subgraphs, generate plain-English attack summaries, and map activities to MITRE ATT\&CK techniques.',
        'advantages': [
            r'Generates easy-to-understand attack narratives for security analysts',
            r'Directly maps detected actions to MITRE ATT\&CK tactics and techniques',
            r'Combines graph anomaly detection with high-level contextual reasoning'
        ],
        'disadvantages': [
            r'High computation cost and latency of LLMs hinder real-time log analysis',
            r'Risk of incorrect or hallucinated explanations during complex investigations',
            r'Does not support privacy-preserving collaborative learning across organizations'
        ]
    },
    {
        'num': 6,
        'author': r'Ferazza, F., Melella, C.\ et al.',
        'title': r'From Logs to Tactics: Unsupervised Reconstruction of APT Campaigns with MITRE-Enriched Meta-Alerts',
        'journal': r'Int. J. Inf. Secur.\ (Springer)',
        'year': '2026',
        'doi': '10.1007/s10207-026-01254-w',
        'url': 'https://doi.org/10.1007/s10207-026-01254-w',
        'summary': r'Proposes an unsupervised framework using Graph Neural Networks and semantic clustering to reconstruct full APT attack steps from noisy system logs, achieving an 87\% F1-score in automatic MITRE ATT\&CK mapping.',
        'advantages': [
            r'GNN sequence modeling connects attack steps better than simple timestamps',
            r'Achieves 87\% F1-score mapping alerts to MITRE ATT\&CK techniques',
            r'Tested on noisy, real-world data from NATO cyber defense exercises'
        ],
        'disadvantages': [
            r'Multi-step offline clustering is too slow for real-time attack prevention',
            r'Focuses on investigating past alerts rather than early threat prediction',
            r'Lacks encrypted federated learning for multi-company collaboration'
        ]
    },
    {
        'num': 7,
        'author': r'Kim, G., Lee, S.\ \& Kim, S.',
        'title': r'A Novel Hybrid Intrusion Detection Method Integrating Anomaly Detection with Misuse Detection',
        'journal': r'Expert Syst. Appl.\ (Elsevier)',
        'year': '2014',
        'doi': '10.1016/j.eswa.2013.08.066',
        'url': 'https://doi.org/10.1016/j.eswa.2013.08.066',
        'summary': r'Proposes a two-tier hybrid architecture where a misuse detection model quickly filters known attacks, and multiple anomaly detection models profile normal behavior to catch new and unknown attacks.',
        'advantages': [
            r'Combines fast detection of known attacks with discovery of new threats',
            r'Reduces false alarms by separating known attack patterns from normal profiles',
            r'Cuts training time by 50\% compared to single monolithic models'
        ],
        'disadvantages': [
            r'Uses older algorithms (Decision Trees and One-Class SVM) on flat tables',
            r'Cannot model complex graph relationships or OS system call chains',
            r'Lacks time-series sequence modeling and federated learning'
        ]
    },
    {
        'num': 8,
        'author': r'Diao, H., Qin, Z.\ et al.',
        'title': r'Self-Supervised Graph Neural Networks for Network Intrusion Detection in Cloud-Edge',
        'journal': r'J. Cloud Comput.\ (Springer)',
        'year': '2026',
        'doi': '10.1186/s13677-026-00847-z',
        'url': 'https://doi.org/10.1186/s13677-026-00847-z',
        'summary': r'Proposes a self-supervised contrastive GNN framework for cloud-edge network intrusion detection that learns topological representations from unlabeled traffic graphs, overcoming the scarcity of labeled attack data.',
        'advantages': [
            r'Eliminates the need for expensive manually labeled attack datasets',
            r'Captures complex network communication topologies at cloud-edge boundaries',
            r'Performs better than standard supervised models when attack data is limited'
        ],
        'disadvantages': [
            r'Monitors only network traffic; completely blind to host OS process causality',
            r'Contrastive data augmentation requires high computation during training',
            r'Lacks homomorphic encryption to protect representations across sites'
        ]
    },
    {
        'num': 9,
        'author': r'Amer, E., El-Sappagh, S.\ et al.',
        'title': r'GraphShield: Advanced Dynamic Graph-Based Malware Detection Using Graph Neural Networks',
        'journal': r'Expert Syst. Appl.\ (Elsevier)',
        'year': '2025',
        'doi': '10.1016/j.eswa.2025.129812',
        'url': 'https://doi.org/10.1016/j.eswa.2025.129812',
        'summary': r'Proposes \textbf{GraphShield}, building dynamic behavioral graphs from program execution traces and applying attention-based GNNs with GNNExplainer to accurately classify malware and explain malicious actions.',
        'advantages': [
            r'Captures live program behavior through rich entity interaction graphs',
            r'Uses GNNExplainer to highlight key malicious subgraphs for analysts',
            r'Achieves significantly higher accuracy than traditional tabular ML models'
        ],
        'disadvantages': [
            r'Supervised training requires labeled malware and fails on novel zero-days',
            r'Analyzes isolated program sandboxes rather than continuous enterprise logs',
            r'Lacks sliding-window temporal tracking and federated privacy'
        ]
    },
    {
        'num': 10,
        'author': r'Abdullayeva, F.\ \& Suleymanzade, S.',
        'title': r'Cyber Security Attack Recognition on Cloud Computing Networks Based on GCN and GraphSAGE Models',
        'journal': r'Results Control Optim.\ (Elsevier)',
        'year': '2024',
        'doi': '10.1016/j.rico.2024.100423',
        'url': 'https://doi.org/10.1016/j.rico.2024.100423',
        'summary': r'Proposes modeling cloud network flows as graphs to classify attacks using GCN and inductive GraphSAGE models, evaluated on the CSE-CIC-IDS2018 dataset to scale across cloud virtual machines.',
        'advantages': [
            r'Captures communication patterns between virtual machines missed by flat flows',
            r'GraphSAGE generalizes well to newly created cloud machines without retraining',
            r'Rigorously tested on the realistic CSE-CIC-IDS2018 cloud dataset'
        ],
        'disadvantages': [
            r'Limited strictly to network flows; cannot see host process/file activities',
            r'Static graph structure ignores how attacks unfold sequentially over time',
            r'Cannot detect zero-day attacks that lack prior training labels'
        ]
    },
    {
        'num': 11,
        'author': r'Abu Bakar, R., Al-Naymat, G.\ et al.',
        'title': r'FTG-Net-E: A Hierarchical Ensemble Graph Neural Network for DDoS Attack Detection',
        'journal': r'Comput. Netw.\ (Elsevier)',
        'year': '2024',
        'doi': '10.1016/j.comnet.2024.110508',
        'url': 'https://doi.org/10.1016/j.comnet.2024.110508',
        'summary': r'Proposes \textbf{FTG-Net-E}, a hierarchical ensemble graph neural network that analyzes network flow topologies to rapidly detect and stop high-volume DDoS floods and volumetric attacks.',
        'advantages': [
            r'Specialized for rapid detection of high-volume DDoS and flood attacks',
            r'Hierarchical ensemble structure achieves near-perfect precision (99.2\%)',
            r'Ideal design for frontline filtering of conventional high-rate network attacks'
        ],
        'disadvantages': [
            r'Ineffective against stealthy, low-and-slow APT intrusions inside hosts',
            r'Does not monitor operating system events or system call relationships',
            r'Lacks unsupervised anomaly scoring and encrypted federated learning'
        ]
    },
    {
        'num': 12,
        'author': r'Siddique, M.\ S., Khan, M.\ et al.',
        'title': r'Intelligent Intrusion Detection for Cyber-Physical Systems Using GAN-LSTM',
        'journal': r'Front. Artif. Intell.',
        'year': '2025',
        'doi': '10.1016/j.fraope.2025.100281',
        'url': 'https://doi.org/10.1016/j.fraope.2025.100281',
        'summary': r'Proposes combining Generative Adversarial Networks (GAN) to generate realistic synthetic attack samples with LSTM recurrent networks to learn temporal sequential patterns in cyber-physical system logs.',
        'advantages': [
            r'Solves severe class imbalance by generating realistic synthetic attack data',
            r'LSTM effectively captures long-term sequential dependencies in event streams',
            r'Improves detection accuracy on complex time-dependent attack patterns'
        ],
        'disadvantages': [
            r'GAN training is complex and prone to mode collapse or unrealistic data',
            r'Processes flat 1D time sequences without spatial graph connections',
            r'Cannot construct causal provenance graphs or map to MITRE ATT\&CK'
        ]
    },
    {
        'num': 13,
        'author': r'Yilmaz, A., Sen, S.\ et al.',
        'title': r'Knowledge Graph Visualization and Anomaly Detection Using Graph Neural Networks',
        'journal': r'Comput. Netw.\ (Elsevier)',
        'year': '2026',
        'doi': '10.1016/j.comnet.2026.112632',
        'url': 'https://doi.org/10.1016/j.comnet.2026.112632',
        'summary': r'Proposes building heterogeneous Cyber Threat Intelligence (CTI) knowledge graphs linking vulnerabilities, adversary groups, and attack techniques, using GNNs to discover anomalies and visualize threats for SOC analysts.',
        'advantages': [
            r'Connects disparate threat intelligence data (CVEs, malware, tactics) into one graph',
            r'Interactive visualization helps security analysts quickly assess complex threats',
            r'GNN link prediction uncovers hidden relationships between security indicators'
        ],
        'disadvantages': [
            r'Operates on high-level intelligence reports rather than live OS kernel logs',
            r'Relies on pre-compiled threat feeds instead of real-time zero-day detection',
            r'Lacks time-series sequence tracking and encrypted federated learning'
        ]
    },
    {
        'num': 14,
        'author': r'Iannizzotto, G., Nucita, A.\ \& Siragusa, A.',
        'title': r'Robust, Efficient Detection of Network Intrusion Attacks: A Large Language Model Approach',
        'journal': r'Comput. Netw.\ (Elsevier)',
        'year': '2026',
        'doi': '10.1016/j.comnet.2026.112559',
        'url': 'https://doi.org/10.1016/j.comnet.2026.112559',
        'summary': r'Proposes converting network packet payloads and flow sequences into text-like tokens, applying pre-trained transformer self-attention to accurately classify network attacks even in noisy conditions.',
        'advantages': [
            r'Self-attention captures complex non-linear patterns in packet payload bytes',
            r'High robustness against noisy, corrupted, or obfuscated network packet headers',
            r'Generalizes well across multiple distinct types of conventional network attacks'
        ],
        'disadvantages': [
            r'Large transformer models require heavy compute memory, causing high latency',
            r'Treats traffic as 1D linear tokens, missing multi-hop graph causality',
            r'Provides limited insight into host-level process execution and disk activity'
        ]
    },
    {
        'num': 15,
        'author': r'Al Mamun, A.\ \& Al-Sahaf, H.\ et al.',
        'title': r'Detection of Advanced Persistent Threat: A Genetic Programming Approach',
        'journal': r'Appl. Soft Comput.\ (Elsevier)',
        'year': '2024',
        'doi': '10.1016/j.asoc.2024.112447',
        'url': 'https://doi.org/10.1016/j.asoc.2024.112447',
        'summary': r'Proposes using multi-tree Genetic Programming (GP) to automatically create effective non-linear feature combinations from high-dimensional audit logs, successfully detecting APTs under severe class imbalance.',
        'advantages': [
            r'Automatically discovers non-linear features without manual feature engineering',
            r'Handles extreme class imbalance where normal events heavily outnumber attacks',
            r'Evolved mathematical feature trees can be inspected by security experts'
        ],
        'disadvantages': [
            r'Flattens audit logs into tables, losing graph causality between processes and files',
            r'Evolutionary search is very slow, requiring multiple hours to train',
            r'Cannot model time-series progression across sliding windows like ST-GNN'
        ]
    },
    {
        'num': 16,
        'author': r'Alshehri, M.',
        'title': r'Dynamic Cyber Deception Using AI-Driven Adaptive Honeypot Networks',
        'journal': r'Ain Shams Eng. J.\ (Elsevier)',
        'year': '2026',
        'doi': '10.1016/j.asej.2026.104061',
        'url': 'https://doi.org/10.1016/j.asej.2026.104061',
        'summary': r'Proposes using AI-driven dynamic honeypots that adapt decoy surfaces in real time to lure attackers away from critical assets, gathering valuable logs on stealthy multi-stage APT tactics.',
        'advantages': [
            r'Actively traps stealthy attackers during reconnaissance and lateral movement',
            r'Gathers pure, high-quality attacker logs without normal user noise',
            r'Dynamically reconfigures decoy services to keep attackers engaged longer'
        ],
        'disadvantages': [
            r'Requires attackers to interact directly with decoys; cannot inspect production hosts',
            r'Does not provide real-time anomaly detection for legitimate enterprise workloads',
            r'Lacks graph neural networks, causal provenance modeling, and federated privacy'
        ]
    }
]

def generate_tex():
    tex = r'''% ============================================================
%  Cyber Attack Prediction Platform -- ST-GNN (Group 14, CEK)
%  B.Tech Project Presentation
%  Compile: pdflatex main.tex  (run twice)
% ============================================================
\documentclass[aspectratio=169,10pt]{beamer}
\usetheme{Madrid}
\usecolortheme{default}
\usefonttheme{professionalfonts}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{booktabs}
\usepackage{tikz}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{ragged2e}
\usetikzlibrary{arrows.meta,positioning,fit,backgrounds,calc,shadows}

\definecolor{prismNavy}{RGB}{13,29,54}
\definecolor{prismBlue}{RGB}{38,126,190}
\definecolor{prismTeal}{RGB}{28,161,157}
\definecolor{prismMint}{RGB}{224,247,242}
\definecolor{prismGold}{RGB}{229,166,50}

\setbeamercolor{structure}{fg=prismBlue}
\setbeamercolor{frametitle}{bg=prismNavy,fg=white}
\setbeamercolor{block title}{bg=prismBlue,fg=white}
\setbeamercolor{block body}{bg=prismMint,fg=black}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{author in head/foot}{bg=prismNavy,fg=white}
\setbeamercolor{title in head/foot}{bg=prismBlue,fg=white}
\setbeamercolor{date in head/foot}{bg=prismNavy,fg=white}
\setbeamertemplate{footline}{%
  \leavevmode\hbox{%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
    \usebeamerfont{author in head/foot}Group 14 (CEK)\end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
    \usebeamerfont{title in head/foot}B.Tech Project\end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
    \usebeamerfont{date in head/foot}\insertdate\hspace*{2em}\insertframenumber{}/\inserttotalframenumber\hspace*{2ex}\end{beamercolorbox}}%
  \vskip0pt}
\setbeamertemplate{itemize item}{\color{prismTeal}$\blacktriangleright$}
\setbeamersize{text margin left=0.5cm,text margin right=0.5cm}

\setbeamertemplate{frametitle}{%
  \nointerlineskip%
  \begin{beamercolorbox}[wd=\paperwidth,ht=1.15cm,dp=0pt,leftskip=0.5cm,rightskip=0.5cm]{frametitle}%
    \vbox to 1.15cm{%
      \vfill%
      \raggedright\fontsize{11.5pt}{14pt}\selectfont\textbf{\insertframetitle}%
      \vfill%
    }%
  \end{beamercolorbox}%
}

\title[Cyber Attack Prediction Platform]{CYBER ATTACK PREDICTION PLATFORM USING SPATIO-TEMPORAL GRAPH NEURAL NETWORKS}
\subtitle{Integrating Spatio-Temporal Graph Neural Networks with Federated Privacy for Dual-Tier Threat Detection}
\author{Muhammed Nasih K P \and Sumayya Ershad \and Najmunniza N \and K.S.\ Mahadev}
\institute{Dept.\ of Computer Science \& Engineering, College of Engineering, Karunagappally}
\date{\today}

\begin{document}

%% ---- TITLE SLIDE ---------------------------------------------------------
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
  % Top Title Banner
  \node[rounded corners=4pt,fill=prismBlue,drop shadow={shadow xshift=2pt,shadow yshift=-2pt,opacity=.35},
        minimum width=15.4cm,minimum height=1.15cm]
        at ([yshift=-0.85cm]current page.north) {};
  \node[text=white,font=\fontsize{12}{14}\selectfont\bfseries,align=center]
        at ([yshift=-0.85cm]current page.north) {CYBER ATTACK PREDICTION PLATFORM USING\\[0.08cm]
        SPATIO-TEMPORAL GRAPH NEURAL NETWORKS};

  % Bottom Footer
  \fill[prismNavy] (current page.south west) rectangle ([yshift=.45cm]current page.south east);
  \fill[prismBlue] ([xshift=5.33cm]current page.south west)
                    rectangle ([xshift=10.66cm,yshift=.45cm]current page.south west);
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=2.66cm,yshift=.22cm]current page.south west) {Group 14 (CEK)};
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=8cm,yshift=.22cm]current page.south west) {B.Tech Project};
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=13.2cm,yshift=.22cm]current page.south west)
        {\today\hspace{1.2cm}1/\inserttotalframenumber};

  % 1. Logo
  \node at ([yshift=6.85cm]current page.south)
        {\includegraphics[height=1.15cm]{cek-logo.png}};

  % 2. Department & College
  \node[font=\footnotesize,align=center,text=prismNavy]
        at ([yshift=5.75cm]current page.south)
        {\textbf{Dept.\ of Computer Science \& Engineering}\\[.04cm]
         \textbf{College of Engineering, Karunagappally}};

  % 3. Guide Info
  \node[font=\small,align=center]
        at ([yshift=4.55cm]current page.south)
        {Under the Guidance of\\[.08cm]
         \textbf{\large  Mrs SYAMA S R}\\[.04cm]
         Assistant Professor};

  % 4. Project Group 14
  \node[font=\large\bfseries,text=prismBlue]
        at ([yshift=3.40cm]current page.south) {Project Group 14};

  % 5. Members Table
  \node[font=\small]
        at ([yshift=1.85cm]current page.south)
        {\begin{tabular}{r@{\quad}l}
           \textbf{MUHAMMED NASIH K P} & \textbf{(KNP23CS074)} \\
           \textbf{SUMAYYA ERSHAD}     & \textbf{(KNP23CS107)} \\
           \textbf{NAJMUNNIZA N}       & \textbf{(LKNP20CS056)} \\
           \textbf{K.S.\ MAHADEV}      & \textbf{(KNP23CS066)}
         \end{tabular}};
\end{tikzpicture}
\end{frame}

%% ---- ROADMAP -------------------------------------------------------------
\begin{frame}{Presentation Roadmap}\tableofcontents\end{frame}

%% ---- INTRODUCTION --------------------------------------------------------
\section{Introduction}
\begin{frame}{Introduction}
\vspace{0.1em}
\begin{itemize}\itemsep0.75em\small
  \item \textbf{Advanced Persistent Threats (APTs):} Stealthy, multi-stage cyber attacks that establish persistence and move laterally across enterprise networks over weeks or months, evading traditional perimeter defenses like Snort and Suricata.

  \item \textbf{Limitations of Traditional Detection:} Conventional machine learning flattens logs into isolated tabular rows and misses the structural and causal relationships between system processes, files, and network sockets.

  \item \textbf{Spatio-Temporal Graph Modeling:} Our platform models operating system audit logs as dynamic provenance graphs, using Spatio-Temporal Graph Neural Networks (GAT + GRU + VGAE) for self-supervised detection of zero-day attacks without requiring labeled data.

  \item \textbf{Privacy-Preserving Collaboration \& Attribution:} Integrates Federated Learning with CKKS Homomorphic Encryption (TenSEAL) to securely train models across organizations without sharing private data, mapping threat subgraphs directly to MITRE ATT\&CK tactics.
\end{itemize}
\end{frame}

%% ---- OBJECTIVES ----------------------------------------------------------
\section{Objectives}
\begin{frame}{Objectives}
\small
\begin{itemize}\itemsep0.35em
  \item \textbf{Construct Dynamic Provenance Graphs from System Logs}
    \begin{itemize}\setlength{\itemsep}{0.1em}\footnotesize
      \item Ingest OS audit logs (Sysmon/auditd) and network events to model causal interactions between processes, files, and sockets.
    \end{itemize}

  \item \textbf{Develop a Unified Spatio-Temporal Autoencoder (ST-VGAE) for APT Detection}
    \begin{itemize}\setlength{\itemsep}{0.1em}\footnotesize
      \item Integrate Graph Attention (GAT) for spatial structure and Recurrent Units (GRU) for temporal evolution inside a Variational Graph Autoencoder (VGAE).
      \item Train self-supervised on benign system behavior to detect zero-day APTs via reconstruction error without requiring labeled attack data.
    \end{itemize}

  \item \textbf{Enable Privacy-Preserving Collaborative Federated Learning}
    \begin{itemize}\setlength{\itemsep}{0.1em}\footnotesize
      \item Secure multi-organization model training using FedAvg combined with CKKS Homomorphic Encryption (TenSEAL) to prevent raw log and gradient leakage.
    \end{itemize}

  \item \textbf{Automate Threat Attribution via MITRE ATT\&CK Mapping}
    \begin{itemize}\setlength{\itemsep}{0.1em}\footnotesize
      \item Map detected anomalous subgraphs directly to standard MITRE ATT\&CK tactics to provide explainable attack narratives for security analysts.
    \end{itemize}

  \item \textbf{Deploy an Interactive SOC Dashboard and Benchmark Real-World Performance}
    \begin{itemize}\setlength{\itemsep}{0.1em}\footnotesize
      \item Implement a containerized FastAPI backend with a real-time visualization UI, evaluated on the DARPA Transparent Computing benchmark.
    \end{itemize}
\end{itemize}
\end{frame}

%% ---- PROBLEM STATEMENT ---------------------------------------------------
\section{Problem Statement}
\begin{frame}{Problem Statement}
\vspace{0.8em}

\begin{beamercolorbox}[rounded=true,shadow=false,sep=1.2em,wd=\textwidth]{block body}
\justifying\small
To design and develop an intelligent, privacy-preserving cyber attack prediction platform that models enterprise audit logs and network flows as dynamic provenance graphs, employing a dual-tier hybrid architecture combining a frontline classifier for high-rate network intrusions with an unsupervised \textbf{Spatio-Temporal Graph Attention Network Autoencoder (ST-GAT + GRU + VGAE)} to detect stealthy, multi-stage \textbf{Advanced Persistent Threats (APTs)} and zero-day attacks without requiring labeled data, while integrating \textbf{Federated Learning with CKKS Homomorphic Encryption (TenSEAL)} for secure cross-organization collaboration, delivering real-time anomaly scores, interactive attack subgraphs, and \textbf{MITRE ATT\&CK} technique mappings on a containerized SOC dashboard.
\end{beamercolorbox}
\end{frame}

%% ---- LITERATURE REVIEW ---------------------------------------------------
\section{Literature Review}

%% Table header macro with "Citation" instead of "Citation & Paper Link"
\newcommand{\lrhdr}{%
  \rowcolor{prismNavy}%
  {\scriptsize\textcolor{white}{\textbf{Citation}}} &
  {\scriptsize\textcolor{white}{\textbf{Paper Summary}}} &
  {\scriptsize\textcolor{white}{\textbf{Key Advantages \& Disadvantages}}} \\}

'''

    # Build the 16 paper review slides with full paper title and clean citation column
    for p in papers:
        num = p['num']
        author = p['author']
        title = p['title']
        journal = p['journal']
        year = p['year']
        summary = p['summary']
        advs = '\n'.join([r'\textbullet~' + a + r'\newline' for a in p['advantages'][:-1]] + [r'\textbullet~' + p['advantages'][-1]])
        diss = '\n'.join([r'\textbullet~' + d + r'\newline' for d in p['disadvantages'][:-1]] + [r'\textbullet~' + p['disadvantages'][-1]])

        # Clean citation column: Author names, year of publication, journal name
        cite_col = (
            f"\\begin{{minipage}}[t][5.92cm][t]{{\\linewidth}}\n"
            f"\\scriptsize\n"
            f"\\textbf{{Author:}} {author}\\par\\vspace{{4pt}}\n"
            f"\\textbf{{Year:}} {year}\\par\\vspace{{4pt}}\n"
            f"\\textbf{{Journal:}} {journal}\n"
            f"\\end{{minipage}}"
        )

        summary_col = (
            f"\\begin{{minipage}}[t][5.92cm][t]{{\\linewidth}}\n"
            f"\\footnotesize {summary}\n"
            f"\\end{{minipage}}"
        )

        adv_dis_col = (
            f"\\begin{{minipage}}[t][5.92cm][t]{{\\linewidth}}\n"
            f"\\footnotesize\n"
            f"\\textcolor{{green!55!black}}{{\\textbf{{Advantages:}}}}\\newline\n"
            f"{advs}\\par\\vspace{{3pt}}\n"
            f"\\textcolor{{red!65!black}}{{\\textbf{{Disadvantages:}}}}\\newline\n"
            f"{diss}\n"
            f"\\end{{minipage}}"
        )

        tex += f'''%% Paper Review {num}
\\begin{{frame}}[t]{{\\normalsize\\textbf{{{title}}}}}
\\vspace{{-0.35em}}
{{\\footnotesize\\setlength{{\\tabcolsep}}{{3.5pt}}\\renewcommand{{\\arraystretch}}{{1.15}}
\\begin{{tabularx}}{{\\textwidth}}{{|>{{\\raggedright\\arraybackslash}}p{{3.40cm}}|>{{\\raggedright\\arraybackslash}}X|>{{\\raggedright\\arraybackslash}}p{{5.50cm}}|}}
\\hline
\\lrhdr
\\hline
{cite_col}
&
{summary_col}
&
{adv_dis_col} \\\\
\\hline
\\end{{tabularx}}}}
\\end{{frame}}

'''

    # Research Gap (Shortened & Punchy), System Architecture, Gantt Chart (SDLC Ordered), Single-Column References, Thanks
    tex += r'''%%% ---- RESEARCH GAP --------------------------------------------------------
\section{Research Gap}
\begin{frame}{Research Gap \& Technical Motivation}
\vspace{0.4em}
\begin{itemize}\itemsep0.65em\small
    \item \textbf{Dichotomy in Threat Detection:}
    Current systems detect either network floods or host APTs separately. None combine fast network filtering with deep host provenance in a unified dual-tier platform.

    \item \textbf{Loss of Causal Context:}
    Standard machine learning models flatten logs into tabular rows, losing the operating system cause-and-effect chain ($process \rightarrow file \rightarrow socket$).

    \item \textbf{Heavy Reliance on Labeled Attack Data:}
    Supervised models fail on novel zero-day APT campaigns. Self-supervised learning on normal system activities is essential to catch unknown intrusions.

    \item \textbf{Privacy Barriers in Collaborative Defense:}
    Enterprises cannot share sensitive raw audit logs, and standard federated learning leaks gradient data without homomorphic encryption protection.

    \item \textbf{Alert Fatigue \& Lack of Attribution:}
    Most anomaly detectors produce raw numbers without context. Security analysts need visual attack graphs mapped directly to the MITRE ATT\&CK matrix.
\end{itemize}
\end{frame}


%%% ---- WORK PLAN & GANTT CHART (SYSTEM LIFE CYCLE ORDER) -------------------
\section{Work Plan \& Gantt Chart}
\begin{frame}{Project Work Plan \& Gantt Chart (System Life Cycle)}
\vspace{-0.15em}
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  x=1.55cm, y=0.72cm,
  done/.style ={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                font=\fontsize{5.2}{6}\selectfont\bfseries\color{white},
                fill=prismNavy!85!black},
  now/.style  ={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                font=\fontsize{5.2}{6}\selectfont\bfseries\color{white},
                fill=prismGold!90!black,
                draw=prismGold, line width=0.8pt},
  future/.style={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                font=\fontsize{5.2}{6}\selectfont\bfseries\color{white!70!gray},
                fill=gray!35},
  hdr/.style={font=\fontsize{6.5}{7.5}\selectfont\bfseries, text=prismNavy},
  lbl/.style={font=\fontsize{6.5}{7.5}\selectfont, text=black, anchor=east},
  gl/.style={draw=gray!22, line width=0.4pt},
  stripe/.style={fill=prismMint!55}
]

%% alternating row stripes
\foreach \r in {1,3,5,7,9} {
  \fill[stripe] (-4.3,\r-0.5) rectangle (9.05,\r+0.5);
}

%% vertical month grid lines & headers (Jul'26=0 ... Mar'27=8)
\foreach \col/\mo in {
  0/{Jul'26}, 1/{Aug'26}, 2/{Sep'26}, 3/{Oct'26}, 4/{Nov'26},
  5/{Dec'26}, 6/{Jan'27}, 7/{Feb'27}, 8/{Mar'27}
} {
  \draw[gl] (\col, 0.5) -- (\col, 10.5);
  \node[hdr] at (\col+0.5, 10.85) {\mo};
}
\draw[gl] (9.0, 0.5) -- (9.0, 10.5);

%% top & bottom rules
\draw[prismNavy, line width=1.0pt] (-4.3, 10.5) -- (9.05, 10.5);
\draw[prismNavy, line width=0.5pt] (-4.3, 0.5)  -- (9.05, 0.5);

%% TODAY line (Sep 2026)
\draw[prismGold!80!orange, line width=1.4pt, dashed] (2.23, 0.5) -- (2.23, 10.5);
\node[font=\fontsize{5.2}{6}\selectfont\bfseries, text=prismGold!80!orange,
      rotate=90, anchor=south] at (2.23, 9.2) {Today};

%% ---- SYSTEM LIFE CYCLE ORDERLY PHASES (Top to Bottom: Phase 1 to 9)
%% Row 9: Phase 1 - Planning & Problem Identification
\node[lbl] at (-0.12, 9) {1. Planning \& Problem Identification};
\node[done, minimum width=1.55cm] at (0.775, 9) {\checkmark\ Completed};

%% Row 8: Phase 2 - Requirement Analysis & Feasibility Study
\node[lbl] at (-0.12, 8) {2. Requirement Analysis \& Feasibility Study};
\node[now, minimum width=1.55cm] at (2.20, 8) {$\blacktriangleright$ In Progress};

%% Row 7: Phase 3 - System Architecture \& Graph Schema Design
\node[lbl] at (-0.12, 7) {3. System Architecture \& Graph Schema Design};
\node[future, minimum width=1.55cm] at (3.275, 7) {Upcoming};

%% Row 6: Phase 4 - Data Ingestion \& Benchmark Preparation
\node[lbl] at (-0.12, 6) {4. Data Ingestion \& Benchmark Preparation};
\node[future, minimum width=1.55cm] at (4.275, 6) {Upcoming};

%% Row 5: Phase 5 - ST-GNN Core Model Implementation};
\node[lbl] at (-0.12, 5) {5. ST-GNN Core Model Implementation};
\node[future, minimum width=1.55cm] at (5.275, 5) {Upcoming};

%% Row 4: Phase 6 - Privacy \& Federated Learning (CKKS)};
\node[lbl] at (-0.12, 4) {6. Privacy \& Federated Learning (CKKS)};
\node[future, minimum width=1.55cm] at (6.275, 4) {Upcoming};

%% Row 3: Phase 7 - SOC Prototype Deployment \& ATT\&CK Mapping
\node[lbl] at (-0.12, 3) {7. SOC Prototype Deployment \& ATT\&CK Mapping};
\node[future, minimum width=1.55cm] at (7.275, 3) {Upcoming};

%% Row 2: Phase 8 - System Testing, Verification \& Benchmarking
\node[lbl] at (-0.12, 2) {8. System Testing, Verification \& Benchmarking};
\node[future, minimum width=1.20cm] at (7.90, 2) {Upcoming};

%% Row 1: Phase 9 - Final Documentation \& Capstone Defense
\node[lbl] at (-0.12, 1) {9. Final Documentation \& Capstone Defense};
\node[future, minimum width=1.55cm] at (8.275, 1) {Upcoming};

\end{tikzpicture}%
}
\vspace{0.10em}
\begin{center}
\fontsize{6.5}{8}\selectfont
{\color{prismNavy!85!black}$\blacksquare$}~\textbf{Completed}\qquad
{\color{prismGold!90!black}$\blacksquare$}~\textbf{In Progress (Now)}\qquad
{\color{gray!55}$\blacksquare$}~\textbf{Upcoming}\qquad
{\color{prismGold!80!orange}$\boldsymbol{|}$}~\textbf{Current Milestone}
\end{center}
\end{frame}

%%% ---- REFERENCES (SINGLE-COLUMN CLEAN LIST ACROSS 2 PAGES) ----------------
\section{References}
\begin{frame}[t]{References}
\vspace{-0.2em}
\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item[\textbf{[1]}] \textbf{M. Cui, Z. Jiang, S. Li, C. Ma, K. Zhang, P. Yang, and H. Feng}, ``MGDA: A provenance graph-based framework for threat detection and attack scenario reconstruction,'' \textit{Computer Networks}, vol. 274, p. 111806, 2025.
  
  \item[\textbf{[2]}] \textbf{Q. Liu, K. Bao, and V. Hagenmeyer}, ``Commander: A robust cross-machine multi-phase Advanced Persistent Threat detector via provenance analytics,'' \textit{Journal of Information Security and Applications}, vol. 91, p. 104057, 2025.
  
  \item[\textbf{[3]}] \textbf{R. Canonico, F. Lista, A. Navarro, G. Sperl\'i, and A. Vignali}, ``Threat detection in reconfigurable Cyber--Physical Systems through Spatio-Temporal Anomaly Detection using graph attention network,'' \textit{Computers \& Security}, vol. 156, p. 104509, 2025.
  
  \item[\textbf{[4]}] \textbf{O. Isaac, B. Appiah, D. Commey, K. Owusu-Agyemang, M. Asante, and B. H. Acquah}, ``EdgeFence: Federated Temporal Graph Neural Networks for Lightweight, Adversarial Malware Detection in Distributed Edge Networks,'' \textit{International Journal of Information Security}, vol. 25, p. 88, 2026.
  
  \item[\textbf{[5]}] \textbf{P. A. Gandhi, P. N. Wudali, Y. Amaru, A. Shukla, Y. Elovici, and A. Shabtai}, ``SHIELD: Advanced persistent threats detection and intelligent explanation using large language models,'' \textit{Engineering Applications of Artificial Intelligence}, vol. 181, p. 115443, 2026.
  
  \item[\textbf{[6]}] \textbf{F. Ferazza, C. Melella, K. Mersinas, R. Lugo, and R. Ottis}, ``From logs to tactics: unsupervised reconstruction of APT campaigns with MITRE-enriched meta-alerts,'' \textit{International Journal of Information Security}, vol. 25, p. 79, 2026.
  
  \item[\textbf{[7]}] \textbf{G. Kim, S. Lee, and S. Kim}, ``A novel hybrid intrusion detection method integrating anomaly detection with misuse detection,'' \textit{Expert Systems with Applications}, vol. 41, no. 4, pp. 1690--1700, 2014.
  
  \item[\textbf{[8]}] \textbf{H. Diao, Z. Qin, Y. Ding, J. Zhang, and X. Shen}, ``Self-supervised graph neural networks for network intrusion detection in cloud-edge,'' \textit{Journal of Cloud Computing}, vol. 15, no. 1, p. 24, 2026.
\end{itemize}
\end{frame}

\begin{frame}[t]{References}
\vspace{-0.2em}
\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item[\textbf{[9]}] \textbf{E. Amer and S. El-Sappagh}, ``GraphShield: Advanced dynamic graph-based malware detection using graph neural networks,'' \textit{Expert Systems with Applications}, vol. 268, p. 129812, 2025.
  
  \item[\textbf{[10]}] \textbf{F. Abdullayeva and S. Suleymanzade}, ``Cyber security attack recognition on cloud computing networks based on GCN and GraphSAGE models,'' \textit{Results in Control and Optimization}, vol. 16, p. 100423, 2024.
  
  \item[\textbf{[11]}] \textbf{R. Abu Bakar, G. Al-Naymat, and N. Ramoly}, ``FTG-Net-E: A hierarchical ensemble graph neural network for DDoS attack detection,'' \textit{Computer Networks}, vol. 248, p. 110508, 2024.
  
  \item[\textbf{[12]}] \textbf{M. S. Siddique, M. Khan, and H. Al-Sahaf}, ``Intelligent intrusion detection for cyber-physical systems using GAN-LSTM,'' \textit{Frontiers in Artificial Intelligence}, vol. 8, p. 100281, 2025.
  
  \item[\textbf{[13]}] \textbf{A. Yilmaz, S. Sen, and E. Peksen}, ``Knowledge graph visualization and anomaly detection using graph neural networks,'' \textit{Computer Networks}, vol. 278, p. 112632, 2026.
  
  \item[\textbf{[14]}] \textbf{G. Iannizzotto, A. Nucita, and A. Siragusa}, ``Robust, efficient detection of network intrusion attacks: A large language model approach,'' \textit{Computer Networks}, vol. 276, p. 112559, 2026.
  
  \item[\textbf{[15]}] \textbf{A. Al Mamun, H. Al-Sahaf, and M. Zhang}, ``Detection of advanced persistent threat: A genetic programming approach,'' \textit{Applied Soft Computing}, vol. 167, p. 112447, 2024.
  
  \item[\textbf{[16]}] \textbf{M. Alshehri}, ``Dynamic cyber deception using AI-driven adaptive honeypot networks,'' \textit{Ain Shams Engineering Journal}, vol. 17, no. 3, p. 104061, 2026.
\end{itemize}
\end{frame}

%% ---- THANKS (LAST PAGE) ---------------------------------------------------
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
  \fill[prismNavy] (current page.south west) rectangle (current page.north east);
  
  % Logo
  \node at ([yshift=2.4cm]current page.center)
        {\includegraphics[height=1.3cm]{cek-logo.png}};

  % Thanks Heading
  \node[text=white,font=\fontsize{32}{36}\selectfont\bfseries]
        at ([yshift=0.7cm]current page.center) {Thanks};
        
  % Subtitle / Discussion
  \node[text=prismGold,font=\large]
        at ([yshift=-0.35cm]current page.center) {Questions \& Discussion};
        
  % Team Members
  \node[text=white!90,font=\small,align=center]
        at ([yshift=-1.65cm]current page.center)
        {\textbf{Muhammed Nasih K P} (KNP23CS074)\qquad \textbf{Sumayya Ershad} (KNP23CS107)\\[0.15cm]
         \textbf{Najmunniza N} (LKNP20CS056)\qquad \textbf{K.S.\ Mahadev} (KNP23CS066)};

  % Department & College
  \node[text=prismMint!80,font=\footnotesize,align=center]
        at ([yshift=-2.6cm]current page.center)
        {Department of Computer Science \& Engineering\\
         College of Engineering, Karunagappally};
\end{tikzpicture}
\end{frame}

\end{document}
'''
    return tex

if __name__ == '__main__':
    content = generate_tex()
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated updated main.tex, total length: {len(content)} bytes.")
