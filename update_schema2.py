"""
Update schema to add registration_cert_path column
"""
import sqlite3
import os

db_path = 'instance/database.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if registration_cert_path column exists
        cursor.execute("PRAGMA table_info(organization)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'registration_cert_path' not in column_names:
            # Add registration_cert_path column
            cursor.execute("ALTER TABLE organization ADD COLUMN registration_cert_path VARCHAR(400)")
            print("✓ Successfully added registration_cert_path column")
        else:
            print("✓ Column registration_cert_path already exists")
        
        conn.commit()
        print("✓ Database schema updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("Database file not found. It will be created on next app run.")
