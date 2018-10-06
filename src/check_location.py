import geopandas as gp
import pandas as pd
from shapely.geometry import Point


def check_if_in_one(polygon, long_lat):
    """Determines if a coordinate is in a particular polygon"""
    long_lat_point = Point(*long_lat)
    return polygon.contains(long_lat_point)


def check_any(long_lat, market_df):
    """Checks to see if a coordinate is within any of the correctly designated zones
    Returns:
    pd.Series containing Geopandas objects if coordinates are within designated zone, empty Geopandas objects if theyt are not"""

    mask = market_df['geometry'].apply(check_if_in_one, long_lat=long_lat)
    return market_df[mask]


def is_geo_empty(geo_obj):
    """Returns whether or not a Geopandas object is empty"""
    if geo_obj.empty:
        return False
    else:
        return True


def get_top_markets(market_df):
    """Returns:
    top_farmers_zoned: a Dataframe containing coordinates that are zoned for farmer's markets, sorted by population density
    top_farmers_not_zoned: a Dataframe containing coordinates that are not zoned for farmer's markets, sorted by population density
    """

    df_pop = pd.read_pickle('data/long_lat_units.pkl').reset_index()
    df_pop.columns = ['long_lat', 'population']

    # Return only the top 200
    test = df_pop.head(200)
    test['geo_data'] = test.long_lat.apply(check_any, market_df=market_df)
    test['geo'] = test.geo_data.apply(is_geo_empty)

    # Split out latitude and longitude for plotting purposes
    test[['Long', 'Lat']] = test.long_lat.apply(pd.Series)

    # Remove unnecessary information about the zone
    top_farmers_zoned = test[test.geo].drop('geo_data', axis=1)
    top_farmers_not_zoned = test[~test.geo].drop('geo_data', axis=1)
    return top_farmers_zoned, top_farmers_not_zoned


def main():
    farmers_mkt = gp.read_file('data/zoning_for_farmers_markets.shp')
    top_farmers_zoned, top_farmers_not_zoned = get_top_markets(farmers_mkt)
    top_farmers_not_zoned.to_csv("data/top_farmers_not_zoned.csv")
    top_farmers_zoned.to_csv("data/top_farmers_zoned.csv")


if __name__ == '__main__':
    main()
