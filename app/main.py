from fastapi import FastAPI
from app.db import init_db
from app.routers import chat, quiz

def create_app():
    app = FastAPI(title="Learnix Educational Chatbot")
    app.include_router(chat.router)
    app.include_router(quiz.router)
    @app.on_event("startup")
    def on_startup():
        init_db()
    return app

app = create_app()
