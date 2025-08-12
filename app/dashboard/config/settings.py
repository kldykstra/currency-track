import os
from datetime import datetime, timedelta

class Config:
    """Configuration settings for the dashboard"""

    # Date range options and mapping
    DATE_RANGE_OPTIONS = [
        (7, '7 Days'),
        (30, '1 Month'),
        (180, '6 Months'),
        (365, '1 Year'),
        (365 * 5, '5 Years'),
        (365 * 100, 'All Time')
    ]

    # Database settings
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "currency-track-database")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "currency_tracker")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
    
    # App settings
    DEBUG_MODE = os.environ.get("DASH_DEBUG_MODE", "false").lower() == "true"
    HOST = "0.0.0.0"
    PORT = 8050
    
    # Chart settings
    DEFAULT_CURRENCY = "USD"
