import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from functions import fetch_openfda_data, process_data

# Fetch and process data

api_key = os.getenv('OPENFDA_API_KEY')

raw_df = fetch_openfda_data(event_types=['drug', 'food'], limit=1000,
                            api_key=api_key)  # Include API key if available
df = process_data(raw_df)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "openFDA Events Dashboard"

app.layout = html.Div([
    html.H1("openFDA Drug and Food Adverse Events Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Event Type:"),
        dcc.Dropdown(
            id='event-type-dropdown',
            options=[
                {'label': 'Drug Events', 'value': 'drug'},
                {'label': 'Food Events', 'value': 'food'},
                {'label': 'All Events', 'value': 'all'}
            ],
            value='all',
            clearable=False
        )
    ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='event-map')
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(df['year'].unique())],
            value=sorted(df['year'].unique())[-1],
            clearable=False
        )
    ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='time-series')
    ]),

    html.Div([
        dcc.Graph(id='top-products')
    ]),

    html.Div([
        dcc.Graph(id='top-reactions')
    ]),

    html.Div([
        html.H4("Data Table"),
        dcc.Graph(
            id='filtered-table',
            figure={}
        )
    ])
])


# Callback for Time Series
@app.callback(
    Output('time-series', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('event-type-dropdown', 'value')]
)
def update_time_series(selected_year, selected_event_type):
    if selected_event_type == 'all':
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df[(df['year'] == selected_year) & (df['event_type'].str.lower() == selected_event_type)]

    if not filtered_df.empty:
        time_counts = filtered_df.groupby('month').size().reset_index(name='counts')
        fig = px.line(time_counts, x='month', y='counts',
                      title=f'Number of Adverse Events per Month in {selected_year}',
                      labels={'month': 'Month', 'counts': 'Number of Events'})
        fig.update_xaxes(tickmode='linear', dtick=1)
        return fig
    else:
        return {}


# Callback for Top Products (Drugs/Foods)
@app.callback(
    Output('top-products', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('event-type-dropdown', 'value')]
)
def update_top_products(selected_year, selected_event_type):
    if selected_event_type == 'all':
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df[(df['year'] == selected_year) & (df['event_type'].str.lower() == selected_event_type)]

    top_products = filtered_df['product_name'].value_counts().nlargest(10).reset_index()
    top_products.columns = ['product_name', 'counts']
    fig = px.bar(top_products, x='counts', y='product_name',
                 orientation='h',
                 title='Top 10 Reported Products',
                 labels={'counts': 'Number of Reports', 'product_name': 'Product'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


# Callback for Top Reactions
@app.callback(
    Output('top-reactions', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('event-type-dropdown', 'value')]
)
def update_top_reactions(selected_year, selected_event_type):
    if selected_event_type == 'all':
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df[(df['year'] == selected_year) & (df['event_type'].str.lower() == selected_event_type)]

    top_reactions = filtered_df['reaction'].value_counts().nlargest(10).reset_index()
    top_reactions.columns = ['reaction', 'counts']
    fig = px.bar(top_reactions, x='counts', y='reaction',
                 orientation='h',
                 title='Top 10 Reactions',
                 labels={'counts': 'Number of Reports', 'reaction': 'Reaction'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


# Callback for Data Table
@app.callback(
    Output('filtered-table', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('event-type-dropdown', 'value')]
)
def update_table(selected_year, selected_event_type):
    if selected_event_type == 'all':
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df[(df['year'] == selected_year) & (df['event_type'].str.lower() == selected_event_type)]

    sample_df = filtered_df[['event_type', 'product_name', 'reaction', 'patient_age', 'patient_sex']].head(20)
    if sample_df.empty:
        fig = go.Figure()
        fig.update_layout(title='No Data Available for Selected Filters')
        return fig

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(sample_df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[sample_df[col] for col in sample_df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    fig.update_layout(title='Sample Adverse Event Reports')
    return fig


@app.callback(
    Output('event-map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('event-type-dropdown', 'value')]
)
def update_event_map(selected_year, selected_event_type):
    if selected_event_type != 'food':
        return go.Figure()  # Return an empty figure if the event type is not 'food'

    filtered_df = df[(df['year'] == selected_year) & (df['event_type'].str.lower() == 'food')]

    if filtered_df.empty:
        return go.Figure()

    fig = px.scatter_geo(filtered_df, locations='state', locationmode='USA-states',
                         title='Geographical Distribution of Food Events',
                         scope='usa', labels={'state': 'State'},
                         hover_data={'state': True, 'counts': True})

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)