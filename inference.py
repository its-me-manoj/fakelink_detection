import pandas as pd
from joblib import load
from google_ranking import google_ranking
import numpy as np

lr = load('model.joblib')
scaler = load('scaler.joblib')

try:
    website_data_df = google_ranking("https://direct-bk-faq-reserved.is/aib/aibgsjsw5001")

    if website_data_df is None:
        print("No data was returned from the website.")
    elif 'error' in website_data_df:
        print(f"Error while accessing website: {website_data_df['error']}")
    else:
        website_data_scaled = scaler.transform(website_data_df)
        print(lr.predict(website_data_scaled))
except Exception as e:
    print(f"An error occurred during the inference process: {str(e)}")