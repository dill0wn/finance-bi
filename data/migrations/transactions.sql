-- Create a new database
CREATE DATABASE transactions;

-- Create a new table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    source TEXT
    account TEXT,
    date DATE,
    description TEXT,
    note TEXT,
    check_number TEXT,
    amount MONEY,
    balance MONEY
);