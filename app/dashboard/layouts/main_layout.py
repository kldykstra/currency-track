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

    """Generate a button for each date range option"""
    buttons = []
    for i, (days, label) in enumerate(Config.DATE_RANGE_OPTIONS):
        buttons.append(html.Button(label, id=f'btn{i+1}', n_clicks=0, style={'marginRight': '10px'}, className='btn btn-primary'))
    
    return html.Div([
        # Header
        html.H1('Euro Conversion Rates', style={'textAlign': 'center'}),
        
        # Controls section
        html.Div([
            # Currency dropdown
            html.Div([
                html.Label('Currencies:', style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='currency-dropdown',
                    options=currency_options,  # Static options from database
                    value=[Config.DEFAULT_CURRENCY],
                    multi=True,
                    placeholder='Select currencies',
                    style={'width': '100%'}
                )
            ], style={'width': '50%', 'display': 'inline-block', 'marginLeft': '60px'})
        ], style={'marginBottom': '20px'}),
        # Date range buttons
        html.Div([
            *buttons,
        ], style={'width': '50%', 'display': 'inline-block', 'marginLeft': '60px'}),
        dcc.Store(id='date-range-filter'),
        
        # Chart
        dcc.Graph(id='chart')
    ])
