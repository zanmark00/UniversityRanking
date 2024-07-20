import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

button_style = {
    'background-color': '#007BFF',
    'color': 'white',
    'border': 'none',
    'padding': '12px 24px',
    'border-radius': '5px',
    'cursor': 'pointer',
    'font-size': '16px',
    'margin': '0 10px',
}

graph_style = {
    'border': '1px solid #ddd',
    'border-radius': '10px',
    'margin-top': '20px',
    'padding': '20px',
    'box-shadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
    'background-color': 'white',
}

university_font_size = 18  # Adjust the font size here

def load_data(region):
    file_map = {
        'Africa': 'africa_university_rankings.csv',
        'Asia': 'asia_university_rankings.csv',
        'Europe': 'europe_university_rankings.csv',
        'Latin America': 'latin_america_university_rankings.csv',
        'Oceania': 'oceania_universities_ranking.csv',
        'US': 'us_university_rankings.csv',
        'World': 'world_university_rankings.csv'
    }
    return pd.read_csv(file_map[region])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Button('Africa', id='btn-africa', n_clicks=0, style=button_style),
        html.Button('Asia', id='btn-asia', n_clicks=0, style=button_style),
        html.Button('Europe', id='btn-europe', n_clicks=0, style=button_style),
        html.Button('Latin America', id='btn-latin-america', n_clicks=0, style=button_style),
        html.Button('Oceania', id='btn-oceania', n_clicks=0, style=button_style),
        html.Button('US', id='btn-us', n_clicks=0, style=button_style),
        html.Button('World', id='btn-world', n_clicks=0, style=button_style)
    ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
    dcc.Graph(
        id='university-rankings-chart',
        config={
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
        },
        style=graph_style
    )
])

@app.callback(
    Output('university-rankings-chart', 'figure'),
    [Input('btn-africa', 'n_clicks'),
     Input('btn-asia', 'n_clicks'),
     Input('btn-europe', 'n_clicks'),
     Input('btn-latin-america', 'n_clicks'),
     Input('btn-oceania', 'n_clicks'),
     Input('btn-us', 'n_clicks'),
     Input('btn-world', 'n_clicks')]
)
def display_universities(btn_africa, btn_asia, btn_europe, btn_latin_america, btn_oceania, btn_us, btn_world):
    ctx = dash.callback_context
    if not ctx.triggered:
        return go.Figure()
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    region_map = {
        'btn-africa': 'Africa',
        'btn-asia': 'Asia',
        'btn-europe': 'Europe',
        'btn-latin-america': 'Latin America',
        'btn-oceania': 'Oceania',
        'btn-us': 'US',
        'btn-world': 'World'
    }
    df = load_data(region_map[button_id])
    df.sort_values(by='Rank', inplace=True)
    y_range = list(range(1, 11))
    fig = go.Figure(data=[
        go.Bar(
            x=df['Score'],
            y=y_range,
            text=df['University'],
            marker=dict(
                color='#007BFF',
            ),
            orientation='h',
            width=0.5
        )
    ])
    fig.update_layout(
        title=f"Top 10 Universities in {region_map[button_id]}",
        xaxis_title="Score",
        yaxis_title="Rank",
        yaxis=dict(
            tickvals=y_range,
            ticktext=y_range
        ),
        width=800,
        height=500,
        margin=dict(l=20, r=20, t=60, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial', size=14, color='#333')
    )
    fig.update_xaxes(
        tickangle=-45,
        tickfont=dict(size=10),
        tickmode='linear',
        dtick=1
    )
    fig.update_yaxes(
        tickfont=dict(size=10),
        tickmode='linear',
        dtick=1
    )
    # Increase font size for universities
    fig.update_traces(textfont_size=university_font_size)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
