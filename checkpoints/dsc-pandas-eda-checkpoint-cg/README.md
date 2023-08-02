# Pandas EDA Checkpoint

This checkpoint is designed to test your understanding of the content from the EDA with Pandas Cumulative Lab.

Specifically, this will cover:

* Using pandas to load data
* Using pandas to engineer a new feature of a dataset
* Using pandas methods and attributes to access information about a dataset


## Your Task: Explore Price per Square Foot and Neighborhoods using `pandas`

### Data Understanding

In this repository under the file path `ames_housing.csv` there is a CSV file containing the Ames Housing dataset. This is the same dataset you have worked with previously, but the file path may differ!

The features of interest for this analysis will be:

**SalePrice**: `Sale price of the house in dollars`

**GrLivArea:** `Above grade (ground) living area square feet`

**Neighborhood:** `Physical locations within Ames city limits`

### Requirements

#### 1. Import the Relevant Library

#### 2. Load the Data into a DataFrame Called `housing_data`

#### 3. Create a New Column `price_per_square_ft`

#### 4. Find the Mean Price per Square Foot

#### 5. Plot Price per Square Foot for Select Neighborhoods

#### 6. Find the Most Common Neighborhood

## 1. Import the Relevant Library

In the cell below, import the `pandas` library using the standard alias `pd`.


```python
# CodeGrade step1
# Import pandas with the standard alias.

```

## 2. Load the Data into a DataFrame Called `housing_data`

The file path is `ames_housing.csv`. Use pandas ([documentation here](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)) to read in the data from this CSV file and create a dataframe named `housing_data`.


```python
# CodeGrade step2
# Replace None with appropriate code

housing_data = None

housing_data.head()
```


```python
assert type(housing_data) == pd.DataFrame
```

## 3. Create a New Column `price_per_square_ft`

Create a new column of the dataframe that represents the price per square foot of the house.

Here you define price per square foot as the `SalePrice` divided by the `GrLivArea`.

The new column should be called `price_per_square_ft`.


```python
# CodeGrade step3
# Put your code here!


```


```python
assert "price_per_square_ft" in housing_data.columns
```

## 4. Find the Mean Price per Square Foot

Assign the value of the mean price per square foot to the variable `mean_price_per_square_ft`.


```python
# CodeGrade step4
# Replace None with appropriate code

mean_price_per_square_ft = None
```


```python
import numpy as np
# mean price per square foot should be a floating point number
assert (type(mean_price_per_square_ft) == float) or (type(mean_price_per_square_ft) == np.float64)
```

## 5. Plot Price per Square Foot for Select Neighborhoods

The plotting code in the cell below is mostly completed for you. You are creating a bar graph showing the average price per square foot by neighborhood, for six specific neighborhoods in west Ames.

You will use `pd.DataFrame.plot.bar` ([documentation here](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.bar.html)).

What is the name of the column (as a string) that you would put into the `x` and `y` parameters of this graph?

The plot this creates should look like this:

![neighborhood plot](neighborhood_plot.png)

(Don't worry too much about the subsetting and grouping that is happening here. `x` and `y` are column names that exist in the full `housing_data` dataframe as well as the `grouped_by_neighborhood` subset.)


```python
# CodeGrade step5
# Replace None with appropriate code
# Remember: x and y should be strings!

x = None
y = None

# Plotting code (do not edit)
subset = housing_data[housing_data["Neighborhood"].isin([
    "SawyerW", "Sawyer", "ClearCr", "CollgCr", "Edwards", "SWISU"
])]
grouped_by_neighborhood = subset.groupby("Neighborhood").mean().reset_index()
ax = grouped_by_neighborhood.plot.bar(x=x, y=y, rot=0, title="Prices per Square Foot in West Ames");
```


```python
# x and y should be strings
assert type(x) == str
assert type(y) == str

# x and y should be names of columns
assert x in housing_data.columns
assert y in housing_data.columns
```

## 6. Find the Most Common Neighborhood

Using the `Neighborhood` column, find the name of the neighborhood that occurs most frequently in this dataset.

Assign `name` to the name of the neighborhood (a string) and `frequency` to the number of times that neighborhood appears (an integer).

If you're getting stuck, check out [this method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html). Your answer can be "hard-coded" (i.e. just typed in surrounded by `"`) or you can find it programmatically.

**Caution**: Because of the names of some of the neighborhoods in Ames, there is potential for confusion. Be aware that *North Ames* and *Northwest Ames* appear, shortened to "NAmes" and to "NWAmes", respectively.


```python
# CodeGrade step6
# Replace None with appropriate code

name = None
frequency = None
```


```python
# name should be a string
assert type(name) == str

# frequency should be an integer
assert type(frequency) == int or type(frequency) == np.int64
```
