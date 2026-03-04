import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Use environment variables for database connection
db_host = os.getenv("DB_HOST", "localhost")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "iare")
db_name = os.getenv("DB_NAME", "fastapi")
db_port = os.getenv("DB_PORT", "3306")

db_url = f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
