from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings


# Configurar el motor (engine)
# check_same_thread=False es necesario solo con sqlite3
engine = create_engine(
    settings.DATABASE_URL,
    # connect_args={"check_same_thread": False},
    # future=True,
    # echo=True  # activá esto solo si querés ver las consultas SQL en consola
)

# Crea una fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base de la que heredarán todos los modelos
Base = declarative_base()

# Dependencia para obtener la sesión en cada request (para FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
