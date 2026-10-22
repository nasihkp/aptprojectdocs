# -*- coding: utf-8 -*-
"""
Generate complete, professional LaTeX Beamer presentation for Group 14 Final Year Project.
Synthesizes MGDA, Commander, and EdgeFence papers into a feasible, production-grade system:
- Ingests DARPA Transparent Computing datasets (CADETS, THEIA, OpTC)
- Spatio-Temporal GNN: GAT (Spatial) + GRU (Temporal) + VGAE (Variational Graph Autoencoder)
- Federated Learning with TenSEAL CKKS Homomorphic Encryption
- Neo4j Graph Database + Relational Metadata Database
- Automated Causal Attack Subgraph Reconstruction and MITRE ATT&CK Mapping
- Real-Time SOC Analyst Dashboard
- Retains existing 16 Literature Review slides verbatim without changes.
"""

import os
import subprocess

def build_latex():
    with open('lr_extracted.tex', 'r', encoding='utf-8') as f:
        lr_slides = f.read()

    # Preamble and custom definitions
    doc = []
    doc.append(r'''% ============================================================
%  Hybrid Cyber Attack Prediction Platform -- Group 14, CEK
%  B.Tech Final-Year Project Review -- Complete Technical Presentation
%  Compile: pdflatex main.tex  (run twice for cross-references)
% ============================================================
\documentclass[aspectratio=169,10pt]{beamer}
\usetheme{Madrid}
\usecolortheme{default}
\usefonttheme{professionalfonts}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{tikz}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{ragged2e}
\usepackage{array}
\usepackage{multirow}
\usetikzlibrary{arrows.meta,positioning,fit,backgrounds,calc,shadows,shapes.geometric}

% ---- TABLE COLUMN TYPES -----------------------------------------------
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}

% ---- COLOUR PALETTE ---------------------------------------------------
\definecolor{prismNavy}{RGB}{13,29,54}
\definecolor{prismBlue}{RGB}{38,126,190}
\definecolor{prismTeal}{RGB}{28,161,157}
\definecolor{prismMint}{RGB}{224,247,242}
\definecolor{prismGold}{RGB}{229,166,50}
\definecolor{rowA}{RGB}{240,248,255}
\definecolor{rowB}{RGB}{255,255,255}
\definecolor{strengthGreen}{RGB}{0,120,60}
\definecolor{limitRed}{RGB}{180,0,0}
\definecolor{codeBg}{RGB}{245,247,250}

% ---- BEAMER COLOURS ---------------------------------------------------
\setbeamercolor{structure}{fg=prismBlue}
\setbeamercolor{frametitle}{bg=prismNavy,fg=white}
\setbeamercolor{block title}{bg=prismBlue,fg=white}
\setbeamercolor{block body}{bg=prismMint,fg=black}
\setbeamertemplate{navigation symbols}{}
\setbeamercolor{author in head/foot}{bg=prismNavy,fg=white}
\setbeamercolor{title in head/foot}{bg=prismBlue,fg=white}
\setbeamercolor{date in head/foot}{bg=prismNavy,fg=white}
\setbeamertemplate{itemize item}{\color{prismTeal}$\blacktriangleright$}
\setbeamertemplate{itemize subitem}{\color{prismBlue}$\triangleright$}
\setbeamersize{text margin left=0.45cm,text margin right=0.45cm}

% ---- FOOTLINE ---------------------------------------------------------
\setbeamertemplate{footline}{%
  \leavevmode\hbox{%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{author in head/foot}%
    \usebeamerfont{author in head/foot}Group 14 (CEK)\end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,center]{title in head/foot}%
    \usebeamerfont{title in head/foot}B.Tech Final-Year Project Review\end{beamercolorbox}%
  \begin{beamercolorbox}[wd=.333333\paperwidth,ht=2.25ex,dp=1ex,right]{date in head/foot}%
    \usebeamerfont{date in head/foot}\insertdate\hspace*{2em}\insertframenumber{}/\inserttotalframenumber\hspace*{2ex}\end{beamercolorbox}}%
  \vskip0pt}

% ---- FRAMETITLE -------------------------------------------------------
\setbeamertemplate{frametitle}{%
  \nointerlineskip%
  \begin{beamercolorbox}[wd=\paperwidth,ht=1.20cm,dp=0pt,leftskip=0.45cm,rightskip=0.45cm]{frametitle}%
    \vbox to 1.20cm{%
      \vfill%
      \raggedright\fontsize{9.2pt}{11.0pt}\selectfont\textbf{\insertframetitle}%
      \vfill%
    }%
  \end{beamercolorbox}%
}

% ---- DOCUMENT METADATA ------------------------------------------------
\title[Cyber Attack Prediction Platform]{CYBER ATTACK PREDICTION PLATFORM USING SPATIO-TEMPORAL GRAPH NEURAL NETWORKS}
\subtitle{Dual-Tier Detection via ST-GNN (GAT+GRU+VGAE), Federated CKKS Encryption \& MITRE ATT\&CK Mapping}
\author{Muhammed Nasih K P \and Sumayya Ershad \and Najmunniza N \and K.S.\ Mahadev}
\institute{Dept.\ of Computer Science \& Engineering, College of Engineering, Karunagappally}
\date{September 2026}

% ---- HELPER COMMANDS --------------------------------------------------
\newcommand{\lrhdr}{%
  \rowcolor{prismNavy}%
  {\scriptsize\textcolor{white}{\textbf{Citation}}} &
  {\scriptsize\textcolor{white}{\textbf{Summary}}} &
  {\scriptsize\textcolor{white}{\textbf{Advantages \& Disadvantages}}} \\}

\newcommand{\stag}[1]{{\color{strengthGreen}\textbf{$\oplus$}~#1}}
\newcommand{\ltag}[1]{{\color{limitRed}\textbf{$\ominus$}~#1}}

% ---- PREVENT HYPHENATION (NO SPLIT WORDS) -----------------------------
\hyphenpenalty=10000
\exhyphenpenalty=10000
\sloppy

\begin{document}
''')

    # SLIDE 1: Title Slide
    doc.append(r'''
%% ======================================================================
%%  TITLE SLIDE
%% ======================================================================
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
  \node[rounded corners=4pt,fill=prismBlue,drop shadow={shadow xshift=2pt,shadow yshift=-2pt,opacity=.35},
        minimum width=15.4cm,minimum height=1.10cm]
        at ([yshift=-0.80cm]current page.north) {};
  \node[text=white,font=\fontsize{11}{13}\selectfont\bfseries,align=center]
        at ([yshift=-0.80cm]current page.north) {CYBER ATTACK PREDICTION PLATFORM\\[0.06cm]
        USING SPATIO-TEMPORAL GRAPH NEURAL NETWORKS};
  \fill[prismNavy] (current page.south west) rectangle ([yshift=.45cm]current page.south east);
  \fill[prismBlue] ([xshift=5.33cm]current page.south west)
                    rectangle ([xshift=10.66cm,yshift=.45cm]current page.south west);
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=2.66cm,yshift=.22cm]current page.south west) {Group 14 (CEK)};
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=8cm,yshift=.22cm]current page.south west) {B.Tech Final-Year Project Review};
  \node[anchor=center,text=white,font=\scriptsize]
        at ([xshift=13.2cm,yshift=.22cm]current page.south west)
        {September 2026\hspace{1.2cm}1/\inserttotalframenumber};
  \node at ([yshift=6.80cm]current page.south)
        {\includegraphics[height=1.10cm]{cek-logo.png}};
  \node[font=\footnotesize,align=center,text=prismNavy]
        at ([yshift=5.65cm]current page.south)
        {\textbf{Dept.\ of Computer Science \& Engineering}\\[.03cm]
         \textbf{College of Engineering, Karunagappally (CEK)}};
  \node[font=\small,align=center]
        at ([yshift=4.45cm]current page.south)
        {Under the Guidance of\\[.06cm]
         \textbf{\large Mrs.\ SYAMA S R}\\[.03cm]
         Assistant Professor, Dept.\ of CSE};
  \node[font=\large\bfseries,text=prismBlue]
        at ([yshift=3.35cm]current page.south) {Project Group 14};
  \node[font=\small]
        at ([yshift=1.80cm]current page.south)
        {\begin{tabular}{r@{\quad}l}
           \textbf{MUHAMMED NASIH K P} & \textbf{(KNP23CS074)} \\
           \textbf{SUMAYYA ERSHAD}     & \textbf{(KNP23CS107)} \\
           \textbf{NAJMUNNIZA N}       & \textbf{(LKNP20CS056)} \\
           \textbf{K.S.\ MAHADEV}      & \textbf{(KNP23CS066)}
         \end{tabular}};
\end{tikzpicture}
\end{frame}
''')

    # SLIDE 2: Roadmap Overview
    doc.append(r'''
%% ======================================================================
%%  PRESENTATION ROADMAP
%% ======================================================================
\begin{frame}{Presentation Overview}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.5em,wd=\textwidth]{block title}
\textbf{\scriptsize Part I: Foundations \& Literature}
\end{beamercolorbox}
\vspace{0.3em}
{\fontsize{7.5pt}{10.0pt}\selectfont
\begin{enumerate}\itemsep0.30em
  \item \textbf{Introduction} (Pointwise \& Concise)
  \item \textbf{Objectives} (Pointwise Methods)
  \item \textbf{Problem Statement} (Core Cyber Dilemmas)
  \item \textbf{Literature Review} (16 Comprehensive Papers)
  \item \textbf{System Design Principles} (Features, Datasets \& Tools)
  \item \textbf{Workflow Diagram} (End-to-End Pipeline)
\end{enumerate}
}
\end{column}
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.5em,wd=\textwidth]{block title}
\textbf{\scriptsize Part II: Architecture \& Engineering}
\end{beamercolorbox}
\vspace{0.3em}
{\fontsize{7.5pt}{10.0pt}\selectfont
\begin{enumerate}\setcounter{enumi}{6}\itemsep0.30em
  \item \textbf{Proposed Methods} (4 Integrated Methodical Pillars)
  \item \textbf{Model Responsibilities \& Inference Flow} (AI Engine)
  \item \textbf{Dataset Preparation \& Model Training} (DARPA TC)
  \item \textbf{Architecture Diagram} (Multi-Tier Architecture)
  \item \textbf{Flowchart Diagram} (Properly Arrowed Flowchart)
  \item \textbf{Database Schema} (Neo4j Graph \& Relational Tables)
  \item \textbf{Algorithms} (Federated ST-VGAE \& Causal Attribution)
\end{enumerate}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 1. INTRODUCTION (Pointwise, simple and small)
    doc.append(r'''
%% ======================================================================
%%  1. INTRODUCTION
%% ======================================================================
\section{Introduction}

\begin{frame}{1. Introduction}
\vspace{0.2em}
{\small
\begin{itemize}\itemsep0.55em
  \item \textbf{Advanced Persistent Threats (APTs):} Sophisticated, stealthy cyber attacks that execute low-and-slow operations over weeks to months, bypassing standard signature firewalls and antivirus tools.
  \item \textbf{Limitations of Flat Log Analysis:} Traditional intrusion detectors treat OS audit logs as isolated tabular rows, completely discarding the causal relationships between processes, files, and network sockets.
  \item \textbf{Dynamic Provenance Graphs:} By modeling system kernel execution as directed provenance graphs, every causal dependency ($Process \rightarrow File \rightarrow Socket$) is preserved as a traceable forensic path.
  \item \textbf{Spatio-Temporal Deep Learning:} Integrates Graph Attention Networks (GAT) for spatial structure, Gated Recurrent Units (GRU) for temporal sequences, and Variational Graph Autoencoders (VGAE) for self-supervised zero-day detection without attack labels.
  \item \textbf{Privacy-Preserving Federated Collaboration:} Federated Learning paired with CKKS Homomorphic Encryption (TenSEAL) enables secure multi-host/cross-enterprise defense without exposing raw audit logs.
  \item \textbf{Automated Threat Attribution:} Anomalous subgraphs are extracted and mapped directly to standard MITRE ATT\&CK tactics, delivering explainable incident reports to SOC analysts.
\end{itemize}
}
\end{frame}
''')

    # 2. OBJECTIVES (Pointwise, only tell what we are achieving or trying to achieve, must be the methods)
    doc.append(r'''
%% ======================================================================
%%  2. OBJECTIVES
%% ======================================================================
\section{Objectives}

\begin{frame}{2. Project Objectives}
\vspace{0.2em}
{\small
\begin{itemize}\itemsep0.55em
  \item \textbf{Dynamic Provenance Graph Construction Method:} Ingest OS audit logs from the DARPA Transparent Computing benchmark and construct causal property graphs connecting Process, File, and Socket entities using semantics-preserving compression.
  \item \textbf{Spatio-Temporal Graph Autoencoder (ST-VGAE) Development Method:} Develop a unified neural model combining Graph Attention Networks (GAT) for spatial structure and Gated Recurrent Units (GRU) for temporal sequence modeling within a Variational Graph Autoencoder (VGAE) to detect zero-day attacks via reconstruction error.
  \item \textbf{Privacy-Preserving Federated Learning Method:} Implement distributed collaborative training across network endpoints using Federated Averaging (FedAvg) combined with CKKS Homomorphic Encryption (TenSEAL) to encrypt weight tensors and eliminate gradient leakage.
  \item \textbf{Bidirectional Causal Attack Reconstruction Method:} Execute bidirectional $k$-hop causal graph traversal from detected high-outlier seed processes to reconstruct complete attack chains while mitigating dependency explosion and session-evasion tactics.
  \item \textbf{Automated MITRE ATT\&CK Mapping \& SOC Deployment Method:} Map anomalous causal subgraphs directly to standard MITRE ATT\&CK tactics and techniques, rendering interactive attack paths on a real-time containerized SOC dashboard.
\end{itemize}
}
\end{frame}
''')

    # 3. PROBLEM STATEMENT (What problem is going to be solved by the project)
    doc.append(r'''
%% ======================================================================
%%  3. PROBLEM STATEMENT
%% ======================================================================
\section{Problem Statement}

\begin{frame}{3. Problem Statement}
\vspace{-0.1em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.7em,wd=\textwidth]{block title}
\textbf{\small Problem Formulation: Detecting Stealthy, Multi-Phase APTs Under Strict Privacy}
\end{beamercolorbox}
\vspace{0.3em}
{\fontsize{7.5pt}{10.0pt}\selectfont
\begin{itemize}\itemsep0.35em
  \item \textbf{Stealthy, Multi-Stage APT Infiltration:} Attackers operate below perimeter thresholds by executing low-and-slow actions across weeks, leveraging legitimate administrative tools (Living-off-the-Land) and moving laterally across endpoints.
  \item \textbf{Failure of Traditional IDSs and Flat ML:} Signature-based IDSs (Snort, Zeek) fail against unknown zero-day exploits, while conventional machine learning flattens logs into tables, stripping essential causal context ($Process \rightarrow File \rightarrow Socket$).
  \item \textbf{Dependency Explosion \& Tracing Gaps in Provenance IDSs:} Naive provenance graph analysis generates millions of edges over time (dependency explosion) and loses track of attacks during cross-machine lateral movement, session hijacking, or persistence reboots.
  \item \textbf{Data Privacy Barriers in Collaborative Defense:} Strict data regulations (GDPR, HIPAA) prohibit sharing raw enterprise audit logs, while standard Federated Learning exposes model updates to gradient inversion and membership inference attacks.
  \item \textbf{Alert Fatigue \& Lack of Threat Attribution:} Existing anomaly detectors produce high volumes of isolated alert scores without causal paths or standardized MITRE ATT\&CK mapping, overwhelming SOC analysts.
\end{itemize}
}
\end{frame}
''')

    # 4. LITERATURE REVIEW (Verbatim existing slides, NO CHANGES!)
    doc.append(r'''
%% ======================================================================
%%  4. LITERATURE REVIEW (16 PAPERS VERBATIM)
%% ======================================================================
''' + lr_slides)

    # 5. SYSTEM DESIGN PRINCIPLES
    doc.append(r'''
%% ======================================================================
%%  5. SYSTEM DESIGN PRINCIPLES
%% ======================================================================
\section{System Design Principles}

\begin{frame}{5. System Design Principles: Features, Libraries, Datasets \& Database}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 1. Extracted Features \& System Libraries}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item \textbf{Node Features ($\mathbf{X} \in \mathbb{R}^{|V| \times d}$):} Entity type (Process, File, Socket), binary path entropy, command-line hash, user ID/privilege level, port numbers.
  \item \textbf{Edge Features ($\mathbf{E} \in \mathbb{R}^{|E| \times d_e}$):} System call type (`fork`, `execve`, `read`, `write`, `connect`, `open`), event timestamp, data volume (bytes).
  \item \textbf{AI \& Graph Libraries:} PyTorch 2.x, PyTorch Geometric (PyG for GAT and GraphVAE layers), NetworkX.
  \item \textbf{Privacy Library:} TenSEAL (Microsoft SEAL-based CKKS Homomorphic Encryption for encrypted tensor addition).
  \item \textbf{API \& Backend:} FastAPI, Uvicorn, Pydantic, Scikit-Learn.
\end{itemize}
}
\end{column}

\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 2. Benchmark Datasets \& Database Principles}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item \textbf{DARPA Transparent Computing (TC) Benchmark:}
    \begin{itemize}\itemsep0.10em
      \item \textbf{CADETS (FreeBSD):} Kernel system call logs covering nginx backdoor and Drakon in-memory execution.
      \item \textbf{THEIA (Linux):} Auditd logs capturing BIND9 exploits, privilege escalation, and data staging.
      \item \textbf{OpTC (Windows):} Enterprise host logs detailing lateral movement, SMB staging, and credential dumping.
    \end{itemize}
  \item \textbf{Database Architecture:}
    \begin{itemize}\itemsep0.10em
      \item \textbf{Neo4j Graph Database:} Native property graph storing entities and causal relationships; provides millisecond-latency Cypher queries for recursive multi-hop backward/forward attack tracing.
      \item \textbf{Relational Metadata Store (SQLite / PostgreSQL):} Stores time-series anomaly scores, host inventory, and encrypted federated training telemetry.
    \end{itemize}
\end{itemize}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 6. WORKFLOW DIAGRAM
    doc.append(r'''
%% ======================================================================
%%  6. WORKFLOW DIAGRAM
%% ======================================================================
\section{Workflow Diagram}

\begin{frame}{6. End-to-End System Workflow Diagram}
\vspace{-0.15em}
\centering
\resizebox{0.97\textwidth}{!}{%
\begin{tikzpicture}[
  node distance=0.85cm and 0.50cm,
  box/.style={draw=prismNavy, fill=white, rounded corners=3pt, line width=0.8pt,
              font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt, drop shadow={opacity=0.15}},
  proc/.style={draw=prismBlue, fill=prismMint!60, rounded corners=3pt, line width=0.8pt,
               font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt, drop shadow={opacity=0.15}},
  fl/.style={draw=prismGold!80!orange, fill=prismGold!20, rounded corners=3pt, line width=0.8pt,
             font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt, drop shadow={opacity=0.15}},
  alert/.style={draw=limitRed, fill=red!10, rounded corners=3pt, line width=0.8pt,
                font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt, drop shadow={opacity=0.15}},
  arrow/.style={-{Stealth[scale=0.9]}, line width=1.0pt, color=prismNavy},
  darrow/.style={-{Stealth[scale=0.9]}, line width=1.0pt, dashed, color=prismBlue}
]

% Row 1: Data Ingestion & Preprocessing
\node[box, fill=prismNavy!10] (raw) {DARPA TC Audit Logs\\[0.05cm]\tiny (CADETS / THEIA / OpTC)};
\node[proc, right=0.60cm of raw] (compress) {Log Parsing \&\\[0.05cm]Semantic Compression\\[0.05cm]\tiny (Merge Identical I/O Events)};
\node[proc, right=0.60cm of compress] (window) {Dynamic Graph Slicer\\[0.05cm]\tiny Sliding Windows $G_t=(V_t,E_t,X_t)$};
\node[proc, right=0.60cm of window] (stgnn) {Local ST-VGAE Model\\[0.05cm]\tiny GAT (Spatial) + GRU (Temporal)};

% Row 2: Federated Privacy & Detection Engine
\node[fl, below=1.0cm of stgnn] (ckks) {TenSEAL CKKS Encryption\\[0.05cm]\tiny $[[\Delta \mathbf{w}_i]] = \text{Enc}(\Delta \mathbf{w}_i, pk)$};
\node[fl, left=0.60cm of ckks] (server) {Encrypted FedAvg Server\\[0.05cm]\tiny $[[\Delta \mathbf{w}_{glob}]] = \sum \frac{N_i}{N} [[\Delta \mathbf{w}_i]]$};
\node[proc, left=0.60cm of server] (vgae) {VGAE Reconstruction\\[0.05cm]\tiny $\hat{\mathbf{A}}_t = \sigma(\mathbf{Z}\mathbf{Z}^T)$ \& Anomaly Loss};
\node[alert, left=0.60cm of vgae] (detect) {Anomaly Scoring\\[0.05cm]\tiny $\text{Score}(G_t) > \tau_{anomaly}$};

% Row 3: Investigation & Response
\node[box, below=1.0cm of detect, fill=prismMint!80] (seed) {Seed Malicious Nodes\\[0.05cm]\tiny High-Outlier Process Entities};
\node[proc, right=0.60cm of seed] (bfs) {Bidirectional Causal Walk\\[0.05cm]\tiny Neo4j $k$-hop BFS + Noise Pruning};
\node[proc, right=0.60cm of bfs] (mitre) {MITRE ATT\&CK Mapping\\[0.05cm]\tiny TTP Rule Matching (Initial $\rightarrow$ Exfil)};
\node[box, right=0.60cm of mitre, fill=strengthGreen!20, draw=strengthGreen] (soc) {Real-Time SOC Dashboard\\[0.05cm]\tiny FastAPI + Cytoscape Graph Visualization};

% Connectors
\draw[arrow] (raw) -- (compress);
\draw[arrow] (compress) -- (window);
\draw[arrow] (window) -- (stgnn);
\draw[arrow] (stgnn) -- (ckks);
\draw[arrow] (ckks) -- (server);
\draw[darrow] (server) -- (vgae) node[midway,above,font=\tiny\color{prismBlue}]{Global Model};
\draw[arrow] (vgae) -- (detect);
\draw[arrow] (detect) -- (seed);
\draw[arrow] (seed) -- (bfs);
\draw[arrow] (bfs) -- (mitre);
\draw[arrow] (mitre) -- (soc);

\end{tikzpicture}}
\vspace{0.2em}
{\fontsize{6.8pt}{8.0pt}\selectfont
\textbf{Pipeline Flow:} Streaming kernel audit logs $\rightarrow$ Semantics-preserving graph reduction $\rightarrow$ Sliding-window ST-VGAE feature encoding $\rightarrow$ TenSEAL CKKS encrypted federated model updates $\rightarrow$ Unsupervised reconstruction scoring $\rightarrow$ Seed extraction $\rightarrow$ Neo4j causal graph walk $\rightarrow$ MITRE ATT\&CK attribution on SOC Dashboard.
}
\end{frame}
''')

    # 7. PROPOSED METHODS (What all methods are implemented to get output of project)
    doc.append(r'''
%% ======================================================================
%%  7. PROPOSED METHODS
%% ======================================================================
\section{Proposed Methods}

\begin{frame}{7. Proposed Methods: Core Technical Pillars}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Method 1: Provenance Graph Construction \& Compression}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item Parses kernel event streams into directed property graphs $G = (V, E)$ where nodes represent system entities (Processes, Files, Sockets) and edges denote system calls.
  \item \textbf{Semantic Event Merging (from MGDA):} Merges redundant consecutive read/write events between identical entities without state changes, cutting graph size by over 80\%.
  \item \textbf{Logon-Session Partitioning (from Commander):} Segments causal paths by user logon sessions, halting dependency explosion.
\end{itemize}
}
\vspace{0.2em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Method 2: Spatio-Temporal VGAE (ST-VGAE)}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item \textbf{Spatial GAT:} Uses multi-head self-attention to capture topological dependencies across neighboring OS entities.
  \item \textbf{Temporal GRU:} Connects hidden states across sliding windows ($G_{t-w}, \dots, G_t$) to track slow APT execution steps.
  \item \textbf{Variational Autoencoder (VGAE):} Reconstructs normal graph adjacency; unseen zero-day attacks trigger high reconstruction error.
\end{itemize}
}
\end{column}

\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Method 3: Privacy-Preserving TenSEAL CKKS Federated Learning}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item Distributed edge/host nodes train local ST-VGAE models exclusively on local audit logs.
  \item Weight differentials $\Delta \mathbf{w}_i$ are encrypted via TenSEAL using the CKKS homomorphic scheme: $[[\Delta \mathbf{w}_i]] \leftarrow \text{Enc}(\Delta \mathbf{w}_i, pk)$.
  \item The server executes secure aggregation directly over ciphertexts ($[[\Delta \mathbf{w}_{glob}]] = \sum \frac{n_i}{N} [[\Delta \mathbf{w}_i]]$) without ever decrypting weights.
\end{itemize}
}
\vspace{0.2em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Method 4: Causal Attack Reconstruction \& MITRE ATT\&CK Mapping}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item High-outlier process nodes serve as forensic seeds.
  \item Executes bidirectional $k$-hop BFS in Neo4j (backward to uncover initial access, forward to evaluate data exfiltration).
  \item Rules correlate causal event subpaths to MITRE ATT\&CK tactics (Initial Access, Execution, Persistence, Lateral Movement, Exfiltration).
\end{itemize}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 8. MODEL RESPONSIBILITIES AND INFERENCE FLOW
    doc.append(r'''
%% ======================================================================
%%  8. MODEL RESPONSIBILITIES & INFERENCE FLOW
%% ======================================================================
\section{Model Responsibilities and Inference Flow}

\begin{frame}{8. Model Responsibilities and Mathematical Formulation}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Model Component Responsibilities}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.25em
  \item \textbf{1. Graph Attention (GAT) Layer:} Learns dynamic attention weights $\alpha_{ij}$ between interacting OS entities:
  $$\alpha_{ij} = \frac{\exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{x}_i \parallel \mathbf{W}\mathbf{x}_j]\right)\right)}{\sum_{k \in \mathcal{N}(i)} \exp\left(\text{LeakyReLU}\left(\mathbf{a}^T [\mathbf{W}\mathbf{x}_i \parallel \mathbf{W}\mathbf{x}_k]\right)\right)}$$
  Extracts structural entity representations $\mathbf{h}_i^{(t)}$.
  \item \textbf{2. Gated Recurrent Unit (GRU) Layer:} Preserves sequential memory across time windows, capturing multi-stage attack evolution:
  $$\mathbf{s}_t = (1 - \mathbf{z}_t) \odot \mathbf{s}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{s}}_t$$
  \item \textbf{3. Variational Graph Autoencoder (VGAE):} Maps spatio-temporal state $\mathbf{s}_t$ to latent distribution $q(\mathbf{Z} \mid \mathbf{A}, \mathbf{X}) \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2)$ and decodes reconstructed adjacency:
  $$\hat{\mathbf{A}}_{ij} = \sigma(\mathbf{z}_i^T \mathbf{z}_j)$$
\end{itemize}
}
\end{column}

\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize Real-Time Model Inference Flow}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.25em
  \item \textbf{Step 1: Streaming Ingestion:} Continuous kernel events are sliced into dynamic temporal window snapshots $G_t = (V_t, E_t, X_t)$ every $\Delta T = 300\text{s}$.
  \item \textbf{Step 2: Spatio-Temporal Forward Pass:} Snapshot $G_t$ is encoded through GAT layers and propagated through the temporal GRU state to generate latent embedding $\mathbf{Z}_t$.
  \item \textbf{Step 3: Adjacency Reconstruction \& Scoring:} Decodes reconstructed topology $\hat{\mathbf{A}}_t$ and evaluates the graph-level anomaly score:
  $$\mathcal{E}(G_t) = \|\mathbf{A}_t - \hat{\mathbf{A}}_t\|_F^2 + \beta D_{KL}(q(\mathbf{Z}_t \mid \mathbf{A}_t, \mathbf{X}_t) \parallel \mathcal{N}(0, \mathbf{I}))$$
  \item \textbf{Step 4: Threshold Evaluation:} If $\mathcal{E}(G_t) > \tau_{anomaly}$, snapshot is flagged anomalous. Node-level reconstruction errors identify seed malicious processes:
  $$v_{\text{seed}} = \{v_i \in V_t \mid \|\mathbf{A}_{i,:} - \hat{\mathbf{A}}_{i,:}\|_2 > \theta_{\text{node}}\}$$
\end{itemize}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 9. DATASET PREPARATION & MODEL TRAINING
    doc.append(r'''
%% ======================================================================
%%  9. DATASET PREPARATION & MODEL TRAINING
%% ======================================================================
\section{Dataset Preparation \& Model Training}

\begin{frame}{9. Dataset Preparation and Model Training Workflow}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 1. DARPA TC Dataset Acquisition \& Cleaning}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item \textbf{Data Sourcing:} Ingests DARPA Transparent Computing program logs (CADETS, THEIA, OpTC) spanning enterprise systems.
  \item \textbf{Attack Scenarios:} Contains verified multi-phase APT emulations:
    \begin{itemize}\itemsep0.05em
      \item Initial compromise via web vulnerability (BIND9 / nginx).
      \item In-memory payload injection and cron persistence.
      \item Lateral movement across network machines via SSH/SMB.
      \item Sensitive data staging and exfiltration via encrypted sockets.
    \end{itemize}
  \item \textbf{Log Standardization:} Raw system call records are parsed into unified 4-tuples: $(\text{subject}, \text{relation}, \text{object}, \text{timestamp})$.
  \item \textbf{Graph Windowing:} Logs are sliced into discrete time-windows $\Delta T = 5\text{ mins}$ with 1-min sliding steps to build dynamic graph sequences $\{G_1, G_2, \dots, G_T\}$.
\end{itemize}
}
\end{column}

\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 2. Self-Supervised Training Algorithm}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.8pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item \textbf{Benign Baseline Profiling:} ST-VGAE is trained strictly on benign baseline system activity, completely eliminating the dependency on scarce or synthetic attack labels.
  \item \textbf{Composite Optimization Loss:}
  $$\mathcal{L} = \mathcal{L}_{\text{reconstruction}} + \beta \mathcal{L}_{\text{KL}}$$
  $$\mathcal{L}_{\text{recon}} = -\frac{1}{|V_t|^2}\sum_{i,j} \left[A_{ij}\log \hat{A}_{ij} + (1-A_{ij})\log(1-\hat{A}_{ij})\right]$$
  $$\mathcal{L}_{\text{KL}} = -\frac{1}{2|V_t|}\sum_{i=1}^{|V_t|}\left(1 + 2\log\boldsymbol{\sigma}_i - \boldsymbol{\mu}_i^2 - \boldsymbol{\sigma}_i^2\right)$$
  \item \textbf{Optimization Parameters:} Adam optimizer, learning rate $\eta = 0.001$, weight decay $10^{-5}$, latent dimension $d_z = 32$, trained across $E=50$ local client epochs.
\end{itemize}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 10. ARCHITECTURE DIAGRAM
    doc.append(r'''
%% ======================================================================
%%  10. ARCHITECTURE DIAGRAM
%% ======================================================================
\section{Architecture Diagram}

\begin{frame}{10. System Architecture Diagram}
\vspace{-0.15em}
\centering
\resizebox{0.96\textwidth}{!}{%
\begin{tikzpicture}[
  node distance=0.45cm and 0.40cm,
  layer/.style={draw=prismNavy, fill=prismMint!30, rounded corners=4pt, line width=0.8pt, inner sep=6pt},
  comp/.style={draw=prismBlue, fill=white, rounded corners=3pt, line width=0.7pt,
               font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt, drop shadow={opacity=0.10}},
  head/.style={font=\fontsize{7.5}{8.5}\selectfont\bfseries, text=prismNavy, align=left},
  arrow/.style={-{Stealth[scale=0.8]}, line width=0.9pt, color=prismNavy},
  darrow/.style={-{Stealth[scale=0.8]}, line width=0.9pt, dashed, color=prismBlue}
]

% Layer 1: Host Ingestion Layer
\node[layer, minimum width=15.0cm, minimum height=1.15cm] (l1) {};
\node[head, anchor=west] at ([xshift=0.3cm, yshift=0.32cm]l1.west) {Layer 1: Host Data Ingestion \& Provenance Construction};
\node[comp, right=0.3cm of l1.west, yshift=-0.15cm] (c1) {OS Kernel Audit Streams\\[0.04cm]\tiny Linux auditd / Sysmon / DARPA TC};
\node[comp, right=0.4cm of c1] (c2) {JSON Log Parser\\[0.04cm]\tiny (Subject, Relation, Object, Time)};
\node[comp, right=0.4cm of c2] (c3) {Semantic Compression\\[0.04cm]\tiny Merge Redundant I/O Loops};
\node[comp, right=0.4cm of c3] (c4) {Session Partitioner\\[0.04cm]\tiny Halts Dependency Explosion};
\node[comp, right=0.4cm of c4] (c5) {Windowed Snapshot Slicer\\[0.04cm]\tiny $G_t = (V_t, E_t, X_t)$};

% Layer 2: Edge ST-VGAE Engine
\node[layer, below=0.35cm of l1, minimum width=15.0cm, minimum height=1.15cm] (l2) {};
\node[head, anchor=west] at ([xshift=0.3cm, yshift=0.32cm]l2.west) {Layer 2: Edge / Endpoint ST-VGAE AI Detection Engine};
\node[comp, right=0.3cm of l2.west, yshift=-0.15cm] (c6) {Spatial Attention (GAT)\\[0.04cm]\tiny Multi-head attention $\alpha_{ij}$};
\node[comp, right=0.5cm of c6] (c7) {Temporal Recurrence (GRU)\\[0.04cm]\tiny Multi-window memory $\mathbf{s}_t$};
\node[comp, right=0.5cm of c7] (c8) {Variational Latent Space\\[0.04cm]\tiny Reparameterize $\mathbf{Z} \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\sigma}^2)$};
\node[comp, right=0.5cm of c8] (c9) {Inner-Product Decoder\\[0.04cm]\tiny Reconstructs $\hat{\mathbf{A}}_t = \sigma(\mathbf{Z}\mathbf{Z}^T)$};
\node[comp, right=0.5cm of c9] (c10) {Anomaly Loss Evaluator\\[0.04cm]\tiny $\|\mathbf{A} - \hat{\mathbf{A}}\|_F^2 > \tau \implies \text{Alert}$};

% Layer 3: Federated Privacy Layer
\node[layer, below=0.35cm of l2, minimum width=15.0cm, minimum height=1.15cm] (l3) {};
\node[head, anchor=west] at ([xshift=0.3cm, yshift=0.32cm]l3.west) {Layer 3: Privacy-Preserving Collaborative Federated Orchestration};
\node[comp, right=0.3cm of l3.west, yshift=-0.15cm] (c11) {Local Model Update\\[0.04cm]\tiny $\Delta \mathbf{w}_i = \mathbf{w}_i^{(r+1)} - \mathbf{w}^{(r)}$};
\node[comp, right=0.7cm of c11] (c12) {TenSEAL CKKS Encryptor\\[0.04cm]\tiny $[[\Delta \mathbf{w}_i]] \leftarrow \text{Enc}(\Delta \mathbf{w}_i, pk)$};
\node[comp, right=0.7cm of c12] (c13) {Homomorphic FedAvg Server\\[0.04cm]\tiny $[[\Delta \mathbf{w}_{glob}]] = \sum \frac{n_i}{N}[[\Delta \mathbf{w}_i]]$};
\node[comp, right=0.7cm of c13] (c14) {Secure Model Broadcast\\[0.04cm]\tiny Global weights $\mathbf{w}^{(r+1)}$ to clients};

% Layer 4: Forensics & UI Layer
\node[layer, below=0.35cm of l3, minimum width=15.0cm, minimum height=1.15cm] (l4) {};
\node[head, anchor=west] at ([xshift=0.3cm, yshift=0.32cm]l4.west) {Layer 4: Threat Intelligence, Causal Attribution \& SOC Dashboard};
\node[comp, right=0.3cm of l4.west, yshift=-0.15cm] (c15) {Neo4j Graph Database\\[0.04cm]\tiny Process, File, Socket Nodes};
\node[comp, right=0.5cm of c15] (c16) {Bidirectional Causal BFS\\[0.04cm]\tiny Root cause \& lateral blast radius};
\node[comp, right=0.5cm of c16] (c17) {MITRE ATT\&CK Classifier\\[0.04cm]\tiny TTP Rule Matching Engine};
\node[comp, right=0.5cm of c17] (c18) {FastAPI Alerting Service\\[0.04cm]\tiny WebSockets real-time push};
\node[comp, right=0.5cm of c18] (c19) {Interactive Web UI\\[0.04cm]\tiny Cytoscape Graph Visualization};

% Intra-layer flows
\draw[arrow] (c1) -- (c2);
\draw[arrow] (c2) -- (c3);
\draw[arrow] (c3) -- (c4);
\draw[arrow] (c4) -- (c5);

\draw[arrow] (c6) -- (c7);
\draw[arrow] (c7) -- (c8);
\draw[arrow] (c8) -- (c9);
\draw[arrow] (c9) -- (c10);

\draw[arrow] (c11) -- (c12);
\draw[arrow] (c12) -- (c13);
\draw[arrow] (c13) -- (c14);

\draw[arrow] (c15) -- (c16);
\draw[arrow] (c16) -- (c17);
\draw[arrow] (c17) -- (c18);
\draw[arrow] (c18) -- (c19);

% Inter-layer connections
\draw[arrow] (c5.south) -- ++(0,-0.12) -| (c6.north);
\draw[darrow] (c10.south) -- ++(0,-0.12) -| (c11.north);
\draw[arrow] (c10.south) -- ++(0,-0.12) -| (c15.north) node[midway,right,font=\tiny\color{limitRed}]{Alert Trigger};

\end{tikzpicture}}
\end{frame}
''')

    # 11. FLOWCHART DIAGRAM (Properly Arrowed)
    doc.append(r'''
%% ======================================================================
%%  11. FLOWCHART DIAGRAM
%% ======================================================================
\section{Flowchart Diagram}

\begin{frame}{11. Runtime Decision \& Attack Reconstruction Flowchart}
\vspace{-0.15em}
\centering
\resizebox{0.95\textwidth}{!}{%
\begin{tikzpicture}[
  node distance=0.60cm and 0.80cm,
  terminal/.style={draw=prismNavy, fill=prismNavy, text=white, rounded corners=6pt,
                   font=\fontsize{6.2}{7.2}\selectfont\bfseries, align=center, inner sep=4pt},
  proc/.style={draw=prismBlue, fill=prismMint!60, rounded corners=3pt, line width=0.8pt,
               font=\fontsize{6.0}{7.0}\selectfont\bfseries, align=center, inner sep=4pt},
  decision/.style={draw=prismGold!90!black, fill=prismGold!25, shape=diamond, aspect=1.8, line width=0.8pt,
                   font=\fontsize{5.8}{6.8}\selectfont\bfseries, align=center, inner sep=2pt},
  alert/.style={draw=limitRed, fill=red!15, rounded corners=3pt, line width=0.8pt,
                font=\fontsize{6.0}{7.0}\selectfont\bfseries, align=center, inner sep=4pt},
  success/.style={draw=strengthGreen, fill=green!15, rounded corners=3pt, line width=0.8pt,
                  font=\fontsize{6.0}{7.0}\selectfont\bfseries, align=center, inner sep=4pt},
  arrow/.style={-{Stealth[scale=0.85]}, line width=0.9pt, color=prismNavy},
  yesno/.style={font=\fontsize{6.0}{7.0}\selectfont\bfseries, color=prismNavy}
]

% Column 1: Ingestion & Inference
\node[terminal] (start) {START: Audit Log Stream};
\node[proc, below=0.45cm of start] (p1) {Parse Entities (Process, File, Socket)\\\& Apply Semantic Compression};
\node[proc, below=0.45cm of p1] (p2) {Slice Logs into Dynamic Sliding\\Window Snapshot $G_t=(V_t,E_t,X_t)$};
\node[proc, below=0.45cm of p2] (p3) {Execute ST-VGAE Forward Pass\\Spatial GAT $\rightarrow$ Temporal GRU $\rightarrow$ VGAE};
\node[proc, below=0.45cm of p3] (p4) {Compute Reconstruction Loss $\mathcal{E}_t$\\\& KL Divergence vs. Normal Prior};

% Column 2: Decision & Forensic Reconstruction
\node[decision, right=1.0cm of p4] (d1) {Anomaly Score\\$\mathcal{E}_t > \tau_{anomaly}$?};
\node[success, above=1.0cm of d1] (benign) {Log as Benign Execution;\\Update GRU Temporal Baseline};
\node[alert, below=0.65cm of d1] (seed) {FLAG ANOMALY:\\Extract Seed Nodes with Outlier Error $> \theta$};
\node[proc, right=1.0cm of seed] (bfs) {Execute Bidirectional $k$-hop BFS in Neo4j\\Backward: Initial Access | Forward: Impact};
\node[proc, above=0.55cm of bfs] (prune) {Prune Redundant Benign Edges\\\& Session-Hijack Paths};
\node[proc, above=0.55cm of prune] (mitre) {Match Reconstructed Causal Chain\\to MITRE ATT\&CK TTP Matrix};
\node[proc, above=0.55cm of mitre] (store) {Store Attack Graph DAG in Neo4j\\\& Log Metadata in Relational DB};
\node[terminal, above=0.50cm of store] (end) {Push Real-Time Alert to SOC UI\\\& Await Analyst Triage};

% Arrows
\draw[arrow] (start) -- (p1);
\draw[arrow] (p1) -- (p2);
\draw[arrow] (p2) -- (p3);
\draw[arrow] (p3) -- (p4);
\draw[arrow] (p4) -- (d1);

\draw[arrow] (d1) -- node[yesno, right]{[NO]} (benign);
\draw[arrow] (benign) |- (p2);

\draw[arrow] (d1) -- node[yesno, right]{[YES]} (seed);
\draw[arrow] (seed) -- (bfs);
\draw[arrow] (bfs) -- (prune);
\draw[arrow] (prune) -- (mitre);
\draw[arrow] (mitre) -- (store);
\draw[arrow] (store) -- (end);

\end{tikzpicture}}
\end{frame}
''')

    # 12. DATABASE SCHEMA (Graph & Relational)
    doc.append(r'''
%% ======================================================================
%%  12. DATABASE SCHEMA
%% ======================================================================
\section{Database Schema}

\begin{frame}{12. Database Schema: Neo4j Graph Database \& Relational Store}
\vspace{-0.2em}
\begin{columns}[T]
\begin{column}{0.50\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 1. Neo4j Graph Database Property Schema}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.6pt}\selectfont
\textbf{Node Labels \& Properties:}
\begin{itemize}\itemsep0.15em
  \item \textbf{\texttt{:Process}}: \texttt{\{pid: Int, name: Str, path: Str, cmdline: Str, uid: Int, host\_id: Str, start\_time: Timestamp\}}
  \item \textbf{\texttt{:File}}: \texttt{\{path: Str, name: Str, file\_type: Str, size\_bytes: Int, permissions: Str\}}
  \item \textbf{\texttt{:Socket}}: \texttt{\{src\_ip: Str, src\_port: Int, dst\_ip: Str, dst\_port: Int, protocol: Str\}}
\end{itemize}
\textbf{Directed Relationship Types:}
\begin{itemize}\itemsep0.15em
  \item \textbf{\texttt{[:FORK]}}: \texttt{(Process) $\rightarrow$ (Process) \{timestamp\}}
  \item \textbf{\texttt{[:EXEC]}}: \texttt{(Process) $\rightarrow$ (File) \{timestamp, cmdline\}}
  \item \textbf{\texttt{[:READ | :WRITE]}}: \texttt{(Process) $\rightarrow$ (File) \{timestamp, bytes\}}
  \item \textbf{\texttt{[:CONNECT]}}: \texttt{(Process) $\rightarrow$ (Socket) \{timestamp, state\}}
\end{itemize}
}
\end{column}

\begin{column}{0.48\textwidth}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.4em,wd=\textwidth]{block title}
\textbf{\scriptsize 2. Relational Metadata Store (SQLite / PostgreSQL)}
\end{beamercolorbox}
\vspace{0.2em}
{\fontsize{6.8pt}{8.6pt}\selectfont
\begin{itemize}\itemsep0.25em
  \item \textbf{\texttt{hosts}}:
    \begin{itemize}\itemsep0.05em
      \item \texttt{host\_id} (PK), \texttt{hostname}, \texttt{os\_platform}, \texttt{ip\_addr}, \texttt{agent\_status}, \texttt{last\_seen}
    \end{itemize}
  \item \textbf{\texttt{anomalies}}:
    \begin{itemize}\itemsep0.05em
      \item \texttt{anomaly\_id} (PK), \texttt{host\_id} (FK), \texttt{window\_id}, \texttt{recon\_loss}, \texttt{kl\_score}, \texttt{threshold}, \texttt{timestamp}
    \end{itemize}
  \item \textbf{\texttt{attack\_subgraphs}}:
    \begin{itemize}\itemsep0.05em
      \item \texttt{subgraph\_id} (PK), \texttt{anomaly\_id} (FK), \texttt{seed\_pid}, \texttt{node\_count}, \texttt{edge\_count}, \texttt{mitre\_tactics}, \texttt{graph\_json}
    \end{itemize}
  \item \textbf{\texttt{federated\_rounds}}:
    \begin{itemize}\itemsep0.05em
      \item \texttt{round\_id} (PK), \texttt{client\_count}, \texttt{global\_loss}, \texttt{ckks\_poly\_degree}, \texttt{duration\_sec}
    \end{itemize}
\end{itemize}
}
\end{column}
\end{columns}
\end{frame}
''')

    # 13. ALGORITHMS (Two clear slides)
    doc.append(r'''
%% ======================================================================
%%  13. ALGORITHMS
%% ======================================================================
\section{Algorithms}

\begin{frame}{13a. Algorithm 1: Privacy-Preserving Federated ST-VGAE Training via TenSEAL CKKS}
\vspace{-0.2em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.35em,wd=\textwidth]{codeBg}
\fontsize{6.0pt}{7.6pt}\selectfont\ttfamily
\textbf{Algorithm 1: Privacy-Preserving Federated ST-VGAE Training}\\
\textbf{Input:} $K$ distributed host clients $\mathcal{S}=\{1,\dots,K\}$, local graph snapshot streams $\mathcal{D}_k$, communication rounds $R$, local epochs $E$, CKKS context $(pk, sk)$.\\
\textbf{Output:} Universally converged global ST-VGAE weights $\mathbf{w}^{(R)}$.
\vspace{0.15cm}
\begin{enumerate}\itemsep0.10em
  \item Server initializes global parameter vector $\mathbf{w}^{(0)}$ and distributes CKKS public encryption key $pk$.
  \item \textbf{for} each federated communication round $r = 0, 1, \dots, R-1$ \textbf{do}:
  \begin{enumerate}\itemsep0.05em
    \item Server broadcasts current global model weights $\mathbf{w}^{(r)}$ to all participating clients $k \in \mathcal{S}$.
    \item \textbf{for} each client $k \in \mathcal{S}$ \textbf{in parallel do}:
    \begin{enumerate}\itemsep0.03em
      \item Set local model weights $\mathbf{w}_k \leftarrow \mathbf{w}^{(r)}$.
      \item \textbf{for} local epoch $e = 1$ to $E$ \textbf{do}:
      \item \quad Feed temporal graph window sequence $\{G_{t-w+1},\dots,G_t\}$ to ST-VGAE.
      \item \quad Compute loss: $\mathcal{L}_k = \text{BCE}(\mathbf{A}_t, \hat{\mathbf{A}}_t) + \beta D_{KL}(q(\mathbf{Z}_t \mid \mathbf{A}_t, \mathbf{X}_t) \parallel \mathcal{N}(0, \mathbf{I}))$.
      \item \quad Update $\mathbf{w}_k \leftarrow \mathbf{w}_k - \eta \nabla \mathcal{L}_k$ using Adam optimizer.
      \item Compute parameter differential: $\Delta \mathbf{w}_k = \mathbf{w}_k - \mathbf{w}^{(r)}$.
      \item Encrypt parameter delta using TenSEAL CKKS: $[[\Delta \mathbf{w}_k]] \leftarrow \text{CKKS.Enc}(\Delta \mathbf{w}_k, pk)$.
      \item Transmit encrypted ciphertext $[[\Delta \mathbf{w}_k]]$ and sample count $N_k$ to Server.
    \end{enumerate}
    \item Server performs homomorphic aggregation on ciphertexts without decryption:
          $$[[\Delta \mathbf{w}_{\text{global}}]] \leftarrow \sum_{k=1}^K \frac{N_k}{\sum_j N_j} [[\Delta \mathbf{w}_k]]$$
    \item Server broadcasts encrypted global update $[[\Delta \mathbf{w}_{\text{global}}]]$ to clients.
    \item Clients decrypt update using private key $sk$: $\Delta \mathbf{w}_{\text{global}} \leftarrow \text{CKKS.Dec}([[\Delta \mathbf{w}_{\text{global}}]], sk)$.
    \item Update global model weights for next round: $\mathbf{w}^{(r+1)} \leftarrow \mathbf{w}^{(r)} + \Delta \mathbf{w}_{\text{global}}$.
  \end{enumerate}
\end{enumerate}
\end{beamercolorbox}
\end{frame}

\begin{frame}{13b. Algorithm 2: Causal Attack Subgraph Reconstruction \& MITRE ATT\&CK Attribution}
\vspace{-0.2em}
\begin{beamercolorbox}[rounded=true,shadow=false,sep=0.35em,wd=\textwidth]{codeBg}
\fontsize{6.0pt}{7.6pt}\selectfont\ttfamily
\textbf{Algorithm 2: Causal Attack Subgraph Reconstruction and MITRE ATT\&CK Attribution}\\
\textbf{Input:} Dynamic Provenance Graph $PG = (V, E)$, Anomaly Seed Nodes $\mathcal{M} = \{m_1, m_2, \dots\}$, Hop Limit $k$, MITRE ATT\&CK Rule Base $\mathcal{R}$.\\
\textbf{Output:} Ordered Attack Scenario Subgraph Directed Acyclic Graph (DAG) $\mathcal{S}_{\text{attack}}$ with attributed TTPs.
\vspace{0.15cm}
\begin{enumerate}\itemsep0.10em
  \item Initialize Attack Scenario Graph $\mathcal{S}_{\text{attack}} \leftarrow \emptyset$.
  \item \textbf{for} each seed node $m \in \mathcal{M}$ \textbf{do}:
  \begin{enumerate}\itemsep0.05em
    \item \textbf{if} $\text{type}(m) == \text{Process}$ \textbf{and} $\text{confidence}(m) > \tau_{\text{outlier}}$ \textbf{then}:
    \begin{enumerate}\itemsep0.03em
      \item \textit{// Backward Causal Traversal to identify Initial Access / Root Cause:}
      \item $\mathcal{V}_{\text{root}} \leftarrow \text{BFS\_Traverse\_Backward}(m, \text{depth}=k, \text{edge\_filters}=\{\text{FORK}, \text{EXEC}, \text{CONNECT}\})$.
      \item \textit{// Forward Causal Traversal to identify Blast Radius, Staging and Exfiltration:}
      \item $\mathcal{V}_{\text{impact}} \leftarrow \text{BFS\_Traverse\_Forward}(m, \text{depth}=k, \text{edge\_filters}=\{\text{READ}, \text{WRITE}, \text{CONNECT}\})$.
      \item Combine subgraph nodes: $\mathcal{V}_{\text{sub}} \leftarrow \{m\} \cup \mathcal{V}_{\text{root}} \cup \mathcal{V}_{\text{impact}}$.
      \item Induce edge set: $\mathcal{E}_{\text{sub}} \leftarrow \{(u, v) \in E \mid u, v \in \mathcal{V}_{\text{sub}}\}$.
      \item \textit{// Semantic Noise Pruning:} Remove whitelisted system background daemons and duplicate read/write cycles.
      \item Construct candidate subgraph: $SG = (\mathcal{V}_{\text{sub}}, \mathcal{E}_{\text{sub}})$.
      \item \textbf{for} each edge $e \in \mathcal{E}_{\text{sub}}$ \textbf{do}:
      \item \quad Match edge semantics against rule base: $\text{label}(e) \leftarrow \{r \in \mathcal{R} \mid \text{MatchCondition}(e, r) == \text{True}\}$.
      \item \quad Assign MITRE TTPs: $\text{TTP}(e) \leftarrow \tau(\text{label}(e))$, $\text{Stage}(e) \leftarrow \sigma(\text{label}(e))$.
      \item Correlate sequence chronologically into attack stages: $SG \leftarrow \langle\text{Initial Access} \rightarrow \text{Persistence} \rightarrow \text{Lateral} \rightarrow \text{Exfil}\rangle$.
      \item $\mathcal{S}_{\text{attack}} \leftarrow \mathcal{S}_{\text{attack}} \cup \{SG\}$.
    \end{enumerate}
  \end{enumerate}
  \item \textbf{return} $\mathcal{S}_{\text{attack}}$.
\end{enumerate}
\end{beamercolorbox}
\end{frame}
''')

    # RESEARCH GAPS & TECHNICAL MOTIVATION
    doc.append(r'''
%% ======================================================================
%%  RESEARCH GAPS & PROPOSED SOLUTIONS
%% ======================================================================
\section{Research Gap}

\begin{frame}{Research Gaps \& Proposed Solutions}
\vspace{-0.2em}
{\fontsize{7.5pt}{9.8pt}\raggedright\selectfont
\begin{itemize}\itemsep0.45em
  \item \textbf{1. Separate Defenses for Network and Host:}\\
  \textbf{Gap:} Current security tools inspect network traffic and host audit logs in isolation, missing stealthy APTs that transition between network entry and host execution.\\
  \textbf{Solution:} We build an integrated platform combining fast network traffic filtering with deep host provenance graph analysis.

  \item \textbf{2. Graph Explosion and Loss of Causal Context:}\\
  \textbf{Gap:} Naive provenance graphs suffer from catastrophic dependency explosion, while tabular machine learning flattens logs, stripping causal chains.\\
  \textbf{Solution:} We implement semantics-preserving compression and session-based execution partitioning to retain critical $Process \rightarrow File \rightarrow Socket$ chains.

  \item \textbf{3. Heavy Dependence on Labeled Attack Data:}\\
  \textbf{Gap:} Supervised detection algorithms require labeled attack samples and fail completely against novel zero-day campaigns.\\
  \textbf{Solution:} We train an unsupervised ST-VGAE (GAT + GRU + VGAE) strictly on benign activity, flagging anomalous graph deviations via reconstruction error.

  \item \textbf{4. Privacy Bottlenecks and Alert Overload:}\\
  \textbf{Gap:} Sharing raw logs across organizations violates privacy laws, while standard Federated Learning leaks gradients, and raw anomaly scores overwhelm analysts.\\
  \textbf{Solution:} We apply TenSEAL CKKS Homomorphic Encryption for secure federated aggregation and map reconstructed attack paths directly to MITRE ATT\&CK tactics.
\end{itemize}
}
\end{frame}
''')

    # WORK PLAN & GANTT CHART
    doc.append(r'''
%% ======================================================================
%%  WORK PLAN & GANTT CHART
%% ======================================================================
\section{Work Plan \& Gantt Chart}

\begin{frame}{Project Work Plan \& Gantt Chart (System Life Cycle)}
\vspace{-0.15em}
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
  x=1.55cm, y=0.72cm,
  done/.style  ={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                 font=\fontsize{5.2}{6}\selectfont\bfseries\color{white},
                 fill=prismNavy!85!black},
  now/.style   ={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                 font=\fontsize{5.2}{6}\selectfont\bfseries\color{white},
                 fill=prismGold!90!black, draw=prismGold, line width=0.8pt},
  future/.style={rounded corners=2pt, minimum height=0.44cm, inner sep=2pt,
                 font=\fontsize{5.2}{6}\selectfont\bfseries\color{white!70!gray},
                 fill=gray!35},
  hdr/.style={font=\fontsize{6.5}{7.5}\selectfont\bfseries, text=prismNavy},
  lbl/.style={font=\fontsize{6.5}{7.5}\selectfont, text=black, anchor=east},
  gl/.style={draw=gray!22, line width=0.4pt},
  stripe/.style={fill=prismMint!55}
]
\foreach \r in {1,3,5,7,9} { \fill[stripe] (-4.3,\r-0.5) rectangle (9.05,\r+0.5); }
\foreach \col/\mo in {0/{Jul'26},1/{Aug'26},2/{Sep'26},3/{Oct'26},4/{Nov'26},5/{Dec'26},6/{Jan'27},7/{Feb'27},8/{Mar'27}} {
  \draw[gl] (\col, 0.5) -- (\col, 10.5);
  \node[hdr] at (\col+0.5, 10.85) {\mo};
}
\draw[gl] (9.0, 0.5) -- (9.0, 10.5);
\draw[prismNavy, line width=1.0pt] (-4.3, 10.5) -- (9.05, 10.5);
\draw[prismNavy, line width=0.5pt] (-4.3, 0.5)  -- (9.05, 0.5);
\draw[prismGold!80!orange, line width=1.4pt, dashed] (2.23, 0.5) -- (2.23, 10.5);
\node[font=\fontsize{5.2}{6}\selectfont\bfseries, text=prismGold!80!orange, rotate=90, anchor=south] at (2.23, 9.2) {Today};
\node[lbl] at (-0.12, 9) {1. Planning \& Problem Identification};
\node[done, minimum width=1.55cm] at (0.775, 9) {\checkmark\ Completed};
\node[lbl] at (-0.12, 8) {2. Requirement Analysis \& Feasibility Study};
\node[now, minimum width=1.55cm] at (2.20, 8) {$\blacktriangleright$ In Progress};
\node[lbl] at (-0.12, 7) {3. System Architecture \& Graph Schema Design};
\node[future, minimum width=1.55cm] at (3.275, 7) {Upcoming};
\node[lbl] at (-0.12, 6) {4. DARPA TC Data Ingestion \& Compression};
\node[future, minimum width=1.55cm] at (4.275, 6) {Upcoming};
\node[lbl] at (-0.12, 5) {5. ST-VGAE Model Implementation (GAT+GRU)};
\node[future, minimum width=1.55cm] at (5.275, 5) {Upcoming};
\node[lbl] at (-0.12, 4) {6. TenSEAL CKKS Federated Learning};
\node[future, minimum width=1.55cm] at (6.275, 4) {Upcoming};
\node[lbl] at (-0.12, 3) {7. Neo4j Causal Tracing \& ATT\&CK Mapping};
\node[future, minimum width=1.55cm] at (7.275, 3) {Upcoming};
\node[lbl] at (-0.12, 2) {8. System Verification, Benchmarking \& SOC UI};
\node[future, minimum width=1.20cm] at (7.90, 2) {Upcoming};
\node[lbl] at (-0.12, 1) {9. Final Documentation \& Capstone Defense};
\node[future, minimum width=1.55cm] at (8.275, 1) {Upcoming};
\end{tikzpicture}}
\vspace{0.10em}
\begin{center}
\fontsize{6.5}{8}\selectfont
{\color{prismNavy!85!black}$\blacksquare$}~\textbf{Completed}\qquad
{\color{prismGold!90!black}$\blacksquare$}~\textbf{In Progress (Now)}\qquad
{\color{gray!55}$\blacksquare$}~\textbf{Upcoming}\qquad
{\color{prismGold!80!orange}$\boldsymbol{|}$}~\textbf{Current Milestone (Sep 2026)}
\end{center}
\end{frame}
''')

    # REFERENCES
    doc.append(r'''
%% ======================================================================
%%  REFERENCES
%% ======================================================================
\section{References}

\begin{frame}[t]{References}
\vspace{-0.2em}
\fontsize{6.5pt}{8.5pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item[\textbf{[1]}] \textbf{Mengjiao Cui, Zhengwei Jiang, Shuai Li, Chunyan Ma, Kai Zhang, Peian Yang, and Huamin Feng}, ``MGDA: A provenance graph-based framework for threat detection and attack scenario reconstruction,'' \textit{Computer Networks}, vol.~274, p.~111806, 2025. DOI: 10.1016/j.comnet.2025.111806
  \item[\textbf{[2]}] \textbf{Qi Liu, Kaibin Bao, and Veit Hagenmeyer}, ``Commander: A robust cross-machine multi-phase Advanced Persistent Threat detector via provenance analytics,'' \textit{Journal of Information Security and Applications}, vol.~91, p.~104057, 2025. DOI: 10.1016/j.jisa.2025.104057
  \item[\textbf{[3]}] \textbf{Roberto Canonico, Francesco Lista, Annalisa Navarro, Giancarlo Sperl{\'\i}, and Andrea Vignali}, ``Threat detection in reconfigurable Cyber--Physical Systems through Spatio-Temporal Anomaly Detection using graph attention network,'' \textit{Computers \& Security}, vol.~156, p.~104509, 2025. DOI: 10.1016/j.cose.2025.104509
  \item[\textbf{[4]}] \textbf{Osei Isaac, Benjamin Appiah, Daniel Commey, Kwabena Owusu-Agyemang, Michael Asante, and Benjamin Hayfrom Acquah}, ``EdgeFence: Federated Temporal Graph Neural Networks for Lightweight, Adversarial Malware Detection in Distributed Edge Networks,'' \textit{International Journal of Information Security}, vol.~25, p.~88, 2026. DOI: 10.1007/s10207-026-01237-x
  \item[\textbf{[5]}] \textbf{Parth Atulbhai Gandhi, Prasanna N. Wudali, Yonatan Amaru, Akansha Shukla, Yuval Elovici, and Asaf Shabtai}, ``SHIELD: Advanced persistent threats detection and intelligent explanation using large language models,'' \textit{Engineering Applications of Artificial Intelligence}, vol.~181, p.~115443, 2026.
  \item[\textbf{[6]}] \textbf{Francesco Ferazza, Cosimo Melella, Konstantinos Mersinas, Ricardo Lugo, and Rain Ottis}, ``From logs to tactics: unsupervised reconstruction of APT campaigns with MITRE-enriched meta-alerts,'' \textit{International Journal of Information Security}, vol.~25, p.~79, 2026.
  \item[\textbf{[7]}] \textbf{Gisung Kim, Seungmin Lee, and Sehun Kim}, ``A novel hybrid intrusion detection method integrating anomaly detection with misuse detection,'' \textit{Expert Systems with Applications}, vol.~41, no.~4, pp.~1690--1700, 2014.
  \item[\textbf{[8]}] \textbf{Haiyang Diao, Xiang Li, Wan Zhang, Yan Sibyl Yu, Ye Wang, and Jing Zhang}, ``Self-supervised graph neural networks for network intrusion detection in cloud-edge,'' \textit{Journal of Cloud Computing}, vol.~15, no.~1, p.~24, 2026.
\end{itemize}
\end{frame}

\begin{frame}[t]{References}
\vspace{-0.2em}
\fontsize{6.5pt}{8.5pt}\selectfont
\begin{itemize}\itemsep0.20em
  \item[\textbf{[9]}] \textbf{Eslam Amer, Shaker El-Sappagh, Tamer Abuhamad, Bander Ali Saleh Al-Rimy, and Alaa Mohasseb}, ``GraphShield: Advanced dynamic graph-based malware detection using graph neural networks,'' \textit{Expert Systems with Applications}, vol.~268, p.~129812, 2025.
  \item[\textbf{[10]}] \textbf{Fargana Abdullayeva and Suleyman Suleymanzade}, ``Cyber security attack recognition on cloud computing networks based on GCN and GraphSAGE models,'' \textit{Results in Control and Optimization}, vol.~16, p.~100423, 2024.
  \item[\textbf{[11]}] \textbf{Rana Abu Bakar, Lorenzo De Marinis, Filippo Cugini, and Francesco Paolucci}, ``FTG-Net-E: A hierarchical ensemble graph neural network for DDoS attack detection,'' \textit{Computer Networks}, vol.~248, p.~110508, 2024.
  \item[\textbf{[12]}] \textbf{Md Shakil Siddique, Md. Ashikur Rahman Khan, Ishtiaq Ahammad, Nishu Nath, Joysri Rani Das, and Fardowsi Rahman}, ``Intelligent intrusion detection for cyber-physical systems using GAN-LSTM,'' \textit{Franklin Open}, vol.~11, p.~100281, 2025.
  \item[\textbf{[13]}] \textbf{Ali Yilmaz, Resul Das, Mehmet Ozdem, and Berk Canberk}, ``Knowledge graph visualization and anomaly detection using graph neural networks,'' \textit{Computer Networks}, vol.~278, p.~112632, 2026.
  \item[\textbf{[14]}] \textbf{Giancarlo Iannizzotto, Andrea Nucita, and Andrea Siragusa}, ``Robust, efficient detection of network intrusion attacks: A large language model approach,'' \textit{Computer Networks}, vol.~276, p.~112559, 2026.
  \item[\textbf{[15]}] \textbf{Abdullah Al Mamun, Harith Al-Sahaf, Ian Welch, and Masood Mansoori}, ``Detection of advanced persistent threat: A genetic programming approach,'' \textit{Applied Soft Computing}, vol.~167, p.~112447, 2024.
  \item[\textbf{[16]}] \textbf{Mohammed Alshehri}, ``Dynamic cyber deception using AI-driven adaptive honeypot networks,'' \textit{Ain Shams Engineering Journal}, vol.~17, no.~3, p.~104061, 2026.
\end{itemize}
\end{frame}
''')

    # CLOSING SLIDE
    doc.append(r'''
%% ======================================================================
%%  CLOSING SLIDE
%% ======================================================================
\begin{frame}[plain]
\begin{tikzpicture}[remember picture,overlay]
  \fill[prismNavy] (current page.south west) rectangle (current page.north east);
  \node at ([yshift=2.4cm]current page.center)
        {\includegraphics[height=1.3cm]{cek-logo.png}};
  \node[text=white,font=\fontsize{32}{36}\selectfont\bfseries]
        at ([yshift=0.7cm]current page.center) {Thank You};
  \node[text=prismGold,font=\large]
        at ([yshift=-0.35cm]current page.center) {Questions \& Discussion};
  \node[text=white!90,font=\small,align=center]
        at ([yshift=-1.65cm]current page.center)
        {\textbf{Muhammed Nasih K P} (KNP23CS074)\qquad \textbf{Sumayya Ershad} (KNP23CS107)\\[0.15cm]
         \textbf{Najmunniza N} (LKNP20CS056)\qquad \textbf{K.S.\ Mahadev} (KNP23CS066)};
  \node[text=prismMint!80,font=\footnotesize,align=center]
        at ([yshift=-2.6cm]current page.center)
        {Department of Computer Science \& Engineering\\
         College of Engineering, Karunagappally};
  \node[text=prismGold!60,font=\scriptsize]
        at ([yshift=-3.3cm]current page.center)
        {Guide: Mrs.\ SYAMA S R, Assistant Professor};
\end{tikzpicture}
\end{frame}

\end{document}
''')

    full_tex = "".join(doc)
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(full_tex)
    print("Successfully wrote main.tex (length: %d chars)" % len(full_tex))

if __name__ == '__main__':
    build_latex()
