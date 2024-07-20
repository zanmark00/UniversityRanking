import plotly.graph_objects as go
import data_processing as dp

def setup_graphs():
    # Load and prepare data
    filepath = '2023_QS_World_University_Rankings_with_Short_Names.csv'
    rankings_df = dp.load_rankings_data(filepath)
    country_name_mapping = {'United States Of America': 'United States of America'}
    rankings_df = dp.standardize_country_names(rankings_df, country_name_mapping)
    world = dp.load_world_data()
    merged = dp.merge_data(rankings_df, world)

    # Create the choropleth figure
    choropleth_fig = dp.create_choropleth_map(merged)

    # Create the bar chart figure
    avg_scores = rankings_df.groupby('location')[['ar score', 'er score', 'cpf score']].mean().reset_index()
    bar_chart_fig = go.Figure(data=[
        go.Bar(x=avg_scores['location'], y=avg_scores['ar score'], name='Academic Reputation Score', marker_color='indianred'),
        go.Bar(x=avg_scores['location'], y=avg_scores['er score'], name='Employer Reputation Score', marker_color='lightblue'),
        go.Bar(x=avg_scores['location'], y=avg_scores['cpf score'], name='Citations per Faculty Score', marker_color='green')
    ])
    bar_chart_fig.update_layout(barmode='stack')

    return choropleth_fig, bar_chart_fig
