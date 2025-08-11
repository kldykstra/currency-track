from config.settings import Config
from dash import html, dcc
from database.db_manager import DatabaseManager
from sqlalchemy import text

def get_currency_options():
    """Get currency options directly from database"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        engine = db_manager.get_engine()
        
        query = """
        SELECT DISTINCT currency_code
        FROM conversion_rates
        WHERE conversion_date >= CURRENT_DATE - INTERVAL '60 days'
        ORDER BY currency_code
        """
        
        with engine.connect() as connection:
            raw_results = connection.execute(text(query))
            results = [r[0] for r in raw_results.fetchall()]
        
        currency_options = [{'label': currency, 'value': currency} for currency in sorted(results)]
        print(f"Found {len(currency_options)} currency options")
        return currency_options
        
    except Exception as e:
        print(f"Error getting currency options: {e}")
        return []

def create_main_layout():
    """Create the main layout for the dashboard"""
    # Get currency options once when creating layout
    currency_options = get_currency_options()
    
    return html.Div([
        # Header
        html.H1('Euro Conversion Rates', style={'textAlign': 'center'}),
        
        # Description
        html.P('Select currencies to compare their conversion rates to EUR'),
        
        # Controls section
        html.Div([
            # Date range dropdown
            html.Div([
                html.Label('Date Range:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='date-range-dropdown',
                    options=Config.DATE_RANGE_OPTIONS,
                    placeholder='Select date range',
                    style={'width': '100%'}
                )
            ], style={'width': '25%', 'display': 'inline-block', 'marginRight': '20px'}),
            
            # Currency dropdown
            html.Div([
                html.Label('Currencies:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='currency-dropdown',
                    options=currency_options,  # Static options from database
                    value=['USD'],
                    multi=True,
                    placeholder='Select currencies',
                    style={'width': '100%'}
                )
            ], style={'width': '50%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        
        # Chart
        dcc.Graph(id='chart')
    ])
