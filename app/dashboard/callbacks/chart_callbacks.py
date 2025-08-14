from datetime import timedelta
from config.settings import Config
from dash import Input, Output, ctx, html
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

    """Populate the scorecards given selected currencies"""
    @app.callback(
        Output('scorecards-container', 'children'),
        Input('currency-dropdown', 'value')
    )
    def update_scorecards(selected_currencies):
        """Update the scorecards given selected currencies"""
        # time period to generate scorecards for
        time_periods = [(7, 'WoW'), (30, 'MoM'), (365, 'YoY')]
        cards = []

        query_curr_string = ','.join([f"'{currency}'" for currency in selected_currencies])
        query = f"""
        SELECT conversion_date, currency_code, conversion_rate 
        FROM conversion_rates 
        WHERE currency_code in ({query_curr_string})
        ORDER BY conversion_date
        """

        try:
            df = pd.read_sql(query, engine)
        except Exception as e:
            print(f"Error updating scorecards: {e}")
            return html.Div([html.H4("Error loading scorecards")])

        for currency in selected_currencies:
            df_currency = df[df['currency_code'] == currency]

            latest_date = df_currency['conversion_date'].max()
            for period, period_name in time_periods:
                latest_period = df_currency[df_currency['conversion_date'] >= latest_date - timedelta(days=period)]
                prior_period = df_currency[df_currency['conversion_date'].between(latest_date - timedelta(days=period * 2), latest_date - timedelta(days=period))]

                if latest_period.empty or prior_period.empty:
                    continue

                latest_period_avg = latest_period['conversion_rate'].mean()
                prior_period_avg = prior_period['conversion_rate'].mean()

                score = (latest_period_avg - prior_period_avg) / prior_period_avg * 100
                if score > 0:
                    score_color = 'green'
                    score_text = '\u2191'
                elif score < 0:
                    score_color = 'red'
                    score_text = '\u2193'
                else:
                    score_color = 'black'

                cards.append(html.Div([
                    html.H5(f"{currency} - {period_name}"),
                    html.H5(f"{score_text}{abs(score):.2f}%", style={'color': score_color})
                ]))
        return cards


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
