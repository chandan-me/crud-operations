"""
models.py
---------
Defines the SQLAlchemy ORM models (database tables structure)

What is an ORM (Object-Relational Mapping)?
An ORM translates between Python classes/objects and relational database tables/rows.
Instead of writing raw SQL strings like 'SELECT * FROM products', we interact with
Python objects like 'Product' and properties like 'product.price'.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric
from database import Base


class Product(Base):    # Product Model representing the 'products' table in MySQL.

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

    """
    Important: 'models.py' describes the database table. It does not define the API request validation.
    That is the responsibility of 'schemas.py'.
    """

    # Friendly string representation for debugging in console
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"

