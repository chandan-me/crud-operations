/**
 * ProductItem.jsx
 * ---------------
 * Functional component representing a single row in the products table.
 *
 * Props:
 * - product: The product object { id, name, description, price, quantity }
 * - onEdit: Callback function invoked when the user clicks the "Edit" button.
 * - onDelete: Callback function invoked when the user clicks the "Delete" button.
 *
 * Concepts Demonstrated:
 * - Functional Component: Pure JS function returning JSX.
 * - Props: Receiving data and event handler callbacks from parent (ProductList).
 * - Conditional CSS classes: Dynamic badge coloring based on stock quantity.
 * - Event Handling: onClick triggering callback functions.
 */

import React from 'react';

function ProductItem({ product, onEdit, onDelete }) {
  // Format the price into Indian currency format (e.g., ₹79.99)
  const formattedPrice = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
  }).format(product.price);

  // Helper to determine inventory status badge color
  const getStockBadge = (quantity) => {
    if (quantity <= 0) {
      return <span className="badge badge-danger">Out of Stock</span>;
    } else if (quantity <= 5) {
      return <span className="badge badge-warning">Low: {quantity} left</span>;
    } else {
      return <span className="badge badge-success">{quantity} in stock</span>;
    }
  };

  return (
    <tr className="product-row">
      {/* 1. Product ID */}
      <td className="col-id">#{product.id}</td>

      {/* 2. Product Name & Description */}
      <td className="col-name">
        <strong>{product.name}</strong>
      </td>

      <td className="col-desc">
        <span className="desc-text" title={product.description || 'No description provided'}>
          {product.description || <em className="text-muted">No description</em>}
        </span>
      </td>

      {/* 3. Product Price */}
      <td className="col-price">{formattedPrice}</td>

      {/* 4. Product Quantity & Stock Badge */}
      <td className="col-qty">
        {getStockBadge(product.quantity)}
      </td>

      {/* 5. Action Buttons (Edit and Delete) */}
      <td className="col-actions">
        <button
          type="button"
          className="btn btn-sm btn-edit"
          onClick={() => onEdit(product)}
          title="Edit this product"
        >
          ✏️ Edit
        </button>
        <button
          type="button"
          className="btn btn-sm btn-delete"
          onClick={() => onDelete(product.id, product.name)}
          title="Delete this product"
        >
          🗑️ Delete
        </button>
      </td>
    </tr>
  );
}

export default ProductItem;

