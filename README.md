# significant-earthquake-predictors

This repository was created as a part of research in Saint Petersburg State University. We provide two types of datasets with cleaned data and filled NaNs. We also provide several models for feature selection.

The data is consists of:
* more than 300 ionosondes from 2 different sources
* earthquakes data (1992 - 2020)

### Prerequisites

Install [pytorch](https://pytorch.org) before running the Neural network model. 

### Data

Data about earthquakes was taken from [USGS website](https://www.usgs.gov/natural-hazards/earthquake-hazards/earthquakes)

The ionosphere data was taken from:
* National centers for environmental information [NOAA](https://www.ngdc.noaa.gov/stp/iono/ionogram.html)
* National Institute of Information and Communication Technology in Japan [NICT](http://wdc.nict.go.jp/IONO/HP2009/ISDJ/index-E.html) 

The data from NICT dataset was not used in further experiments due to different parameters set. But it should be used in the future reasearch.

All the data in both ionosphere data sources is in a 15-minutes time format.

### Missing values

The data with more than 50% of missing values was not considered. 
The data were grouped by earthquake id, date and time and then the missing values were filled with mean of such group.

### Datasets

We applied two approaches when creating datasets.

#### Location-formed dataset

 Described in the [paper by Pulinets 2004](https://www.researchgate.net/publication/215972520_Ionospheric_Precursors_of_Earthquakes_Recent_Advances_in_Theory_and_Practical_Applications) this approach based on the earthquake preparation zone. We consider pairs of sondes - one inside the preparation zone, the other one - outside. 

<img src="imgs/pair_of_sondes.png" width="300">

Then the data was aggregated by an hour and was flattened in a way that 1 earthquake is 1 sample (1 row) - to do this each feature was renamed in a next way `feature-name_nday_nhour`. Where `nday` - number of days before the earthquake and `nhour` - number of hour in the day `nday` (from 0 to 23).
The files with data are located in the `NOAA/datasets_LR_model`
The structure of the file is presented below:

| D_0_0   |   D_0_1|   ...|  D_7_23 | ... | foF2_0_0 |  ...  | foF2_7_23 | res |
|-------: |------: |------:|------:|------:|------:  |------:|------:|------:|
| Value of parameter D at 0 day before the earthquake at 00:00 |  Value of parameter D at 0 day before the earthquake at 01:00 | ... | Value of parameter D at 7 day before the earthquake at 23:00  |  ... | Value of parameter foF2 at 0 day before the earthquake at 00:00    | ...   | Value of parameter foF2 at 7 day before the earthquake at 23:00  | target value 0 - no earthquake, 1 - is earthquake  |
 

The other version of the same data with 30 minutes data samples which were not flattened and were used for NN model is located at `NOAA/datasets_NN_model/sondes_in_ml.csv` (should be taken as positive sample) and `NOAA/datasets_NN_model/sondes_out_ml.csv` (should be taken as negative sample)

The structure of the file is presented below, where `id` is an earthquake id, `h` and `m` - time:

| foF2   |   D     |  M(D)      |  ...|  id         | date    | nday   |  h    | m      | 
|-------:  |------:|------:|------:   |------:       |------: |------:  |------:|------:|
| Value of parameter foF2  |   Value of parameter D|  Value of parameter M(D) | ... | earthquake id | date | days before the earthquake  |hour  | minute  |


#### Time-formed dataset

The data from sondes inside the preparation zone are positive samples. Then in order to create negative samples we took data from the same sondes but 1 year ago of 1 year after the earthquake (in case if there were no other earthquakes registered at that time). 

Then the data was aggregated by an hour and flatten in a way that 1 earthquke is 1 sample (1 row) to run the LinearRegression. The file is located in the `NOAA/datasets_LR_model/flattened_ds_y_ago_y_after_7days.csv`

The other version of the same data with 30 minutes data samples which was not flattened and was used for NN model is located at `NOAA/datasets_NN_model/sondes_in_ml.csv and sondes_year_before_after_ml.csv`

The files have the same structure as the Location formed dataset.

All the datasets are stored in .csv format with separator = ','

### Principal component analysis 

We used Principal component analysis as a new approach to creating a feature for earthquake prediction. You can find precalculated features in `predictors/pca/pca_components.csv` and the pipeline for calculation in the `predictors/pca/ pca_calculation.ipynb`. The data was normalized before the components were calculated.

The table has the following format:
| id   |   date     |  nday                          |  h|  m         | foF2   | h'Es   |  comp_1    | comp_2     | 
|-------:  |------:|------:|------:   |------:  |------: |------:  |------:|------:|
| earthquake id |   date| days before the earthquake  | hour | minute | Value of parameter foF2  | Value of parameter h'Es  | component 1  | component 2  |

### Models
Several different modes were used for feature selection and feature creation (PCA).

#### Linear Regression + PCA

This experiment and models is at `models/PCA_Logistic_Rigression.ipynb`

#### Linear Regression + L1 regularisation

Feature selection with L1 regularization id at `models/L1_feature_selection.ipynb`

#### Neural network

Feature selection with NN regularization id at `models/NN_ablation_test.ipynb`

The Neural network architecture is described at the image below:

<img src="imgs/Model_FC_eng.png" width="300">

## Acknowledgments

* The data from NOAA was taken from <em>https://github.com/DaryaChaplygina/ionoshpere_dataset</em> 
* This research was inspired by the work above
