from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

def init_db():
    import app.models as models  # ensure models are imported
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
