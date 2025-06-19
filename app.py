import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Import layout creation functions
from gui.layout import create_layout as create_upload_layout # Renamed for clarity
from gui.plot_layout import create_plot_layout

# Import callback registration functions
from backend.callbacks import register_callbacks as register_main_callbacks
from backend.plot_callbacks import register_plot_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True) # suppress_callback_exceptions is important for multi-page apps with callbacks in different files

# Define the main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), # Component to track and update the URL
    html.Div(id='page-content')            # Container where page content will be rendered
])

# Callback to update page content based on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/plot':
        return create_plot_layout()
    # Default to upload layout for root or any other path
    # Can add more specific routing here if needed (e.g. 404 page)
    else:
        return create_upload_layout()

# Register callbacks for the main upload page
register_main_callbacks(app)

# Register callbacks for the plot page
register_plot_callbacks(app)

# Add the main execution block
if __name__ == '__main__':
    app.run_server(debug=True)
