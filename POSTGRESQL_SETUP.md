# Instructions for Local PostgreSQL Setup

## Option 1: If you know your PostgreSQL postgres user password
1. Edit odoo.conf and set db_password to your postgres password
2. Start Odoo with: start_odoo.bat

## Option 2: If you don't know the postgres password
You can reset it or use Windows authentication:

### Method A: Reset postgres password
1. Open Command Prompt as Administrator
2. Run: net stop postgresql-x64-17
3. Edit: C:\Program Files\PostgreSQL\17\data\pg_hba.conf
4. Change "md5" to "trust" for local connections
5. Run: net start postgresql-x64-17
6. Run: psql -U postgres
7. In psql: ALTER USER postgres PASSWORD 'newpassword';
8. Change pg_hba.conf back to "md5"
9. Restart PostgreSQL

### Method B: Use integrated Windows authentication
1. Edit odoo.conf and set:
   db_user = your_windows_username
   db_password = 
2. Make sure pg_hba.conf allows your Windows user

## Option 3: Continue with remote database
If local setup is complex, we can continue with the remote database
but use command-line initialization instead of web interface.

## What to do next:
1. Choose one of the above options
2. Test connection with: 
   psql -U postgres -d postgres -c "SELECT version();"
3. Start Odoo with the updated configuration
