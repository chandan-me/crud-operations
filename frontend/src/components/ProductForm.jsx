/**
 * ProductForm.jsx
 * ---------------
 * Functional component providing an input form to create a new product
 * or edit an existing one.
 *
 * Props:
 * - onSubmit: Callback function (create or update) passing the validated formData.
 * - editingProduct: Product object if currently in "Edit Mode", or null for "Add Mode".
 * - onCancelEdit: Callback function to cancel editing mode and reset the form.
 *
 * Concepts Demonstrated:
 * - Controlled Components: Form input values are driven by React state (formData).
 * - useState: Manages local form inputs (name, description, price, quantity).
 * - useEffect: Synchronizes form fields when 'editingProduct' prop changes.
 * - Form Validation: Ensures user inputs valid values before submitting to the backend.
 * - Event Handling: Handles onChange and onSubmit events.
 */

import React, { useState, useEffect } from 'react';

// Initial empty state for resetting the form
const initialFormState = {
  name: '',
  description: '',
  price: '',
  quantity: '',
};

function ProductForm({ onSubmit, editingProduct, onCancelEdit }) {
  // 1. Local state for form input values
  const [formData, setFormData] = useState(initialFormState);

  // 2. Local state for inline validation warning message
  const [formError, setFormError] = useState('');

  // 3. useEffect hook to populate form when editing an existing product
  // Whenever the 'editingProduct' prop changes:
  // - If it's a product, fill the form fields with that product's values.
  // - If it's null (user cancelled or finished), reset the form back to blank.
  useEffect(() => {
    if (editingProduct) {
      setFormData({
        name: editingProduct.name || '',
        description: editingProduct.description || '',
        price: editingProduct.price !== undefined ? editingProduct.price.toString() : '',
        quantity: editingProduct.quantity !== undefined ? editingProduct.quantity.toString() : '',
      });
      setFormError('');
    } else {
      setFormData(initialFormState);
      setFormError('');
    }
  }, [editingProduct]);

  // 4. Input Change Handler
  // Uses computed property names [name]: value to dynamically update matching state field
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear validation error when user begins typing
    if (formError) setFormError('');
  };

  // 5. Form Submit Handler
  const handleSubmit = (e) => {
    // Prevent the default browser behavior of reloading the full page on submit
    e.preventDefault();

    // Basic Client-Side Validation
    if (!formData.name.trim()) {
      setFormError('Product Name is required.');
      return;
    }

    const parsedPrice = parseFloat(formData.price);
    if (isNaN(parsedPrice) || parsedPrice <= 0) {
      setFormError('Please enter a valid price greater than 0.');
      return;
    }

    const parsedQuantity = parseInt(formData.quantity, 10);
    if (isNaN(parsedQuantity) || parsedQuantity < 0) {
      setFormError('Quantity cannot be negative.');
      return;
    }

    // Prepare payload formatted for backend Pydantic schema
    const payload = {
      name: formData.name.trim(),
      description: formData.description.trim() || null,
      price: parsedPrice,
      quantity: parsedQuantity,
    };

    // Pass data up to parent component (App.jsx)
    onSubmit(payload);

    // If we were adding (not editing), reset the form inputs
    if (!editingProduct) {
      setFormData(initialFormState);
    }
  };

  // 6. Cancel Edit Handler
  const handleCancel = () => {
    setFormData(initialFormState);
    setFormError('');
    if (onCancelEdit) {
      onCancelEdit();
    }
  };

  const isEditMode = Boolean(editingProduct);

  return (
    <div className={`card form-card ${isEditMode ? 'form-card-edit-mode' : ''}`}>
      <div className="card-header">
        <h2>{isEditMode ? `Edit Product #${editingProduct.id}` : 'Add New Product'}</h2>
        {isEditMode && <span className="mode-badge">Editing Mode</span>}
      </div>

      {formError && (
        <div className="alert alert-warning" role="alert">
          ⚠️ {formError}
        </div>
      )}

      <form onSubmit={handleSubmit} className="product-form" noValidate>
        <div className="form-grid">
          {/* Product Name */}
          <div className="form-group">
            <label htmlFor="name">
              Product Name <span className="required">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Ergonomic Keyboard"
              required
            />
          </div>

          {/* Product Price */}
          <div className="form-group">
            <label htmlFor="price">
              Price (₹ INR) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="price"
              name="price"
              step="0.01"
              min="0.01"
              value={formData.price}
              onChange={handleChange}
              placeholder="e.g. 799.00"
              required
            />
          </div>

          {/* Product Quantity */}
          <div className="form-group">
            <label htmlFor="quantity">
              Quantity in Stock <span className="required">*</span>
            </label>
            <input
              type="number"
              id="quantity"
              name="quantity"
              min="0"
              step="1"
              value={formData.quantity}
              onChange={handleChange}
              placeholder="e.g. 25"
              required
            />
          </div>

          {/* Product Description */}
          <div className="form-group form-group-full">
            <label htmlFor="description">Product Description (Optional)</label>
            <textarea
              id="description"
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              placeholder="e.g. Wireless RGB mechanical keyboard with blue switches..."
            ></textarea>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {isEditMode ? '💾 Save Changes' : '➕ Add Product'}
          </button>

          {isEditMode && (
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleCancel}
            >
              ✖ Cancel Edit
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default ProductForm;

