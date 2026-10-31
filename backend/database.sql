-- ==============================================================================
-- MySQL Database Creation Script for Product Management CRUD Application
-- ==============================================================================

-- 1. Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS product_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. Select the database
USE product_management;

-- 3. Create the products table
-- Fields:
-- - id: Primary Key, Auto Incrementing unique integer
-- - name: Product name (VARCHAR up to 255 characters, required)
-- - description: Detailed text description of the product (optional)
-- - price: Decimal number with 10 digits total and 2 decimal places (required)
-- - quantity: Stock count integer (required, defaults to 0)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    INDEX idx_products_name (name)
);

-- 4. Insert initial sample products (Optional starter data)
INSERT INTO products (name, description, price, quantity) VALUES
('Ergonomic Mechanical Keyboard', 'RGB backlit gaming keyboard with tactile blue switches', 79.99, 25),
('Wireless Bluetooth Mouse', 'Rechargeable 2.4GHz optical mouse with silent click', 29.50, 50),
('Ultra HD 4K Monitor 27-inch', '144Hz IPS display with HDR400 and ultra-thin bezels', 299.99, 12),
('Noise-Cancelling Headphones', 'Over-ear wireless headphones with active noise cancellation', 149.00, 18);

-- 5. Verify the data
SELECT * FROM products;

