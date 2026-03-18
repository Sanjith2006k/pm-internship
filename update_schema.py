"""
Update schema to replace gst_number with cin_number
"""
import sqlite3
import os

db_path = 'instance/database.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if gst_number column exists
        cursor.execute("PRAGMA table_info(organization)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'gst_number' in column_names:
            # Rename gst_number to cin_number
            cursor.execute("ALTER TABLE organization RENAME COLUMN gst_number TO cin_number")
            print("✓ Successfully renamed gst_number to cin_number")
        elif 'cin_number' in column_names:
            print("✓ Column cin_number already exists")
        else:
            # Add cin_number column if it doesn't exist
            cursor.execute("ALTER TABLE organization ADD COLUMN cin_number VARCHAR(100)")
            print("✓ Successfully added cin_number column")
        
        conn.commit()
        print("✓ Database schema updated successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print("Database file not found. It will be created on next app run.")
