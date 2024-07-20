import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from graph_utils import load_data
from graph_setup import setup_graphs
import plotly.graph_objects as go

app = dash.Dash(__name__)

button_style = {
    'background-color': '#007BFF',
    'color': 'white',
    'border': 'none',
    'padding': '6px 12px',
    'border-radius': '5px',
    'cursor': 'pointer',
    'font-size': '14px',
    'margin': '0 3px',
    'transition': 'background-color 0.3s ease-in-out',
}

# Improved button style without changing the size
improved_button_style = {
    **button_style,
    'background-color': '#0056b3',  # Darker blue
}

def create_top_10_universities_graph(region):
    df = load_data(region)
    df.sort_values('Score', ascending=False, inplace=True)
    df = df.head(10)
    fig = go.Figure(go.Bar(
        x=df['Score'],
        y=[str(i) for i in range(1, 11)],
        text=df['University'],
        textposition='auto',
        orientation='h'
    ))
    fig.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 11)),
            ticktext=list(range(1, 11))
        ),
        xaxis=dict(title='Score'),
        title='Top 10 Universities',
        title_x=0.5,  # Move the title more to the left
        title_font=dict(size=22, color='navy'),
        height=300,
        margin=dict(l=10, r=10, t=50, b=20),
        autosize=True
    )
    fig.update_yaxes(autorange="reversed")
    return fig

choropleth_fig, bar_chart_fig = setup_graphs()

choropleth_fig.update_layout(
    title='QS University Rankings',
    title_x=0.554,  # Keep the title on the left
    title_font=dict(size=22, color='navy'),
    height=300,
    margin=dict(l=0, r=100, t=30, b=0),  # Move the world map to the right
    autosize=True,
    coloraxis_colorbar=dict(
        x=-0.2,  # Move the color scale to the left
    ),
)

bar_chart_fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), autosize=True)

initial_university_rankings_fig = create_top_10_universities_graph('World')

app.layout = html.Div([
    html.Div([
        html.Button('Africa', id='btn-africa', n_clicks=0, style=improved_button_style),
        html.Button('Asia', id='btn-asia', n_clicks=0, style=improved_button_style),
        html.Button('Europe', id='btn-europe', n_clicks=0, style=improved_button_style),
        html.Button('Latin America', id='btn-latin-america', n_clicks=0, style=improved_button_style),
        html.Button('Oceania', id='btn-oceania', n_clicks=0, style=improved_button_style),
        html.Button('US', id='btn-us', n_clicks=0, style=improved_button_style),
        html.Button('World', id='btn-world', n_clicks=0, style=improved_button_style)
    ], style={'display': 'flex', 'justify-content': 'flex-end', 'padding': '10px'}),
    html.Div([
        dcc.Graph(figure=choropleth_fig, id='choropleth-chart', config={'displayModeBar': False}),
    ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        dcc.Graph(figure=initial_university_rankings_fig, id='university-rankings-chart', config={'displayModeBar': False}),
    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        dcc.Graph(figure=bar_chart_fig, id='bar-chart', config={'displayModeBar': False}),
    ], style={'height': '300px', 'overflowX': 'auto', 'padding-top': '20px'})
], style={'height': '100vh', 'maxWidth': '100vw', 'overflow': 'hidden'})

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
        return initial_university_rankings_fig
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
    fig = create_top_10_universities_graph(region_map[button_id])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
