# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
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
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                    ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: f'{i}' for i in range(0, 10001, 1000)},
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
# Function decorator to specify function input and output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # Use the global spacex_df dataframe
    filtered_df = spacex_df

    if entered_site == 'ALL':
        # Group by 'Launch Site' and count successes (class=1) for each site
        all_sites_df = filtered_df[filtered_df['class'] == 1].groupby('Launch Site').size().reset_index(name='counts')
        
        # Create a pie chart showing success counts per site
        fig = px.pie(all_sites_df, 
                     values='counts', 
                     names='Launch Site',  # 'Launch Site' for different sites
                     title='Total Success Launches by Site')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        # Create a pie chart for success vs failure for the specific site
        fig = px.pie(filtered_site_df, 
                     names='class',  # 'class' indicates success (1) or failure (0)
                     title=f'Total Success Launches for {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, payload_range):
    # Filter the dataframe by payload range
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site == 'ALL':
        # If all sites are selected, create a scatter plot for all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',  # Color points by Booster Version Category
            title='Correlation between Payload and Success for All Sites',
            hover_data=['Launch Site']  # Optional: Show site names on hover
        )
        return fig
    else:
        # If a specific site is selected, filter the dataframe for the selected site
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
        # Create a scatter plot for the specific site
        fig = px.scatter(
            filtered_site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',  # Color points by Booster Version Category
            title=f'Correlation between Payload and Success for {entered_site}',
            hover_data=['Booster Version']  # Optional: Show booster version on hover
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
