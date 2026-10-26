from retrieval import retrieve_knowledge
from llm.local_provider import LocalLLMProvider

"""
Run this test from the project root with:

python -m tests.rag_test
"""

'''
Test of an isolated RAG pipeline.

The query is used to retrieve relevant knowledge from the database.
The retrieved text is joined into a context and passed to the local LLM,
which generates an answer based only on that context.
'''

# wrap the llm in a class container
llm = LocalLLMProvider("Qwen/Qwen3-4B-Instruct-2507")

query = "When does school open?"

# control question: should return that the question can not be answered
# query = "What is the school's phone number?"

# retrieve the results from database
results = retrieve_knowledge(query)

# provide context by joining the results
context = "\n".join(result["text"] for result in results)

# construct a prompt consisting of context and query to the llm
prompt = f"""
Use only the information in the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

# generate the answer
answer = llm.generate(prompt) 

# print the answer, what was retrieved and the context
print(answer)

print("Retrieved:")
for result in results:
    print(result)

print("\nContext:")
print(context)