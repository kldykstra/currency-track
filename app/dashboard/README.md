# Dashboard Code Organization

This dashboard follows best practices for organizing Plotly Dash applications by separating concerns into modular components.

## Directory Structure

```
dashboard/
├── app_new.py              # Main application entry point
├── app.py                  # Original single-file app (kept for reference)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── config/                # Configuration and settings
│   ├── __init__.py
│   └── settings.py        # App configuration and constants
├── database/              # Database management
│   ├── __init__.py
│   └── db_manager.py      # Database connection and utilities
├── layouts/               # UI layout components
│   ├── __init__.py
│   └── main_layout.py     # Main dashboard layout
├── callbacks/             # Dash callbacks (interactivity)
│   ├── __init__.py
│   ├── chart_callbacks.py # Chart update callbacks
│   └── data_callbacks.py  # Data loading callbacks
└── assets/                # Static assets (CSS, JS, images)
```

## Benefits of This Structure

1. **Separation of Concerns**: Each file has a single responsibility
2. **Maintainability**: Easier to find and fix issues
3. **Scalability**: Easy to add new features without cluttering main files
4. **Reusability**: Components can be reused across different parts of the app
5. **Testing**: Easier to write unit tests for individual components
6. **Team Development**: Multiple developers can work on different components simultaneously

## Key Components

### `app_new.py`
- Main entry point that orchestrates all components
- Creates the Dash app instance
- Registers all callbacks
- Sets up the layout

### `config/settings.py`
- Centralized configuration management
- Environment variable handling
- Constants and default values

### `database/db_manager.py`
- Database connection management
- Connection retry logic
- Connection testing utilities

### `layouts/main_layout.py`
- UI layout definition
- Component styling
- Responsive design considerations

### `callbacks/`
- **chart_callbacks.py**: Handles chart updates and interactions
- **data_callbacks.py**: Manages data loading and dropdown population

## Development Workflow

1. **Layout Changes**: Modify files in `layouts/`
2. **New Features**: Add new callback files in `callbacks/`
3. **Configuration**: Update `config/settings.py`
4. **Database**: Modify `database/db_manager.py`
5. **Main App**: Update `app_new.py` for major structural changes

## Running the App

### Development (with hot-reloading)
```bash
cd app
./dev.sh
```

### Production
```bash
cd app
docker-compose up --build
```

## Adding New Features

1. **New Layout Component**: Create new file in `layouts/`
2. **New Callback**: Add to appropriate file in `callbacks/`
3. **New Configuration**: Extend `config/settings.py`
4. **Register**: Update `app_new.py` to use new components

This structure makes the codebase much more maintainable and follows industry best practices for Dash applications.
