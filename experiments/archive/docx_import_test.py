'''
run from project root:
python -m experiments.docx_import_test
'''

from imports.document_parser import extract_docx_chunks
from retrieval import create_embedding
from database import add_knowledge

'''
Testing 4 cases:
1. Valid file, happy path
2. Non-existent file
3. Wrong file type
4. Broken docx file
'''

# 1 happy path
try:
    file_path = "experiments/test_document.docx"
    text = extract_docx_chunks(file_path)
    for chunk in text:
        embedding = create_embedding(chunk)
        added = add_knowledge(chunk, embedding, source="test_document.docx")
        print(f"added: {added}")
        print(f"embedding length: {len(embedding)}")
        print(f"{chunk}\n")

except Exception as error:
    print(f"ERROR: {error}")

# 2 does not exist
try:
    file_path = "experiments/test_document2.docx"
    text = extract_docx_chunks(file_path)
    print(text)
except Exception as error:
    print(f"ERROR: {error}")

# 3 Wrong type
try:
    file_path = "experiments/test_document3.txt"
    text = extract_docx_chunks(file_path)
    print(text)
except Exception as error:
    print(f"ERROR {error}")

# 4 Broken docx
try:
    file_path = "experiments/test_document4.docx"
    text = extract_docx_chunks(file_path)
    print(text)
except Exception as error:
    print(f"ERROR: {error}")