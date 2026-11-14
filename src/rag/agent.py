from src.guardrails.input_guardrails import check_input
import json
import ollama
from src.rag.rag_chain import generate_answer


# Tool 1: Search the document
def search_document(question):

    answer = generate_answer(question)

    return answer


# Tool 2: Summarize the document
def summarize_document():

    # Load document chunks
    with open("data/processed/chunks.json", "r", encoding="utf-8") as file:

        chunks = json.load(file)

    # Combine document text
    context = ""

    for chunk in chunks:
        context += chunk["text"] + "\n"

    # Limit text sent to the model
    context = context[:12000]

    prompt = f"""
    Summarize the following document.

    Include:
    1. Main topic
    2. Important points
    3. Key conclusions

    Document:
    {context}
    """

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# Agent: Decide which tool to use
def run_agent(question):

    # Step 1: Validate user input
    allowed, message = check_input(question)

    if not allowed:
        return message

    question_lower = question.lower()

    # Step 2: Select the appropriate tool
    if "summarize" in question_lower or "summary" in question_lower:

        print("Agent selected: Summarize tool")

        return summarize_document()

    else:

        print("Agent selected: Search tool")

        return search_document(question)



if __name__ == "__main__":

    question = input("Ask your document: ")

    answer = run_agent(question)

    print("\nAgent Answer:")
    print(answer)
