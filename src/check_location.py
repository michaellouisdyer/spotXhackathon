import pandas as pd
import geopandas as gp

def check_if_in_one(polygon, long_lat):
    long_lat_point = Point(*long_lat)
    return polygon.contains(long_lat_point)

def check_any(long_lat, market_df):
    mask = market_df['geometry'].apply(check_if_in_one, long_lat =long_lat)
    # print(mask)
    return market_df[mask]
    # return mask

def is_geo_empty(geo_obj):
    if geo_obj.empty:
        return False
    else:
        return True

def get_top_markets(df_pop, market_df):
    df_pop = pd.read_pickle('../long_lat_units.pkl').reset_index()
    df_pop.columns = ['long_lat', 'population']
    test = df_pop.head(200)
    test['geo_data'] = test.long_lat.apply(check_any, market_df=farmers_mkt)
    test['geo'] = test.geo_data.apply(is_geo_empty)
    test[['Long', 'Lat']] = test.long_lat.apply(pd.Series)
    top_farmers_zoned = test[test.geo].drop('geo_data', axis = 1)
    top_farmers_not_zoned = test[~test.geo].drop('geo_data', axis = 1)
    return top_farmers_zoned, top_farmers_not_zoned

def main():
    farmers_mkt = gp.read_file('../data/zoning_for_farmers_markets.shp')
    top_farmers_zoned, top_farmers_not_zoned =  get_top_markets(df_pop, market_df)
    top_farmers_not_zoned.to_csv("top_farmers_not_zoned.csv")
    top_farmers_zoned.to_csv("top_farmers_zoned.csv")


if __name__ == '__main__':
    main()
