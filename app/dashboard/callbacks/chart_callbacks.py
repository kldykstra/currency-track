from config.settings import Config
from dash import Input, Output, ctx
import plotly.express as px
import pandas as pd
from sqlalchemy import text

def register_chart_callbacks(app, engine):
    """Register all chart-related callbacks"""

    buttons = [f'btn{i+1}' for i in range(len(Config.DATE_RANGE_OPTIONS))]
    button_inputs = [Input(button, 'n_clicks') for button in buttons]

    """Update date range filter depending on which button is clicked"""
    @app.callback(
        Output('date-range-filter', 'data'),
        *button_inputs
    )
    def update_date_range(*n_clicks):
        if ctx.triggered_id is not None:
            for i, button in enumerate(buttons):
                if ctx.triggered_id == button:
                    return Config.DATE_RANGE_OPTIONS[i][0]
        return Config.DATE_RANGE_OPTIONS[-1][0]

    """Populate the timeseries chart given selected currencies and date range"""
    @app.callback(
        Output('chart', 'figure'),
        Input('currency-dropdown', 'value'),
        Input('date-range-filter', 'data')
    )
    def update_chart(selected_currencies, selected_date_range):
        """Update the chart based on selected currencies and date range"""
        
        # Handle date range
        date_filter = f">= CURRENT_DATE - INTERVAL '{selected_date_range} days'"
        
        # Handle multiple selections
        currencies = "', '".join(selected_currencies)
        query = f"""
        SELECT conversion_date, currency_code, conversion_rate 
        FROM conversion_rates 
        WHERE currency_code IN ('{currencies}')
        AND conversion_date {date_filter}
        ORDER BY conversion_date
        """
        
        try:
            df = pd.read_sql(query, engine)
            
            if df.empty:
                return px.line(title='No data available for selected criteria')
            
            fig = px.line(df, x='conversion_date', y='conversion_rate', color='currency_code')
            
            # Update the axis labels
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Conversion Rate')
            
            # Update the legend
            fig.update_layout(legend_title_text='Currency')
            
            return fig
            
        except Exception as e:
            print(f"Error updating chart: {e}")
            return px.line(title='Error loading chart data')
