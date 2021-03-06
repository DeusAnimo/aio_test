from sqlalchemy import Column, Integer, create_engine, String, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

DB_URI = 'sqlite:///refdb.db'

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)

Base = declarative_base()


class Medias(Base):
    __tablename__ = 'medias'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, nullable=False)
    tag = Column(String(50), default='my_image')
    image_id = Column(String, default=lambda: str(uuid.uuid4()))
    red = Column(Float)


if __name__ == "__main__":
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
