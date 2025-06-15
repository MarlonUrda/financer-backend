from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

# Ejemplo de URL para PostgreSQL:
# postgresql://usuario:contraseña@host:puerto/nombre_basedatos
# Por ejemplo:
# postgresql://postgres:mi_contraseña@localhost:5432/mi_basedatos

database_url = os.getenv("DB_URL")

engine = create_engine(database_url, echo=False)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()