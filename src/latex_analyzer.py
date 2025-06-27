import re
import os
from datetime import datetime
from .shared_utils import check_for_missing_citations, check_structure

def _get_full_tex_content(file_path, base_dir, visited_files=None):
    """
    Recursively reads content from a LaTeX file and its included files.
    Avoids infinite loops by tracking visited files.
    """
    if visited_files is None:
        visited_files = set()

    # Resolve the absolute path to handle relative includes correctly
    abs_file_path = os.path.abspath(file_path)

    if abs_file_path in visited_files:
        return ""
    visited_files.add(abs_file_path)

    full_content = ""
    try:
        with open(abs_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        full_content += content

        # Find included files (e.g., \input{file}, \include{file})
        # This regex is simplified and might need refinement for more complex cases
        included_files = re.findall(r'\\(?:input|include)\{(.*?)\}', content)
        
        current_dir = os.path.dirname(abs_file_path)

        for included_file in included_files:
            # Handle cases where .tex extension is omitted
            if not included_file.endswith('.tex'):
                included_file += '.tex'
            
            # Construct the path relative to the current file's directory
            included_path = os.path.join(current_dir, included_file)
            
            if os.path.exists(included_path):
                full_content += _get_full_tex_content(included_path, current_dir, visited_files)
            else:
                print(f"Warning: Included file not found: {included_path}")

    except FileNotFoundError:
        print(f"Error: LaTeX file not found: {abs_file_path}")
    except Exception as e:
        print(f"Error reading LaTeX file {abs_file_path}: {e}")

    return full_content

def analyze_tex_file(tex_path):
    """
    Analyzes a LaTeX file (and its included files) and returns a dictionary of findings.
    """
    report_data = {}
    
    # Get the full content by recursively reading included files
    full_content = _get_full_tex_content(tex_path, os.path.dirname(tex_path))

    title = re.search(r'\\title\{(.*?)\}', full_content)
    author = re.search(r'\\author\{(.*?)\}', full_content)
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', full_content, re.DOTALL)
    sections = re.findall(r'\\section\{(.*?)\}', full_content)

    report_data['metadata'] = {
        'title': title.group(1) if title else "Not Found",
        'author': author.group(1) if author else "Not Found"
    }
    
    found_sections_and_abstract = sections
    if abstract:
        found_sections_and_abstract.append("abstract")
        
    report_data['found_sections'] = found_sections_and_abstract
    report_data['missing_sections'] = check_structure(found_sections_and_abstract)

    in_text_citations = set(re.findall(r'\\cite\{(.*?)\}', full_content))
    bib_items = set(re.findall(r'\\bibitem\{(.*?)\}', full_content))

    report_data['unresolved_citations'] = list(in_text_citations - bib_items)
    report_data['unused_references'] = list(bib_items - in_text_citations)

    report_data['missing_citation_sentences'] = check_for_missing_citations(full_content)

    # --- Reference Age Analysis ---
    current_year = datetime.now().year
    reference_years = []
    for item in re.finditer(r'\\bibitem\{.*?\}(.*?)(?:\\par|$)', full_content, re.DOTALL):
        bibitem_content = item.group(1)
        year_match = re.search(r'(?:19|20)\d{2}', bibitem_content)
        if year_match:
            year = int(year_match.group(0))
            reference_years.append(year)

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
