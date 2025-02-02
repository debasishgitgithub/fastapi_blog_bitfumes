from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./blog.db', connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)
Base = declarative_base()