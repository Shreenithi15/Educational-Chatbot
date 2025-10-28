from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services import quiz_generator
from app import crud

router = APIRouter(prefix="/quiz", tags=["quiz"])

class QuizQuestion(BaseModel):
    id: int
    question: str
    choices: List[str]

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

@router.get("/", response_model=QuizResponse)
def get_quiz(topic: str = "general", n: int = 3):
    qs = quiz_generator.generate_quiz(topic, n_qs=n)
    out = []
    for q in qs:
        out.append(QuizQuestion(id=q["id"], question=q["question"], choices=q["choices"]))
    return {"questions": out}

class QuizAnswer(BaseModel):
    session_id: str
    question_id: int
    selected_index: int  # 0-based

class QuizAnswerResult(BaseModel):
    correct: bool
    correct_index: int
    explanation: str

@router.post("/answer", response_model=QuizAnswerResult)
def answer_quiz(ans: QuizAnswer, topic: str = "general"):
    qs = quiz_generator.generate_quiz(topic, n_qs=10)  # ensure includes
    q = next((x for x in qs if x["id"] == ans.question_id), None)
    if not q:
        return {"correct": False, "correct_index": -1, "explanation": "Question not found"}
    correct_index = q["answer"]
    correct = ans.selected_index == correct_index
    explanation = f"The best answer is choice index {correct_index}."
    # optional: store user's quiz attempt as conversation message
    conv = crud.get_or_create_conversation(ans.session_id)
    crud.add_message(conv.id, "user", f"Answered quiz {ans.question_id} -> {ans.selected_index}")
    crud.add_message(conv.id, "bot", f"Quiz feedback: {explanation} (correct={correct})")
    return {"correct": correct, "correct_index": correct_index, "explanation": explanation}
