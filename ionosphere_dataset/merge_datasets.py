import datetime
import geopy.distance
import pandas as pd
import os

sondes = {
          'WK545': ((45.39, 141.68),[x for x in range(1992, 2004)]),
          'WK546' : ((45.16, 141.75),[x for x in range(2001, 2021)]),
          'AK539' : ((39.725, 140.053),[x for x in range(1992, 1994)]),
          'TO535' : ((35.71, 139.45),[x for x in range(1992, 2003)]),
          'TO536' : ((35.71, 139.45),[x for x in range(2001, 2021)]),
          'YG431' : ((31.20, 130.62),[x for x in range(1992, 2021)]),
          'OK426' : ((26.28, 127.81),[x for x in range(1992, 2021)])
          'SY951' : ((-69.00, 39.59),[x for x in range(1996, 2006)])
         }

numdays = 15

def clean_time(df):
	 """
        Creates new time column, converts Object value to DateTime 

        Arguments:
        df - dataframe
    """
    df['time'] = df['#                       fmin  ']
    df['time'] = df['time'].apply(lambda x: x.split(':')[0])
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    return df[df.time.notnull()]

def convert_tz(row, tz_old = 'Asia/Tokyo', tz_new = 'UTC'):
	 """
        Converts column value from tz_old to tz_new
        Arguments:
        row - a row of dataframe
        tz_old - current time zone
        tz_new - new time zone

        Returns:
        row with new value
    """
    stamp = Timestamp(pd.to_datetime(row['time'], errors='ignore'), tz=tz_old)
    row['time'] = stamp.tz_convert(tz=tz_new)
    return row

def filter_by_prep_zone(row):
	"""
        Filters out the earthquakes for which there are no sonde in their prep zone
        Using 10^(0.43*M) formula where M is the magnitude of the earthquake

        Arguments:
        row - a row of dataframe

        Returns:
        True if there is at least 1 sonde in the earthquake prep zone anf False otherwise 
    """
    radius = 10**(0.43*row['mag'])
    coord_e = (row['latitude'], row['longitude'])
    for name, (coord_s, _) in sondes.items():
        dist = geopy.distance.geodesic(coord_e, coord_s).km
        if dist <= radius:
            return True
    return False

def walk_earthquakes(df_s, earthquakes_folder):
	"""
        Walks throught the earthquakes dataset, filters by prep zone and merges it with sonde data.
        If the sonde recorded the data on the earthquake day, 
        then records for the current sonde will be saved for 15 days before the earthquake. 

        Arguments:
        df_s - dataframe with data from one sonde

        Returns:
        df_res - the resulting dataframe with filtered data sorted by time
    """
    
    df_s_columns = df_s.columns.values.tolist()
    df_res = pd.DataFrame(columns=df_s_columns)
    
    earthquakes_list = os.listdir(earthquakes_folder)
    print(earthquakes_list)
    e_count = 0
    for name_e in earthquakes_list:
        path = earthquakes_folder +'/'+ name_e
        print(path)
        df = pd.read_csv(path, sep='\t')
        #filter by prep zone radius
        df_e = df[df.apply(filter_by_prep_zone, axis=1)]
        df_e['time'] = pd.to_datetime(df_e['time'])
        # extract date
        df_e['date'] = [datetime.datetime.date(d) for d in df_e['time']] 
        df_s['date'] = [datetime.datetime.date(d) for d in df_s['time']] 
        
        for d in df_e['date']:
            if d not in df_s.date.unique(): #checking if sonde was working on the day of the earthquake
                continue
            e_count += 1
            date_list = [d - datetime.timedelta(days=x) for x in range(numdays)]
            df_dates = pd.DataFrame(date_list, columns =['date'])
            df_temp = df_s[df_s.date.isin(df_dates.date)]
            df_res = pd.concat([df_res, df_temp]).drop_duplicates()
        print('df_res size', len(df_res))
    print('{count} earthquakes matched with current sonde'.format(count = e_count))

    df_res = df_res.sort_values(by=['time'])
    return df_res

                
def walk_sondes(sondes_folder, earthquakes_folder):
	"""
        Walks throught the sondes dataset, converts date column to UTC time zone
        and merges data with earthquake dataset using walk_earthquakes function

        Arguments:
        sondes_folder, earthquakes_folder - folder names of the datasets

        Returns:
        Saves the merged data to a new folder. Each file corresponds to a single sonde.
    """
    sondes_names = os.listdir(sondes_folder)
#     for i in os.walk('sondes_japan_data'):
#         folder_sondes.append(i)
    print(sondes_names)
    for name_s in sondes_names:
        if '.csv' not in name_s:
            continue
        path = sondes_folder +'/'+ name_s
        print(path)
        df_s = pd.read_csv(path, sep=',')
        df_s = clean_time(df_s)            
        if "SY951" in name_s:
            df_s = df_s.apply(convert_tz, tz_old = 'Antarctica/Syowa',  axis=1)
        else:
            df_s = df_s.apply(convert_tz, axis=1)
            
        df_res = walk_earthquakes(df_s, earthquakes_folder)

        sonde_name = name_s.split('.')[0]
        fname = str.format("sondes_data_merged/{sonde}_merged.csv", path = address, sonde = sonde_name)
        print(fname)
        df_res.to_csv(fname)
        print('Data for the {sonde} sonde was saved to {sonde}_merged.csv'.format(sonde = sonde_name))