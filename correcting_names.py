import pandas as pd
import geopandas as gpd

def correct_country_names(df, mapping):
    df['location'] = df['location'].replace(mapping)
    return df

# Load your rankings data
rankings_df = pd.read_csv('2023 QS World University Rankings.csv')

country_name_mapping = {
    'Bahrain': 'Bahrain',
    'Iran, Islamic Republic of': 'Iran',
    'Malta': 'Malta',
    'Macau SAR': 'Macao',
    'China (Mainland)': 'China',
    'Palestinian Territory, Occupied': 'Palestine',
    'Hong Kong SAR': 'Hong Kong',
    'United States': 'United States of America',
    'Singapore': 'Singapore',
    'Czech Republic': 'Czechia',
    'Dominican Republic': 'Dominican Rep.',
    'Syrian Arab Republic': 'Syria',
    'Bosnia and Herzegovina': 'Bosnia and Herz.'
}

# Correct the country names in the rankings dataframe
rankings_df = correct_country_names(rankings_df, country_name_mapping)

# Save the corrected DataFrame
rankings_df.to_csv('2023 QS World University Rankings_corrected.csv', index=False)

# Load the GeoPandas world dataset
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Perform the non-matching countries check
rankings_countries = set(rankings_df['location'].unique())
world_countries = set(world['name'].unique())

non_matching_countries = rankings_countries - world_countries
non_matching_world = world_countries - rankings_countries

print("Country names in the rankings but not in the GeoPandas world dataset:")
print(non_matching_countries)

print("\nCountry names in the GeoPandas world dataset but not in the rankings:")
print(non_matching_world)
