from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
import chromadb
from .config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(autoflush=False,
                 autocommit=False,
                 bind=engine)
)

Base: DeclarativeMeta = declarative_base()
Base.query = db_session.query_property()

chroma_client = chromadb.Client()
fore_collection = chroma_client.create_collection(name="fore_collection")

def init_db():
    Base.metadata.create_all(bind=engine)
