import os
import time
from datetime import datetime, timedelta

import dash
from dash import dcc, html, Input, Output
import numpy as np
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

app = dash.Dash(__name__)

# Use Docker service name for database connection
DB_HOST = os.environ.get("POSTGRES_HOST", "currency-track-database")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ.get("POSTGRES_DB", "currency_tracker")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "password")
print(f"Connecting to database: {DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create engine with retry logic
def create_db_engine():
    return create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

engine = create_db_engine()

def wait_for_database(max_retries=30, delay=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
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

# Wait for database on startup
if not wait_for_database():
    print("Warning: Database connection failed, app may not work properly")

def get_currency_options():
    try:
        query = """
        SELECT DISTINCT currency_code
        FROM conversion_rates
        WHERE conversion_date >= CURRENT_DATE - INTERVAL '60 days'
        """
        # get query results as a list
        with engine.connect() as connection:
            raw_results = connection.execute(text(query))
            results = [r[0] for r in raw_results.fetchall()]
        currency_options = [{'label': currency, 'value': currency} for currency in sorted(results)]
        print(f"Found {len(currency_options)} currency options")
        return currency_options
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return []

@app.callback(
    Output('chart', 'figure'),
    Input('currency-dropdown', 'value')
)
def update_chart(selected_currencies):
    if not selected_currencies:
        return px.line(title='Select currencies')
    
    # Handle multiple selections
    currencies = "', '".join(selected_currencies)
    query = f"""
    SELECT conversion_date, currency_code, conversion_rate 
    FROM conversion_rates 
    WHERE currency_code IN ('{currencies}')
    ORDER BY conversion_date
    """
    df = pd.read_sql(query, engine)
    
    fig = px.line(df, x='conversion_date', y='conversion_rate', color='currency_code', 
                  title='Multiple Currency Comparison')
    return fig

app.layout = html.Div([
    dcc.Dropdown(
        id='currency-dropdown',
        options=get_currency_options(),
        multi=True,
        placeholder='Select currencies'
    ),
    dcc.Graph(id='chart')
])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
