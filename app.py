import dash
import dash_html_components as html

app = dash.Dash(__name__) # Dash will automatically serve files from an 'assets' folder

app.layout = html.Div([ # This Div is targeted by '#_dash-app-content > div'
    html.Header([ # Targeted by 'header' tag selector
        html.Button('X', id='close-button'), # Targeted by 'header button' selector
        html.H1('File Upload'), # Targeted by 'header h1' selector
        html.Button('☰', id='menu-button'), # Targeted by 'header button' selector
    ]),

    html.Div(id='file-upload-container', children=[
        # JSON Section
        html.Div(id='json-section', className='file-section', children=[
            html.Div(className='phone-screen', children=[
                html.Div("Cloud Icon + X", className='icon-placeholder')
            ]),
            html.Button('UPLOAD', id='upload-json-button', className='upload-button'),
            html.Div(className='dots-row', children=[
                html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot')
            ]),
            html.Button('Json', id='json-type-button', className='file-type-button'),
        ]),

        # CSV Section
        html.Div(id='csv-section', className='file-section', children=[
            html.Div(className='phone-screen', children=[
                html.Div("List Icon", className='icon-placeholder')
            ]),
            html.Button('UPLOAD', id='upload-csv-button', className='upload-button'),
            html.Div(className='dots-row', children=[
                html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot')
            ]),
            html.Button('CSV', id='csv-type-button', className='file-type-button'),
        ]),

        # Excel Section
        html.Div(id='excel-section', className='file-section', children=[
            html.Div(className='phone-screen', children=[
                html.Div("Document Icon", className='icon-placeholder')
            ]),
            html.Button('UPLOAD', id='upload-excel-button', className='upload-button'),
            html.Div(className='dots-row', children=[
                html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot'), html.Span(className='dot')
            ]),
            html.Button('Excel', id='excel-type-button', className='file-type-button'),
        ]),
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'padding': '20px'}), # Style for the container
])

if __name__ == '__main__':
    app.run_server(debug=True)
