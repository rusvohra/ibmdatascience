# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_names = [{'label':row['Launch Site'], 'value':row['Launch Site']} for index, row in spacex_df.iterrows()]

site_names = [{'label':i, 'value':i} for i in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create a default pie chart for 'ALL' as initial value
default_pie_chart = px.pie(spacex_df, values='class', 
                           names='Launch Site', 
                           title='Total Success Launches By Site')

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                            html.Label("Select Statistics:"),
                                            dcc.Dropdown(
                                                id='site-dropdown',
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                    ]+site_names,
                                                placeholder='Select a Launch Site here',
                                                searchable=True
                                                # style={....}
                                                )
                                        ]),

                                # Use default pie chart as the initial value
                                html.Div(dcc.Graph(id='success-pie-chart', figure=default_pie_chart)),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    print(entered_site)
    if entered_site == 'ALL':
        print('here')
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df_class = filtered_df['class'].value_counts().reset_index()
        filtered_df_class.columns = ['class', 'count']
        print(filtered_df_class)
        fig = px.pie(filtered_df_class, values='count', 
        names='class', 
        title='Total Success Launches for site {}'.format(entered_site))
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
