@echo off
echo Installing PostgreSQL locally for better performance...
echo.
echo This will download and install PostgreSQL 15 on your machine.
echo After installation, we'll configure it for Odoo.
echo.
pause

REM Download PostgreSQL installer
echo Downloading PostgreSQL...
curl -o postgresql-installer.exe "https://get.enterprisedb.com/postgresql/postgresql-15.4-1-windows-x64.exe"

echo.
echo Run the installer with these settings:
echo - Password for postgres user: postgres
echo - Port: 5432
echo - Locale: Default
echo.
echo After installation, run setup_local_db.bat
pause

postgresql-installer.exe
