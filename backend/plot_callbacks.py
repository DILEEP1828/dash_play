import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np # For placeholder data or calculations

import base64
from io import BytesIO
from asammdf import MDF # Corrected import

def register_plot_callbacks(app):

    @app.callback(
        [Output('time-slider', 'min'),
         Output('time-slider', 'max'),
         Output('time-slider', 'value'),
         Output('time-slider', 'marks'),
         Output('signal-dropdown', 'options'),
         Output('signal-dropdown', 'value')],
        [Input('url', 'pathname')], # Trigger when navigating to the plot page
        [State('mf4_file_for_plotting_store', 'data')] # Get the stored MF4 data
    )
    def populate_slider_and_dropdown(pathname, mf4_file_data):
        if pathname != '/plot' or mf4_file_data is None:
            # Not on the plot page or no data, return default/empty states
            default_slider_marks = {i: str(i) for i in range(0, 101, 10)}
            return 0, 100, 50, default_slider_marks, [{'label': 'No MF4 data loaded', 'value': 'none'}], None

        try:
            content_type, content_string = mf4_file_data['contents'].split(',')
            decoded_mf4 = base64.b64decode(content_string)

            with MDF(BytesIO(decoded_mf4)) as mdf_file:
                # Time Slider properties
                # Use start_time and last_timestamp from the MDF object header if available
                # These are generally more reliable for the whole file's range.
                # If not available, we might need to iterate signals, but that's less efficient.
                # For now, let's assume mdf_file.header.start_time and a calculated end time.
                # A robust way is to get min/max timestamps from all channels.

                all_timestamps = []
                signal_names = []

                if not mdf_file.channels_db: # Check if channels_db is empty
                     # Fallback if no channels or if direct header times are preferred
                    min_time = 0.0
                    max_time = 1.0 # Default if no signals
                    if hasattr(mdf_file.header, 'start_time'): # Check if start_time exists
                         min_time = mdf_file.header.start_time.timestamp() # Convert datetime to timestamp
                         # last_timestamp is not directly in header usually, need to find it
                         # Iterate to find the true max timestamp
                         max_ts_val = min_time
                         for group in mdf_file.groups:
                            for ch_group in group.channel_groups:
                                if ch_group.samples_count > 0:
                                    master = mdf_file.get_master(group.index, ch_group.index)
                                    if master is not None and len(master)>0:
                                        max_ts_val = max(max_ts_val, master[-1])
                         max_time = max_ts_val if max_ts_val > min_time else min_time + 1.0


                else: # If channels_db is not empty
                    for signal_name_cand in mdf_file.channels_db:
                        # Filter for actual signals, not master channels if they appear in channels_db
                        # A simple check: master channels often have specific names or no unit.
                        # For now, assume all in channels_db are plottable signals.
                        # A more robust way is to iterate mdf_file.iter_channels()
                        pass # Will use iter_channels below for more robust signal list

                    first_signal = True
                    min_time = float('inf')
                    max_time = float('-inf')

                    for signal in mdf_file.iter_channels(raw=False): # raw=False to get physical values
                        if signal.timestamps is not None and len(signal.timestamps) > 0:
                            signal_names.append({'label': signal.name, 'value': signal.name})
                            current_min = signal.timestamps[0]
                            current_max = signal.timestamps[-1]
                            if first_signal:
                                min_time = current_min
                                max_time = current_max
                                first_signal = False
                            else:
                                min_time = min(min_time, current_min)
                                max_time = max(max_time, current_max)

                if not signal_names: # If iter_channels yielded nothing or all had no timestamps
                    signal_names = [{'label': 'No plottable signals found', 'value': 'none'}]
                    # Keep min_time, max_time as determined (or defaults if header also failed)
                    if max_time <= min_time : max_time = min_time +1 # ensure max_time > min_time

                slider_min = min_time
                slider_max = max_time
                slider_value = slider_min

                # Create marks for the slider
                num_marks = 10
                mark_step = (slider_max - slider_min) / num_marks if num_marks > 0 and slider_max > slider_min else 1
                slider_marks = {i: f'{i:.2f}' for i in np.arange(slider_min, slider_max + mark_step/2, mark_step)} # ensure last mark is included

                default_signal = signal_names[0]['value'] if signal_names and signal_names[0]['value'] != 'none' else None

                return slider_min, slider_max, slider_value, slider_marks, signal_names, default_signal

        except Exception as e:
            print(f"Error populating slider/dropdown: {e}")
            default_slider_marks = {i: str(i) for i in range(0, 101, 10)}
            return 0, 100, 50, default_slider_marks, [{'label': f'Error: {str(e)[:50]}...', 'value': 'error'}], None


    @app.callback(
        Output('time-series-plot', 'figure'),
        [Input('time-slider', 'value'),
         Input('signal-dropdown', 'value')],
        [State('mf4_file_for_plotting_store', 'data')]
    )
    def update_time_series_plot(selected_time, selected_signal, mf4_file_data):
        if selected_signal is None or selected_signal == 'none' or selected_signal == 'error' or mf4_file_data is None:
            return go.Figure().update_layout(title_text="Please select an MF4 file and a signal.")

        try:
            content_type, content_string = mf4_file_data['contents'].split(',')
            decoded_mf4 = base64.b64decode(content_string)

            with MDF(BytesIO(decoded_mf4)) as mdf_file:
                signal_obj = mdf_file.get(selected_signal)
                if signal_obj is None:
                    return go.Figure().update_layout(title_text=f"Signal '{selected_signal}' not found.")

                timestamps = signal_obj.timestamps
                samples = signal_obj.samples

                fig = px.line(x=timestamps, y=samples, labels={'x': 'Time (s)', 'y': signal_obj.unit or 'Value'}, title=f"Time Series: {selected_signal}")

                fig.add_vline(x=selected_time, line_width=2, line_dash="dash", line_color="red", annotation_text="Selected Time", annotation_position="top right")

                return fig

        except Exception as e:
            print(f"Error updating time series plot: {e}")
            return go.Figure().update_layout(title_text=f"Error plotting signal: {str(e)[:50]}...")


    @app.callback(
        Output('polygon-plot', 'figure'),
        [Input('time-slider', 'value')]
    )
    def update_polygon_plot(selected_time):
        # For now, a simple polygon. Its properties can be made dependent on selected_time.
        # Example: Change color based on time, or shift one vertex.

        # Define base polygon vertices (e.g., a square or pentagon)
        x_coords = [1, 2, 2, 1, 1]
        y_coords = [1, 1, 2, 2, 1]

        # Example of making it dynamic: shift one vertex based on slider
        # Normalize selected_time to a factor, e.g., if slider is 0-100, map to 0-0.5 shift
        # This is just a placeholder for more meaningful dynamic behavior
        time_factor = (selected_time or 0) / 100.0 # Assuming slider max is 100 for this example

        shifted_x_coords = [x + time_factor * 0.5 for x in x_coords]
        shifted_y_coords = [y + time_factor * 0.2 for y in y_coords]


        fig = go.Figure(go.Scatter(
            x=shifted_x_coords,
            y=shifted_y_coords,
            fill="toself",
            fillcolor=f'rgba({int(time_factor*255)}, 100, 150, 0.5)', # Color changes with time
            line_color='darkblue'
        ))

        fig.update_layout(
            title_text=f"2D Polygon Plot (Time: {selected_time:.2f}s)",
            xaxis_title="X-axis",
            yaxis_title="Y-axis",
            xaxis_range=[0, 3], # Adjust ranges as needed
            yaxis_range=[0, 3]
        )
        # Ensure the polygon aspect ratio is 1 if it's a geometric shape
        fig.update_yaxes(scaleanchor="x", scaleratio=1)

        return fig
