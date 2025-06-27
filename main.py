

import fitz  # PyMuPDF
import re
import os
from src.report_generator import create_report
from datetime import datetime
from src.shared_utils import check_for_missing_citations, check_structure
from src.pdf_analyzer import analyze_pdf_file
from src.latex_analyzer import analyze_tex_file
from fpdf.errors import FPDFException

# --- Display Functions ---

def display_metadata(report_data):
    print("\n--- Metadata ---")
    metadata = report_data.get('metadata', {})
    if metadata:
        for key, value in metadata.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("No metadata found.")

def display_sections(report_data):
    print("\n--- Sections Found ---")
    found_section_names = report_data.get('found_sections', [])
    if found_section_names:
        for section in found_section_names:
            print(f"- {section.capitalize()}")
    else:
        print("No sections found.")

    missing_sections = report_data.get('missing_sections', [])
    if missing_sections:
        print("\n--- Missing Sections ---")
        for section in missing_sections:
            print(f"- {section}")
    else:
        print("All standard sections appear to be present.")

def display_citation_analysis(report_data):
    print("\n--- Citation Analysis ---")
    if report_data.get('citation_count') is not None:
        print(f"Found {report_data['citation_count']} potential in-text citations (PDF analysis).")

    unresolved_citations = report_data.get('unresolved_citations', [])
    if unresolved_citations:
        print("Unresolved Citations (in text but not in bibliography):")
        for citation in unresolved_citations:
            print(f"- {citation}")
    else:
        print("All in-text citations seem to be in the bibliography.")

    unused_references = report_data.get('unused_references', [])
    if unused_references:
        print("\nUnused References (in bibliography but not in text):")
        for reference in unused_references:
            print(f"- {reference}")
    else:
        print("All bibliography entries seem to be cited in the text.")

def display_missing_citation_check(report_data):
    print("\n--- Missing Citation Check ---")
    missing_citations = report_data.get('missing_citation_sentences', [])
    if missing_citations:
        print("Found sentences that may be missing citations:")
        for sentence in missing_citations:
            print(f'- "{sentence}"')
    else:
        print("No sentences with potential missing citations found.")

def display_reference_age_analysis(report_data):
    print("\n--- Reference Age Analysis ---")
    if report_data.get('average_reference_age') != "N/A":
        print(f"Average Reference Age: {report_data['average_reference_age']}")
        print(f"References older than 10 years: {report_data['old_references_count']} ({report_data['old_references_percentage']})")
    else:
        print("Reference age analysis not available or no references found.")

# --- Main ---

def main():
    print("Welcome to the Academic Paper Review Helper!")

    # Get file path from user
    file_path = input("Please enter the full path to your PDF or LaTeX file: ")
    while not os.path.exists(file_path):
        print("File not found. Please try again.")
        file_path = input("Please enter the full path to your PDF or LaTeX file: ")

    # Get output path from user
    output_path = input("Please enter the desired name for the output PDF report (e.g., report.pdf): ")

    _, file_extension = os.path.splitext(file_path)

    report_data = None
    if file_extension.lower() == '.pdf':
        report_data = analyze_pdf_file(file_path)
    elif file_extension.lower() == '.tex':
        report_data = analyze_tex_file(file_path)
    else:
        print(f"Error: Unsupported file type '{file_extension}'. Please provide a .pdf or .tex file.")
        return

    if report_data:
        print("\n--- Analysis Complete! ---")
        print(f"Report will be saved to {output_path}")
        try:
            create_report(report_data, output_path)
            print(f"Report saved to {output_path}")
        except FPDFException as e:
            print(f"Error generating PDF report: {e}")
            print("This might be due to missing or malformed metadata in the PDF. Please try a different PDF or a LaTeX file.")

        while True:
            print("\n--- Choose an option to view details ---")
            print("1. View Metadata")
            print("2. View Sections Analysis")
            print("3. View Citation Analysis")
            print("4. View Missing Citation Check")
            print("5. View Reference Age Analysis")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                display_metadata(report_data)
            elif choice == '2':
                display_sections(report_data)
            elif choice == '3':
                display_citation_analysis(report_data)
            elif choice == '4':
                display_missing_citation_check(report_data)
            elif choice == '5':
                display_reference_age_analysis(report_data)
            elif choice == '6':
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
