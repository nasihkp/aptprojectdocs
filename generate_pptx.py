import os
import sys
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import pymupdf

def build_presentation():
    prs = Presentation()
    # 16:9 widescreen: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette from nobinsijo.pdf
    NAVY = RGBColor(15, 34, 64)        # #0F2240
    BLUE = RGBColor(24, 76, 120)       # #184C78
    MINT = RGBColor(208, 232, 225)     # #D0E8E1
    MINT_LIGHT = RGBColor(235, 245, 242)
    GOLD = RGBColor(212, 143, 56)      # #D48F38
    BG_LIGHT = RGBColor(248, 250, 252) # #F8FAFC
    WHITE = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(20, 25, 35)
    TEXT_MUTED = RGBColor(90, 100, 115)
    BORDER_LIGHT = RGBColor(215, 225, 235)
    GREEN = RGBColor(45, 125, 70)
    RED = RGBColor(179, 38, 30)

    # Open PDF to extract rendered slides for diagrams and literature review
    pdf_path = os.path.join("pptformat", "main.pdf")
    doc = pymupdf.open(pdf_path)
    
    # Directory to store rendered page images (clean cache to prevent stale page mappings)
    if os.path.exists("ppt_images"):
        shutil.rmtree("ppt_images")
    os.makedirs("ppt_images", exist_ok=True)
    
    def render_pdf_page(page_idx):
        img_path = os.path.join("ppt_images", f"page_{page_idx+1}.png")
        if not os.path.exists(img_path):
            page = doc[page_idx]
            pix = page.get_pixmap(dpi=300)
            pix.save(img_path)
        return img_path

    def add_standard_header(slide, title_text, section_category="B.Tech Final Year Project"):
        # Top Gold Accent Line
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = GOLD
        top_line.line.color.rgb = GOLD
        
        # Header banner area
        header_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.18), Inches(10.5), Inches(0.85))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Section category small label
        p_sec = tf.paragraphs[0]
        p_sec.text = section_category.upper()
        p_sec.font.name = "Arial"
        p_sec.font.size = Pt(8.5)
        p_sec.font.bold = True
        p_sec.font.color.rgb = BLUE
        p_sec.space_after = Pt(2)
        
        # Main Slide Title
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(17.5)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        
        # CEK logo in top right if exists
        logo_path = os.path.join("pptformat", "cek-logo.png")
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(12.0), Inches(0.18), height=Inches(0.70))

        # Bottom thin header line
        b_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.10), Inches(12.133), Inches(0.015))
        b_line.fill.solid()
        b_line.fill.fore_color.rgb = BORDER_LIGHT
        b_line.line.color.rgb = BORDER_LIGHT

        # Standard Footer
        f_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.01))
        f_line.fill.solid()
        f_line.fill.fore_color.rgb = BORDER_LIGHT
        f_line.line.color.rgb = BORDER_LIGHT

        ft_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.10), Inches(12.133), Inches(0.30))
        ft_tf = ft_box.text_frame
        ft_tf.margin_left = ft_tf.margin_top = ft_tf.margin_right = ft_tf.margin_bottom = 0
        p_ft = ft_tf.paragraphs[0]
        p_ft.text = "College of Engineering Karunagappally  |  Department of Computer Science & Engineering  |  B.Tech Capstone 2026-27"
        p_ft.font.name = "Arial"
        p_ft.font.size = Pt(8.0)
        p_ft.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, bg_color=WHITE, border_color=BORDER_LIGHT):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        
        if title:
            # Title banner on card
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.35))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = NAVY
            
            # Subtle divider
            div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.2), top + Inches(0.52), width - Inches(0.4), Inches(0.01))
            div.fill.solid()
            div.fill.fore_color.rgb = border_color
            div.line.color.rgb = border_color
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Page 1)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    # Top gold accent
    t_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    t_bar.fill.solid()
    t_bar.fill.fore_color.rgb = GOLD
    t_bar.line.color.rgb = GOLD

    # College Logo
    logo_path = os.path.join("pptformat", "cek-logo.png")
    if os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(5.966), Inches(0.65), height=Inches(1.2))

    # Title & Subtitle Box
    tbox = slide1.shapes.add_textbox(Inches(0.8), Inches(2.05), Inches(11.733), Inches(1.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "CYBER ATTACK PREDICTION PLATFORM"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = GOLD
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Privacy-Preserving Provenance Graph Threat Detection & Cross-Machine Attack Scenario Reconstruction in Enterprise and ICS Networks"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.color.rgb = WHITE

    # Project Details Container
    pcard = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.1), Inches(10.933), Inches(2.65))
    pcard.fill.solid()
    pcard.fill.fore_color.rgb = RGBColor(22, 48, 85) # Slightly lighter navy
    pcard.line.color.rgb = GOLD
    pcard.line.width = Pt(1.2)

    # Team Members (Left)
    tm_box = slide1.shapes.add_textbox(Inches(1.5), Inches(4.25), Inches(5.0), Inches(2.3))
    tm_tf = tm_box.text_frame
    tm_tf.word_wrap = True
    tm_h = tm_tf.paragraphs[0]
    tm_h.text = "PROJECT TEAM MEMBERS:"
    tm_h.font.name = "Arial"
    tm_h.font.size = Pt(10.5)
    tm_h.font.bold = True
    tm_h.font.color.rgb = MINT
    tm_h.space_after = Pt(6)

    members = [
        ("Muhammed Nasih K P", "KNP23CS074"),
        ("Sumayya Ershad", "KNP23CS107"),
        ("Najmunniza N", "LKNP20CS056"),
        ("K.S. Mahadev", "KNP23CS066")
    ]
    for name, reg in members:
        p = tm_tf.add_paragraph()
        p.text = f"•  {name}  ({reg})"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        p.space_after = Pt(3)

    # Department & Guide (Right)
    dg_box = slide1.shapes.add_textbox(Inches(6.9), Inches(4.25), Inches(4.8), Inches(2.3))
    dg_tf = dg_box.text_frame
    dg_tf.word_wrap = True
    dg_h = dg_tf.paragraphs[0]
    dg_h.text = "INSTITUTION & SUPERVISION:"
    dg_h.font.name = "Arial"
    dg_h.font.size = Pt(10.5)
    dg_h.font.bold = True
    dg_h.font.color.rgb = MINT
    dg_h.space_after = Pt(6)

    inst_lines = [
        "Project Guide: Mrs. SYAMA S R, Assistant Professor",
        "Department of Computer Science & Engineering",
        "College of Engineering Karunagappally",
        "APJ Abdul Kalam Technological University (KTU)",
        "Academic Year: 2026-2027"
    ]
    for line in inst_lines:
        p = dg_tf.add_paragraph()
        p.text = f"•  {line}"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = WHITE
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 2: Presentation Overview (Page 2)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide2, "Presentation Overview: Project Phases & Agenda", "B.Tech Capstone Project Structure")
    
    # Left Column: Phases I - III
    add_card(slide2, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "PHASES I - III: Foundations, Architecture & Models", BG_LIGHT)
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(2.05), Inches(5.3), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    part1_items = [
        ("Phase I: Foundations & Problem Formulation", [
            ("01. Introduction", "Problem context, causal telemetry, core thesis"),
            ("02. Problem Statement", "Siloed logs, class imbalance, dependency explosion"),
            ("03. Objectives", "End-to-end telemetry reduction, edge AI, zero-day discovery"),
            ("04. Literature Review", "16 peer-reviewed base papers (2024-2026)"),
            ("05. Research Gaps & Solutions", "4 key enterprise vulnerabilities vs 4 proposed solutions")
        ]),
        ("Phase II: System Architecture & Workflow", [
            ("06. System Design Principles", "Streaming ingestion, models, datasets, dual-tier DB"),
            ("07. Workflow Diagram", "End-to-end ingestion, detection, and tracing pipeline")
        ]),
        ("Phase III: Multi-Model Detection Pipeline", [
            ("08. Proposed Methods", "Edge-TGNN, Masked-GAT autoencoder, tracing logic"),
            ("09. Model Responsibilities", "Role separation between edge sentry, SOC analyzer, tracing"),
            ("10. Inference Flow", "Real-time edge screening and scenario attribution")
        ])
    ]
    p_first = True
    for phase_name, items in part1_items:
        p_ph = tf.paragraphs[0] if p_first else tf.add_paragraph()
        p_first = False
        p_ph.text = phase_name.upper()
        p_ph.font.name = "Arial"
        p_ph.font.size = Pt(8.0)
        p_ph.font.bold = True
        p_ph.font.color.rgb = BLUE
        p_ph.space_after = Pt(2)
        for item, desc in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}: {desc}"
            p.font.name = "Arial"
            p.font.size = Pt(7.5)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(2)

    # Right Column: Phases IV - VI
    add_card(slide2, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "PHASES IV - VI: Data, Algorithms & Implementation", BG_LIGHT)
    tb2 = slide2.shapes.add_textbox(Inches(7.0), Inches(2.05), Inches(5.3), Inches(4.5))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    part2_items = [
        ("Phase IV: Data Engineering & Model Training", [
            ("11. Dataset Preparation", "DARPA TC benchmarks, 85% compaction, CDM schema"),
            ("12. Model Training & Evaluation", "Chronological splitting, loss functions, metrics")
        ]),
        ("Phase V: Deep Schemas & Core Algorithms", [
            ("13. System Architecture Diagram", "4-layer enterprise-grade SOC architecture"),
            ("14. Development Flowchart", "Lifecycle: Ingestion -> Training -> Testing -> Deploy"),
            ("15. Database Schema", "Neo4j graph property schema + PostgreSQL relational store"),
            ("16. Algorithms & Pseudocode", "Unified master pipeline + 3 detailed algorithms")
        ]),
        ("Phase VI: Implementation, Plan & Conclusion", [
            ("17. Implementation & Tech Stack", "Frameworks (PyG, Neo4j, FastAPI, Cytoscape)"),
            ("18. Project Work Plan & Gantt", "Implementation schedule, phases, and milestones"),
            ("19. Conclusion & Future Scope", "Project summary, achievements, and roadmap"),
            ("20. References", "Complete academic literature bibliography")
        ])
    ]
    p_first2 = True
    for phase_name, items in part2_items:
        p_ph = tf2.paragraphs[0] if p_first2 else tf2.add_paragraph()
        p_first2 = False
        p_ph.text = phase_name.upper()
        p_ph.font.name = "Arial"
        p_ph.font.size = Pt(8.0)
        p_ph.font.bold = True
        p_ph.font.color.rgb = BLUE
        p_ph.space_after = Pt(2)
        for item, desc in items:
            p = tf2.add_paragraph()
            p.text = f"•  {item}: {desc}"
            p.font.name = "Arial"
            p.font.size = Pt(7.5)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(2)

    # =========================================================================
    # SLIDE 3: 1. Introduction (Page 3)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide3, "1. Introduction", "Phase I: Foundations & Problem Formulation")
    
    # Large Card
    add_card(slide3, Inches(0.8), Inches(1.4), Inches(11.733), Inches(3.2), "Project Essence: Holistic Provenance-Based Cyber Defense", WHITE)
    tb = slide3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.133), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = (
        "Modern enterprise networks face hidden cyberattacks called Advanced Persistent Threats (APTs), which avoid traditional security systems by behaving like normal users over long periods. Traditional intrusion detection systems often analyze logs separately, missing important connections between processes, files, and network connections (Process → File → Socket).\n\n"
        "Our system represents system activities as dynamic provenance graphs and combines Graph Attention Networks (GAT), Gated Recurrent Units (GRU), and Variational Graph Autoencoders (VGAE) to learn normal behavior and detect unknown attacks without labeled training data. It also uses TenSEAL CKKS-encrypted Federated Learning to enable secure collaboration between organizations while protecting their data."
    )
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY
    p.line_spacing = 1.3

    # 3 Pill Badges Below
    pill_w = Inches(3.7)
    pill_h = Inches(1.8)
    pills = [
        ("Dynamic Provenance Graphs", "Captures exact kernel causality (Process → File → Socket), converting raw isolated audit events into directed execution dependency graphs.", MINT_LIGHT, BLUE),
        ("Unsupervised AI Detection", "Combines GAT + GRU + VGAE reconstruction loss to learn normal system behavior and detect unknown zero-day attacks without labeled data.", BG_LIGHT, NAVY),
        ("TenSEAL CKKS Privacy", "Applies homomorphic encryption to federated learning, enabling secure multi-organization collaboration without raw telemetry leakage.", MINT_LIGHT, GREEN)
    ]
    for i, (p_title, p_desc, p_bg, p_col) in enumerate(pills):
        px = Inches(0.8 + i * 4.01)
        add_card(slide3, px, Inches(4.9), pill_w, pill_h, p_title, p_bg)
        ptb = slide3.shapes.add_textbox(px + Inches(0.15), Inches(5.5), pill_w - Inches(0.3), Inches(1.1))
        ptf = ptb.text_frame
        ptf.word_wrap = True
        pp = ptf.paragraphs[0]
        pp.text = p_desc
        pp.font.name = "Arial"
        pp.font.size = Pt(8.5)
        pp.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: 2. Problem Statement (Page 4)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide4, "2. Problem Statement", "Phase I: Foundations & Problem Formulation")

    # Card 1: Silos & Explosion (Human-friendly, simple English, zero numbers)
    add_card(slide4, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.35), "Siloed Telemetry & Missed Connections", BG_LIGHT)
    tb1 = slide4.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.2), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "Traditional security systems struggle to detect stealthy, multi-stage cyberattacks because they analyze system logs separately, miss complex relationships and time-based attack patterns, and generate false alarms from normal activities.\n\n"
        "They also struggle to detect unknown zero-day threats while protecting sensitive data across distributed enterprise endpoints."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.35

    # Card 2: Proposed Solution
    add_card(slide4, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.35), "Proposed Graph AI & Privacy Framework", BG_LIGHT)
    tb2 = slide4.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "This project proposes a spatio-temporal graph-based anomaly detection framework using GAT, GRU, and VGAE to detect suspicious activities, reconstruct attack paths, map threats to the MITRE ATT&CK framework, and enable privacy-preserving collaborative detection."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.35

    # =========================================================================
    # SLIDE 5: 3. Objectives (Page 5)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide5, "3. Objectives", "Phase I: Foundations & Problem Formulation")

    add_card(slide5, Inches(0.8), Inches(1.4), Inches(11.733), Inches(3.2), "Primary Project Objective: Intelligent Privacy-Preserving APT Investigation", WHITE)
    tb = slide5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(11.133), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = (
        "The main objective of this project is to develop an intelligent and privacy-preserving cybersecurity system that detects hidden, multi-stage APT attacks and traces their attack paths across enterprise networks.\n\n"
        "The system converts raw kernel audit logs from the DARPA Transparent Computing dataset into provenance graphs and uses GAT, GRU, and VGAE to detect unknown attacks by identifying unusual graph patterns. It also supports secure collaborative training using TenSEAL CKKS encryption, reconstructs attack paths across multiple computers, maps detected threats to the MITRE ATT&CK framework, and displays the results on an interactive SOC dashboard."
    )
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY
    p.line_spacing = 1.3

    # 4 Objective Badges
    ob_w = Inches(2.78)
    ob_h = Inches(1.8)
    objs = [
        (">85% Telemetry Compaction", "Eliminates repetitive execution loops and redundant I/O operations with 0% causality loss.", MINT_LIGHT, BLUE),
        ("Spatio-Temporal Detection", "Unsupervised GAT + GRU + VGAE flags zero-day anomalies via graph reconstruction error.", BG_LIGHT, NAVY),
        ("TenSEAL CKKS Encryption", "Enables encrypted federated aggregation without raw telemetry or model gradient leakage.", MINT_LIGHT, GREEN),
        ("MITRE ATT&CK Attribution", "Reconstructs multi-host causal attack subgraphs with interactive real-time SOC triage.", BG_LIGHT, GOLD)
    ]
    for i, (o_title, o_desc, o_bg, o_col) in enumerate(objs):
        ox = Inches(0.8 + i * 2.98)
        add_card(slide5, ox, Inches(4.9), ob_w, ob_h, o_title, o_bg)
        otb = slide5.shapes.add_textbox(ox + Inches(0.12), Inches(5.5), ob_w - Inches(0.24), Inches(1.1))
        otf = otb.text_frame
        otf.word_wrap = True
        op = otf.paragraphs[0]
        op.text = o_desc
        op.font.name = "Arial"
        op.font.size = Pt(8.5)
        op.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDES 6 to 21: 4. Literature Review (16 Papers Preserved Exactly Unchanged)
    # =========================================================================
    # Requirement: Keep every existing literature review slide exactly unchanged.
    # Do not modify text, tables, colors, citations, or order.
    for page_idx in range(5, 21):
        s = prs.slides.add_slide(blank_layout)
        img = render_pdf_page(page_idx)
        s.shapes.add_picture(img, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 22: 5. Research Gaps & Proposed Solutions (Page 22)
    # =========================================================================
    slide22 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide22, "5. Identified Research Gaps & Proposed Solutions", "Phase I: Foundations & Problem Formulation")
    
    card_w = Inches(5.7)
    card_h = Inches(5.6)
    
    # Left Tab: Research Gaps
    add_card(slide22, Inches(0.8), Inches(1.35), card_w, card_h, "Research Gaps (Existing Systems)", BG_LIGHT)
    tb_gaps = slide22.shapes.add_textbox(Inches(1.0), Inches(1.95), card_w - Inches(0.4), card_h - Inches(0.7))
    tf_gaps = tb_gaps.text_frame
    tf_gaps.word_wrap = True
    gaps_text = (
        "• 1. Isolated Logs and Missed Attack Paths:\n"
        "Existing tools analyze each computer separately, making it difficult to track attackers moving between machines. Combining all logs can also increase storage and processing costs.\n\n"
        "• 2. Dependence on Known Attacks:\n"
        "Many AI models require labeled attack data, making it difficult to detect new, unknown zero-day attacks and increasing false alarms.\n\n"
        "• 3. Privacy Risks and High Resource Usage:\n"
        "Sharing raw logs creates privacy risks, while complex graph AI models require too much time and computing power for resource-limited devices."
    )
    p = tf_gaps.paragraphs[0]
    p.text = gaps_text
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DARK
    p.line_spacing = 1.3

    # Right Tab: Proposed Solutions
    add_card(slide22, Inches(6.8), Inches(1.35), card_w, card_h, "Proposed Solutions (Our System)", MINT_LIGHT)
    tb_sols = slide22.shapes.add_textbox(Inches(7.0), Inches(1.95), card_w - Inches(0.4), card_h - Inches(0.7))
    tf_sols = tb_sols.text_frame
    tf_sols.word_wrap = True
    sols_text = (
        "• 1. Network-Wide Attack Tracking:\n"
        "Connect related events across multiple computers to reconstruct complete attack paths while reducing unnecessary graph complexity.\n\n"
        "• 2. Unsupervised Zero-Day Detection:\n"
        "Use Masked-GAT to learn normal system behavior and identify unknown attacks without requiring labeled attack data.\n\n"
        "• 3. Lightweight and Privacy-Preserving AI:\n"
        "Run a compact model locally for fast detection and use TenSEAL CKKS-encrypted Federated Learning to train collaboratively without sharing raw system logs."
    )
    p = tf_sols.paragraphs[0]
    p.text = sols_text
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.color.rgb = NAVY
    p.line_spacing = 1.3

    # =========================================================================
    # SLIDE 23: 6. System Design Principles: Core Features & Architecture (Slide 1/2)
    # =========================================================================
    slide23 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide23, "6. System Design Principles: Core Features & Architecture", "Phase II: System Architecture & Workflow (Part 1/2)")

    add_card(slide23, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Core System Features & Architecture", BG_LIGHT)
    tb1 = slide23.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Continuous Telemetry Ingestion:\n"
        "  Streams DARPA TC CDM Avro/JSON logs, Linux Auditd, CamFlow LSM hooks, Windows Sysmon v14, Security Event Logs (4624, 4768, 4778), and ICS Modbus/DNP3 events.\n\n"
        "• Semantics-Preserving Compaction:\n"
        "  Collapses high-frequency execution loops (reads, writes, socket polling) reducing volume >85% while guaranteeing 0% causality loss.\n\n"
        "• Decoupled Feature Representation:\n"
        "  Encodes entities into 6D one-hot vectors for microsecond GPU tensor computation; offloads heavy string attributes to external lookup tables.\n\n"
        "• Dual-Tier AI Detection Engine:\n"
        "  On-device Edge-TGNN (79.63 KB footprint, 3.2 ms latency) with 3-step PGD adversarial hardening + SOC Masked-GAT autoencoder with K-d tree anomaly scoring.\n\n"
        "• Whole-Network Kill-Chain Tracing:\n"
        "  Logon-session partitioned bidirectional BFS with synthetic pseudo-edges, bridging disjoint attacks across Windows AD, Linux, and ICS networks."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide23, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Technologies, Frameworks & Core Libraries", BG_LIGHT)
    tb2 = slide23.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Deep Learning & Graph Frameworks:\n"
        "  - Python 3.10+, PyTorch v2.2.0, PyTorch Geometric (PyG v2.5.0)\n"
        "  - Deep Graph Library (DGL v1.1) for scalable message passing\n"
        "  - SciPy v1.12 for Spatial K-d Tree indexing (k=10 neighbor search)\n"
        "  - Scikit-Learn & NumPy for data modeling and vector math\n\n"
        "• Privacy-Preserving Federated Cryptography:\n"
        "  - TenSEAL CKKS Homomorphic Encryption for secure model aggregation\n"
        "  - Decentralized FedAvg training preserving raw audit privacy\n\n"
        "• Ingestion Sensors & Forensics Dashboard:\n"
        "  - FastAvro v1.9 for binary CDM stream ingestion\n"
        "  - Linux Auditd, CamFlow v0.5 LSM hooks, Windows Sysmon v14\n"
        "  - FastAPI async backend + Cytoscape.js interactive graph canvas"
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(8.8)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.22

    # =========================================================================
    # SLIDE 24: 6. System Design Principles: Datasets & Dual-Tier Database Architecture (Slide 2/2)
    # =========================================================================
    slide24 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide24, "6. System Design Principles: Datasets & Database Architecture", "Phase II: System Architecture & Workflow (Part 2/2)")

    add_card(slide24, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "3. Benchmark Dataset: DARPA Transparent Computing (TC)", BG_LIGHT)
    tb1 = slide24.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Gold Standard for APT Provenance Analytics:\n"
        "  The project exclusively utilizes the DARPA Transparent Computing (TC) Engagement 3 (E3) dataset, the authoritative benchmark for evaluating whole-system provenance-based intrusion detection.\n\n"
        "• Subsets Evaluated (Real Multi-Stage Red-Team Attacks):\n"
        "  - E3-CADETS (FreeBSD / OpenBSM): 1.62M nodes, 3.30M edges\n"
        "    Nginx memory corruption exploit, dropper installation, and Drakon in-memory injection into sshd.\n"
        "  - E3-THEIA (Linux Ubuntu / LSM): 1.62M nodes, 2.87M edges\n"
        "    Browser drive-by exploits, root privilege escalation, credential theft, and sensitive file exfiltration.\n"
        "  - E3-TRACE (Linux CamFlow & Auditd): 3.28M nodes, 4.08M edges\n"
        "    Continuous 2-week recording featuring a stealthy Firefox backdoor, cron persistence, and SSH lateral movement.\n\n"
        "• Why Exclusively DARPA TC? Ground-Truth Enterprise Provenance:\n"
        "  Contains authentic multi-stage cyber attacks executed by nation-state caliber red teams interleaved with dense benign background activity. It provides full kernel-level causal visibility under a unified Common Data Model (CDM)."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide24, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "4. Dual-Tier Database Architecture", BG_LIGHT)
    tb2 = slide24.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Neo4j Enterprise 5.x (Graph Provenance Store):\n"
        "  - Purpose: High-speed DAG indexing and causal traversal engine.\n"
        "  - Node Labels: :Process, :File, :Socket, :Host\n"
        "  - Relationship Types: [:FORK], [:EXEC], [:READ], [:WRITE], [:CONNECT]\n"
        "  - Synthetic Pseudo-Edges: [:PERSISTENCE_PSEUDO_EDGE], [:PORTFWD_CROSS_MACHINE]\n"
        "  - Performance: Native graph pointers deliver sub-second multi-hop causal reachability queries.\n\n"
        "• PostgreSQL 16 (Relational Metadata Store):\n"
        "  - Purpose: Structured persistence of host assets, detection seeds, and federated updates.\n"
        "  - Key Tables: hosts (inventory), anomalies (AI seeds), attack_graphs (scenario DAGs), federated_updates (edge parameter weights)\n"
        "  - ACID Compliance: Guarantees transactional consistency for compliance audits and SOC forensics."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 25: 7. Workflow Diagram (Page 27 in PDF)
    # =========================================================================
    slide25 = prs.slides.add_slide(blank_layout)
    img25 = render_pdf_page(26) # 0-indexed 26 = page 27 (Workflow Diagram)
    slide25.shapes.add_picture(img25, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 26: 8. Proposed Methods: Edge-TGNN & Masked-GAT (Slide 1/2)
    # =========================================================================
    slide26 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide26, "8. Proposed Methods: Edge-TGNN & Masked-GAT Autoencoder", "Phase III: Multi-Model Detection Pipeline (Part 1/2)")

    add_card(slide26, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Lightweight Edge-TGNN with Adversarial Defense", BG_LIGHT)
    tb1 = slide26.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Spatial GNN (3-Layer GraphSAGE):\n"
        "  Mean aggregation pooling local causal neighborhoods:\n"
        "  h_v^(l) = ReLU(W_self h_v^(l-1) + W_neigh (1/|N(v)|) ∑ h_u^(l-1))\n"
        "  Hidden dimension d_h = 32 maintains ultra-low memory footprint.\n\n"
        "• Temporal Recurrence (Gated Recurrent Unit):\n"
        "  Captures sequential transitions across rolling graph snapshots:\n"
        "  h_(i,t)^temp = GRU(h_Gt, h_(i,t-1)^temp) with hidden size d_gru = 64.\n\n"
        "• 3-Step Continuous PGD Adversarial Hardening:\n"
        "  Perturbation ascent maximizing classification loss:\n"
        "  δ* = argmax_(||δ||≤Ω) ℓ(f_θ(G+δ), y) with k_mod ≤ 3, ε = 0.05.\n\n"
        "• On-Device Federated Learning (FedAvg):\n"
        "  Transmits only 79.63 KB parameter deltas Δθ_i to central SOC; raw kernel logs never leave endpoint devices."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide26, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Self-Supervised Masked-GAT Autoencoder", BG_LIGHT)
    tb2 = slide26.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• 50% Stochastic Attribute Masking:\n"
        "  Randomly corrupts node features while preserving structural causality, forcing the encoder to learn intrinsic contextual patterns.\n\n"
        "• Multi-Layer Attention Message Passing:\n"
        "  Computes edge-type aware attention coefficients α_nu^(l) and concatenates layer representations: H_n = h_n^(1) || h_n^(2) || h_n^(3).\n\n"
        "• Tri-Task Self-Supervised Decoder:\n"
        "  - Task 1: Multi-view re-masking with Scaled Cosine Error (SCE, γ = 2.0)\n"
        "  - Task 2: Latent target feature representation matching\n"
        "  - Task 3: Edge existence structural link prediction via BCE loss\n\n"
        "• K-d Tree Spatial Outlier Scoring:\n"
        "  Evaluates distance ratio (D_test / D_train_neighbors) > θ across 10 nearest normal neighbors to flag stealthy zero-day attack seeds."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 27: 8. Proposed Methods: Cross-Machine Tracing & Threat Scoring (Slide 2/2)
    # =========================================================================
    slide27 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide27, "8. Proposed Methods: Cross-Machine Tracing & Threat Scoring", "Phase III: Multi-Model Detection Pipeline (Part 2/2)")

    add_card(slide27, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "3. Session-Partitioned Cross-Machine Tracing Engine", BG_LIGHT)
    tb1 = slide27.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Logon-Session Boundary Isolation:\n"
        "  Partitions execution by Logon Session IDs to conquer dependency explosion; confines graph reachability to causal process lifecycles.\n\n"
        "• Cyber Persistence Pseudo-Edges:\n"
        "  Connects malicious registry Run keys and Scheduled Tasks to their subsequent spawned processes across system reboots.\n\n"
        "• Session Hijacking & Token Theft Resolution:\n"
        "  Detects privilege elevation by mapping Windows Security Events 4624/4768 and lsass token duplication into explicit causal edges.\n\n"
        "• Reverse Proxy Port Forwarding Linking:\n"
        "  Correlates inbound listening sockets with outbound target connections, revealing multi-hop lateral pivots across jump hosts."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide27, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "4. Quantitative ATT&CK Threat Scoring & Prioritization", MINT_LIGHT)
    tb2 = slide27.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Total Threat Scoring Formulation:\n"
        "  TS_total = ∑ [TS_edge(e) · (1 + DA_entity) · Crit_target]\n"
        "  - TS_edge: Edge severity weight based on operational criticality\n"
        "  - DA_entity: Domain Administrator and privileged account boost factor\n"
        "  - Crit_target: High-value asset criticality multiplier (e.g. Domain Controller, ICS PLC)\n\n"
        "• MITRE ATT&CK Matrix Mapping:\n"
        "  Maps reconstructed provenance subgraphs across the full kill-chain (TA0001 Initial Access through TA0010 Exfiltration/Impact).\n\n"
        "• Rank-1 Attack Prioritization:\n"
        "  Surfaces true multi-host red-team intrusion scenarios at Rank 1 (0 FP / 0 FN), eliminating analyst alert fatigue."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 28A: 9. Model Responsibilities: Model 1 — Edge-TGNN (Perimeter Sentry)
    # =========================================================================
    slide28a = prs.slides.add_slide(blank_layout)
    add_standard_header(slide28a, "9. Model Responsibilities: Model 1 — Edge-TGNN (Perimeter Sentry)", "Phase III: Multi-Model Detection Pipeline (Slide 1/5)")

    add_card(slide28a, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Edge Architecture & Real-Time Specifications", BG_LIGHT)
    tb1 = slide28a.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Primary Operational Role:\n"
        "  First line of perimeter defense deployed on local edge nodes, IoT gateways, and endpoint agents for millisecond-level screening.\n\n"
        "• Input Telemetry Stream:\n"
        "  Dynamic rolling temporal graph snapshots {G_(t-9), ..., G_t} with slice duration ΔT = 1.0s and historical window w = 10 (10s observation).\n\n"
        "• Spatial GNN Feature Extraction:\n"
        "  3-Layer GraphSAGE encoder with mean aggregation (hidden dimension d_h = 32) pooling local causal neighborhoods.\n\n"
        "• Temporal Sequence Modeling:\n"
        "  Single-layer Gated Recurrent Unit (GRU, hidden dimension d_gru = 64) with global mean pooling readout.\n\n"
        "• Edge Operational Constraints:\n"
        "  Ultra-compact 79.63 KB parameter footprint, runs in <1 MB RAM, and executes inference in just 3.2 ms per snapshot."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide28a, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Adversarial Hardening & Federated Defense", MINT_LIGHT)
    tb2 = slide28a.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• 3-Step Continuous PGD Adversarial Training:\n"
        "  Hardened against structural evasion via client-side Projected Gradient Descent:\n"
        "  δ* = argmax_(||δ||≤Ω) ℓ(f_θ(G + δ), y) with k_mod ≤ 3 and ε = 0.05.\n\n"
        "• Privacy-Preserving Federated Aggregation:\n"
        "  Trained collaboratively across edge endpoints using Federated Averaging (FedAvg) over TenSEAL CKKS Homomorphic Encryption.\n\n"
        "• Zero Telemetry Leakage:\n"
        "  Endpoints transmit only encrypted 79.63 KB weight deltas Δθ_i to central SOC; sensitive raw OS logs never leave local host memory.\n\n"
        "• Edge Detection Criterion:\n"
        "  Outputs local maliciousness probability s_(i,t) ∈ [0, 1]. Whenever s_(i,t) ≥ τ_edge, an immediate isolation alarm is triggered and the compacted subgraph is forwarded to the SOC."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 28B: 9. Model Responsibilities: Model 2 — Masked-GAT (SOC Deep Analyzer)
    # =========================================================================
    slide28b = prs.slides.add_slide(blank_layout)
    add_standard_header(slide28b, "9. Model Responsibilities: Model 2 — Masked-GAT (SOC Deep Analyzer)", "Phase III: Multi-Model Detection Pipeline (Slide 2/5)")

    add_card(slide28b, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Neural Architecture & Self-Supervised Tri-Task Decoder", BG_LIGHT)
    tb1 = slide28b.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Primary Operational Role:\n"
        "  Centralized enterprise analyzer running on GPU clusters to pinpoint stealthy zero-day process execution anomalies without labeled training data.\n\n"
        "• Multi-Scale Graph Attention Encoder:\n"
        "  Stacked multi-layer GAT with edge-type aware attention coefficients α_nu^(l) and layer concatenation:\n"
        "  H_n = h_n^(1) || h_n^(2) || h_n^(3)\n\n"
        "• 50% Stochastic Attribute Masking:\n"
        "  Randomly masks 50% of node features while preserving structural causality, forcing the model to learn deep contextual execution patterns.\n\n"
        "• Tri-Task Self-Supervised Decoder:\n"
        "  - Task 1: Multi-view re-masking with Scaled Cosine Error (SCE, γ = 2.0)\n"
        "  - Task 2: Latent target feature representation matching\n"
        "  - Task 3: Edge existence structural link prediction via BCE loss."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide28b, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Unsupervised Zero-Day Detection & Spatial Outlier Criteria", MINT_LIGHT)
    tb2 = slide28b.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• 100% Benign Baseline Training:\n"
        "  Trained strictly on the earliest 70% chronological benign audit logs, mapping normal system behavior without requiring labeled attack samples.\n\n"
        "• K-d Tree Benign Neighborhood Memory:\n"
        "  Builds a high-dimensional spatial K-d tree indexing normal node representations (k = 10 nearest normal neighbors).\n\n"
        "• Anomaly Decision Criterion:\n"
        "  Evaluates relative spatial outlier distance ratio:\n"
        "  Score(v) = (D_test / D_train_neighbors) > θ\n\n"
        "• Threshold Calibration:\n"
        "  Threshold θ = 1.5 is calibrated on the middle 10% validation split at the 99.9th percentile, ensuring a strict false positive rate FPR ≤ 0.1%.\n\n"
        "• Seed Isolation Output:\n"
        "  Flags process nodes exceeding θ as anomalous attack seeds M, forwarded to the Tracing Engine."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 28C: 9. Model Responsibilities: Model 3 — Causal Tracing Engine
    # =========================================================================
    slide28c = prs.slides.add_slide(blank_layout)
    add_standard_header(slide28c, "9. Model Responsibilities: Model 3 — Causal Tracing Engine", "Phase III: Multi-Model Detection Pipeline (Slide 3/5)")

    add_card(slide28c, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Dependency Explosion Mitigation & Synthetic Pseudo-Edges", BG_LIGHT)
    tb1 = slide28c.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Primary Operational Role:\n"
        "  Connects disconnected attack steps across execution boundaries, machines, and network domains to reconstruct the complete multi-stage APT attack scenario.\n\n"
        "• Logon-Session Boundary Isolation:\n"
        "  Partitions audit graphs by Logon Session IDs (L_id); confines causal traversal strictly to process lifecycles, fully eliminating dependency explosion.\n\n"
        "• Anti-Evasion Synthetic Pseudo-Edge Insertion:\n"
        "  - Cyber Persistence: Connects startup registry Run keys and Scheduled Tasks to subsequent execution sessions across reboots.\n"
        "  - Session Hijacking: Connects SYSTEM token duplication (Event 4624/4768) to new unauthorized logon sessions.\n"
        "  - Port Forwarding: Remaps local proxy loopback sockets to remote target endpoints, exposing multi-hop lateral pivots across jump hosts."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide28c, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Multi-Host Attack Reconstruction & ATT&CK Attribution", MINT_LIGHT)
    tb2 = slide28c.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Bidirectional Causal Traversal:\n"
        "  Executes backward causality (tracking initial entry point and exploit) and forward causality (tracking data exfiltration and destruction) from seeds M.\n\n"
        "• Cross-Domain IT-to-OT Correlation:\n"
        "  Correlates enterprise Windows/Linux jump hosts with industrial protocols (Modbus, IEC 60870-5-104, Siemens SIPROTEC, Hitachi RTU500).\n\n"
        "• Quantitative ATT&CK Threat Scoring:\n"
        "  TS_total = ∑ [TS_edge(e) · (1 + DA_entity) · Crit_host]\n"
        "  Weights edges by operational severity, Domain Admin rights, and asset criticality.\n\n"
        "• Rank-1 SOC Output:\n"
        "  Surfaces true multi-host red-team intrusion scenarios at Rank 1 (0 False Positives / 0 False Negatives) on Cytoscape.js interactive canvas."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 29A: 10. Inference Flow: Phase 1 — Real-Time Edge Screening (Slide 4/5)
    # =========================================================================
    slide29a = prs.slides.add_slide(blank_layout)
    add_standard_header(slide29a, "10. Inference Flow: Phase 1 — Real-Time Edge Screening & Zero-Day Isolation", "Phase III: Multi-Model Detection Pipeline (Slide 4/5)")

    add_card(slide29a, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "Step 1: Continuous Ingestion & Loop Compaction", BG_LIGHT)
    tb1 = slide29a.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• OS Kernel Telemetry Ingestion:\n"
        "  Low-overhead audit hooks (Linux auditd, CamFlow, Windows Sysmon) capture high-fidelity process, file, and socket operations.\n\n"
        "• Semantics-Preserving Event Compaction:\n"
        "  Repetitive I/O loops (consecutive read, write, recvfrom calls) are collapsed into weighted edges w(e) ← w(e) + 1.\n\n"
        "• Compaction Performance:\n"
        "  - Over 85% data volume reduction across DARPA TC benchmarks\n"
        "  - Zero causality loss: 100% of causal attack chains are preserved.\n\n"
        "• Dynamic Snapshot Construction:\n"
        "  Slices continuous event streams into rolling temporal snapshots G_(i,t) with ΔT = 1.0s and historical observation window w = 10."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide29a, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "Step 2: Sub-4ms Edge Screening & Masked-GAT Isolation", MINT_LIGHT)
    tb2 = slide29a.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Real-Time Edge-TGNN Evaluation:\n"
        "  On-device 3-layer GraphSAGE + GRU evaluates each snapshot in 3.2 ms. If anomaly score s_(i,t) ≥ τ_edge, an immediate perimeter alert is raised.\n\n"
        "• Compacted Telemetry Streaming:\n"
        "  Flagged subgraphs are uploaded to the centralized SOC cluster; non-anomalous background traffic is discarded, saving >95% network bandwidth.\n\n"
        "• Centralized Masked Reconstruction:\n"
        "  SOC Masked-GAT autoencoder reconstructs masked node features across the uploaded candidate graph.\n\n"
        "• Spatial K-d Tree Outlier Scoring:\n"
        "  Evaluates relative distance ratio (D_test / D_train_neighbors) > θ against normal baseline memory, isolating malicious process seeds M."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 29B: 10. Inference Flow: Phase 2 — Whole-Network Tracing & Attribution (Slide 5/5)
    # =========================================================================
    slide29b = prs.slides.add_slide(blank_layout)
    add_standard_header(slide29b, "10. Inference Flow: Phase 2 — Whole-Network Tracing & Attack Scenario Attribution", "Phase III: Multi-Model Detection Pipeline (Slide 5/5)")

    add_card(slide29b, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "Step 3: Session-Partitioned Bidirectional Traversal", BG_LIGHT)
    tb1 = slide29b.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Backward Causality Tracing (Root Cause Analysis):\n"
        "  Originates from anomaly seeds M and traverses backward along incoming edges to discover initial compromise vectors (e.g., Nginx web exploit, phishing attachment).\n\n"
        "• Forward Causality Tracing (Blast Radius Analysis):\n"
        "  Traverses forward along outgoing edges to discover child processes, stolen credential files, modified registry keys, and exfiltration sockets.\n\n"
        "• Logon-Session Boundary Confinement:\n"
        "  Traversal is restricted strictly within active Logon Session IDs (L_id), terminating at session boundaries to prevent branch explosion.\n\n"
        "• Multi-Host Traversal:\n"
        "  Crosses network socket boundaries to correlate adjacent hosts in the enterprise network."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide29b, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "Step 4: Synthetic Pseudo-Edge Stitching & Final ATT&CK Output", MINT_LIGHT)
    tb2 = slide29b.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Multi-Stage Pseudo-Edge Stitching:\n"
        "  Inserts synthetic edges bridging persistence mechanisms across reboots, SYSTEM token theft across logoffs, and reverse proxy port hops across jump hosts.\n\n"
        "• IT-to-OT Industrial Correlation:\n"
        "  Traces attacker actions through engineering workstations into industrial field devices (Siemens SIPROTEC, Hitachi RTU500).\n\n"
        "• Quantitative ATT&CK Threat Scoring:\n"
        "  Computes TS_total by multiplying edge severities with Domain Admin and host criticality multipliers, categorizing stages by MITRE ATT&CK tactics.\n\n"
        "• Rank-1 Incident Presentation:\n"
        "  Surfaces the true APT attack DAG at Rank 1 (0 FP / 0 FN) on Cytoscape.js interactive SOC canvas for instant forensic triage."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = NAVY
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 30: 11. Dataset Preparation: Acquisition & CDM Schema (Slide 1/2)
    # =========================================================================
    slide30 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide30, "11. Dataset Preparation: Acquisition & CDM Schema", "Phase IV: Data Engineering & Model Training (Part 1/2)")

    add_card(slide30, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Dataset Acquisition (DARPA TC Program)", BG_LIGHT)
    tb1 = slide30.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• DARPA Transparent Computing (TC) Program:\n"
        "  Designed specifically to diagnose enterprise-scale APT attacks by capturing high-fidelity, whole-system audit provenance streams.\n\n"
        "• Realistic Multi-Host Attack Engagements:\n"
        "  Blends high-volume benign enterprise workload (web browsing, document editing, compilation, background daemons) with sophisticated nation-state red-team campaigns.\n\n"
        "• Multi-OS Platform Telemetry:\n"
        "  Encompasses heterogeneous operating systems including FreeBSD (CADETS), Linux (THEIA, TRACE), and Windows hosts across multi-week continuous evaluation cycles."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.2)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.3

    add_card(slide30, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Common Data Model (CDM) Schema & Subsets", BG_LIGHT)
    tb2 = slide30.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Standardized CDM Schema (v18/v20 Entities):\n"
        "  - Subject: Process entities with PID, PPID, cmdLine, UID, credentials\n"
        "  - FileObject: Files with path, size, permissions, and cryptographic hash\n"
        "  - NetFlow: Sockets with local/remote IP and port numbers\n"
        "  - Event: Causal relationships (EXEC, FORK, READ, WRITE, CONNECT) with nanosecond timestamps\n\n"
        "• Investigated Benchmark Subsets:\n"
        "  - CADETS (FreeBSD): 1.62M nodes, 3.30M edges (Nginx exploit & Drakon injection)\n"
        "  - THEIA (Linux): 1.62M nodes, 2.87M edges (Browser dropper & exfiltration)\n"
        "  - TRACE (Linux Auditd): 3.28M nodes, 4.08M edges (Continuous 2-week cycle, SSH pivot)"
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.2)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.3

    # =========================================================================
    # SLIDE 31: 11. Dataset Preparation: Preprocessing & Feature Extraction (Slide 2/2)
    # =========================================================================
    slide31 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide31, "11. Dataset Preparation: Preprocessing & Feature Extraction", "Phase IV: Data Engineering & Model Training (Part 2/2)")

    add_card(slide31, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Semantics-Preserving Event Compaction", BG_LIGHT)
    tb1 = slide31.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Repetitive Loop Elimination:\n"
        "  High-frequency benign operations (e.g., repeated file cache reads, continuous socket polling loops) generate millions of redundant events.\n\n"
        "• Execution State Equivalence Rule:\n"
        "  If two consecutive events e_1 = (s, r, o, t_1) and e_2 = (s, r, o, t_2) exhibit identical subject, object, and system state:\n"
        "  Merge e_2 into e_1 and increment edge weight: w(e) ← w(e) + 1.\n\n"
        "• Quantitative Impact:\n"
        "  - Volume Reduction: Over 85% graph reduction across all DARPA TC benchmarks\n"
        "  - Causality Guarantee: 100% causal preservation (0% attack path loss)\n"
        "  - Memory Efficiency: Enables full-graph in-memory training on standard GPUs."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.2)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.3

    add_card(slide31, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Decoupled Feature Representation", BG_LIGHT)
    tb2 = slide31.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Compact 6D One-Hot Tensor Vectors:\n"
        "  Each graph node v is mapped to a normalized 6-dimensional one-hot vector X_v encoding entity type (Process, File, Socket, Controller) and basic privilege state.\n\n"
        "• Offloading Heavy String Metadata:\n"
        "  Variable-length string attributes (file system paths, command-line arguments, SHA-256 hashes) are detached from the tensor graph and indexed in an external key-value lookup store.\n\n"
        "• Computational Advantages:\n"
        "  - Keeps message-passing tensors ultra-compact and cache-aligned\n"
        "  - Eliminates slow NLP/tokenization overhead in the real-time detection path\n"
        "  - Enables Edge-TGNN to operate within strict 1 MB embedded memory limits."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.2)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.3

    # =========================================================================
    # SLIDE 32: 12. Model Training & Evaluation: Chronological Data Splitting Strategy (Slide 1/2)
    # =========================================================================
    slide32 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide32, "12. Model Training & Evaluation: Chronological Data Splitting", "Phase IV: Data Engineering & Model Training (Part 1/2)")

    add_card(slide32, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Temporal Splitting Protocol (Zero Data Leakage)", BG_LIGHT)
    tb1 = slide32.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Strict Temporal Order Preservation:\n"
        "  Standard randomized k-fold cross-validation causes fatal future-to-past data leakage in temporal graph streams. Telemetry is partitioned strictly along the historical time axis.\n\n"
        "• Realistic Operational Simulation:\n"
        "  Ensures that detection models are evaluated only on future events that occurred after the training window, accurately mimicking enterprise SOC deployment.\n\n"
        "• Label Imbalance Reflection:\n"
        "  Preserves real-world enterprise class distribution where attacks constitute <0.001% of all system events."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.2)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.3

    add_card(slide32, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Dataset Split Allocations & Roles", BG_LIGHT)
    tb2 = slide32.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Training Split (Earliest 70% of Timeline):\n"
        "  - Content: 100% benign baseline enterprise activity (zero attacks present)\n"
        "  - Purpose: Trains self-supervised Masked-GAT autoencoder and builds K-d tree normal baseline neighborhood memory.\n\n"
        "• Validation Split (Middle 10% of Timeline):\n"
        "  - Content: Benign operational logs\n"
        "  - Purpose: Calibrates anomaly decision threshold θ = 1.5, strictly ensuring false positive rate FPR ≤ 0.1%.\n\n"
        "• Testing Split (Latest 20% of Timeline):\n"
        "  - Content: Unseen operational timeline containing actual red-team APT attacks (Nginx exploit, Drakon injection, browser droppers, SSH lateral hops) mixed with background noise."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.2)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.3

    # =========================================================================
    # SLIDE 33: 12. Model Training & Evaluation: Training Algorithms & Evaluation (Slide 2/2)
    # =========================================================================
    slide33 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide33, "12. Model Training & Evaluation: Training Algorithms & Metrics", "Phase IV: Data Engineering & Model Training (Part 2/2)")

    add_card(slide33, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Optimization Algorithms & Loss Formulations", BG_LIGHT)
    tb1 = slide33.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = (
        "• Adversarial Training Loss (Edge-TGNN):\n"
        "  L_adv(θ) = BCE(f_θ(G), y) + 0.8 · BCE(f_θ(G + δ*), y)\n"
        "  - δ* generated via 3-step continuous PGD ascent with ε = 0.05 and k_mod ≤ 3.\n"
        "  - Optimizer: Adam (lr = 0.001, weight decay = 1e-4) over 100 epochs.\n\n"
        "• Tri-Task Self-Supervised Loss (Masked-GAT):\n"
        "  L_total = L_input + L_latent + 0.5 L_struct\n"
        "  - L_input: Scaled Cosine Error (SCE) with scaling factor γ = 2.0:\n"
        "    SCE(x, x̂) = (1 - (x · x̂) / (||x|| ||x̂||))^γ\n"
        "  - L_latent: MSE between encoder representation and target projector\n"
        "  - L_struct: Binary Cross-Entropy edge link prediction loss."
    )
    p1.font.name = "Arial"
    p1.font.size = Pt(9.0)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.25

    add_card(slide33, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Quantitative Evaluation Metrics", BG_LIGHT)
    tb2 = slide33.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Anomaly Detection Performance:\n"
        "  - Precision, Recall, F1-Score, and False Positive Rate (target FPR ≤ 0.1%)\n"
        "  - Area Under the ROC Curve (AUROC) and Area Under Precision-Recall (AUPRC).\n\n"
        "• Edge Operational Efficiency:\n"
        "  - Parameter Footprint: Model size in storage/RAM (79.63 KB)\n"
        "  - Inference Latency: Per-snapshot classification speed (3.2 ms).\n\n"
        "• Scenario Attribution & Reconstruction:\n"
        "  - Provenance Scenario Accuracy: Recall of ground-truth attack nodes\n"
        "  - Ranking Precision: Top-1 ranking of the true red-team intrusion scenario via TS_total (0 False Positives / 0 False Negatives)."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 34: 13. System Architecture Diagram (Page 45 in PDF)
    # =========================================================================
    slide34 = prs.slides.add_slide(blank_layout)
    img34 = render_pdf_page(44) # 0-indexed 44 = page 45 (System Architecture Diagram)
    slide34.shapes.add_picture(img34, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 35: 14. Development & Testing Flowchart (Page 46 in PDF)
    # =========================================================================
    slide35 = prs.slides.add_slide(blank_layout)
    img35 = render_pdf_page(45) # 0-indexed 45 = page 46 (Testing Flowchart)
    slide35.shapes.add_picture(img35, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 36: 15. Database Schema: Neo4j Graph Database & Relational Store (Page 36)
    # =========================================================================
    slide36 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide36, "15. Database Schema: Neo4j Graph Database & Relational Store", "Phase V: Deep Schemas & Core Algorithms")

    add_card(slide36, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Neo4j Graph Database Property Schema", BG_LIGHT)
    tb1 = slide36.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "Node Labels & Key Properties:\n• :Process: {uuid, pid, name, path, cmdline, uid, session_id, host}\n• :File: {uuid, path, name, file_type, size_bytes, permissions, hash}\n• :Socket: {uuid, src_ip, src_port, dst_ip, dst_port, protocol}\n• :Controller: {uuid, model, ip, protocol, firmware, trip_curve}\n\nDirected Relationship Types:\n• [:FORK | :EXEC]: (Process) → (Process/File) {timestamp}\n• [:READ | :WRITE]: (Process) → (File) {timestamp, count}\n• [:CONNECT]: (Process) → (Socket) {timestamp, state}\n• [:PERSISTENCE_PSEUDO_EDGE]: (SetupSession) → (ExecSession)\n• [:PORTFWD_CROSS_MACHINE]: (ProxySrc) → (TargetDst)"
    p1.font.name = "Arial"
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.3

    add_card(slide36, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Relational Metadata Store (PostgreSQL)", BG_LIGHT)
    tb2 = slide36.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = "Relational Tables & Schema Definition:\n\n• hosts (Endpoint Inventory):\n  host_id (PK), hostname, os_platform, domain_name, ip_addr, is_dc, last_seen\n\n• anomalies (AI-Flagged Seed Events):\n  anomaly_id (PK), host_id (FK), session_id, score, detector_source, timestamp\n\n• attack_graphs (Reconstructed Scenarios):\n  graph_id (PK), seed_uuid, threat_score, tactics_list, node_count, edge_count, graph_json\n\n• federated_updates (Edge-TGNN Training):\n  round_id (PK), client_id, loss_clean, loss_adv, param_norm, timestamp"
    p2.font.name = "Arial"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.3

    # =========================================================================
    # SLIDE 37: 16. Algorithms & Pseudocode: Master Detection Pipeline (Page 49 in PDF)
    # =========================================================================
    slide37 = prs.slides.add_slide(blank_layout)
    img37 = render_pdf_page(48) # 0-indexed 48 = page 49
    slide37.shapes.add_picture(img37, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 38: 16. Algorithms & Pseudocode: Algorithm 1 — Edge-TGNN Training (Page 50 in PDF)
    # =========================================================================
    slide38 = prs.slides.add_slide(blank_layout)
    img38 = render_pdf_page(49) # 0-indexed 49 = page 50
    slide38.shapes.add_picture(img38, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 39: 16. Algorithms & Pseudocode: Algorithm 2 — Masked-GAT Detection (Page 51 in PDF)
    # =========================================================================
    slide39 = prs.slides.add_slide(blank_layout)
    img39 = render_pdf_page(50) # 0-indexed 50 = page 51
    slide39.shapes.add_picture(img39, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 40: 16. Algorithms & Pseudocode: Algorithm 3 — Whole-Network Tracing (Page 52 in PDF)
    # =========================================================================
    slide40 = prs.slides.add_slide(blank_layout)
    img40 = render_pdf_page(51) # 0-indexed 51 = page 52
    slide40.shapes.add_picture(img40, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 41: 17. Implementation & Technology Stack (Page 52)
    # =========================================================================
    slide41 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide41, "17. Implementation & Technology Stack: Modules & Integrations", "Phase VI: Implementation, Project Plan & Conclusion")

    add_card(slide41, Inches(0.8), Inches(1.35), Inches(5.7), Inches(5.45), "1. Core Modules & Architecture Components", BG_LIGHT)
    tb1 = slide41.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "• Kernel Ingestion & Parsing Engine:\n  Low-overhead audit probe hooks (Linux auditd, CamFlow LSM hooks, Windows Sysmon v14). Ingests raw audit logs and converts to CDM JSON/Avro records.\n\n• Semantics-Preserving Event Compactor:\n  High-throughput Rust/Python microservice evaluating execution state equivalence and collapsing repetitive I/O loops (reduces raw volume >85%).\n\n• Dual-Tier AI Detection Server:\n  PyTorch Geometric microservice running lightweight Edge-TGNN (79.63 KB) on edge gateways and centralized self-supervised Masked-GAT on GPU cluster.\n\n• Whole-Network Causal Tracing Engine:\n  Logon-session partitioned DFS/BFS crawler inserting pseudo-edges to bridge persistence, token hijacking, and reverse proxy tunnels."
    p1.font.name = "Arial"
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = TEXT_DARK
    p1.line_spacing = 1.3

    add_card(slide41, Inches(6.8), Inches(1.35), Inches(5.7), Inches(5.45), "2. Technology Stack, Libraries & Frameworks", BG_LIGHT)
    tb2 = slide41.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = (
        "• Deep Learning & Graph Frameworks:\n"
        "  Python 3.10+, PyTorch v2.2.0, PyTorch Geometric (PyG v2.5.0), DGL v1.1, SciPy v1.12 (K-d Tree spatial index), NumPy, Scikit-Learn.\n\n"
        "• Privacy-Preserving Federated Cryptography:\n"
        "  TenSEAL CKKS Homomorphic Encryption for encrypted parameter updates without gradient or raw telemetry leakage.\n\n"
        "• Dual-Tier Database & Graph Storage Engines:\n"
        "  Neo4j Enterprise 5.x with Cypher interface & APOC for high-speed DAG traversal; PostgreSQL 16 for metadata & inventory.\n\n"
        "• Telemetry Sensors & Forensic Dashboard:\n"
        "  FastAvro v1.9, Linux Auditd, CamFlow v0.5 LSM hooks, Windows Sysmon v14; FastAPI REST backend + Cytoscape.js SOC canvas."
    )
    p2.font.name = "Arial"
    p2.font.size = Pt(8.8)
    p2.font.color.rgb = TEXT_DARK
    p2.line_spacing = 1.25

    # =========================================================================
    # SLIDE 42: 18. Project Work Plan & Gantt Roadmap (Page 55 in PDF)
    # =========================================================================
    slide42 = prs.slides.add_slide(blank_layout)
    img42 = render_pdf_page(54) # 0-indexed 54 = page 55
    slide42.shapes.add_picture(img42, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))

    # =========================================================================
    # SLIDE 43: 19. References (Page 56 in PDF)
    # =========================================================================
    slide43 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide43, "19. References: Primary Research Foundations", "Phase VI: References & Literature Foundation")
    
    add_card(slide43, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.45), "Key Literature Citations [1] - [8]", WHITE)
    tb_ref1 = slide43.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(11.233), Inches(4.6))
    tf_ref1 = tb_ref1.text_frame
    tf_ref1.word_wrap = True
    refs_1 = [
        ("[1]", "Osei Isaac, Benjamin Appiah, Daniel Commey, Kwabena Owusu-Agyemang, Michael Asante, and Benjamin Hayfrom Acquah, 'EdgeFence: Federated Temporal Graph Neural Networks for Lightweight, Adversarial Malware Detection in Distributed Edge Networks,' International Journal of Information Security, vol. 25, p. 88, 2026. DOI: 10.1007/s10207-026-01237-x"),
        ("[2]", "Mengjiao Cui, Zhengwei Jiang, Shuai Li, Chunyan Ma, Kai Zhang, Peian Yang, and Huamin Feng, 'MGDA: A provenance graph-based framework for threat detection and attack scenario reconstruction,' Computer Networks, vol. 274, p. 111806, 2026. DOI: 10.1016/j.comnet.2025.111806"),
        ("[3]", "Qi Liu, Kaibin Bao, and Veit Hagenmeyer, 'Commander: A robust cross-machine multi-phase Advanced Persistent Threat detector via provenance analytics,' Journal of Information Security and Applications, vol. 91, p. 104057, 2025. DOI: 10.1016/j.jisa.2025.104057"),
        ("[4]", "Roberto Canonico, Francesco Lista, Annalisa Navarro, Giancarlo Sperlí, and Andrea Vignali, 'Threat detection in reconfigurable Cyber–Physical Systems through Spatio-Temporal Anomaly Detection using graph attention network,' Computers & Security, vol. 156, p. 104509, 2025. DOI: 10.1016/j.cose.2025.104509"),
        ("[5]", "Parth Atulbhai Gandhi, Prasanna N. Wudali, Yonatan Amaru, Akansha Shukla, Yuval Elovici, and Asaf Shabtai, 'SHIELD: Advanced persistent threats detection and intelligent explanation using large language models,' Engineering Applications of Artificial Intelligence, vol. 181, p. 115443, 2026."),
        ("[6]", "Francesco Ferazza, Cosimo Melella, Konstantinos Mersinas, Ricardo Lugo, and Rain Ottis, 'From logs to tactics: unsupervised reconstruction of APT campaigns with MITRE-enriched meta-alerts,' International Journal of Information Security, vol. 25, p. 79, 2026."),
        ("[7]", "Gisung Kim, Seungmin Lee, and Sehun Kim, 'A novel hybrid intrusion detection method integrating anomaly detection with misuse detection,' Expert Systems with Applications, vol. 41, no. 4, pp. 1690–1700, 2014."),
        ("[8]", "Haiyang Diao, Xiang Li, Wan Zhang, Yan Sibyl Yu, Ye Wang, and Jing Zhang, 'Self-supervised graph neural networks for network intrusion detection in cloud-edge,' Journal of Cloud Computing, vol. 15, no. 1, p. 24, 2026.")
    ]
    for i, (num, cit) in enumerate(refs_1):
        p = tf_ref1.paragraphs[0] if i == 0 else tf_ref1.add_paragraph()
        p.text = f"{num}  {cit}"
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 44: 19. References Contd. (Page 57 in PDF)
    # =========================================================================
    slide44 = prs.slides.add_slide(blank_layout)
    add_standard_header(slide44, "19. References: Additional Literature Sources", "Phase VI: References & Literature Foundation")
    
    add_card(slide44, Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.45), "Additional Literature Citations [9] - [16]", WHITE)
    tb_ref2 = slide44.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(11.233), Inches(4.6))
    tf_ref2 = tb_ref2.text_frame
    tf_ref2.word_wrap = True
    refs_2 = [
        ("[9]", "Eslam Amer, Shaker El-Sappagh, Tamer Abuhamad, Bander Ali Saleh Al-Rimy, and Alaa Mohasseb, 'GraphShield: Advanced dynamic graph-based malware detection using graph neural networks,' Expert Systems with Applications, vol. 268, p. 129812, 2025."),
        ("[10]", "Fargana Abdullayeva and Suleyman Suleymanzade, 'Cyber security attack recognition on cloud computing networks based on GCN and GraphSAGE models,' Results in Control and Optimization, vol. 16, p. 100423, 2024."),
        ("[11]", "Rana Abu Bakar, Lorenzo De Marinis, Filippo Cugini, and Francesco Paolucci, 'FTG-Net-E: A hierarchical ensemble graph neural network for DDoS attack detection,' Computer Networks, vol. 248, p. 110508, 2024."),
        ("[12]", "Md Shakil Siddique, Md. Ashikur Rahman Khan, Ishtiaq Ahammad, Nishu Nath, Joysri Rani Das, and Fardowsi Rahman, 'Intelligent intrusion detection for cyber-physical systems using GAN-LSTM,' Franklin Open, vol. 11, p. 100281, 2025."),
        ("[13]", "Ali Yilmaz, Resul Das, Mehmet Ozdem, and Berk Canberk, 'Knowledge graph visualization and anomaly detection using graph neural networks,' Computer Networks, vol. 278, p. 112632, 2026."),
        ("[14]", "Giancarlo Iannizzotto, Andrea Nucita, and Andrea Siragusa, 'Robust, efficient detection of network intrusion attacks: A large language model approach,' Computer Networks, vol. 276, p. 112559, 2026."),
        ("[15]", "Abdullah Al Mamun, Harith Al-Sahaf, Ian Welch, and Masood Mansoori, 'Detection of advanced persistent threat: A genetic programming approach,' Applied Soft Computing, vol. 167, p. 112447, 2024."),
        ("[16]", "Mohammed Alshehri, 'Dynamic cyber deception using AI-driven adaptive honeypot networks,' Ain Shams Engineering Journal, vol. 17, no. 3, p. 104061, 2026.")
    ]
    for i, (num, cit) in enumerate(refs_2):
        p = tf_ref2.paragraphs[0] if i == 0 else tf_ref2.add_paragraph()
        p.text = f"{num}  {cit}"
        p.font.name = "Arial"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 45: Closing Slide (Page 58 in PDF)
    # =========================================================================
    slide45 = prs.slides.add_slide(blank_layout)
    bg45 = slide45.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg45.fill.solid()
    bg45.fill.fore_color.rgb = NAVY
    bg45.line.color.rgb = NAVY

    if os.path.exists(logo_path):
        slide45.shapes.add_picture(logo_path, Inches(5.966), Inches(0.8), height=Inches(1.3))

    tbox45 = slide45.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(11.333), Inches(1.8))
    tf45 = tbox45.text_frame
    tf45.word_wrap = True
    p1 = tf45.paragraphs[0]
    p1.text = "Thank You"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(8)

    p2 = tf45.add_paragraph()
    p2.text = "Questions & Discussion"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.color.rgb = GOLD

    card45 = slide45.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(4.3), Inches(8.933), Inches(2.5))
    card45.fill.solid()
    card45.fill.fore_color.rgb = RGBColor(22, 48, 85)
    card45.line.color.rgb = GOLD
    card45.line.width = Pt(1.2)

    cbox45 = slide45.shapes.add_textbox(Inches(2.5), Inches(4.45), Inches(8.333), Inches(2.2))
    ctf45 = cbox45.text_frame
    ctf45.word_wrap = True
    cp1 = ctf45.paragraphs[0]
    cp1.text = "Muhammed Nasih K P (KNP23CS074)   •   Sumayya Ershad (KNP23CS107)\nNajmunniza N (LKNP20CS056)   •   K.S. Mahadev (KNP23CS066)"
    cp1.alignment = PP_ALIGN.CENTER
    cp1.font.name = "Arial"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = WHITE
    cp1.space_after = Pt(8)

    cp2 = ctf45.add_paragraph()
    cp2.text = "Department of Computer Science & Engineering\nCollege of Engineering, Karunagappally"
    cp2.alignment = PP_ALIGN.CENTER
    cp2.font.name = "Arial"
    cp2.font.size = Pt(10.5)
    cp2.font.color.rgb = MINT
    cp2.space_after = Pt(8)

    cp3 = ctf45.add_paragraph()
    cp3.text = "Guide: Mrs. SYAMA S R, Assistant Professor"
    cp3.alignment = PP_ALIGN.CENTER
    cp3.font.name = "Arial"
    cp3.font.size = Pt(10)
    cp3.font.color.rgb = GOLD

    output_pptx = "Cyber_Threat_Detection_Presentation.pptx"
    prs.save(output_pptx)
    print(f"PowerPoint Presentation successfully created: {output_pptx} with {len(prs.slides)} slides.")

if __name__ == "__main__":
    build_presentation()
