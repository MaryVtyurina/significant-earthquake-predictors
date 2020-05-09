import csv
from urllib.request import urlopen
import pandas as pd   
    
def get_earthquake_dataset(start_year, end_year, path):
    """
        Downloads earthquake data from earthquake.usgs.gov for a sertain period of time

        Arguments:
        start_year, end_year - start and end of the time period for the dataset
        mag - lower border of the magnitude of the earthquakes
        path - the path to the directory in which the dataset will be saved
    """
    df_res = pd.DataFrame()
    for y in range(start_year, end_year+1):
        print(y)
        url = 'https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime={year}-01-01%2000%3A00%3A00&endtime={year}-12-24%2023%3A59%3A59&minmagnitude={mag}&orderby=time'.format(year = year, mag = mag)
        df_eq = pd.read_csv(url)
        df_eq = get_earthquake_data_csv(y, 5.0)
        df_res = pd.concat([df_res, df_e])
    df_res.to_csv(path, index=False)
        
get_earthquake_dataset(1992, 2020, 'earthquakes_data.csv')