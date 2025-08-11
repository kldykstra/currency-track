import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.engine = None
        self._setup_connection()
    
    def _setup_connection(self):
        """Setup database connection with retry logic"""
        # Use Docker service name for database connection
        db_host = os.environ.get("POSTGRES_HOST", "currency-track-database")
        db_port = os.environ.get("POSTGRES_PORT", "5432")
        db_name = os.environ.get("POSTGRES_DB", "currency_tracker")
        db_user = os.environ.get("POSTGRES_USER", "postgres")
        db_pass = os.environ.get("POSTGRES_PASSWORD", "password")
        
        print(f"Connecting to database: {db_host}:{db_port}/{db_name}")
        
        connection_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        self.engine = create_engine(connection_string)
    
    def wait_for_database(self, max_retries=30, delay=2):
        """Wait for database to be ready"""
        for attempt in range(max_retries):
            try:
                with self.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    print("Database connection successful!")
                    return True
            except OperationalError as e:
                print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    print("Failed to connect to database after all retries")
                    return False
        return False
    
    def get_engine(self):
        """Get the database engine"""
        return self.engine
    
    def test_connection(self):
        """Test if database connection is working"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
