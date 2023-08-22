import pandas as pd
from joblib import load
from google_ranking import google_ranking
import numpy as np

# Load your model and scaler
lr = load('model.joblib')
scaler = load('scaler.joblib')

# Load the dataset_phishing.csv file
phishing_df = pd.read_csv('dataset_phishing.csv')

# Create a DataFrame for the results with two separate columns for legitimate and phishing URLs
results_df = pd.DataFrame(columns=['legitimate', 'phishing'])

# Save the column names (headers) to the CSV file before the loop
results_df.to_csv('results.csv', index=False)

# Initialize counter
counter = 0

# Iterate over the URLs in the 'url' column
for url in phishing_df['url']:
    try:
        # Fetch website data
        website_data_df = google_ranking(url)
        if website_data_df is None:
            print("No data was returned from the website.")
            continue
        elif 'error' in website_data_df:
            print(f"Error while accessing website: {website_data_df['error']}")
            continue
        # Scale the data and predict
        website_data_scaled = scaler.transform(website_data_df)
        prediction = lr.predict(website_data_scaled)
        # Classify the URL based on the prediction and add to appropriate column
        if prediction == 1:
            results_df = pd.DataFrame({'legitimate': [np.nan], 'phishing': [url]})
        else:
            results_df = pd.DataFrame({'legitimate': [url], 'phishing': [np.nan]})
    except Exception as e:
        print(f"An error occurred during the inference process: {str(e)}")
        continue

    # Append the result to the CSV file
    results_df.to_csv('results.csv', mode='a', header=False, index=False)
    counter += 1
    print(f"Processed URLs: {counter}")
