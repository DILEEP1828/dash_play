import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
# Unused imports will be removed based on the subtask description.

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
        Output('pickle-output', 'children'), # Changed
        [Input('upload-pickle', 'contents')],
        [State('upload-pickle', 'filename')]
    )
    def validate_pickle_upload(list_of_contents, list_of_filenames):
        contents, filenames = parse_contents_and_filenames(list_of_contents, list_of_filenames)
        messages = []
        # stored_pickle_data logic removed
        if not contents:
            return html.Div(messages) # Changed
        for content, filename in zip(contents, filenames):
            if filename and (filename.endswith('.pkl') or filename.endswith('.pickle')):
                messages.append(html.P(f"File '{filename}': Valid Pickle format detected.", style={'color': 'green', 'marginBottom': '5px'}))
                # Logic for storing in stored_pickle_data removed
            else:
                messages.append(html.P(f"File '{filename}': Invalid file type. Please upload a .pkl or .pickle file.", style={'color': 'red', 'marginBottom': '5px'}))
        return html.Div(messages) # Changed

    @app.callback(
        Output('mf4-output', 'children'), # Changed
        [Input('upload-mf4', 'contents')],
        [State('upload-mf4', 'filename')]
    )
    def validate_mf4_upload(list_of_contents, list_of_filenames):
        contents, filenames = parse_contents_and_filenames(list_of_contents, list_of_filenames)
        messages = []
        # stored_mf4_data logic removed
        if not contents:
            return html.Div(messages) # Changed
        for content, filename in zip(contents, filenames):
            if filename and filename.endswith('.mf4'):
                messages.append(html.P(f"File '{filename}': Valid MF4 format detected.", style={'color': 'green', 'marginBottom': '5px'}))
                # Logic for appending to stored_mf4_data removed
            else:
                messages.append(html.P(f"File '{filename}': Invalid file type. Please upload an .mf4 file.", style={'color': 'red', 'marginBottom': '5px'}))
        return html.Div(messages) # Changed

    @app.callback(
        Output('submit-status-output', 'children'), # Reverted to single output
        [Input('global-submit-button', 'n_clicks')]
        # Removed State for pickle-file-store and mf4-file-store
    )
    def handle_global_submit(n_clicks): # Removed pickle_data, mf4_data from parameters
        if n_clicks is None or n_clicks == 0:
            return ""

        # Reverted to simple confirmation message
        return html.P(f"Submit button clicked {n_clicks} times. Action registered (no data processing).",
                      style={'color': 'blue', 'fontWeight': 'bold'})
