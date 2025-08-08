import os
from datetime import datetime, timedelta

import dash
from dash import dcc, html, Input, Output
import numpy as np
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text

app = dash.Dash(__name__)

DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ.get("POSTGRES_DB", "mydatabase")
DB_USER = os.environ.get("POSTGRES_USER", "myuser")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "mypassword")
print(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS)
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def get_currency_options():
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
    return currency_options

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
