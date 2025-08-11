import os
from datetime import datetime, timedelta

class Config:
    """Configuration settings for the dashboard"""

    # Set class variables directly on Config, not using self or __init__
    # Generate date range options at class definition time
    @staticmethod
    def _get_date_range_options():
        """Generate date range options for the dropdown.
        
        Options are in the format "'YYYY-MM-DD' to 'YYYY-MM-DD' (X days)".
        """
        days_to_label = [
            7,
            30,
            90,
            180,
            365
        ]
        today = datetime.now()
        options = []
        for days in days_to_label:
            start_date = today - timedelta(days=days)
            end_date = today
            dropdown_label = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({days} days)"
            options.append({'label': dropdown_label, 'value': days})

        return options

    # Date range options and mapping
    DATE_RANGE_OPTIONS = _get_date_range_options.__func__()

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
