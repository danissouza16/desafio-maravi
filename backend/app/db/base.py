from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from app.core.config import settings

engine = create_engine(str(settings.DATABASE_URL), echo=True)

def create_db_and_tables():
    from app.db.models import Alerta
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@contextmanager
def get_session_context():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        print("Erro na sessão do banco de dados.")
        raise
    finally:
        session.close()
