"""
models.py
---------
Defines the SQLAlchemy ORM models (database tables) for the Product Management application.

What is an ORM (Object-Relational Mapping)?
An ORM translates between Python classes/objects and relational database tables/rows.
Instead of writing raw SQL strings like 'SELECT * FROM products', we interact with
Python objects like 'Product' and properties like 'product.price'.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric
from database import Base


class Product(Base):
    """
    Product Model representing the 'products' table in MySQL.
    
    Database Schema:
    ----------------
    - id: Primary key integer, automatically increments with each new record.
    - name: String up to 255 characters, required (nullable=False), indexed for fast search.
    - description: Variable-length text for longer product descriptions (optional).
    - price: Precise numeric decimal with 10 total digits and 2 decimal places (e.g., 99.99).
    - quantity: Integer representing items in stock, defaults to 0.
    """
    
    # 1. Table name in MySQL database
    __tablename__ = "products"

    # 2. Primary key column (auto-incrementing unique identifier)
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Unique identifier for the product"
    )

    # 3. Product name (VARCHAR(255), cannot be NULL)
    name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Name or title of the product"
    )

    # 4. Product description (TEXT, can be NULL if empty)
    description = Column(
        Text,
        nullable=True,
        doc="Detailed description of the product"
    )

    # 5. Product price (DECIMAL(10, 2), cannot be NULL)
    # Using Numeric(10, 2) is best practice for currency to prevent floating-point rounding errors.
    price = Column(
        Numeric(10, 2),
        nullable=False,
        doc="Retail price of the product"
    )

    # 6. Inventory quantity (INTEGER, defaults to 0)
    quantity = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Units currently available in inventory"
    )

    def __repr__(self) -> str:
        """Friendly string representation for debugging in console."""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"

