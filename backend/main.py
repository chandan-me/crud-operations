"""
main.py
-------
The main entry point for the FastAPI backend application.

Key Responsibilities:
1. Initialize the FastAPI application instance.
2. Configure CORS (Cross-Origin Resource Sharing) middleware to allow React frontend requests.
3. Automatically generate database tables using SQLAlchemy ORM models.
4. Define RESTful API endpoints for the complete CRUD operations on Products:
   - POST   /products       -> Create a new product
   - GET    /products       -> Get all products
   - GET    /products/{id}  -> Get a specific product by ID
   - PUT    /products/{id}  -> Update an existing product
   - DELETE /products/{id}  -> Delete a product by ID
5. Provide a root endpoint (/) for health check and API overview.
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import local modules
import database
import models
import schemas
import crud

# ==============================================================================
# 1. Initialize FastAPI Application
# ==============================================================================
app = FastAPI(
    title="Product Management System API",
    description="A beginner-friendly Monolithic REST API built with FastAPI, SQLAlchemy, and MySQL.",
    version="1.0.0",
    docs_url="/docs",  # Interactive Swagger UI documentation URL
    redoc_url="/redoc"  # Alternative API documentation URL
)

# ==============================================================================
# 2. Database Initialization
# Automatically create the 'products' table in the MySQL database if it doesn't exist.
# ==============================================================================
try:
    models.Base.metadata.create_all(bind=database.engine)
    print(">> Database tables verified/created successfully.")
except Exception as e:
    print(f">> Notice: Could not connect to MySQL at startup ({e}).")
    print(">> Please ensure MySQL is running and database 'product_management' exists.")


# ==============================================================================
# 3. Configure CORS Middleware
# Browsers block HTTP requests between different ports (e.g. React on 5173,
# FastAPI on 8000) for security. CORS middleware explicitly authorizes the
# React frontend to communicate with this backend.
# ==============================================================================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"  # Allows all origins for local learning and development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers (e.g., Content-Type, Authorization)
)


# ==============================================================================
# 4. Root Health Check Endpoint
# ==============================================================================
@app.get(
    "/",
    tags=["Root"],
    summary="API Health Check & Welcome Message"
)
def root():
    """
    Returns a simple welcome message and pointers to interactive documentation.
    """
    return {
        "message": "Welcome to the Product Management API!",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "get_all_products": "GET /products",
            "create_product": "POST /products",
            "get_product_by_id": "GET /products/{id}",
            "update_product": "PUT /products/{id}",
            "delete_product": "DELETE /products/{id}"
        }
    }


# ==============================================================================
# 5. REST API CRUD Endpoints
# ==============================================================================

# ------------------------------------------------------------------------------
# 5.1 Create a New Product (POST /products)
# ------------------------------------------------------------------------------
@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    summary="Create a new product"
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db)
):
    """
    Creates a new product in the database.

    Flow:
    1. React sends JSON body: { "name": "...", "description": "...", "price": 10.0, "quantity": 5 }
    2. Pydantic validates incoming payload against 'ProductCreate' schema.
    3. 'Depends(database.get_db)' injects an active SQLAlchemy session.
    4. 'crud.create_product' writes the new record to MySQL and returns the saved object.
    5. FastAPI serializes the result into 'ProductResponse' JSON with HTTP 201 status code.
    """
    created_product = crud.create_product(db=db, product=product)
    return created_product


# ------------------------------------------------------------------------------
# 5.2 Read All Products (GET /products)
# ------------------------------------------------------------------------------
@app.get(
    "/products",
    response_model=List[schemas.ProductResponse],
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Retrieve all products"
)
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """
    Retrieves a list of all products from the MySQL database.

    Flow:
    1. React sends GET request to '/products'.
    2. 'crud.get_products' queries MySQL: 'SELECT * FROM products LIMIT 100 OFFSET 0'.
    3. Returns a list of Product ORM objects.
    4. FastAPI converts them into an array of JSON objects matching 'ProductResponse'.
    """
    products = crud.get_products(db=db, skip=skip, limit=limit)
    return products


# ------------------------------------------------------------------------------
# 5.3 Read Single Product by ID (GET /products/{id})
# ------------------------------------------------------------------------------
@app.get(
    "/products/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Retrieve a single product by ID"
)
def read_product_by_id(
    product_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieves a single product by its unique database ID.

    Flow:
    1. React requests '/products/5'.
    2. 'crud.get_product_by_id' searches for the product with id=5.
    3. If not found, raises an HTTPException with 404 status code and error message.
    4. If found, returns the product data serialized as JSON.
    """
    product = crud.get_product_by_id(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return product


# ------------------------------------------------------------------------------
# 5.4 Update an Existing Product (PUT /products/{id})
# ------------------------------------------------------------------------------
@app.put(
    "/products/{product_id}",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Update an existing product"
)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(database.get_db)
):
    """
    Updates the specified fields of an existing product.

    Flow:
    1. React sends PUT request to '/products/5' with updated values in JSON body.
    2. 'crud.update_product' looks up the product and applies modifications to MySQL.
    3. If the product is not found, raises a 404 error.
    4. Returns the updated product record as JSON.
    """
    updated_product = crud.update_product(
        db=db, product_id=product_id, product_update=product_update
    )
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return updated_product


# ------------------------------------------------------------------------------
# 5.5 Delete a Product (DELETE /products/{id})
# ------------------------------------------------------------------------------
@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Delete a product by ID"
)
def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Deletes a product from the database.

    Flow:
    1. React sends DELETE request to '/products/5'.
    2. 'crud.delete_product' checks for product existence and issues DELETE SQL.
    3. If product does not exist, raises a 404 error.
    4. Returns a success confirmation message in JSON format.
    """
    deleted_product = crud.delete_product(db=db, product_id=product_id)
    if not deleted_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    return {
        "success": True,
        "message": f"Product '{deleted_product.name}' (ID: {product_id}) was successfully deleted."
    }

