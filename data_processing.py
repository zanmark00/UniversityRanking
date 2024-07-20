import pandas as pd
import geopandas as gpd
import plotly.express as px

def load_rankings_data(filepath):
    df = pd.read_csv(filepath)
    df['location'] = df['location'].str.title()
    return df

def standardize_country_names(df, name_mapping):
    df['location'] = df['location'].replace(name_mapping)
    return df

def merge_data(rankings_df, world):
    top_universities = rankings_df.groupby('location').apply(
        lambda x: '<br>'.join([''] + x.nsmallest(3, 'Rank')['institution'].tolist())
    ).reset_index().rename(columns={0: 'Top 3 Universities'})
    average_rankings = rankings_df.groupby('location')['Rank'].mean().reset_index()
    merged_data = average_rankings.merge(top_universities, on='location')
    merged = world.merge(merged_data, left_on='name', right_on='location', how='left')
    merged['Top 3 Universities'] = merged['Top 3 Universities'].fillna('No data')
    return merged

def create_choropleth_map(merged):
    fig = px.choropleth(
        merged,
        locations="iso_a3",
        color="Rank",
        hover_name="name",
        hover_data={
            'Rank': ':.2f',
            'Top 3 Universities': True,
            'iso_a3': False
        },
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="equirectangular"
    )
    rank_min = merged['Rank'].min()
    rank_max = merged['Rank'].max()
    fig.update_coloraxes(cmin=rank_min, cmax=rank_max)
    fig.update_layout(
        title_x=0.5,
        coloraxis_colorbar={
            'title': 'Rank',
            'lenmode': 'fraction',
            'len': 0.85,
            'x': 0.02,
            'xanchor': 'left',
            'y': 0.5,
            'yanchor': 'middle',
            'tickvals': [rank_min, rank_max * 0.25, rank_max * 0.5, rank_max * 0.75, rank_max],
            'ticktext': ['Best', 'Better', 'Good', 'Average', 'Poor']
        }
    )
    return fig

def get_top_10_universities(rankings_df):
    return rankings_df.nsmallest(10, 'Rank')[['institution', 'Rank']]

def load_world_data():
    return gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
