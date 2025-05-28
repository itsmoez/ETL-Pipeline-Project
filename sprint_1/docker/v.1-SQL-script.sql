docker run --rm \
  --name pg-volume-test \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v ~/my-sql-scripts:/docker-entrypoint-initdb.d \
  postgres
  docker stop pg-volume-demo
  docker rm pg-volume-demo

-- Create branch table
CREATE TABLE branches (
    branch_id UUID PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL
);

-- Create transactions table
CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY,
    branch_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    total NUMERIC(10, 2),
    transaction_type VARCHAR(50),
    CONSTRAINT fk_branch
        FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
        ON DELETE CASCADE
);

-- Create transaction_items table
CREATE TABLE transaction_items (
    transaction_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (transaction_id, product_id),
    CONSTRAINT fk_transactions
        FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_products
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
);