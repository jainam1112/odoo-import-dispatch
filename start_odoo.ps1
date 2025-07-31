# Odoo 17 Start Script
Write-Host "Starting Odoo 17..." -ForegroundColor Green
Write-Host "Make sure PostgreSQL is running on port 5432" -ForegroundColor Yellow
Write-Host "Database: odoo, User: odoo, Password: odoo" -ForegroundColor Yellow
Write-Host ""

Set-Location "d:\sagar"
& "D:\sagar\.venv\Scripts\python.exe" "odoo-17\odoo-bin" -c "odoo.conf"
