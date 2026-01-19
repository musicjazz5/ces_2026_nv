#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "ces_charts"
# Path to user provided resources
RESOURCE_DIR = Path("/home/grant/macair_download/nv/to_spark")
IMG_FLOW = RESOURCE_DIR / "nvflow.png"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Font settings
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class CESReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.font_family = "Arial"

    def header(self):
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"NVIDIA CES 2026 & Benchmark Report", 0, 1, "L")
        self.line(10, 18, 200, 18)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family, "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def section_title(self, title):
        self.set_font(self.font_family, "B", 14)
        self.set_text_color(0, 102, 204) # Nvidia Green/Blue
        self.set_fill_color(240, 248, 255)
        self.cell(0, 10, title, 0, 1, "L", fill=True)
        self.ln(3)

    def add_box(self, title, content, color="blue"):
        if color == "blue":
            self.set_fill_color(235, 245, 255)
        elif color == "green":
            self.set_fill_color(235, 255, 235)
        elif color == "red":
            self.set_fill_color(255, 235, 235)
            
        self.set_font(self.font_family, "B", 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title, 1, 1, "L", fill=True)
        
        self.set_font(self.font_family, "", 10)
        self.multi_cell(0, 6, content, 1, "L", fill=True)
        self.ln(5)

def create_bar_chart(title, generations, values, ylabel, filename, color_hex="#76b900"):
    plt.figure(figsize=(8, 5))
    bars = plt.bar(generations, values, color=color_hex, width=0.6)
    plt.title(title, fontsize=12, fontweight='bold')
    plt.ylabel(ylabel, fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',
                 ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    path = str(CHART_DIR / filename)
    plt.savefig(path, dpi=150)
    plt.close()
    return path

def generate_report():
    print("Generating Combined CES & Benchmark Report...")

    # --- Data Definition (From PDF Extraction) ---
    # HBM Memory Bandwidth (TB/s)
    gens_bw = ['Blackwell (B200)', 'Rubin (R100)']
    bw_vals = [8.0, 22.0] # Source: 2.8x improvement
    
    # AI Inference Performance (PFLOPS - NVFP4)
    gens_perf = ['Blackwell', 'Rubin']
    perf_vals = [10.0, 50.0] # Source: 5x Blackwell
    
    # NVLink Bandwidth (TB/s)
    gens_link = ['Blackwell', 'Rubin']
    link_vals = [1.8, 3.6] # Source: 2x Blackwell

    # --- Create Charts ---
    chart_bw = create_bar_chart("HBM Memory Bandwidth (TB/s)", gens_bw, bw_vals, "Bandwidth (TB/s)", "ces_bw.png", "#76b900")
    chart_perf = create_bar_chart("AI Inference Performance (NVFP4 PFLOPS)", gens_perf, perf_vals, "PFLOPS", "ces_perf.png", "#4e9a06")
    chart_link = create_bar_chart("NVLink Bandwidth per GPU (TB/s)", gens_link, link_vals, "Bandwidth (TB/s)", "ces_link.png", "#204a87")

    # --- Create PDF ---
    pdf = CESReportPDF()
    
    # Page 1: Cover & Executive Summary
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.ln(10)
    pdf.cell(0, 15, "NVIDIA CES 2026 Impact Report", 0, 1, "C")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Benchmarks & Strategic Analysis", 0, 1, "C")
    pdf.ln(10)

    summary = (
        "CES 2026 marked a pivotal shift for NVIDIA, moving beyond 'Just LLMs' to 'Physical AI' and 'Agentic AI'. "
        "With the introduction of the Vera Rubin platform, NVIDIA has quintupled AI performance (50 PFLOPS) and "
        "nearly tripled memory bandwidth (22 TB/s) to solve the 'Memory Wall' for next-gen reasoning models."
    )
    pdf.add_box("Executive Summary", summary, "green")
    
    # Page 2: Vera Rubin Platform Specs
    pdf.add_page()
    pdf.section_title("1. The Vera Rubin Platform (Technical Specs)")
    
    # Page 2: Vera Rubin Platform Detailed Specs
    pdf.add_page()
    pdf.section_title("1. Vera Rubin Platform: The Quantifiable Leap")
    
    # Vera CPU Specs
    cpu_specs = (
        "- Cores: 88 Custom Olympus Cores (176 Threads)\n"
        "- Memory: 1.5 TB LPDDR5X System Memory\n"
        "- Improvement: 3X Memory Capacity vs. Grace CPU\n"
        "- Transistors: 227 Billion"
    )
    pdf.add_box("NVIDIA Vera CPU", cpu_specs, "blue")

    # Rubin GPU Specs
    gpu_specs = (
        "- NVFP4 Inference: 50 PFLOPS (5X vs Blackwell)\n"
        "- NVFP4 Training: 35 PFLOPS (3.5X vs Blackwell)\n"
        "- HBM4 Bandwidth: 22 TB/s (2.8X vs Blackwell)\n"
        "- NVLink Bandwidth: 3.6 TB/s (2X vs Blackwell)\n"
        "- Transistors: 336 Billion (1.6X vs Blackwell)"
    )
    pdf.add_box("NVIDIA Rubin GPU", gpu_specs, "blue")

    # NVL72 Rack Specs
    rack_specs = (
        "- Total Inference: 3.6 ExaFLOPS (5X improvement)\n"
        "- Total Training: 2.5 ExaFLOPS (3.5X improvement)\n"
        "- Memory Capacity: 54 TB LPDDR5X (3X) + 20.7 TB HBM (1.5X)\n"
        "- Scale-Up Bandwidth: 260 TB/s (2X improvement)"
    )
    pdf.add_box("Vera Rubin NVL72 (Rack Scale)", rack_specs, "green")
    
    # Visual: Inference Performance
    pdf.image(chart_perf, x=20, w=170)
    pdf.ln(5)
    pdf.multi_cell(0, 6, "Rubin delivers a 5x leap in inference performance over Blackwell, specifically optimized for 'Thinking' models (Test-Time Scaling).")

    # Page 3: Economic & Scaling Trends
    pdf.add_page()
    pdf.section_title("2. The Economics of Intelligence")
    
    econ_text = (
        "Key scaling laws driving the industry (Source: EPOCH AI & Artificial Analysis):\n"
        "1. Model Size: Growing 10x Parameters per Year.\n"
        "2. Test-Time Scaling ('Thinking'): Demanding 5x more Tokens per Year.\n"
        "3. Cost Efficiency: Token Cost dropping 10x Cheaper per Year."
    )
    pdf.add_box("Insane Demand for AI Computing", econ_text, "red")

    eco_text = (
        "NVIDIA is empowering an open ecosystem including:\n"
        "- Major Models: DeepSeek, Qwen (Alibaba), Kimi, Llama (Meta), Mistral, Google.\n"
        "- Strategic Focus: 'Physical AI' (Cosmos) and 'AV' (Alpamayo) are the next frontiers."
    )
    pdf.add_box("Open Model Ecosystem", eco_text, "green")

    # Page 4: Detailed Infrastructure Specs
    pdf.add_page()
    pdf.section_title("3. Infrastructure & Networking Revolution")
    
    net_specs = (
        "- ConnectX-9 SuperNIC: 800 Gb/s Ethernet, Programmable RDMA.\n"
        "- BlueField-4 DPU: 800 Gb/s, 6x Compute vs BF3, 64-Core Grace CPU embedded.\n"
        "- NVLink 6 Switch: 3.6 TB/s per-GPU bandwidth, enabling the NVL72 rack to act as one giant GPU.\n"
        "- Spectrum-X: Ethernet Co-Packaged Optics, scaling to 512 ports of 200 Gb/s."
    )
    pdf.add_box("Networking: The Nervous System", net_specs, "blue")

    # Page 5: Industrial & Physical AI
    pdf.add_page()
    pdf.section_title("4. Physical AI & Industrial Digital Twins")
    
    partners_text = (
        "NVIDIA is integrating with the world's leading engineering platforms:\n"
        "- EDA Partners: Cadence (Cerebrus, Virtuoso), Synopsys (AgentEngineer), Siemens.\n"
        "- CAE/Simulation: Ansys, Beta CAE.\n"
        "- Use Cases: Semiconductor DT, Industrial DT, Robotics DT, Automotive DT."
    )
    pdf.add_box("Strategic Partnerships (EDA/CAE)", partners_text, "green")
    
    # Visual: Memory Bandwidth (Keep this as it's critical)
    pdf.image(chart_bw, x=20, w=170)
    pdf.multi_cell(0, 6, "HBM4 (22 TB/s) is the enabler for these 'Physical AI' workloads which require massive real-time data ingestion.")

    # Page 4: Strategic Highlights (CES)
    pdf.add_page()
    pdf.section_title("3. CES 2026 Strategic Highlights")
    
    highlights = (
        "1. Physical AI & Robotics:\n"
        "   - 'Robotics is the next wave of AI'.\n"
        "   - Alpamayo: Open Reasoning VLA for Autonomous Vehicles.\n"
        "   - GR00T: Foundation model for humanoid robots.\n\n"
        "2. Agentic AI & Cosmos:\n"
        "   - Agents are now Multi-Model, Multi-Cloud, and Hybrid.\n"
        "   - 'Compute is Data' -> NVIDIA Cosmos platform.\n\n"
        "3. New Infrastructure:\n"
        "   - ConnectX-9 SuperNIC & Spectrum-X for Ethernet Scale-Out.\n"
        "   - 'Context Memory Storage' platform using BlueField-4."
    )
    pdf.add_box("Key Themes: Physical & Agentic AI", highlights, "green")

    # Page 5: Visual Flow / Architecture (User Provided Image)
    if os.path.exists(IMG_FLOW):
        pdf.add_page()
        pdf.section_title("4. System Architecture & Flow")
        # Scale image to fit
        pdf.image(str(IMG_FLOW), x=10, w=190)
        pdf.ln(5)
        pdf.multi_cell(0, 6, "Fig 1. NVIDIA AI Flow & Ecosystem Visualization (Source: CES 2026)")
    else:
        print(f"Warning: Image not found at {IMG_FLOW}")

    # Output
    out_file = OUTPUT_DIR / f"Benchmark_Report_CES_2026_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(str(out_file))
    print(f"✅ Report generated: {out_file}")

if __name__ == "__main__":
    generate_report()
