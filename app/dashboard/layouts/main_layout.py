import dash_bootstrap_components as dbc
from config.settings import Config
from dash import html, dcc
from database.db_manager import DatabaseManager
from sqlalchemy import text

INFO_HEADER = 'Source: European Central Bank'
INFO_TEXT = 'Conversion rate data as provided by the European Central Bank (ECB). ' + \
'Historical time periods are relative to the latest published date.'

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
    # spacing to keep to the left of page elements
    SIDE_MARGIN = '20px'
    # define horizontal divider style (resused)
    HORIZONTAL_DIVIDER = {
        'border': 'none',
        'borderTop': '2px solid #dee2e6',
        'margin': '20px 0',
        'width': '100%'
    }

    """Generate radio buttons for date range selection"""
    date_range_radio = dbc.ButtonGroup([
        dbc.Button(
            label,
            id=f'btn-{days}',
            n_clicks=1 if label.upper() == "1 Month" else 0
        ) for days, label in Config.DATE_RANGE_OPTIONS
    ], id='date-range-radio-group')

    return html.Div([
        # Enclose header in a div with a border
        html.Div([
            # Header
            html.H1(
                'Euro Conversion Rates',
                style={'textAlign': 'Left', 'color': 'white',
                       'borderRadius': '5px', 'display': 'inline-block', 'padding': '20px'}),
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
                    'top': '-4px',  # Adjust this value as needed to center vertically
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
        ], style={'backgroundColor': 'var(--bs-primary)', 'marginLeft': f'-{SIDE_MARGIN}', 'marginRight': f'-{SIDE_MARGIN}'}),
        
        # Currency selection section
        html.Div([
            # Currency dropdown
            html.Div([
                html.H4('Currencies:',
                className='mb-2',
                style={
                    'display': 'inline-block',
                    'marginBottom': '20px',
                    'marginTop': '20px'
                }),
                html.Div(
                    dcc.Dropdown(
                        id='currency-dropdown',
                        options=currency_options,  # Static options from database
                        value=[Config.DEFAULT_CURRENCY],
                        multi=True,
                        placeholder='Select currencies',
                        style={'width': '250px', 'marginLeft': '10px'}
                    ),
                    className='mb-2',
                    style={'display': 'inline-block', 'verticalAlign': 'middle'}
                )
            ])
        ]),
        # horizontal divider
        html.Hr(style=HORIZONTAL_DIVIDER),
        html.Div([
            html.H4("Scorecards", style={'marginBottom': '20px'}),
            html.Div(id="scorecards-container", style={"display": "flex", "flexWrap": "wrap", "marginBottom": "20px"})
        ]),
        # horizontal divider
        html.Hr(style=HORIZONTAL_DIVIDER),
        # Date range selection section
        html.Div([
            html.H4('Date Range:', style={'display': 'inline-block', 'marginRight': '10px'}),
            date_range_radio,
            dcc.Store(id='date-range-filter'),
            dcc.Store(id='current-selection')
        ], style={'marginBottom': '20px'}),
        
        # Chart
        dcc.Graph(id='chart')
    ], style={'marginLeft': SIDE_MARGIN, 'marginRight': SIDE_MARGIN})
