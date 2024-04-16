# PropertyPricer
#### Video Demo:  <https://youtu.be/fzc0oWAwfW8?si=YyW_9a83fp_7h17s>
#### Description:
PropertyPricer is an innovative web platform designed to forecast property prices within Madinaty, a vibrant city nestled in Cairo, Egypt. Leveraging a robust Polynomial Regression Model fueled by an extensive dataset sourced from diverse real estate listings, our platform accurately predicts property values based on four primary features: Area, Bedrooms, Bathrooms, and Type. Our aim is to empower users with insightful property valuations, providing an informed perspective for buyers, sellers, and investors in Madinaty's dynamic real estate market.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Setting Up](#setting-up)
- [Usage](#usage)
- [File Explanations](#file-explanations)


## Features

- **Polynomial Regression Model:** Utilizes a robust polynomial regression model on real data extracted from diverse real estate listings.
- **Accurate Predictions:** Provides accurate property price forecasts based on key features such as Area, Bedrooms, Bathrooms, and Type.
- **Insightful Valuations:** Empowers users with valuable insights for making informed decisions in Madinaty's real estate market.
- **User Friendly Interface:** The HTML, CSS and JS used ensures simplicity. Having the option to select location from a map enhances the accessability and usability of the program.

## Setting Up
To set up and run the project locally, follow these steps:

### 1. Navigate to Project Directory
```
cd
cd project
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run the Application
```
flask run
```

## Usage
Here's how you can use PropertyPricer:

1. Open the application in your web browser.
2. Select your location from the map
3. Enter the required property features: Area, Bedrooms, Bathrooms, and Type.
4. Click on the 'Predict' button to get the forecasted property price.

## File Explanations

### 'model.py'
- Loads the dataset into a dataframe.
- Removes outliers and separates it into X input features and y target variable.
- Encodes the type of property using LabelEncoder.
- Splits the test set, performs feature scaling, and defines the function used for price prediction in app.py.

### 'model.pkl'
- The file which contains the loaded model

### 'app.py'
- Configures the Flask route with functions index() (loads the home page) and getDetails() (handles form submission)

### 'script.js'
- Creates the map, defines coordinates to set a GeoJSON border.
- Adds the map, marker, and reverseGeocoding functionality.
- Includes event listeners for element in the HTML file (Area).

### 'data.csv'
- Contains the dataset scraped from aqarmap, a property listing website used in Cairo.

### 'styles.css'
- Contains all the stylings of the webpage.

### 'layout.html'
- The layout used in the rest of the HTML files.

### 'requirements.txt'
- Contains all the necessary installations in order to run the program
