import dash
from gui.layout import create_layout
from backend.callbacks import register_callbacks

# Initialize the Dash app
# suppress_callback_exceptions=True is important as callbacks are defined in another file
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Set the app's layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Add the main execution block
if __name__ == '__main__':
    app.run_server(debug=True)
