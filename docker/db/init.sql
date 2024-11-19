-- This SQL file is automatically run by PostgreSQL during the first startup

-- Create a new schema
CREATE SCHEMA secrets_schema;

-- Create a new table within the schema
CREATE TABLE secrets_schema.secrets_table (
    id SERIAL PRIMARY KEY,
    fkey BYTEA UNIQUE NOT NULL,
    value BYTEA UNIQUE NOT NULL,
    path VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
