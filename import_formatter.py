import pandas as pd

def check_excel_columns(input_path):
    """Check what columns are available in the Excel file"""
    df_raw = pd.read_excel(input_path)
    print("📋 Available columns in your Excel file:")
    for i, col in enumerate(df_raw.columns):
        print(f"{i+1:2d}. '{col}'")
    print(f"\n📊 Total rows: {len(df_raw)}")
    print(f"📊 Total columns: {len(df_raw.columns)}")
    return df_raw.columns.tolist()

def transform_partner_excel(input_path, output_path):
    # First, let's check what columns are available
    available_columns = check_excel_columns(input_path)
    
    # Load your raw Excel file
    df_raw = pd.read_excel(input_path)

    # Fill NaNs to avoid string concatenation issues
    df_raw = df_raw.fillna('')
    
    print("\n🔍 First few rows of data:")
    print(df_raw.head())
    
    # We'll create a more flexible mapping based on common column name patterns
    column_mapping = {}
    
    # Try to find the right columns by looking for common patterns
    for col in df_raw.columns:
        col_lower = col.lower().strip()
        if 'party' in col_lower or 'name' in col_lower or 'company' in col_lower:
            column_mapping['name'] = col
        elif 'gstin' in col_lower or 'gst' in col_lower:
            column_mapping['vat'] = col
        elif 'address1' in col_lower or ('address' in col_lower and '1' in col_lower):
            column_mapping['address1'] = col
        elif 'address2' in col_lower or ('address' in col_lower and '2' in col_lower):
            column_mapping['address2'] = col
        elif 'address3' in col_lower or ('address' in col_lower and '3' in col_lower):
            column_mapping['address3'] = col
        elif 'city' in col_lower:
            column_mapping['city'] = col
        elif 'pin' in col_lower or 'zip' in col_lower or 'postal' in col_lower:
            column_mapping['zip'] = col
        elif 'tel' in col_lower or ('phone' in col_lower and 'mobile' not in col_lower):
            column_mapping['phone'] = col
        elif 'mobile' in col_lower:
            column_mapping['mobile'] = col
        elif 'email' in col_lower or 'mail' in col_lower:
            column_mapping['email'] = col
    
    print(f"\n🗺️  Column mapping found:")
    for odoo_field, excel_col in column_mapping.items():
        print(f"  {odoo_field} ← '{excel_col}'")
    
    # Build the transformation dynamically
    transformation_dict = {}
    
    # Name (required)
    if 'name' in column_mapping:
        transformation_dict["name"] = df_raw[column_mapping['name']].astype(str).str.strip()
    else:
        print("❌ Could not find a name/party column!")
        return
    
    # VAT/GSTIN
    if 'vat' in column_mapping:
        transformation_dict["vat"] = df_raw[column_mapping['vat']].astype(str).str.strip()
    
    # Address combination
    address_parts = []
    if 'address1' in column_mapping:
        address_parts.append(df_raw[column_mapping['address1']].astype(str).str.strip())
    if 'address2' in column_mapping:
        address_parts.append(df_raw[column_mapping['address2']].astype(str).str.strip())
    
    if address_parts:
        transformation_dict["street"] = address_parts[0]
        if len(address_parts) > 1:
            transformation_dict["street"] = address_parts[0] + ', ' + address_parts[1]
    
    if 'address3' in column_mapping:
        transformation_dict["street2"] = df_raw[column_mapping['address3']].astype(str).str.strip()
    
    # Other fields
    for field in ['city', 'zip', 'phone', 'mobile', 'email']:
        if field in column_mapping:
            transformation_dict[field] = df_raw[column_mapping[field]].astype(str).str.strip()
    
    # Add required Odoo fields
    transformation_dict["is_company"] = True
    transformation_dict["customer_rank"] = 1  # Mark as customer
    
    # Create DataFrame
    df_transformed = pd.DataFrame(transformation_dict)
    
    # Data validation and cleanup
    print(f"\n🧹 Cleaning data...")
    initial_count = len(df_transformed)
    
    # Remove rows with empty names
    df_transformed = df_transformed[df_transformed['name'].str.strip() != '']
    df_transformed = df_transformed[df_transformed['name'] != 'nan']
    df_transformed = df_transformed[df_transformed['name'].notna()]
    
    # Clean up VAT/GSTIN - remove invalid entries
    if 'vat' in df_transformed.columns:
        df_transformed['vat'] = df_transformed['vat'].replace('nan', '')
        df_transformed['vat'] = df_transformed['vat'].replace('0', '')
        df_transformed.loc[df_transformed['vat'].str.len() < 15, 'vat'] = ''
    
    # Clean up phone numbers - remove invalid entries
    for phone_field in ['phone', 'mobile']:
        if phone_field in df_transformed.columns:
            df_transformed[phone_field] = df_transformed[phone_field].replace('nan', '')
            df_transformed[phone_field] = df_transformed[phone_field].replace('0', '')
    
    # Clean up email - remove invalid entries
    if 'email' in df_transformed.columns:
        df_transformed['email'] = df_transformed['email'].replace('nan', '')
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df_transformed.loc[~df_transformed['email'].str.match(email_pattern, na=False), 'email'] = ''
    
    # Remove duplicate names (keep first occurrence)
    df_transformed = df_transformed.drop_duplicates(subset=['name'], keep='first')
    
    final_count = len(df_transformed)
    print(f"📊 Removed {initial_count - final_count} invalid/duplicate records")
    print(f"📊 Final records to import: {final_count}")
    
    # Show sample of cleaned data
    print(f"\n📋 Sample of cleaned data:")
    print(df_transformed[['name', 'vat', 'city']].head())
    
    # Save to Excel
    df_transformed.to_excel(output_path, index=False)
    print(f"✅ Transformed file saved at: {output_path}")
    
    # Show validation summary
    print(f"\n✅ Validation Summary:")
    print(f"  - Records with names: {final_count}")
    print(f"  - Records with GSTIN: {df_transformed['vat'].str.len().ge(15).sum() if 'vat' in df_transformed.columns else 0}")
    print(f"  - Records with email: {df_transformed['email'].str.len().gt(0).sum() if 'email' in df_transformed.columns else 0}")
    print(f"  - Records with phone: {df_transformed['phone'].str.len().gt(0).sum() if 'phone' in df_transformed.columns else 0}")


# Example usage
input_file = "C:\\Users\\jaina\\Downloads\\KRASIKLAL MASTER DETAIL.XLS"
output_file = "res_partner_transformed.xlsx"
transform_partner_excel(input_file, output_file)
