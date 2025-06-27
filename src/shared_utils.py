import re

def check_for_missing_citations(text):
    """
    Scans text for sentences containing common research phrases
    that should be followed by a citation and flags those that are not.
    """
    keywords = [
        "studies show", "research indicates", "it is known",
        "evidence suggests", "experts agree", "it has been demonstrated",
        "the prevailing view is", "is widely accepted", "has been found to"
    ]
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\n)\s', text)
    missing_citation_sentences = []
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            if not (re.search(r'\\cite\{.*?\}', sentence) or
                    re.search(r'\[\d+\]', sentence) or
                    re.search(r'\([\w\s.,;]+,\s*\d{4}\)', sentence) or
                    re.search(r'\[[\w\s.,;]+,\s*\d{4}\]', sentence)):
                missing_citation_sentences.append(sentence.strip())
    return missing_citation_sentences

def check_structure(found_sections):
    """Checks for the presence of standard academic paper sections."""
    standard_sections = [
        "abstract", "introduction", "methods",
        "results", "discussion", "references"
    ]
    found_sections_lower = [str(s).lower() for s in found_sections]
    missing_sections = []
    for standard_section in standard_sections:
        if standard_section not in found_sections_lower:
            missing_sections.append(standard_section.capitalize())
    return missing_sections
