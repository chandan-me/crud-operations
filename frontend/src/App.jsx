/**
 * App.jsx
 * -------
 * The root component of the Product Management application.
 *
 * Responsibilities:
 * 1. Maintain global UI state using useState:
 *    - products: Array of products retrieved from FastAPI backend.
 *    - isLoading: Loading indicator state while fetching products.
 *    - editingProduct: Product object being edited (or null).
 *    - notification: Success/error feedback messages for the user.
 * 2. Fetch data from backend on initial mount using useEffect.
 * 3. Communicate with FastAPI using the standard browser Fetch API:
 *    - GET /products         -> Fetch list of products
 *    - POST /products        -> Add a new product
 *    - PUT /products/{id}    -> Update existing product
 *    - DELETE /products/{id} -> Delete a product
 * 4. Coordinate child components (ProductForm, ProductList).
 */

import React, { useState, useEffect } from 'react';
import ProductForm from './components/ProductForm.jsx';
import ProductList from './components/ProductList.jsx';
import './App.css';

// Base URL of the FastAPI Backend
const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  // ============================================================================
  // 1. State Management (useState)
  // ============================================================================
  // List of all products fetched from backend
  const [products, setProducts] = useState([]);

  // Flag to indicate when network requests are in progress
  const [isLoading, setIsLoading] = useState(false);

  // Holds the product currently being edited (null when not in edit mode)
  const [editingProduct, setEditingProduct] = useState(null);

  // Notification object: { type: 'success' | 'error', message: string }
  const [notification, setNotification] = useState(null);

  // Helper function to show self-dismissing notification messages
  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    // Automatically clear notification after 4 seconds
    setTimeout(() => {
      setNotification((current) => (current?.message === message ? null : current));
    }, 4000);
  };

  // ============================================================================
  // 2. Fetch All Products (Read Operation - GET /products)
  // ============================================================================
  const fetchProducts = async () => {
    setIsLoading(true);
    try {
      // Step 1: Send GET request to FastAPI
      const response = await fetch(`${API_BASE_URL}/products`);

      // Step 2: Check if HTTP status is in the 200-299 range
      if (!response.ok) {
        throw new Error(`Failed to fetch products (HTTP ${response.status})`);
      }

      // Step 3: Parse response JSON body
      const data = await response.json();

      // Step 4: Update React state, which triggers a UI re-render
      setProducts(data);
    } catch (err) {
      console.error('Error fetching products:', err);
      showNotification(
        `Unable to connect to backend: ${err.message}. Ensure FastAPI is running on port 8000.`,
        'error'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // ============================================================================
  // 3. Lifecycle Hook (useEffect)
  // The empty dependency array [] tells React to run this effect ONCE when
  // the component first mounts on screen.
  // ============================================================================
  useEffect(() => {
    fetchProducts();
  }, []);

  // ============================================================================
  // 4. Create Product (Create Operation - POST /products)
  // ============================================================================
  const handleCreateProduct = async (productData) => {
    try {
      // Send POST request with JSON body
      const response = await fetch(`${API_BASE_URL}/products`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(productData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned HTTP ${response.status}`);
      }

      const newProduct = await response.json();

      // Optimistically update products list or prepend the new product
      setProducts((prev) => [newProduct, ...prev]);
      showNotification(`Product "${newProduct.name}" created successfully!`, 'success');
    } catch (err) {
      console.error('Error creating product:', err);
      showNotification(`Failed to create product: ${err.message}`, 'error');
    }
  };

  // ============================================================================
  // 5. Update Product (Update Operation - PUT /products/{id})
  // ============================================================================
  const handleUpdateProduct = async (productData) => {
    if (!editingProduct) return;

    try {
      // Send PUT request to the specific product endpoint
      const response = await fetch(`${API_BASE_URL}/products/${editingProduct.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(productData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned HTTP ${response.status}`);
      }

      const updated = await response.json();

      // Update the modified product in local state
      setProducts((prev) =>
        prev.map((item) => (item.id === updated.id ? updated : item))
      );

      // Exit edit mode
      setEditingProduct(null);
      showNotification(`Product "${updated.name}" updated successfully!`, 'success');
    } catch (err) {
      console.error('Error updating product:', err);
      showNotification(`Failed to update product: ${err.message}`, 'error');
    }
  };

  // Dispatcher function passed to ProductForm
  const handleFormSubmit = (formData) => {
    if (editingProduct) {
      handleUpdateProduct(formData);
    } else {
      handleCreateProduct(formData);
    }
  };

  // ============================================================================
  // 6. Delete Product (Delete Operation - DELETE /products/{id})
  // ============================================================================
  const handleDeleteProduct = async (id, name) => {
    const confirmed = window.confirm(`Are you sure you want to delete "${name}" (ID #${id})?`);
    if (!confirmed) return;

    try {
      // Send DELETE request to FastAPI
      const response = await fetch(`${API_BASE_URL}/products/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned HTTP ${response.status}`);
      }

      // Filter out the deleted product from local state
      setProducts((prev) => prev.filter((item) => item.id !== id));

      // If the deleted item was currently being edited, cancel edit mode
      if (editingProduct?.id === id) {
        setEditingProduct(null);
      }

      showNotification(`Product "${name}" deleted successfully.`, 'success');
    } catch (err) {
      console.error('Error deleting product:', err);
      showNotification(`Failed to delete product: ${err.message}`, 'error');
    }
  };

  // ============================================================================
  // 7. Edit Selection Handlers
  // ============================================================================
  const handleSelectEdit = (product) => {
    setEditingProduct(product);
    // Smoothly scroll up to the form for better user experience
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCancelEdit = () => {
    setEditingProduct(null);
  };

  // ============================================================================
  // 8. Render UI
  // ============================================================================
  return (
    <div className="app-container">
      {/* Top Application Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>📦 Product Management System</h1>
        </div>
      </header>

      {/* Main Content Layout */}
      <main className="app-main">
        {/* Notification Toast Banner */}
        {notification && (
          <div className={`notification-banner banner-${notification.type}`} role="alert">
            <span className="banner-icon">
              {notification.type === 'success' ? '✅' : '❌'}
            </span>
            <span className="banner-text">{notification.message}</span>
            <button
              className="banner-close"
              onClick={() => setNotification(null)}
              aria-label="Dismiss notification"
            >
              ×
            </button>
          </div>
        )}

        {/* Product Input / Edit Form Component */}
        <ProductForm
          onSubmit={handleFormSubmit}
          editingProduct={editingProduct}
          onCancelEdit={handleCancelEdit}
        />

        {/* Products Table List Component */}
        <ProductList
          products={products}
          isLoading={isLoading}
          onEdit={handleSelectEdit}
          onDelete={handleDeleteProduct}
        />
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          FastAPI Backend running at <a href="http://127.0.0.1:8000" target="_blank" rel="noreferrer">http://127.0.0.1:8000</a> |
          Interactive Swagger Docs at <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">http://127.0.0.1:8000/docs</a>
        </p>
      </footer>
    </div>
  );
}

export default App;

