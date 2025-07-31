-- PostgreSQL setup for Odoo with correct permissions
DROP USER IF EXISTS odoo;
CREATE USER odoo WITH 
    CREATEDB 
    CREATEROLE 
    SUPERUSER 
    LOGIN 
    PASSWORD '2609';

-- Grant necessary permissions
ALTER USER odoo CREATEDB;
ALTER USER odoo CREATEROLE;

-- Test the setup
\du odoo
