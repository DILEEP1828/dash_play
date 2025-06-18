import dash_html_components as html
import dash_core_components as dcc # Make sure dcc is imported

def create_layout():
    layout = html.Div([
        # dcc.Store components for pickle-file-store and mf4-file-store REMOVED

        html.Header([
            html.Button('X', id='close-button'),
            html.H1('File Upload'),
            html.Button('☰', id='menu-button'),
        ]),

        html.Div(id='file-upload-container', children=[
            # Pickle Section
            html.Div(id='pickle-section', className='file-section', children=[
                html.Div(className='phone-screen', children=[
                    html.Div("Pickle Icon Placeholder", className='icon-placeholder')
                ]),
                dcc.Upload(
                    id='upload-pickle',
                    children=html.Div([ # Keep the child Div for better styling control from CSS
                        'Drag and Drop or ',
                        html.A('Select Pickle Files') # Changed text
                    ]),
                    className='custom-upload-component', # New class for styling via CSS
                    multiple=True # Changed to True
                ),
                html.Div(id='pickle-output', className='output-message-div'), # For validation messages
                html.Div(className='dots-row', children=[
                    html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot')
                ]),
                html.Button('Pickle', id='pickle-type-button', className='file-type-button'),
            ]),

            # MF4 Section
            html.Div(id='mf4-section', className='file-section', children=[
                html.Div(className='phone-screen', children=[
                    html.Div("MF4 Icon Placeholder", className='icon-placeholder')
                ]),
                dcc.Upload(
                    id='upload-mf4',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select MF4 Files') # Changed text
                    ]),
                    className='custom-upload-component', # New class for styling via CSS
                    multiple=True # Changed to True
                ),
                html.Div(id='mf4-output', className='output-message-div'), # For validation messages
                html.Div(className='dots-row', children=[
                    html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot')
                ]),
                html.Button('MF4', id='mf4-type-button', className='file-type-button'),
            ]),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}),

        # New Submit Button Area
        html.Div(id='submit-button-container', children=[
            html.Button('Submit', id='global-submit-button')
        ]),

        html.Div(id='submit-status-output', style={'marginTop': '10px'})
        # ... (remains unchanged) ...

        # html.Div(id='mf4-data-display-area') REMOVED
    ])
    return layout
