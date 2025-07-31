-- PostgreSQL Database Setup for Odoo 17
-- Run this script as PostgreSQL superuser (postgres)

-- Create Odoo user
CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';

-- Create Odoo database
CREATE DATABASE odoo OWNER odoo ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' TEMPLATE=template0;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE odoo TO odoo;

-- Connect to the odoo database and create extensions
\c odoo;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO odoo;
GRANT CREATE ON SCHEMA public TO odoo;
