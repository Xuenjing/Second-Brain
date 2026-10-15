from imports.pdf_parser import extract_pdf_chunks
from imports.pdf_importer import import_pdf_to_database

file_path = "experiments/test_document_2.pdf"

chunks = extract_pdf_chunks(file_path)

for index, chunk in enumerate(chunks, start=1):
    print(f"\nCHUNK {index}:")
    print(chunk)

added_count = import_pdf_to_database(file_path)

print(f"Added {added_count} chunks")