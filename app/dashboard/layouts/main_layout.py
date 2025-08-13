import dash_bootstrap_components as dbc
from config.settings import Config
from dash import html, dcc
from database.db_manager import DatabaseManager
from sqlalchemy import text

INFO_HEADER = 'Source: European Central Bank'
INFO_TEXT = 'Conversion rate data as provided by the European Central Bank (ECB).' + \
'Historical time periods are relative to the latest available data.'

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
        # Enclose header in a div with a border
        html.Div([
            # Header
            html.H1(
                'Euro Conversion Rates',
                style={'textAlign': 'Left', 'color': 'white',
                       'padding': '10px', 'borderRadius': '5px', 'marginLeft': '60px', 'display': 'inline-block'}),
            # Info icon popover
            html.I(
                className='bi bi-info-circle',
                id='info-icon',
                style={
                    'color': 'white',
                    'fontSize': '1.5em',
                    'display': 'inline-block',
                    'marginLeft': '10px',
                    'position': 'relative',
                    'top': '-6px',  # Adjust this value as needed to center vertically
                }
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader(INFO_HEADER),
                    dbc.PopoverBody(INFO_TEXT),
                ],
                id='popover',
                is_open=False,
                target='info-icon',
                placement='right',
                trigger='hover'

            )
        ], style={'backgroundColor': 'var(--bs-primary)'}),
        
        # Controls section
        html.Div([
            # Currency dropdown
            html.Div([
                html.H4('Currencies:',
                className='mb-2',
                style={
                    'display': 'inline-block',
                    'marginRight': '10px',
                    'margin': '20px'
                }),
                html.Div(
                    dcc.Dropdown(
                        id='currency-dropdown',
                        options=currency_options,  # Static options from database
                        value=[Config.DEFAULT_CURRENCY],
                        multi=True,
                        placeholder='Select currencies',
                        style={'width': '250px'}
                    ),
                    className='mb-2',
                    style={'display': 'inline-block', 'verticalAlign': 'middle'}
                )
            ], style={'marginLeft': '60px', 'marginBottom': '20px'}),
        # Date range buttons
        html.Div([
            *buttons,
        ], style={'width': '50%', 'display': 'inline-block', 'marginLeft': '60px'}),
        dcc.Store(id='date-range-filter'),
        ]),
        
        # Chart
        dcc.Graph(id='chart')
    ])
