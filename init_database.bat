@echo off
echo Initializing Odoo Database...
echo This may take a few minutes...
echo.

cd /d "d:\sagar"

echo Step 1: Dropping existing database...
D:\sagar\.venv\Scripts\python.exe -c "import psycopg2; conn = psycopg2.connect(host='34.232.141.144', port=5432, user='odoo', password='StrongNewPasswordHere', database='postgres'); conn.autocommit = True; cur = conn.cursor(); cur.execute('DROP DATABASE IF EXISTS odoo_dispatch'); cur.execute('CREATE DATABASE odoo_dispatch OWNER odoo'); print('Database recreated successfully'); conn.close()"

echo.
echo Step 2: Initializing base modules...
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf -d odoo_dispatch -i base --stop-after-init --without-demo=all

echo.
echo Step 3: Installing web module...
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf -d odoo_dispatch -i web --stop-after-init --without-demo=all

echo.
echo Database initialization complete!
echo You can now run start_odoo.bat
pause
