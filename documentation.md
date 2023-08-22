# PhishGuard: An Online Phishing Detection System

## Project Structure

The project consists of four Python scripts and a directory for HTML templates:

1. `serve.py` - This is the main Flask application file. It includes the web server's routing logic.

2. `google_ranking.py` - This script includes the function for extracting various features from a given URL. These features are used by the machine learning model to make predictions.

3. `train.py` - This script includes the code to train the machine learning model.

4. `inference.py` - This script includes the code to make predictions using the trained machine learning model.

5. `templates` - This directory includes HTML templates for rendering the web pages.

### serve.py

This script sets up the Flask application, including routing for the main page. It uses POST and GET methods to receive URLs from users and return the prediction results.

### google_ranking.py

The `google_ranking()` function in this script takes a URL as input and extracts various features that can indicate whether it's a phishing URL. These features include the length of the URL, the number of dots in the URL, presence of IP address, phishing hints, Google index status, and others.

### train.py

This script includes code for training the machine learning model. The training process includes data pre-processing, splitting the data into training and testing sets, model training, and saving the trained model for later use.

### inference.py

The `load_model()` function in this script is used to load the trained model, and the `predict()` function uses this model to predict whether a given URL is a phishing site or not.

### templates/index.html

This is the main webpage of the application. Users can enter a URL into the form on this page. The prediction result or error message will be displayed on this page.

## How to Use

To use PhishGuard, simply start the server by running the `serve.py` script. Then, open your web browser and go to `http://localhost:5000` (or the appropriate IP and port if you're not running locally). Enter a URL into the form and click "Inspect URL". The system will analyze the URL and display whether it is likely to be a phishing site or not.

Please note that you need to train the model before running the server, which you can do by running the `train.py` script.

## Requirements

PhishGuard requires Python 3.6+ and the following libraries:

- Flask
- numpy
- pandas
- scikit-learn
- requests
- BeautifulSoup
- tldextract
- python-whois
- googlesearch-python