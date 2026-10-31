# 📦 Product Management System (Monolithic Full Stack CRUD)

A clean, beginner-friendly Product Management CRUD application built with **React.js**, **Python FastAPI**, **SQLAlchemy ORM**, and **MySQL**.

This project demonstrates the end-to-end communication flow between a client-side frontend, a RESTful API server, an Object-Relational Mapper (ORM), and a relational database.

---

## 📑 Table of Contents

1. [Project Overview & Architecture](#-project-overview--architecture)
2. [Folder Structure](#-folder-structure)
3. [MySQL Database Setup](#-mysql-database-setup)
4. [Backend (FastAPI + SQLAlchemy)](#-backend-fastapi--sqlalchemy)
   - [File-by-File Breakdown](#backend-file-by-file-breakdown)
   - [Core Concepts Explained](#backend-core-concepts-explained)
   - [REST API Endpoints Reference](#rest-api-endpoints-reference)
5. [Frontend (React + Vite)](#-frontend-react--vite)
   - [Component-by-Component Breakdown](#frontend-component-by-component-breakdown)
   - [Core React Concepts Explained](#core-react-concepts-explained)
6. [Complete Step-by-Step CRUD Flows](#-complete-step-by-step-crud-flows)
   - [1. Add Product (Create Flow)](#1-add-product-create-flow)
   - [2. View Products (Read Flow)](#2-view-products-read-flow)
   - [3. Update Product (Update Flow)](#3-update-product-update-flow)
   - [4. Delete Product (Delete Flow)](#4-delete-product-delete-flow)
7. [Running Instructions (Step-by-Step)](#-running-instructions)
8. [Automated Testing](#-automated-testing)

---

## 🏛 Project Overview & Architecture

This application uses a **Monolithic Architecture** where the backend handles all business logic, data validation, database transactions, and API endpoints within a single cohesive Python application.

```
+-------------------------------------------------------------+
|                      React Frontend                         |
|  (ProductForm, ProductList, ProductItem, useState, useEffect)|
+-------------------------------------------------------------+
                              |
                              | HTTP Request (JSON Body / Headers)
                              v
+-------------------------------------------------------------+
|                     FastAPI Backend                         |
|         (CORS Middleware, Routers, Exception Handling)       |
+-------------------------------------------------------------+
                              |
                              | Pydantic Validation & Dependency Injection
                              v
+-------------------------------------------------------------+
|                  Python CRUD Functions                      |
|                     (crud.py)                               |
+-------------------------------------------------------------+
                              |
                              | ORM Operations (add, commit, refresh, query)
                              v
+-------------------------------------------------------------+
|                    SQLAlchemy ORM                           |
|               (Engine, SessionLocal, Base)                  |
+-------------------------------------------------------------+
                              |
                              | SQL Dialect Driver (PyMySQL)
                              v
+-------------------------------------------------------------+
|                    MySQL Database                           |
|               (Database: product_management)                |
|                    (Table: products)                        |
+-------------------------------------------------------------+
```

### Communication Cycle:
1. **React** dispatches an asynchronous HTTP request using the browser `fetch()` API.
2. **FastAPI** intercepts the request and verifies CORS headers.
3. **Pydantic** validates incoming JSON data types and constraints.
4. **FastAPI** injects a dedicated database session using `Depends(database.get_db)`.
5. **crud.py** executes the corresponding ORM query on the SQLAlchemy `Product` model.
6. **SQLAlchemy** translates the Python query into raw SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) via `PyMySQL`.
7. **MySQL** executes the query and returns relational row data.
8. **SQLAlchemy** maps relational rows back into Python model instances.
9. **FastAPI** serializes model instances into clean JSON matching `ProductResponse`.
10. **React** parses the JSON payload and updates state using `useState()`.
11. **React Virtual DOM** re-renders only the changed UI components.

---

## 📁 Folder Structure

```
product-management/
│
├── frontend/
│   ├── package.json               # Node packages and scripts
│   ├── vite.config.js             # Vite development server configuration
│   ├── index.html                 # HTML single-page template
│   └── src/
│       ├── components/
│       │   ├── ProductForm.jsx    # Controlled form for Add and Edit modes
│       │   ├── ProductList.jsx    # Table container with loading & empty states
│       │   └── ProductItem.jsx    # Single table row with Action buttons
│       ├── App.jsx                # Main state container & Fetch API coordinator
│       ├── main.jsx               # React entry point mounting to DOM
│       └── App.css                # Pure CSS styles (responsive design)
│
├── backend/
│   ├── main.py                    # FastAPI instance, CORS, & REST endpoints
│   ├── database.py                # Engine, SessionLocal, Base, & get_db dependency
│   ├── models.py                  # SQLAlchemy ORM Product database model
│   ├── schemas.py                 # Pydantic validation and serialization models
│   ├── crud.py                    # Pure database query operations
│   ├── database.sql               # MySQL database and table creation script
│   ├── requirements.txt           # Python dependencies
│   ├── test_main.py               # Automated pytest suite for all CRUD endpoints
│   ├── .env.example               # Template for environment variables
│   └── .env                       # Active local environment variables
│
└── README.md                      # Complete documentation and tutorial
```

---

## 🗄 MySQL Database Setup

The application stores data in MySQL inside a database named `product_management`.

### Database Fields:
- `id`: `INT`, Primary Key, Auto Increment
- `name`: `VARCHAR(255)`, Required
- `description`: `TEXT`, Optional
- `price`: `DECIMAL(10, 2)`, Required
- `quantity`: `INT`, Required (Default: `0`)

### SQL Setup Script (`backend/database.sql`):
```sql
-- 1. Create database
CREATE DATABASE IF NOT EXISTS product_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE product_management;

-- 2. Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    INDEX idx_products_name (name)
);

-- 3. Insert initial starter data
INSERT INTO products (name, description, price, quantity) VALUES
('Ergonomic Mechanical Keyboard', 'RGB backlit gaming keyboard with tactile blue switches', 79.99, 25),
('Wireless Bluetooth Mouse', 'Rechargeable 2.4GHz optical mouse with silent click', 29.50, 50),
('Ultra HD 4K Monitor 27-inch', '144Hz IPS display with HDR400 and ultra-thin bezels', 299.99, 12);
```

---

## 🐍 Backend (FastAPI + SQLAlchemy)

### Backend File-by-File Breakdown

#### 1. `database.py`
- **Purpose**: Establishes connection to MySQL and manages database transactions.
- **Key Lines**:
  - `load_dotenv()`: Reads `.env` so database credentials are not hardcoded.
  - `engine = create_engine(DATABASE_URL)`: Manages low-level database connection pool.
  - `SessionLocal = sessionmaker(...)`: Generates database sessions on demand.
  - `Base = declarative_base()`: Common class that all ORM models inherit from.
  - `def get_db()`: Generator function that opens a session, `yield`s it to the route, and closes it in a `finally` block to prevent connection leaks.

#### 2. `models.py`
- **Purpose**: Defines how the `products` table looks inside the MySQL database using Python classes.
- **Key Lines**:
  - `class Product(Base)`: Maps the Python class to the relational table.
  - `__tablename__ = "products"`: Table name inside MySQL.
  - `id = Column(Integer, primary_key=True, autoincrement=True)`: Primary key.
  - `price = Column(Numeric(10, 2), nullable=False)`: Uses `DECIMAL(10, 2)` to eliminate floating-point rounding errors on money.

#### 3. `schemas.py`
- **Purpose**: Pydantic schemas validate data coming in from HTTP requests and shape data going out to React.
- **Key Schemas**:
  - `ProductBase`: Contains fields common to all schemas (`name`, `description`, `price`, `quantity`).
  - `ProductCreate`: Validates payload for `POST /products`.
  - `ProductUpdate`: Allows partial updates for `PUT /products/{id}`.
  - `ProductResponse`: Includes the database-generated `id` and sets `model_config = ConfigDict(from_attributes=True)` so Pydantic can read attributes directly from SQLAlchemy ORM objects.

#### 4. `crud.py`
- **Purpose**: Contains the raw database query functions separated from the HTTP routes.
- **Key Functions**:
  - `get_products(db, skip, limit)`: Runs `db.query(Product).offset(skip).limit(limit).all()`.
  - `get_product_by_id(db, product_id)`: Runs `db.query(Product).filter(Product.id == product_id).first()`.
  - `create_product(db, product)`: Uses `db.add()`, `db.commit()`, and `db.refresh()`.
  - `update_product(db, product_id, product_update)`: Mutates attributes and commits changes.
  - `delete_product(db, product_id)`: Issues `db.delete()` and commits.

#### 5. `main.py`
- **Purpose**: Central FastAPI server entry point.
- **Key Features**:
  - `app = FastAPI(...)`: Creates API app instance with interactive Swagger docs at `/docs`.
  - `CORSMiddleware`: Authorizes requests coming from `http://localhost:5173`.
  - `models.Base.metadata.create_all(...)`: Automatically creates tables in MySQL if they do not exist.
  - REST Endpoints: Defined with `@app.get`, `@app.post`, `@app.put`, `@app.delete`.

### Backend Core Concepts Explained

#### How `Depends()` Works (Dependency Injection)
In `main.py`, endpoints receive the database session via:
```python
@app.get("/products")
def read_products(db: Session = Depends(database.get_db)):
```
`Depends(database.get_db)` tells FastAPI to:
1. Execute `get_db()`.
2. Grab the `Session` instance generated by `yield db`.
3. Provide that session to `read_products` as parameter `db`.
4. When the endpoint finishes sending the response, resume execution inside `get_db()` and run `db.close()`.
This guarantees database connections are never left open or leaked.

#### Models vs Schemas
| Feature | SQLAlchemy Model (`models.py`) | Pydantic Schema (`schemas.py`) |
| :--- | :--- | :--- |
| **Domain** | Relational Database (MySQL) | Network Request / Response (HTTP JSON) |
| **Duty** | Defines database columns, keys, types | Validates input constraints, serializes JSON |
| **Example** | `Column(Numeric(10, 2))` | `price: float = Field(..., gt=0)` |

---

### REST API Endpoints Reference

| Method | Endpoint | Description | Request Body | Response Body | HTTP Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | API Health Check | None | `{"status": "online", ...}` | `200 OK` |
| **POST** | `/products` | Create product | `ProductCreate` JSON | `ProductResponse` JSON | `201 Created` |
| **GET** | `/products` | Get all products | None | `Array<ProductResponse>` | `200 OK` |
| **GET** | `/products/{id}`| Get product by ID | None | `ProductResponse` JSON | `200 OK` (or `404`) |
| **PUT** | `/products/{id}`| Update product | `ProductUpdate` JSON | `ProductResponse` JSON | `200 OK` (or `404`) |
| **DELETE**| `/products/{id}`| Delete product | None | `{"success": true, ...}` | `200 OK` (or `404`) |

---

## ⚛️ Frontend (React + Vite)

### Frontend Component-by-Component Breakdown

#### 1. `App.jsx`
- **Purpose**: Root container that manages the application state and backend API calls.
- **State Managed**:
  - `products`: Array of product items.
  - `isLoading`: Boolean controlling the spinner display.
  - `editingProduct`: Object currently being modified (or `null`).
  - `notification`: Feedback alert object `{ type: 'success' | 'error', message: string }`.
- **Functions**:
  - `fetchProducts()`: Dispatches `GET /products`.
  - `handleCreateProduct(formData)`: Dispatches `POST /products`.
  - `handleUpdateProduct(formData)`: Dispatches `PUT /products/{id}`.
  - `handleDeleteProduct(id, name)`: Prompts confirmation, then dispatches `DELETE /products/{id}`.

#### 2. `components/ProductForm.jsx`
- **Purpose**: Controlled form allowing users to add or edit a product.
- **Features**:
  - Automatically switches between **Add Mode** and **Edit Mode** depending on the `editingProduct` prop.
  - Uses `useEffect` to pre-populate input fields when editing.
  - Performs instant client-side validation (checks non-empty name, positive price, valid quantity).
  - Provides a "Cancel Edit" button in edit mode.

#### 3. `components/ProductList.jsx`
- **Purpose**: Displays the tabular inventory view.
- **Features**:
  - Shows an animated loading spinner when `isLoading` is true.
  - Shows a helpful empty state when no products exist.
  - Renders the table and maps each product to a `ProductItem` component.

#### 4. `components/ProductItem.jsx`
- **Purpose**: Renders a single row `<tr>` inside the inventory table.
- **Features**:
  - Formats raw numbers into currency (e.g. `₹799.00`).
  - Displays color-coded inventory badges (**In Stock**, **Low Stock**, **Out of Stock**).
  - Provides **Edit** and **Delete** action buttons with event callbacks.

#### 5. `App.css`
- **Purpose**: Clean, responsive styling using CSS variables, flexbox, and CSS grid.

---

### Core React Concepts Explained

#### 1. Functional Components
A modern React component is simply a JavaScript function that takes `props` (inputs) and returns JSX (the HTML structure to render).
```jsx
function ProductItem({ product, onEdit, onDelete }) {
  return <tr>...</tr>;
}
```

#### 2. Props (Properties)
Props allow parent components to pass data and functions down to child components.
- In `App.jsx`: `<ProductList products={products} onDelete={handleDeleteProduct} />`
- `ProductList` receives `products` and `onDelete` as arguments and uses them.

#### 3. `useState`
`useState` allows components to remember values between renders. Calling the setter function (e.g., `setProducts`) causes React to re-render the component with the new data.
```jsx
const [products, setProducts] = useState([]);
```

#### 4. `useEffect`
Used for side effects like fetching data from an API. The dependency array `[]` ensures the effect runs only once when the component is initially mounted.
```jsx
useEffect(() => {
  fetchProducts();
}, []);
```

#### 5. Controlled Form Inputs
In React, form `<input>` values are tied directly to state variables. When the user types, `onChange` updates state, and state updates the input's `value`.
```jsx
<input
  name="name"
  value={formData.name}
  onChange={handleChange}
/>
```

---

## 🔄 Complete Step-by-Step CRUD Flows

### 1. Add Product (Create Flow)

```
[ User types details ] -> [ Clicks "Add Product" ]
        |
        v
[ React: ProductForm.jsx checks client-side validation ]
        |
        v
[ React: App.jsx sends POST http://127.0.0.1:8000/products with JSON payload ]
        |
        v
[ FastAPI: main.py intercepts request, CORS allows origin ]
        |
        v
[ Pydantic: schemas.ProductCreate validates payload (price > 0, quantity >= 0) ]
        |
        v
[ FastAPI: database.get_db() dependency injects active SQLAlchemy Session ]
        |
        v
[ CRUD: crud.create_product creates models.Product and runs db.add() ]
        |
        v
[ SQLAlchemy: Issues INSERT INTO products (...) VALUES (...) to MySQL ]
        |
        v
[ MySQL: Inserts row, generates new auto-increment ID ]
        |
        v
[ SQLAlchemy: db.refresh() reads newly generated ID ]
        |
        v
[ FastAPI: Returns HTTP 201 Created with JSON matching ProductResponse ]
        |
        v
[ React: response.json() received; setProducts([newProduct, ...prev]) updates UI ]
```

---

### 2. View Products (Read Flow)
1. User loads the React application in the web browser.
2. `App.jsx` mounts and executes its `useEffect(..., [])` hook.
3. React sends `GET http://127.0.0.1:8000/products`.
4. FastAPI invokes `read_products` with `db: Session = Depends(database.get_db)`.
5. `crud.get_products` runs `db.query(models.Product).all()`.
6. SQLAlchemy sends `SELECT * FROM products` to MySQL.
7. MySQL returns all matching rows.
8. FastAPI serializes the list into JSON using `ProductResponse`.
9. React receives the JSON array and runs `setProducts(data)`.
10. `ProductList.jsx` maps over the products and displays the table rows.

---

### 3. Update Product (Update Flow)
1. User clicks the **Edit** button next to a product row.
2. `ProductItem` calls `onEdit(product)`.
3. `App.jsx` sets `editingProduct` state to that product object.
4. `ProductForm.jsx` detects `editingProduct` change via `useEffect` and pre-populates form inputs.
5. User modifies the price or stock quantity and clicks **Save Changes**.
6. Form submits and calls `handleUpdateProduct(formData)`.
7. React dispatches `PUT http://127.0.0.1:8000/products/{id}` with updated fields.
8. FastAPI validates incoming data via `ProductUpdate` schema.
9. `crud.update_product` issues an `UPDATE products SET ... WHERE id = {id}` to MySQL.
10. MySQL commits the updated record.
11. FastAPI returns HTTP 200 with updated product JSON.
12. React replaces the old product in state and exits edit mode.

---

### 4. Delete Product (Delete Flow)
1. User clicks the **Delete** button next to a product row.
2. Browser displays a confirmation dialog: *"Are you sure you want to delete...?"*
3. If confirmed, React dispatches `DELETE http://127.0.0.1:8000/products/{id}`.
4. FastAPI receives request and calls `crud.delete_product(db, product_id)`.
5. SQLAlchemy verifies the product exists, then executes `DELETE FROM products WHERE id = {id}`.
6. MySQL permanently removes the row.
7. FastAPI returns `{"success": true, "message": "Product ... deleted"}`.
8. React filters out the deleted product from local state:
   ```javascript
   setProducts((prev) => prev.filter((item) => item.id !== id));
   ```
9. The table row instantly disappears from the browser without a full page refresh.

---

## 🚀 Running Instructions

Follow these exact commands to run the application locally.

### Prerequisites:
- Python 3.10+ installed
- Node.js 18+ and npm installed
- MySQL Server 8.0+ running

---

### Step 1: Configure MySQL Database
Open your MySQL terminal or MySQL Workbench and execute the setup script:

```bash
# Log in to MySQL as root
mysql -u root -p
```

Inside the MySQL prompt, run:
```sql
CREATE DATABASE IF NOT EXISTS product_management;
```

*(Optional: You can run the entire `backend/database.sql` script to create tables and sample data immediately, or let FastAPI auto-create the table on startup!)*

---

### Step 2: Configure Backend Environment
Navigate to the `backend` folder:
```bash
cd backend
```

Copy the example environment file:
```bash
# On Windows (PowerShell):
copy .env.example .env

# On macOS/Linux:
cp .env.example .env
```

Open `.env` and verify your MySQL credentials:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/product_management
```

---

### Step 3: Set Up Python Virtual Environment & Install Dependencies
Inside the `backend` directory:

```bash
# 1. Create a virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (CMD):
.\venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt
```

---

### Step 4: Start the FastAPI Server
With the virtual environment active, run:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- Backend API URL: **http://127.0.0.1:8000**
- Interactive Swagger Documentation: **http://127.0.0.1:8000/docs**
- Alternative ReDoc Documentation: **http://127.0.0.1:8000/redoc**

---

### Step 5: Set Up and Start React Frontend
Open a **new terminal window** and navigate to the `frontend` folder:

```bash
cd frontend

# 1. Install Node.js dependencies
npm install

# 2. Start the Vite development server
npm run dev
```

The frontend will start at:
- **http://127.0.0.1:5173** (or `http://localhost:5173`)

Open this URL in your web browser to use the application!

---

## 🧪 Automated Testing

The project includes an automated test suite verifying all 5 CRUD operations, input validations, and error status codes using an isolated in-memory test database.

To run tests:
```bash
cd backend
.\venv\Scripts\python -m pytest -v
```

Expected output:
```
test_main.py::test_root_endpoint PASSED                         [ 14%]
test_main.py::test_create_product PASSED                        [ 28%]
test_main.py::test_create_product_validation_failure PASSED     [ 42%]
test_main.py::test_get_all_products PASSED                      [ 57%]
test_main.py::test_get_product_by_id PASSED                     [ 71%]
test_main.py::test_update_product PASSED                        [ 85%]
test_main.py::test_delete_product PASSED                        [100%]
======================== 7 passed in 0.89s =========================
```

