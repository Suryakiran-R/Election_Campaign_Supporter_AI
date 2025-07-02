import sys
import os

# Add the parent folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from document_loader import load_pdf_content

pdf_path = "data/party_docs/sample_manifesto.pdf"

if __name__ == "__main__":
    content = load_pdf_content(pdf_path)
    print("------ Extracted Text Preview ------")
    print(content[:1000])
    print("\n✅ PDF loaded successfully!")