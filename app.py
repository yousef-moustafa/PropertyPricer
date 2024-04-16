from model import predict_price
from flask import Flask, render_template, request
import pickle

# Configure application
app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

TYPES = ["STUDIO", "APARTMENT", "TWIN HOUSE", "STANDALONE VILLA"]
BEDROOMS = [str(i) for i in range (1,11)]
BATHROOMS = [str(i) for i in range (1,11)]
AREAS =[str(i) for i in range(20, 2001, 10)]
LOCATION = {'district': None, 'lat': None, 'lng': None}
DETAILS = [
    {'name': "type", 'values': TYPES},
    {'name': "bedroom", 'values': BEDROOMS},
    {'name': "bathroom", 'values': BATHROOMS},
    {'name': "area", 'values': AREAS},
]

@app.route('/')
def index():
    return render_template('index.html', types=TYPES, bedrooms=BEDROOMS, bathrooms=BATHROOMS)

@app.route('/getDetails', methods=["POST"])
def getDetails():
    input = {}
    for dict in DETAILS:
        value = request.form.get(dict['name'])
        if not value or value not in dict['values']:
            error_message = "Please input a suitable value for " + str(dict['name'])
            return render_template('error.html', error_message=error_message)
        input[dict['name']] = value
    for data in LOCATION:
        value = request.form.get(data)
        if not value:
            error_message = "Please select a location from the map"
            return render_template('error.html', error_message=error_message)
        LOCATION[data] = value
    input['location'] = LOCATION['district']
    prediction = predict_price(input['area'], input['bedroom'], input['bathroom'], input['type']) * 1000000
    return render_template('dashboard.html', data=input, predicted_price=prediction)
