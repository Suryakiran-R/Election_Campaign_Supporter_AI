
from ai_agent.responder import generate_response

def generate_ai_response(user_query: str) -> str:
    # Bypass retriever to reduce memory
    prompt = f"User: {user_query}\nAI:"
    return generate_response(prompt)
# # ai_agent/ai_agent.py

# from ai_agent.document_loader import load_all_pdfs
# from ai_agent.retriever import SimpleRetriever
# from ai_agent.responder import query_huggingface

# def generate_ai_response(user_query: str) -> str:
#     try:
#         # Step 1: Load all document chunks
#         chunks = load_all_pdfs()

#         # Step 2: Retrieve relevant chunks for the query
#         retriever = SimpleRetriever(chunks)
#         relevant_chunks = retriever.retrieve(user_query, top_k=3)

#         # Step 3: Build the final prompt
#         context = "\n".join(relevant_chunks)
#         prompt = (
#             f"You are an AI assistant for an election campaign.\n"
#             f"Use the following context to answer the question.\n\n"
#             f"Context:\n{context}\n\n"
#             f"Question:\n{user_query}\n\n"
#             f"Answer:"
#         )

#         # Step 4: Generate response from model
#         return query_huggingface(prompt)

#     except Exception as e:
#         return f"Error while generating response: {str(e)}"
