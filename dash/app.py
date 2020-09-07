import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as pyo
import plotly.graph_objects as go
import pandas as pd
import json
from dash.dependencies import Input, Output
import plotly.express as px


path = r'C:\Users\Raza\OneDrive\startup-where\data\Neighbourhoods.geojson'
with open(path) as f:
        neighbourhoods = json.load(f)

json_neighbourhoods = {'type': 'FeatureCollection', 'features': []}
for feature in neighbourhoods['features']:

    feature = {
        'type':'Feature',
        'id': feature['properties']['AREA_NAME'],
        'geometry': json.loads(json.dumps(feature['geometry']))
        }
    json_neighbourhoods['features'].append(feature)

import mysql.connector    
cnx = mysql.connector.connect(user='root', password='admin',
                              host='127.0.0.1',
                              database='meetup_db')


cursor = cnx.cursor()
cursor.execute("""
      select * from joined_df
   """)
result = cursor.fetchall()
df = pd.DataFrame(result)
field_names = [i[0] for i in cursor.description]
df.columns = field_names

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(style={
            'textAlign': 'center'}, children=['Startup Where']),
    html.H4(style={
            'textAlign': 'center'}, children=['Discover Potential Toronto Neighbourhoods For Launching Your Next Venture']),
    html.P(html.Label('Choose The View You Want to Explore:'),style={'font-weight': 'bold'}),
    html.P(),
    dcc.RadioItems(id = 'view_picker', options=[{'label':'Yelp Average Ratings', 'value':'avg_rating'}, {'label':'Yelp Sum Reviews', 'value':'sum_reviews'},
    {'label':'Meetup Responses', 'value':'sum_responses'},{'label':'Incubators and Accelerators Count', 'value':'incubator_count'}, {'label':'Combined', 'value':'combined'}
    ], value='avg_rating'),
    html.Div(dcc.Graph(id='graph')),
    html.P(),
    html.P(style={
            'textAlign': 'left'}, children=['Made in Toronto, Canada'])
])




@app.callback(Output('graph', 'figure'),
              [Input('view_picker', 'value')])
def update_figure(selected_view):

    fig = px.choropleth_mapbox(df, geojson=json_neighbourhoods, locations='neighbourhood', color=selected_view,
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           opacity=0.5,
                          )
                

    fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=9.5, mapbox_center = {"lat": 43.71, "lon": -79.34})
    fig.update_layout(margin={"r":10,"t":0,"l":0,"b":0})


    return fig

if __name__ == '__main__':
    app.run_server()