import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from functions import fetch_openfda_data, process_data

# Fetch and process data
raw_df = fetch_openfda_data(limit=1000)  # Adjust limit as needed
df = process_data(raw_df)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "openFDA Events Dashboard"

app.layout = html.Div([
    html.H1("openFDA Drug Adverse Events Dashboard", style={'textAlign': 'center'}),

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
        dcc.Graph(id='top-drugs')
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
    Input('year-dropdown', 'value')
)
def update_time_series(selected_year):
    filtered_df = df[df['year'] == selected_year]
    if not filtered_df.empty:
        time_counts = filtered_df.groupby('month').size().reset_index(name='counts')
        fig = px.line(time_counts, x='month', y='counts',
                      title=f'Number of Adverse Events per Month in {selected_year}',
                      labels={'month': 'Month', 'counts': 'Number of Events'})
        return fig
    else:
        return {}


# Callback for Top Drugs
@app.callback(
    Output('top-drugs', 'figure'),
    Input('year-dropdown', 'value')
)
def update_top_drugs(selected_year):
    filtered_df = df[df['year'] == selected_year]
    top_drugs = filtered_df['drug_name'].value_counts().nlargest(10).reset_index()
    top_drugs.columns = ['drug_name', 'counts']
    fig = px.bar(top_drugs, x='counts', y='drug_name',
                 orientation='h',
                 title='Top 10 Reported Drugs',
                 labels={'counts': 'Number of Reports', 'drug_name': 'Drug'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig


# Callback for Top Reactions
@app.callback(
    Output('top-reactions', 'figure'),
    Input('year-dropdown', 'value')
)
def update_top_reactions(selected_year):
    filtered_df = df[df['year'] == selected_year]
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
    Input('year-dropdown', 'value')
)
def update_table(selected_year):
    filtered_df = df[df['year'] == selected_year].head(20)
    table = px.imshow(filtered_df[['drug_name', 'reaction', 'patient_age', 'patient_sex']].isin([None]))
    # Alternatively, use plotly's table
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(filtered_df[['drug_name', 'reaction', 'patient_age', 'patient_sex']].columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[
            filtered_df['drug_name'],
            filtered_df['reaction'],
            filtered_df['patient_age'],
            filtered_df['patient_sex']
        ],
            fill_color='lavender',
            align='left'))
    ])
    fig.update_layout(title='Sample Adverse Event Reports')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)