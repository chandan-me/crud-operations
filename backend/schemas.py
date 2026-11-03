"""
schemas.py
----------
Defines Pydantic models (schemas) for request data validation and response serialization.

Why do we need Schemas in addition to ORM Models?
------------------------------------------------
1. Validation: Pydantic inspects incoming JSON payloads to make sure:
   - Required fields are present.
   - Types match (e.g., price is a valid positive number).
   - Constraints are met (e.g., quantity cannot be negative).
2. Security & Serialization: Schemas control what data is exposed back to the client.
3. Documentation: FastAPI uses these schemas to automatically generate interactive
   Swagger UI documentation (at /docs).
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# ==============================================================================
# Base Schema (Shared attributes between Create, Update, and Response)
# ==============================================================================
class ProductBase(BaseModel): # acts as a gatekepper for incoming & outgoing data
    """
    Common fields shared across Product schemas.
    """
    name: str = Field(
        ..., # this filed is strictly required
        min_length=1,
        max_length=255,
        description="Name of the product (must not be empty)",
        examples=["Mechanical Keyboard"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional detailed description of the product",
        examples=["RGB backlit keyboard with mechanical switches"]
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in INR (must be strictly greater than 0)",
        examples=[799.00]
    )
    quantity: int = Field(
        ...,
        ge=0,
        description="Stock inventory count (must be 0 or higher)",
        examples=[25]
    )


# ==============================================================================
# Create Schema (Used for POST /products requests)
# ==============================================================================
    """   
    Schema representing the incoming payload when creating a new product.
    Inherits name, description, price, and quantity from ProductBase.
    Does not require an 'id' because the database generates the id automatically.
    """
class ProductCreate(ProductBase):
    pass


# ==============================================================================
# Update Schema (Used for PUT /products/{id} requests)
# ==============================================================================
class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    All fields are optional: only provided fields will be modified.
    """
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated product name",
        examples=["Updated Keyboard Name"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Updated product description",
        examples=["Updated detailed description"]
    )
    price: Optional[float] = Field(
        default=None,
        gt=0,
        description="Updated price in INR (must be greater than 0)",
        examples=[899.00]
    )
    quantity: Optional[int] = Field(
        default=None,
        ge=0,
        description="Updated stock count (must be 0 or higher)",
        examples=[30]
    )


# ==============================================================================
# Response Schema (Used for data sent back to React client)
# ==============================================================================
class ProductResponse(ProductBase):
    """
    Schema returned to the client for GET, POST, and PUT operations.
    Includes the database-generated 'id' along with the product fields.
    """
    id: int = Field(..., description="Unique database identifier (Primary Key)")
    model_config = ConfigDict(from_attributes=True)
    # model_config => By default, Pydantic expects data in standard Python dictionary format (e.g., product["name"]). However, SQLAlchemy returns data as standard database object models (e.g., product.name).

     # Pydantic V2 Configuration: from_attributes tells Pydantic to read data directly
