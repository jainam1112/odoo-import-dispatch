@echo off
echo Setting up local PostgreSQL database for Odoo...
echo.

REM Find PostgreSQL installation
for /d %%i in ("C:\Program Files\PostgreSQL\*") do set PGPATH=%%i\bin

echo Using PostgreSQL at: %PGPATH%
echo.

REM Create Odoo user and database
echo Creating Odoo user and database...
"%PGPATH%\psql.exe" -U postgres -c "DROP USER IF EXISTS odoo;"
"%PGPATH%\psql.exe" -U postgres -c "CREATE USER odoo WITH CREATEDB CREATEROLE PASSWORD 'odoo';"

echo.
echo Testing connection...
"%PGPATH%\psql.exe" -U odoo -d postgres -c "SELECT version();"

echo.
echo Local PostgreSQL setup complete!
echo You can now use the local database configuration.
pause
