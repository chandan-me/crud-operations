"""
database.py
-----------
Handles the database connection and session management for the application.

Key Responsibilities:
1. Load environment variables from .env file (database credentials).
2. Create the SQLAlchemy database engine connected to MySQL.
3. Configure the SessionLocal class for issuing queries.
4. Provide the declarative Base class for ORM models.
5. Provide the get_db() dependency function used by FastAPI endpoints.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Load environment variables from the .env file in the current directory or parent directory
load_dotenv()

# 2. Retrieve DATABASE_URL from environment variables.
# Format: mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>
DATABASE_URL = os.getenv("DATABASE_URL")

# 3.create_engine = The connection manager between Python and MySQL.( or db pineline)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # prints generated SQL statements to the terminal
    pool_pre_ping=True,  # Automatically check if connection is alive before using it
)

# 4. Createing SessionLocal factory
# Each instance of SessionLocal = represents an individual database conversation/transaction.
SessionLocal = sessionmaker(
    autocommit=False, # autocommit=False, ensures transactions are explicitly committed using db.commit().
    autoflush=False, # autoflush=False, prevents automatic flushing of changes before queries unless requested.
    bind=engine
)

# 5. Base class for declarative ORM models
Base = declarative_base() #  foundation blueprint for creating database tables using Python classes.

# 6. Database Dependency for FastAPI endpoints
"""
FastAPI dependency that yields a database session for a single HTTP request.

How this works:
1. A request comes from React.
2. FastAPI calls get_db().
3. A database session is created.
4. yield db provides the session to the API endpoint.
5. The endpoint performs its database operation.
6. After the request finishes, db.close() executes.

This prevents database sessions from remaining open unnecessarily.
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
