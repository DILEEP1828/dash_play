import dash_html_components as html
import dash_core_components as dcc

def create_plot_layout():
    layout = html.Div([
        dcc.Link('Go back to Upload Page', href='/', style={'marginBottom': '20px', 'display': 'block'}),

        html.Div([ # Row for Time Slider
            html.Label('Time Selector:', style={'marginRight': '10px'}),
            dcc.Slider(
                id='time-slider',
                min=0, # Placeholder, will be updated by callback
                max=100, # Placeholder
                value=50, # Placeholder
                step=1, # Placeholder
                marks=None, # Placeholder, {i: str(i) for i in range(0, 101, 10)}
                tooltip={"placement": "bottom", "always_visible": True},
            )
        ], style={'padding': '20px', 'border': '1px solid #eee', 'borderRadius': '5px', 'marginBottom': '20px'}),

        html.Div([ # Row for Signal Dropdown
            html.Label('Select Signal:', style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='signal-dropdown',
                options=[{'label': 'No signals loaded', 'value': 'none'}], # Placeholder
                value=None, # Placeholder
                style={'width': '100%'}
            )
        ], style={'padding': '20px', 'border': '1px solid #eee', 'borderRadius': '5px', 'marginBottom': '20px'}),

        dcc.Tabs(id="plot-tabs", value='tab-time-series', children=[
            dcc.Tab(label='Time Series Plot', value='tab-time-series', children=[
                dcc.Graph(id='time-series-plot')
            ]),
            dcc.Tab(label='2D Polygon Plot', value='tab-polygon', children=[
                dcc.Graph(id='polygon-plot')
            ]),
        ]),

        # Store for holding the currently selected MF4 file's signal list and time range
        # This could be useful if multiple callbacks need this info and we want to avoid re-parsing MF4
        # For now, plot_callbacks will fetch from mf4_file_for_plotting_store directly
        # dcc.Store(id='current-mf4-metadata-store')
    ])
    return layout
