import numpy as np
import pandas as pd

# scikit for building model and testing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, LabelEncoder
from sklearn.model_selection import train_test_split

# Serialises model for use in flask server
import pickle

from scraping import getListings

df = pd.read_csv('dataset.csv')
df = df.dropna()

# ***** Clean DataFrame (Remove Outliers) *****

# Create new input feature called Price Per Meter
df['Price_per_meter'] = df['Price'] / df['Size (in meters)']

def remove_PPM_outliers(df):
    df_out = pd.DataFrame()
    for i, subdf in df.groupby('Type'):
        mean = np.mean(subdf.Price_per_meter)
        std_dev = np.std(subdf.Price_per_meter)
        reduced_df = subdf[(subdf.Price_per_meter>(mean-std_dev)) & (subdf.Price_per_meter<=(mean+std_dev))]
        df_out = pd.concat([df_out,reduced_df],ignore_index=True)
    return df_out

df = remove_PPM_outliers(df)

# Data Seperation as X and Y
y = df['Price'] / 1000000
X = df.drop(columns=['Price_per_meter', 'Price'], axis=1)

# Convert Y to 2D
y = y.values.ravel()

# Encoding caterogical input variables into numerical representations
type_hierarchy = ["STUDIO", "APARTMENT", "TWIN HOUSE", "STANDALONE VILLA"]
type_encoder = LabelEncoder()
type_encoder.fit(type_hierarchy)

# Encoding 'Type'
X['Type'] = type_encoder.transform(X['Type'])

# Get 60% of the dataset as the training set. Store the rest in tmp variables
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=1)

### Applying feature scaling ###
scaler = StandardScaler()

# Training Set
X_train_scaled = scaler.fit_transform(X_train)

# Test Set
X_test_scaled = scaler.transform(X_test)


poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train_scaled)
X_test_poly = poly.transform(X_test_scaled)


model_poly = LinearRegression()
model_poly.fit(X_train_poly, y_train)


def predict_price(area, bedrooms, bathrooms, unit_type):
    encoded_unit_type = type_encoder.transform([unit_type])[0]
    x = np.zeros(len(X.columns))
    x[0] = area
    x[1] = bedrooms
    x[2] = bathrooms
    x[3] = encoded_unit_type

    scaled_x = scaler.transform([x])
    scaled_poly_x = poly.transform(scaled_x)
    return model_poly.predict(scaled_poly_x)[0]


# Save the model to a file
pickle.dump(model_poly, open("model.pkl", "wb"))
