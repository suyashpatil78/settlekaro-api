-- add users and expenses tables
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    expenses text[] DEFAULT '{}'::text[] NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id VARCHAR(255) PRIMARY KEY,
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    expense_details jsonb DEFAULT '[]'::jsonb,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
