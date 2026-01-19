---
name: documentation
description: A skill for researching topics and generating comprehensive documentation or reports.
---

# Documentation Skill

This skill is designed to help you generate high-quality documentation and reports. It involves research, outlining, and content generation.

## Process

1.  **Understand the Request**: Identify the topic, the target audience, and the desired format (Markdown, PDF, etc.).
2.  **Research (if needed)**:
    *   Use `search_web` to gather information about the topic.
    *   For recent events (like CES 2026), ensure you get the latest details.
    *   Collect key facts, dates, product announcements, and technical specifications.
3.  **Outline**:
    *   Create a structure for the document.
    *   Typical structure: Title, Executive Summary, Key Highlights, Detailed Analysis, Conclusion/Outlook.
4.  **Drafting**:
    *   Write the content. Use clear, professional language.
    *   Use the templates in `templates/` if applicable.
    *   If the report is about a specific event (like Nvidia CES), focus on the major announcements (e.g., new GPUs, AI chips, partnerships).
5.  **Review and Save**:
    *   Review the content for accuracy and flow.
    *   Save the file to the user's workspace, ideally in a `reports` or `docs` directory, or as specified.

## specialized Instructions for Event Reports (e.g., CES)

1.  **Keynote Summary**: Start with the main keynote (e.g., Jensen Huang).
2.  **Product Launches**: List and describe new hardware/software.
3.  **Strategic Partnerships**: Mention any new collaborations.
4.  **Impact Analysis**: Discuss what these announcements mean for the industry.

## Quantitative Analysis & PDF Generation

To generate professional PDF reports with charts (Bar charts, comparisons):

1.  **Prepare Data**: Identify key metrics to compare (e.g., Performance, Bandwidth, TCO) across generations or competitors.
2.  **Generate Script**: Create a Python script based on `.agent/skills/documentation/scripts/generate_comparison_pdf.py`.
    *   This script acts as a template.
    *   It uses `fpdf` for layout and `matplotlib` for charts.
    *   Customize the `gens` (labels) and `values` lists in the script.
3.  **Execute**: Run the script to produce the PDF in the `outputs/` directory.

### Example: Comparing GPU Generations
If the user asks for a benchmark comparison (e.g., Rubin vs Blackwell):
1.  Verify the specs using `search_web`.
2.  Update the data in the python script.
3.  Run the script to generate a visual report.

## Multi-Source Integration (PDF/Drive)

When integrating external data (e.g., Google Drive PDFs):
1.  **Extract Content**: Use `pdftotext` to read the external files.
    ```bash
    pdftotext input.pdf - | head -n 50
    ```
2.  **Synthesize**: Identify new domains (e.g., Healthcare, Robotics) not covered in the initial report.
3.  **Update Report**: Add dedicated sections to the Markdown report.
4.  **Update Script**: Modify the python generation script to include new pages or metrics corresponding to the new data.


