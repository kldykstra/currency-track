import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "currency_tracker"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )

def test_connection():
    """Test PostgreSQL connection"""
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"Connected to PostgreSQL: {version['version']}")
            
            # Test table access
            cur.execute("SELECT COUNT(*) FROM currency_rates;")
            count = cur.fetchone()
            print(f"Found {count['count']} records in currency_rates table")
            
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting upload container...")
    test_connection() 