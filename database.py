from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "mysql://root:iare@localhost:3306/fastapi"
engine=create_engine(db_url)

Session = sessionmaker(bind=engine,autocommit=False,autoflush=False)
