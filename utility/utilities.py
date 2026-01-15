from config.config import app , db
import os

# Helper function to get database type from environment or config
def get_db_type():
    """Gets database type from environment variable or app config"""
    # First try environment variable (available at import time)
    db_type = os.getenv("DB_TYPE", "").upper()
    if db_type in ("MYSQL", "MSSQL"):
        return db_type
    # Fallback to app config if available
    try:
        db_type = app.config.get("DB_TYPE", "MSSQL")
        return db_type.upper() if isinstance(db_type, str) else "MSSQL"
    except (RuntimeError, AttributeError):
        # Default to MSSQL if app context not available
        return "MSSQL"

# Helper function to get table args based on database type
def get_table_args():
    """Returns table arguments based on database type (MySQL doesn't support schemas)"""
    db_type = get_db_type()
    if db_type == "MYSQL":
        return {}  # MySQL doesn't support schemas or implicit_returning
    else:
        return {"schema": "CW2", 'implicit_returning': False}

# Helper function to get foreign key reference based on database type
def fk_ref(table_name, column_name):
    """Returns foreign key reference with or without schema prefix based on DB_TYPE"""
    db_type = get_db_type()
    if db_type == "MYSQL":
        return f"{table_name}.{column_name}"
    else:
        return f"CW2.{table_name}.{column_name}"

# Helper function to get default timestamp function based on database type
def get_timestamp_default():
    """Returns appropriate timestamp default function based on database type"""
    db_type = get_db_type()
    if db_type == "MYSQL":
        return db.func.now()
    else:
        return db.func.sysdatetime()