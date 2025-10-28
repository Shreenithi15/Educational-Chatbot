from typing import List, Dict

def generate_quiz(topic: str, n_qs: int = 3) -> List[Dict]:
    # Simple deterministic quiz generator — replace with real content generation if needed.
    # Each question dict: {id, question, choices, answer}
    base = [
        {"question": f"What is the main idea of {topic}?", "choices": ["A", "B", "C", "D"], "answer": 0},
        {"question": f"Which concept is central to {topic}?", "choices": ["X", "Y", "Z", "W"], "answer": 1},
        {"question": f"How is {topic} applied in practice?", "choices": ["Option1", "Option2", "Option3", "Option4"], "answer": 2},
    ]
    # return first n_qs
    return [{"id": idx+1, **q} for idx, q in enumerate(base[:n_qs])]
