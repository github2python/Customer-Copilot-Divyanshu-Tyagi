"""
SQLite compatibility fix for Streamlit Cloud deployment.
This must be imported before chromadb to fix SQLite version issues.
"""

import sys
import os

def fix_sqlite():
    """Fix SQLite compatibility for ChromaDB on Streamlit Cloud."""
    try:
        import pysqlite3
        sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
        print("✅ SQLite compatibility fix applied successfully")
    except ImportError:
        print("⚠️  pysqlite3 not available, using system SQLite")
        pass

# Apply the fix when this module is imported
fix_sqlite()
