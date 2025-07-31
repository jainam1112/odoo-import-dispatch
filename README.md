# Odoo Import Dispatch Module

Custom dispatch tracking module for import company.

## Setup Instructions

### Prerequisites
1. **PostgreSQL** - Install PostgreSQL and create a database
2. **Python 3.8+** - Already configured with virtual environment
3. **Git** - For version control

### Database Setup
```sql
-- Connect to PostgreSQL as superuser and run:
CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';
CREATE DATABASE odoo OWNER odoo;
```

### Quick Start
1. **Install Dependencies** (already done):
   ```bash
   # Python packages are already installed in the virtual environment
   ```

2. **Configure Database**:
   - Make sure PostgreSQL is running on port 5432
   - Create user 'odoo' with password 'odoo'
   - Create database 'odoo' owned by user 'odoo'

3. **Start Odoo**:
   ```bash
   # Using PowerShell
   .\start_odoo.ps1
   
   # Or using batch file
   start_odoo.bat
   
   # Or manually
   D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf
   ```

4. **Access Odoo**:
   - Open browser and go to http://localhost:8069
   - Create a new database or use existing 'odoo' database
   - Install your custom module: 'Import Dispatch Process'

### Development
- Custom module files are in the root directory
- Odoo 17 source code is in `odoo-17/` folder
- Configuration file: `odoo.conf`
- Development mode is enabled for auto-reload

### Module Structure
```
├── __manifest__.py          # Module manifest
├── views/                   # XML views
│   └── dispatch_order_views.xml
├── security/               # Access rights
│   └── ir.model.access.csv
└── models/                 # Python models (to be created)
```

### Useful Commands
```bash
# Update module
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf -u import_dispatch_process

# Install module
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf -i import_dispatch_process

# Run with debug mode
D:\sagar\.venv\Scripts\python.exe odoo-17\odoo-bin -c odoo.conf --dev=all
```