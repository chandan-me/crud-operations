"""
database.py
-----------
Handles the database connection and session management for the Product Management application.

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
# Default fallback to standard local MySQL configuration if not set in .env
DEFAULT_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/product_management"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# 3. Create the SQLAlchemy Engine
# The engine is the central entry point to the database. It manages database connections,
# translates SQLAlchemy queries into dialect-specific SQL (MySQL in this case), and manages
# a connection pool for efficient reuse of connections.
# echo=True prints generated SQL statements to the terminal (great for beginners learning SQL!)
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True if you want to see raw SQL logs in the terminal
    pool_pre_ping=True,  # Automatically check if connection is alive before using it
    connect_args=connect_args,
)

# 4. Create SessionLocal factory
# Each instance of SessionLocal represents an individual database conversation/transaction.
# autocommit=False ensures transactions are explicitly committed using db.commit().
# autoflush=False prevents automatic flushing of changes before queries unless requested.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 5. Base class for declarative ORM models
# All database models (like Product in models.py) will inherit from this Base class.
# SQLAlchemy uses it to track which tables and columns need to be mapped to Python objects.
Base = declarative_base()


# 6. Database Dependency for FastAPI endpoints
def get_db():
    """
    FastAPI dependency that yields a database session for a single HTTP request.
    
    How this works:
    1. A new SessionLocal() session is instantiated when an HTTP request arrives.
    2. 'yield db' passes the session to the FastAPI endpoint handler.
    3. The endpoint uses 'db' to execute CRUD operations (SELECT, INSERT, UPDATE, DELETE).
    4. The 'finally' block GUARANTEES that db.close() runs after the request completes,
       preventing database connection leaks even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
