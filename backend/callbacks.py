import dash
from dash.dependencies import Input, Output, State # State is used by validation callbacks
import dash_html_components as html

def parse_contents_and_filenames(list_of_contents, list_of_filenames):
    if list_of_contents is None or list_of_filenames is None:
        return [], []
    if not isinstance(list_of_contents, list):
        list_of_contents = [list_of_contents]
    if not isinstance(list_of_filenames, list):
        list_of_filenames = [list_of_filenames]
    return list_of_contents, list_of_filenames

def register_callbacks(app):
    @app.callback(
        Output('pickle-output', 'children'),
        [Input('upload-pickle', 'contents')],
        [State('upload-pickle', 'filename')]
    )
    def validate_pickle_upload(list_of_contents, list_of_filenames):
        contents, filenames = parse_contents_and_filenames(list_of_contents, list_of_filenames)
        messages = []
        if not contents:
            return html.Div(messages)
        for content, filename in zip(contents, filenames):
            if filename and (filename.endswith('.pkl') or filename.endswith('.pickle')):
                messages.append(html.P(f"File '{filename}': Valid Pickle format detected.", style={'color': 'green', 'marginBottom': '5px'}))
            else:
                messages.append(html.P(f"File '{filename}': Invalid file type. Please upload a .pkl or .pickle file.", style={'color': 'red', 'marginBottom': '5px'}))
        return html.Div(messages)

    @app.callback(
        [Output('mf4-output', 'children'), Output('mf4_file_for_plotting_store', 'data')], # Updated Output
        [Input('upload-mf4', 'contents')],
        [State('upload-mf4', 'filename')]
    )
    def validate_mf4_upload(list_of_contents, list_of_filenames):
        contents, filenames = parse_contents_and_filenames(list_of_contents, list_of_filenames)
        messages = []
        stored_mf4_for_plotting = None # Will store data for the first valid mf4 file

        if not contents:
            return html.Div(messages), stored_mf4_for_plotting

        for content, filename in zip(contents, filenames):
            if filename and filename.endswith('.mf4'):
                messages.append(html.P(f"File '{filename}': Valid MF4 format detected.", style={'color': 'green', 'marginBottom': '5px'}))
                if stored_mf4_for_plotting is None: # Store only the first valid one
                    stored_mf4_for_plotting = {'filename': filename, 'contents': content}
            else:
                messages.append(html.P(f"File '{filename}': Invalid file type. Please upload an .mf4 file.", style={'color': 'red', 'marginBottom': '5px'}))

        return html.Div(messages), stored_mf4_for_plotting

    @app.callback(
        [Output('url', 'pathname', allow_duplicate=True), Output('submit-status-output', 'children')], # Updated Output
        [Input('global-submit-button', 'n_clicks')],
        prevent_initial_call=True # Applied to the callback itself
    )
    def handle_global_submit(n_clicks):
        # n_clicks will be 1 or more due to prevent_initial_call=True
        # The (n_clicks is None or n_clicks == 0) check is technically redundant here
        # but kept for clarity if prevent_initial_call were removed or changed.
        if n_clicks is None or n_clicks == 0:
            return dash.no_update, ""

        # Navigate to plot page and update status
        return "/plot", "Navigating to plot page..."
