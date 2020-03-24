import csv
from urllib.request import urlopen
import pandas as pd
	
 def get_earthquake_data_csv(year, mag,  filepath):
 	"""
        Downloads earthquake data from earthquake.usgs.gov for 1 year with 

        Arguments:
        year - year, data will be collected from 01.01 00:00:00 to 12.12 23:59:59 of this year
        mag - lower border of the magnitude of the earthquakes
        filepath - the path to the directory in which the dataset will be saved

        Returns:
        saves the csv file to the dataset and prints an info message
    """
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query.csv?starttime={year}-01-01%2000%3A00%3A00&endtime={year}-12-24%2023%3A59%3A59&minmagnitude={mag}&orderby=time'.format(year = year, mag = mag)
    df = pd.read_csv(url)
    df.to_csv(filepath + 'earthquake_{year}.csv'.format(year = year), sep='\t')
    print('Data for the {year} was saved to earthquake_{year}.csv'.format(year = year))
    
def get_earthquake_dataset(start_year, end_year, path):
	"""
        Downloads earthquake data from earthquake.usgs.gov for a sertain period of time

        Arguments:
        start_year, end_year - start and end of the time period for the dataset
        mag - lower border of the magnitude of the earthquakes
        path - the path to the directory in which the dataset will be saved
    """
    for y in range(start_year, end_year+1):
        get_earthquake_data_csv(y, 4.5, path)
        
get_earthquake_dataset(1995, 2000, 'earthquakes_data/')