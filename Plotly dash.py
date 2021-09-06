# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'ALL', 'value': 'All'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload,
                                max=max_payload,step=1000,value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pie(site_dropdown):
    if site_dropdown == 'ALL':
        title_pie = f"Success Launches for site {site_dropdown}"
        fig = px.pie(spacex_df, values='class', names='Launch Site', title=title_pie)

    else:
        title_pie = f"Success Launches for site {site_dropdown}"
        site_b = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        class_b = site_b.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(class_b, values='class count', names='class', title=title_pie)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value'))
def scatter_plot(payload_in,site_dropdown):
    low, high = payload_in
    if site_dropdown == 'ALL':
        spacex_df1 = spacex_df
    else:
        spacex_df1 =spacex_df[spacex_df['Launch Site'] == site_dropdown]
    mask = (spacex_df1['Payload Mass (kg)'] > low) & (spacex_df1['Payload Mass (kg)'] < high)
    fig1 = px.scatter(
        spacex_df1[mask], x='Payload Mass (kg)', y="class",
        color="Booster Version Category")
    return(fig1)

# Run the app
if __name__ == '__main__':
    app.run_server()

