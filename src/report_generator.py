from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def __init__(self, paper_title="Untitled Paper", paper_author="Unknown Author", analysis_date=None):
        super().__init__()
        self.paper_title = paper_title
        self.paper_author = paper_author
        self.analysis_date = analysis_date if analysis_date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font("Roboto", "", "Roboto-Regular.ttf")
        self.add_font("Roboto", "B", "Roboto-Bold.ttf")
        self.add_font("Roboto", "I", "Roboto-Italic.ttf")

    def header(self):
        if self.page_no() > 1: # Don't show header on the title page
            self.set_font('Roboto', 'B', 10)
            self.set_text_color(50, 50, 50) # Dark gray
            self.cell(0, 10, 'Academic Paper Review Report', 0, 0, 'L')
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')
            self.ln(10)
            self.set_draw_color(200, 200, 200) # Light gray line
            self.line(10, 20, 200, 20) # Draw a line under the header

    def footer(self):
        self.set_y(-15)
        self.set_font('Roboto', 'I', 8)
        self.set_text_color(128, 128, 128) # Gray
        self.cell(0, 10, f'Generated on {self.analysis_date}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Roboto', 'B', 16)
        self.set_fill_color(230, 230, 250) # Light purple background for titles
        self.set_text_color(0, 0, 0) # Black text
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Roboto', '', 11)
        self.set_text_color(0, 0, 0) # Black text
        self.multi_cell(0, 6, body)
        self.ln(5)

    def add_section(self, title, content):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(content)

def create_report(report_data, output_path):
    # Retrieve metadata, providing empty string as default if key is missing
    paper_title = report_data.get('metadata', {}).get('title', '')
    paper_author = report_data.get('metadata', {}).get('author', '')
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ensure title and author are never empty strings for FPDF
    # This handles cases where metadata exists but is empty or whitespace-only
    if not paper_title.strip():
        paper_title = "N/A"
    if not paper_author.strip():
        paper_author = "N/A"

    pdf = PDFReport(paper_title, paper_author, analysis_date)
    pdf.add_page()

    # Title Page
    pdf.set_font('Roboto', 'B', 24)
    pdf.set_y(80)
    pdf.cell(0, 15, 'Academic Paper Review Report', 0, 1, 'C')
    pdf.ln(20)

    pdf.set_font('Roboto', '', 14)
    pdf.cell(0, 10, f'Paper Title: {paper_title}', 0, 1, 'C')
    pdf.cell(0, 10, f'Author: {paper_author}', 0, 1, 'C')
    pdf.ln(10)

    pdf.set_font('Roboto', 'I', 10)
    pdf.cell(0, 10, f'Analysis Date: {analysis_date}', 0, 1, 'C')
    pdf.ln(30)

    # Summary Section
    summary_content = "This report provides an automated analysis of the academic paper for common review checkpoints. Below is a summary of key findings, followed by detailed sections."
    
    # Retrieve all necessary data from report_data with default empty lists/values
    missing_sections = report_data.get('missing_sections', [])
    unresolved_citations = report_data.get('unresolved_citations', [])
    missing_citation_sentences = report_data.get('missing_citation_sentences', [])
    unused_references = report_data.get('unused_references', [])
    average_reference_age = report_data.get('average_reference_age', "N/A")
    old_references_percentage = report_data.get('old_references_percentage', "0.0%")

    if missing_sections:
        summary_content += f"\n\nCritical: Missing sections detected: {', '.join(missing_sections)}."
    if unresolved_citations:
        summary_content += f"\nCritical: Unresolved citations found: {len(unresolved_citations)}."
    if missing_citation_sentences:
        summary_content += f"\nSuggestion: {len(missing_citation_sentences)} sentences may be missing citations."
    if unused_references:
        summary_content += f"\nSuggestion: {len(unused_references)} unused references found."
    if average_reference_age != "N/A":
        summary_content += f"\nSuggestion: Average reference age is {average_reference_age}. {old_references_percentage} of references are older than 10 years."

    pdf.add_section("1. Report Summary", summary_content)

    # Detailed Analysis Sections

    # Structural Analysis
    structural_content = ""
    if missing_sections:
        structural_content += "The following standard sections were identified as missing or not clearly defined:\n"
        for section in missing_sections:
            structural_content += f"- {section}\n"
    else:
        structural_content += "All standard academic sections (Abstract, Introduction, Methods, Results, Discussion, References) appear to be present.\n"
    pdf.add_section("2. Structural Analysis", structural_content)

    # Citation Analysis
    citation_content = ""
    if report_data.get('citation_count') is not None:
        citation_content += f"Total potential in-text citations (PDF analysis): {report_data['citation_count']}\n\n"

    if unresolved_citations:
        citation_content += "Unresolved Citations (cited in text but not found in bibliography):\n"
        for citation in unresolved_citations:
            citation_content += f"- {citation}\n"
        citation_content += "\n"
    else:
        citation_content += "All in-text citations seem to have corresponding entries in the bibliography.\n\n"

    if unused_references:
        citation_content += "Unused References (in bibliography but not cited in text):\n"
        for reference in unused_references:
            citation_content += f"- {reference}\n"
        citation_content += "\n"
    else:
        citation_content += "All bibliography entries seem to be cited in the text.\n\n"
    pdf.add_section("3. Citation Analysis", citation_content)

    # Missing Citation Check
    missing_citation_check_content = ""
    if missing_citation_sentences:
        missing_citation_check_content += "The following sentences contain strong claims or statements that may require a citation:\n"
        for i, sentence in enumerate(missing_citation_sentences):
            missing_citation_check_content += f"{i+1}. \"{sentence}\"\n"
    else:
        missing_citation_check_content += "No sentences with potential missing citations were identified based on common heuristics.\n"
    pdf.add_section("4. Missing Citation Check", missing_citation_check_content)

    # Reference Age Analysis
    reference_age_content = ""
    if average_reference_age != "N/A":
        reference_age_content += f"Average age of references: {average_reference_age}\n"
        reference_age_content += f"Percentage of references older than 10 years: {old_references_percentage}\n"
        reference_age_content += f"Number of references older than 10 years: {report_data.get('old_references_count', 0)}\n\n"
        reference_age_content += "Consider reviewing older references for more recent and relevant literature.\n"
    else:
        reference_age_content += "Reference age analysis not available (e.g., no references found or could not be parsed).\n"
    pdf.add_section("5. Reference Age Analysis", reference_age_content)

    pdf.output(output_path, 'F')