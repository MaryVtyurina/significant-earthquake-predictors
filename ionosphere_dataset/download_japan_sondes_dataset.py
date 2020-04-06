import pandas as pd

sondes = {'WK545': [x for x in range(1992, 2004)],
          'WK546' : [x for x in range(2001, 2021)],
          'AK539' : [x for x in range(1992, 1994)],
          'TO535' : [x for x in range(1992, 2003)],
          'TO536' : [x for x in range(2001, 2021)],
          'YG431' : [x for x in range(1992, 2021)],
          'OK426' : [x for x in range(1992, 2021)],
          'SY951' : [x for x in range(1996, 2006)]}

def get_df_columns():
    url_txt = "http://wdc.nict.go.jp/IONO/observation-history/factor-auto-WK546-2011.sjis.txt"
    df = pd.read_csv(url_txt)
    df_columns = df.columns.values.tolist()
    return df_columns

def get_japan_data_csv(sondes, df_columns, filepath):
    """
        Downloads all automatically scaled data from ionosondes in Japan from http://wdc.nict.go.jp catalog

        Arguments:
        sondes - dictionary with keys - ionosondes names and values - years with records
        df_columns - list of columns with the structure of catalog
        filepath - the path to the directory in which the dataset will be saved

        Returns:
        saves the csv file to the dataset and prints an info message
    """
    url_str_beg = "http://wdc.nict.go.jp/IONO/observation-history/factor-auto-"
    url_str_end = ".sjis.txt"
    for sonde, years in sondes.items():
        df = pd.DataFrame(columns=df_columns)
        for year in years:
            url = url_str_beg + sonde + "-" + str(year) + url_str_end
#             print("Downloading data from ", url)
            df1 = pd.read_csv(url)
            df = pd.concat([df, df1])
        fname = str.format("{path}{sonde}.csv", path = filepath, sonde = sonde)
        df.to_csv(fname)
        print('Data for the {sonde} sonde was saved to {sonde}.csv'.format(sonde = sonde))
    
df_columns = get_df_columns()
path = "sondes_japan_data/"
get_japan_data_csv(sondes, df_columns, path)