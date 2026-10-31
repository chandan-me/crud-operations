"""
crud.py
-------
Contains reusable CRUD (Create, Read, Update, Delete) database functions.

Why separate CRUD functions from API routes?
--------------------------------------------
1. Single Responsibility Principle: Routes in main.py handle HTTP requests and responses,
   while crud.py handles interacting with the database.
2. Reusability: These CRUD functions can be reused across different routes, background
   tasks, or test suites without duplicating SQL query logic.
3. Testability: You can easily unit test database logic in isolation.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
import models
import schemas


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """
    Retrieve a list of products from the database with pagination support.

    Parameters:
    - db: The active database session.
    - skip: Number of records to skip (for pagination, default: 0).
    - limit: Maximum number of records to return (default: 100).

    SQL Equivalent:
        SELECT * FROM products OFFSET <skip> LIMIT <limit>;
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Retrieve a single product by its primary key ID.

    Parameters:
    - db: The active database session.
    - product_id: The unique integer ID of the product.

    Returns:
    - The Product ORM object if found, otherwise None.

    SQL Equivalent:
        SELECT * FROM products WHERE id = <product_id> LIMIT 1;
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Insert a new product record into the MySQL database.

    Step-by-step Explanation:
    1. Instantiate a new SQLAlchemy model object with data from the Pydantic schema:
       product.model_dump() converts Pydantic fields into a Python dictionary.
    2. db.add(db_product): Stages the new object in the current transaction.
    3. db.commit(): Sends the INSERT statement to MySQL and permanently commits the transaction.
    4. db.refresh(db_product): Reloads the object from MySQL to fetch database-generated
       values (such as the auto-incremented primary key 'id').

    SQL Equivalent:
        INSERT INTO products (name, description, price, quantity)
        VALUES ('...', '...', 10.0, 5);
    """
    # 1. Convert validated Pydantic schema into a dictionary and unpack into SQLAlchemy model
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )

    # 2. Stage the object in the database session
    db.add(db_product)

    # 3. Commit the transaction to save changes permanently to MySQL
    db.commit()

    # 4. Refresh the instance from the database so it contains the new 'id'
    db.refresh(db_product)

    return db_product


def update_product(
    db: Session, product_id: int, product_update: schemas.ProductUpdate
) -> Optional[models.Product]:
    """
    Update an existing product's fields in the database.

    Step-by-step Explanation:
    1. Look up the existing product in the database by its ID.
    2. If the product does not exist, return None so the route can raise a 404 error.
    3. Iterate over the fields provided in the update payload.
       exclude_unset=True ensures only fields explicitly sent by the user are updated.
    4. Modify the attributes on the ORM object.
    5. Commit the transaction to apply the UPDATE statement in MySQL.
    6. Refresh and return the updated object.

    SQL Equivalent:
        UPDATE products SET name='...', price=... WHERE id = <product_id>;
    """
    # 1. Fetch the existing product record
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None

    # 2. Extract only fields that were actually provided in the request
    update_data = product_update.model_dump(exclude_unset=True)

    # 3. Apply the changes to the ORM model attributes
    for key, value in update_data.items():
        setattr(db_product, key, value)

    # 4. Save updates to MySQL
    db.commit()

    # 5. Refresh the ORM object to reflect database state
    db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Delete a product from the database by its ID.

    Step-by-step Explanation:
    1. Search for the product using its ID.
    2. If found, mark it for deletion using db.delete(db_product).
    3. Commit the transaction to execute the DELETE SQL query in MySQL.
    4. Return the deleted product record (or None if it was not found).

    SQL Equivalent:
        DELETE FROM products WHERE id = <product_id>;
    """
    # 1. Fetch the target product
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        return None

    # 2. Mark for deletion in session
    db.delete(db_product)

    # 3. Commit the delete transaction in MySQL
    db.commit()

    return db_product

