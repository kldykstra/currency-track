from datetime import timedelta
from config.settings import Config
from dash import Input, Output, ctx, html
import plotly.express as px
import pandas as pd
from sqlalchemy import text

def register_chart_callbacks(app, engine):
    """Register all chart-related callbacks"""

    # Find the default days value (30 days)
    DEFAULT_DAYS = 30

    """Update date range filter depending on which button is clicked"""
    @app.callback(
        [Output('date-range-filter', 'data'),
         Output('current-selection', 'data')],
        [Input(f'btn-{days}', 'n_clicks') for days, _ in Config.DATE_RANGE_OPTIONS]
    )
    def update_date_range(*n_clicks):
        if ctx.triggered_id is not None:
            # Extract the days value from the button ID (e.g., 'btn-30' -> 30)
            days = int(ctx.triggered_id.split('-')[1])
            return days, days
        return DEFAULT_DAYS, DEFAULT_DAYS

    """Update button styles depending on which button is clicked"""
    @app.callback(
        [Output(f'btn-{days}', 'className') for days, _ in Config.DATE_RANGE_OPTIONS],
        Input('current-selection', 'data')
    )
    def update_button_styles(selected_value):
        button_classes = []
        for days, _ in Config.DATE_RANGE_OPTIONS:
            if days == selected_value:
                button_classes.append('btn btn-primary')
            else:
                button_classes.append('btn btn-light')
        return button_classes

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

            # Enclose each card (currency and its scorecards) in an outline box with rounded corners
            card_children = [
                html.H3(f"{currency}", 
                    style={
                        'display': 'inline-block',
                        'vertical-align': 'center',
                        'padding': '10px',
                        'margin': '10px',
                        'font-weight': 'bold',
                        'position': 'relative',
                        'top': '-8px'
                    })
            ]

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
                    score_text = ''

                card_children.append(
                    html.Div([
                        html.H5(f"{period_name}"),
                        html.H5(f"{score_text}{abs(score):.2f}%", style={'color': score_color})
                    ], style={
                        'display': 'inline-block',
                        'width': '100px',
                        'text-align': 'center',
                        'border': '0px solid black',
                        'padding': '10px',
                        'margin': '10px',
                        'border-radius': '8px',
                        'background': '#f8f9fa'
                    })
                )
            # Wrap the card_children in a shadow box with rounded corners
            cards.append(
                html.Div(
                    card_children,
                    style={
                        'border-radius': '12px',
                        'padding': '20px',
                        'margin': '15px',
                        'display': 'inline-block',
                        'vertical-align': 'top',
                        'background': '#f5f7fa',
                        'box-shadow': '0 2px 8px rgba(0,0,0,0.04)'
                    }
                )
            )
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

            # Add a title to the chart
            fig.update_layout(title=f"Conversion Rate from Eur to Selected Currencies (Higher value = stronger Euro)")
            # Add an info icon popover to the title
            fig.update_layout(
                title_x=0.5,
                title_y=0.95,
                title_font_size=20,
                title_font_color='#2c3e50',
                title_font_family='Lato, "Helvetica Neue", Arial, Helvetica, sans-serif'
            )
            # Add a tooltip to the chart
            fig.update_layout(
                hovermode='x unified',
                hoverlabel=dict(bgcolor='white', font_size=12, font_family='Lato, "Helvetica Neue", Arial, Helvetica, sans-serif'),
                hoverlabel_bgcolor='white',
                hoverlabel_font_size=12,
                hoverlabel_font_family='Lato, "Helvetica Neue", Arial, Helvetica, sans-serif'
            )
            
            # Update the axis labels
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Conversion Rate')
            
            # Update the legend
            fig.update_layout(legend_title_text='Currency')
            
            return fig
            
        except Exception as e:
            print(f"Error updating chart: {e}")
            return px.line(title='Error loading chart data')
