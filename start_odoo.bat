@echo off
echo Starting Odoo 17 with Local PostgreSQL...
echo Database Server: localhost:5432
echo Database User: odoo
echo.
echo This will show the database creation interface
echo where you can create a new database properly.
echo.

cd /d "d:\sagar"
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf

pause
