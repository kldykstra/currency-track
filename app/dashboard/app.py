import dash
from dash import dcc, html

# Import our modular components
from config.settings import Config
from database.db_manager import DatabaseManager
from layouts.main_layout import create_main_layout
from callbacks.chart_callbacks import register_chart_callbacks

def create_app(config):
    """Create and configure the Dash application"""
    
    # Initialize the app
    app = dash.Dash(
        __name__, 
        suppress_callback_exceptions=True,
        title="Currency Tracker Dashboard",
        external_stylesheets=[
            "https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/flatly/bootstrap.min.css"
            ,"https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
        ]
    )
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Wait for database to be ready
    if not db_manager.wait_for_database():
        print("Warning: Database connection failed, app may not work properly")
    
    # Set the layout
    app.layout = create_main_layout()
    
    # Register chart callbacks only
    engine = db_manager.get_engine()
    register_chart_callbacks(app, engine)
    
    return app

def main():
    """Main entry point for the application"""

    # Initialize the config
    config = Config()

    app = create_app(config)
    
    # Run the app
    app.run(
        debug=config.DEBUG_MODE,
        host=config.HOST,
        port=config.PORT,
        dev_tools_hot_reload=config.DEBUG_MODE,
        dev_tools_ui=config.DEBUG_MODE
    )
if __name__ == '__main__':
    main()

