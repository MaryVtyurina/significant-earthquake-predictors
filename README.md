# significant-earthquake-predictors

This repository was created as a part of research in Saint Petersburg State University. We provide two types of datasets with cleaned data and filled NaNs. We also provide several model for feature selection.

### Prerequisites

You might need to install pytorch before running the models. https://pytorch.org

### Data

Data about earthquakes was taken from [USGS website](https://www.usgs.gov/natural-hazards/earthquake-hazards/earthquakes)

The ionisphere data was taken from:
* National centers for environmental information [NOAA](https://www.ngdc.noaa.gov/stp/iono/ionogram.html)
* National Institute of Information and Communication Technology in Japan [NICT](http://wdc.nict.go.jp/IONO/HP2009/ISDJ/index-E.html) 

### Missing values

The data with more than 50% of missing values was not concidered. 
The data was grouped by earthquake id, date and time and then the missing values were filled with mean of such group.

### Datasets

We applied two approaches when were creating the datasets.

1. Described in the [paper by Pulinets 2004](https://www.researchgate.net/publication/215972520_Ionospheric_Precursors_of_Earthquakes_Recent_Advances_in_Theory_and_Practical_Applications) this approched based on earthquake preparation zone. We consider pairs of sondes - one inside the preparation zone, the other one - outside. Then the data was flatten in a way that 1 earthquke is 1 sample (1 row). The file is located in the <em>NOAA/datasets_LR_model/flattened_ds_sondes_in_out_7days.csv</em>
The other version of the same data which was not flattened and can be used for NN model is located at <em>NOAA/datasets_NN_model/sondes_in_ml.csv and sondes_out_ml.csv</em>

2. We take data from sondes inside the preparation zone as positive samples. Then we took data from the same sondes but 1 year ago of 1 year after the earthquke (in case if there were no other earthquake registered at that time). Then the data was flatten in a way that 1 earthquke is 1 sample (1 row) to run the LinearRegression. The file is located in the <em>NOAA/datasets_LR_model/flattened_ds_y_ago_y_after_7days.csv</em>
The other version of the same data which was not flattened and was used for NN model is located at <em>NOAA/datasets_NN_model/sondes_in_ml.csv and sondes_year_before_after_ml.csv</em>

### Models
Several different modes were used for feature selection and feature creation (PCA).

#### Linear Regression + PCA

This experiment and models is at <em>models/PCA_Logistic_Rigression.ipynb</em>

#### Linear Regression + L1 regularisation

Feature selection with L1 regularization id at <em>models/L1_feature_selection.ipynb</em>

#### Neural network

Feature selection with NN regularization id at <em>models/NN_ablation_test.ipynb</em>

The Neural network architecture is described at the image below:
![NN schema](imgs/Model_FC_eng.png)
## Acknowledgments

* The data from NOAA was taken from <em>https://github.com/DaryaChaplygina/ionoshpere_dataset</em> 
* This research was inspired by the work above
