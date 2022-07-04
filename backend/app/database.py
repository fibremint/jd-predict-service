from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jd.util import get_path_from_service_root

engine = create_engine(
    'sqlite:///' + get_path_from_service_root('DATABASE_PATH'),
    connect_args={'check_same_thread': False}
)

SessoinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessoinLocal()
    try:
        yield db
    finally:
        db.close()
