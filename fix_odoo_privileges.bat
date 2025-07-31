@echo off
echo Fixing PostgreSQL user privileges for Odoo...
echo.

REM Find PostgreSQL installation
for /d %%i in ("C:\Program Files\PostgreSQL\*") do set PGPATH=%%i\bin

echo Using PostgreSQL at: %PGPATH%
echo.

echo You will be prompted for the postgres user password
echo Please enter your postgres superuser password when prompted.
echo.

REM Grant superuser privileges to odoo user
echo Granting superuser privileges to odoo user...
"%PGPATH%\psql.exe" -U postgres -d postgres -c "ALTER USER odoo SUPERUSER;"

echo.
echo Verifying user privileges...
"%PGPATH%\psql.exe" -U postgres -d postgres -c "\du odoo"

echo.
echo PostgreSQL user privileges updated!
echo The odoo user now has superuser privileges for database creation.
pause
