import fitz  # PyMuPDF
import re
from datetime import datetime
from .shared_utils import check_for_missing_citations, check_structure

def extract_text_and_metadata_pdf(pdf_path):
    """Extracts text and metadata from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    metadata = doc.metadata
    return text, metadata

def find_sections_pdf(text):
    """Identifies key sections in the academic paper from PDF text."""
    sections = {
        "abstract": None,
        "introduction": None,
        "methods": None,
        "results": None,
        "discussion": None,
        "references": None
    }
    for section in sections.keys():
        match = re.search(r"\n" + section + r"\n", text, re.IGNORECASE)
        if match:
            sections[section] = match.start()
    return sections

def analyze_pdf_file(pdf_path):
    """Analyzes a PDF file and returns a dictionary of findings."""
    report_data = {}
    text, metadata = extract_text_and_metadata_pdf(pdf_path)
    report_data['metadata'] = metadata

    sections_found = find_sections_pdf(text)
    found_section_names = [key for key, value in sections_found.items() if value is not None]
    report_data['found_sections'] = found_section_names
    report_data['missing_sections'] = check_structure(found_section_names)

    citations = re.findall(r'(\[\d+\]|\([\w\s.,;]+,\s*\d{4}\))|\[[\w\s.,;]+,\s*\d{4}\]', text)
    report_data['citation_count'] = len(citations)

    report_data['missing_citation_sentences'] = check_for_missing_citations(text)

    # --- Reference Age Analysis for PDF ---
    current_year = datetime.now().year
    reference_years = []

    # Attempt to find the references section
    references_match = re.search(r'(?:References|Bibliography|LITERATURE CITED)\n(.*?)(?:\n\n|$)', text, re.DOTALL | re.IGNORECASE)
    if references_match:
        references_text = references_match.group(1)
        # Find all 4-digit numbers that look like years
        years_found = re.findall(r'(?:19|20)\d{2}', references_text)
        reference_years = [int(year) for year in years_found]

    if reference_years:
        average_age = current_year - (sum(reference_years) / len(reference_years))
        old_references = [year for year in reference_years if (current_year - year) > 10]
        report_data['average_reference_age'] = f"{average_age:.1f} years"
        report_data['old_references_count'] = len(old_references)
        report_data['old_references_percentage'] = f"{len(old_references) / len(reference_years) * 100:.1f}%"
    else:
        report_data['average_reference_age'] = "N/A"
        report_data['old_references_count'] = 0
        report_data['old_references_percentage'] = "0.0%"

    return report_data
