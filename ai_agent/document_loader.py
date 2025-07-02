# ai_agent/document_loader.py

import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_into_chunks(text, max_tokens=300):
    sentences = text.split('.')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) < max_tokens:
            current_chunk += sentence + '.'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '.'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def load_all_pdfs(folder_path="data/party_docs/"):
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            chunks = split_into_chunks(text)
            all_chunks.extend(chunks)
    return all_chunks

