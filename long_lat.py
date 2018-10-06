import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def find_household_density(df):
    '''
    Converts addresses dataframe to latitude and longitude by units
    '''
    df['tup_long_lat'] = list(zip(round(df['LATITUDE'],3), round(df['LONGITUDE'],3)))
    agg_df = df['tup_long_lat'].value_counts()
    return agg_df



if __name__ == '__main__':
    df = pd.read_csv('addresses.csv')
    density_df = find_household_density(df)
