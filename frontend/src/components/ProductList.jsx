/**
 * ProductList.jsx
 * ---------------
 * Functional component that renders the product inventory table.
 *
 * Props:
 * - products: Array of product objects fetched from FastAPI.
 * - isLoading: Boolean flag indicating if products are currently being fetched.
 * - onEdit: Callback function passed down to ProductItem for editing.
 * - onDelete: Callback function passed down to ProductItem for deleting.
 *
 * Concepts Demonstrated:
 * - Conditional Rendering: Displays a loader spinner when isLoading is true,
 *   an empty message when products is empty, or the table when data exists.
 * - Array.prototype.map(): Iterating over the products array to generate ProductItem elements.
 * - The 'key' Prop: Providing a unique identifier (product.id) so React can efficiently
 *   re-render and update the DOM when items change.
 */

import React from 'react';
import ProductItem from './ProductItem.jsx';

function ProductList({ products, isLoading, onEdit, onDelete }) {
  // 1. Loading State Display
  if (isLoading) {
    return (
      <div className="card loading-card">
        <div className="spinner"></div>
        <p>Loading products from server...</p>
      </div>
    );
  }

  // 2. Empty State Display
  if (!products || products.length === 0) {
    return (
      <div className="card empty-card">
        <div className="empty-icon">📦</div>
        <h3>No Products Available</h3>
        <p>Your inventory is currently empty. Use the form above to add your first product!</p>
      </div>
    );
  }

  // 3. Render Table with Products
  return (
    <div className="card table-card">
      <div className="card-header">
        <h2>Product Inventory</h2>
        <span className="count-pill">{products.length} {products.length === 1 ? 'Product' : 'Products'}</span>
      </div>

      <div className="table-responsive">
        <table className="products-table">
          <thead>
            <tr>
              <th className="col-id">ID</th>
              <th className="col-name">Name</th>
              <th className="col-desc">Description</th>
              <th className="col-price">Price</th>
              <th className="col-qty">Quantity</th>
              <th className="col-actions">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <ProductItem
                key={product.id}
                product={product}
                onEdit={onEdit}
                onDelete={onDelete}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ProductList;

