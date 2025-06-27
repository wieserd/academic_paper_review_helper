# Academic Paper Review Helper

The Academic Paper Review Helper is a Python-based command-line interface (CLI) tool designed to assist academic reviewers and authors in checking their papers for common issues before submission or review. It supports both PDF and LaTeX (`.tex`) files, extracting key information and performing various analyses to highlight potential problems.

## Features

*   **Modular Architecture:** The codebase is refactored into a modular structure (`src` folder with dedicated modules for shared utilities, PDF analysis, LaTeX analysis, and report generation) for improved maintainability and extensibility.
*   **Multi-format Support:** Analyzes both PDF documents and LaTeX source files (including recursively included `.tex` files).
*   **Metadata Extraction:** Extracts title, author, and other available metadata from papers. Gracefully handles missing metadata by displaying "N/A" in the report.
*   **Structural Analysis:** Identifies standard academic sections (Abstract, Introduction, Methods, Results, Discussion, References) and flags missing ones.
*   **Citation Analysis (LaTeX):** Checks for consistency between in-text citations (`\cite{}`) and bibliography entries (`\bibitem{}`), reporting unresolved citations and unused references.
*   **Missing Citation Check:** Scans the text for common phrases that imply a claim or statement requiring a citation (e.g., "studies show," "it is known") and flags sentences where a citation appears to be missing.
*   **Reference Age and Relevance Analysis:** Analyzes the publication years of references (from `\bibitem` in LaTeX or extracted from text in PDFs) to report on average reference age and the percentage of older references.
*   **Enhanced PDF Report Generation:** Generates a beautifully formatted PDF report with a professional design, including a dedicated title page (with paper name, author, and analysis date), consistent headers/footers, and clear presentation of all analysis findings categorized into "Critical Issues" and "Suggestions."
*   **Interactive Mode:** Provides a menu-driven interface after analysis to view detailed results in the terminal.

## Installation

1.  **Navigate to the project directory:**
    ```bash
    cd /Users/dw2022/academic_paper_review_helper
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Fonts (Crucial for PDF Report Design):**
    For the PDF report to render correctly with the intended design, you need to download the Roboto font family. Go to [https://fonts.google.com/specimen/Roboto](https://fonts.google.com/specimen/Roboto), click "Download family," extract the `.zip` file, and copy the following `.ttf` files into the `academic_paper_review_helper/src/` directory:
    *   `Roboto-Regular.ttf`
    *   `Roboto-Bold.ttf`
    *   `Roboto-Italic.ttf`

## Usage

To run the Academic Paper Review Helper, execute the `main.py` script. The program will then guide you through the process interactively.

```bash
python main.py
```

You will be prompted to:

1.  **Enter the full path to your PDF or LaTeX file:** Provide the absolute path to the paper you wish to analyze. If your LaTeX paper consists of multiple `.tex` files, provide the path to the main `.tex` file that includes others (e.g., `main.tex`).
2.  **Enter the desired name for the output PDF report:** Specify the filename for the generated PDF report (e.g., `review_report.pdf`).

After the analysis is complete and the PDF report is generated, an interactive menu will appear in the terminal, allowing you to view specific details of the analysis.

### Example Walkthrough

```
Welcome to the Academic Paper Review Helper!
Please enter the full path to your PDF or LaTeX file: /Users/dw2022/Desktop/my_paper.pdf
Please enter the desired name for the output PDF report (e.g., report.pdf): my_paper_review.pdf
--- Analysis Complete! ---
Report will be saved to my_paper_review.pdf
Report saved to my_paper_review.pdf

--- Choose an option to view details ---
1. View Metadata
2. View Sections Analysis
3. View Citation Analysis
4. View Missing Citation Check
5. View Reference Age Analysis
6. Exit
Enter your choice (1-6): 2

--- Sections Found ---
- Abstract
- Introduction
- Methods
- Results
- Discussion
- References

--- Missing Sections ---
All standard sections appear to be present.

--- Choose an option to view details ---
1. View Metadata
2. View Sections Analysis
3. View Citation Analysis
4. View Missing Citation Check
5. View Reference Age Analysis
6. Exit
Enter your choice (1-6): 6
Exiting. Goodbye!
```

## Future Enhancements

*   **Readability Scores:** Calculate Flesch-Kincaid or similar scores to assess text complexity.
*   **Advanced PDF Citation Parsing:** Improve the accuracy of in-text citation and reference list extraction from PDFs.
*   Support for additional citation styles (e.g., APA, MLA, IEEE) for PDF analysis.
*   Advanced formatting checks (e.g., font sizes, line spacing).
*   Integration with external APIs for grammar and style checks.

## License

This project is open-source and available under the [MIT License](LICENSE).
