import sys
import os
from pdf_text_check import evaluate_pdf

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_one_pdf.py /path/to/file.pdf")
        sys.exit(1)
    path = sys.argv[1]
    if not path.lower().endswith(".pdf") or not os.path.isfile(path):
        print("Error: Not a valid PDF file.")
        sys.exit(1)
    evaluate_pdf(path)

if __name__ == "__main__":
    main()

