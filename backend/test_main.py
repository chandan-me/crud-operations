"""
test_main.py
------------
Automated test suite verifying all 5 CRUD API endpoints using FastAPI's TestClient
and an in-memory SQLite database.

This ensures all routes, Pydantic schemas, and CRUD logic work 100% correctly
in isolation without needing a live MySQL server running during automated testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import database
import models
from main import app

# 1. Setup isolated in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 2. Override get_db dependency to point to the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_db] = override_get_db

# 3. Create tables in test database
models.Base.metadata.create_all(bind=engine)

# 4. Instantiate TestClient
client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Runs before each test: clears products table to guarantee test isolation."""
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield


def test_root_endpoint():
    """Verify health check / root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "documentation" in data


def test_create_product():
    """Test POST /products successfully creates a product."""
    payload = {
        "name": "Wireless Mouse",
        "description": "Ergonomic 2.4G mouse",
        "price": 25.99,
        "quantity": 10
    }
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Wireless Mouse"
    assert data["price"] == 25.99
    assert data["quantity"] == 10


def test_create_product_validation_failure():
    """Test POST /products rejects invalid inputs (negative price, empty name)."""
    # Empty name
    response = client.post("/products", json={"name": "", "price": 10, "quantity": 1})
    assert response.status_code == 422

    # Negative price
    response = client.post("/products", json={"name": "Pen", "price": -5, "quantity": 1})
    assert response.status_code == 422


def test_get_all_products():
    """Test GET /products returns the list of all created products."""
    client.post("/products", json={"name": "Item A", "price": 10.0, "quantity": 5})
    client.post("/products", json={"name": "Item B", "price": 20.0, "quantity": 8})

    response = client.get("/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item A"
    assert data[1]["name"] == "Item B"


def test_get_product_by_id():
    """Test GET /products/{id} retrieves the correct product or returns 404."""
    create_res = client.post("/products", json={"name": "Headphones", "price": 99.99, "quantity": 12})
    prod_id = create_res.json()["id"]

    # Valid ID
    response = client.get(f"/products/{prod_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Headphones"

    # Non-existent ID -> 404
    missing_response = client.get("/products/9999")
    assert missing_response.status_code == 404


def test_update_product():
    """Test PUT /products/{id} updates fields properly."""
    create_res = client.post("/products", json={"name": "Old Monitor", "price": 150.0, "quantity": 2})
    prod_id = create_res.json()["id"]

    update_payload = {
        "name": "Upgraded 4K Monitor",
        "price": 199.99,
        "quantity": 5
    }
    response = client.put(f"/products/{prod_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Upgraded 4K Monitor"
    assert data["price"] == 199.99
    assert data["quantity"] == 5

    # Update non-existent product -> 404
    missing_update = client.put("/products/9999", json={"name": "Ghost"})
    assert missing_update.status_code == 404


def test_delete_product():
    """Test DELETE /products/{id} deletes the product or returns 404."""
    create_res = client.post("/products", json={"name": "Temporary Cable", "price": 5.0, "quantity": 1})
    prod_id = create_res.json()["id"]

    # Delete existing product
    del_response = client.delete(f"/products/{prod_id}")
    assert del_response.status_code == 200
    assert del_response.json()["success"] is True

    # Verify it is deleted from database
    get_res = client.get(f"/products/{prod_id}")
    assert get_res.status_code == 404

    # Deleting again should return 404
    del_again = client.delete(f"/products/{prod_id}")
    assert del_again.status_code == 404

