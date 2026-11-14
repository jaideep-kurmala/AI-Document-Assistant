import json
import time

from src.rag.vector_store import search_vectors
from src.rag.rag_chain import generate_answer


# Step 1: Load evaluation questions
with open("evaluation/questions.json", "r", encoding="utf-8") as file:

    test_data = json.load(file)


# Store evaluation results
results = []


# Step 2: Test each question
for item in test_data:

    question = item["question"]
    expected_keywords = item["expected_keywords"]

    print("\nQuestion:", question)

    # Measure response time
    start_time = time.time()

    # Retrieve relevant chunks
    retrieved_chunks = search_vectors(question, top_k=3)

    # Combine retrieved text
    context = " ".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    # Generate AI answer
    answer = generate_answer(question)

    end_time = time.time()

    response_time = round(end_time - start_time, 2)

    # Step 3: Check retrieval relevance
    retrieval_hits = sum(
        1 for word in expected_keywords
        if word.lower() in context.lower()
    )

    retrieval_score = (
        retrieval_hits / len(expected_keywords) * 100
        if expected_keywords else 0
    )

    # Step 4: Check answer keyword coverage
    answer_hits = sum(
        1 for word in expected_keywords
        if word.lower() in answer.lower()
    )

    answer_score = (
        answer_hits / len(expected_keywords) * 100
        if expected_keywords else 0
    )

    # Step 5: Store results
    results.append({
        "question": question,
        "retrieval_score": round(retrieval_score, 2),
        "answer_score": round(answer_score, 2),
        "response_time": response_time
    })

    print("AI Answer:", answer)
    print("Retrieval score:", round(retrieval_score, 2), "%")
    print("Answer keyword score:", round(answer_score, 2), "%")
    print("Response time:", response_time, "seconds")


# Step 6: Calculate average scores
if results:

    average_retrieval = sum(
        item["retrieval_score"] for item in results
    ) / len(results)

    average_answer = sum(
        item["answer_score"] for item in results
    ) / len(results)

    average_time = sum(
        item["response_time"] for item in results
    ) / len(results)

    print("\n========== EVALUATION REPORT ==========")

    print("Total questions:", len(results))

    print("Average retrieval score:",
          round(average_retrieval, 2), "%")

    print("Average answer keyword score:",
          round(average_answer, 2), "%")

    print("Average response time:",
          round(average_time, 2), "seconds")

    # Save results
    with open("evaluation/results.json", "w", encoding="utf-8") as file:

        json.dump(results, file, indent=4)

    print("\nEvaluation results saved successfully!")
