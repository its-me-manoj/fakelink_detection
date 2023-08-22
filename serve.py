from flask import Flask, render_template, request
import pandas as pd
from joblib import load
from google_ranking import google_ranking

app = Flask(__name__)

lr = load('model.joblib')
scaler = load('scaler.joblib')

@app.route('/', methods=['POST', 'GET'])
def index():
    prediction = None
    error_message = None
    if request.method == 'POST':
        url = request.form.get('url')

        website_data_df = google_ranking(url)

        if website_data_df is not None:

            if isinstance(website_data_df, dict) and 'error' in website_data_df:
                error_message = website_data_df['error']
            else:
                website_data_df.fillna(0, inplace=True)
                print(website_data_df.shape)  

                website_data_scaled = scaler.transform(website_data_df)

                prediction = int(lr.predict(website_data_scaled)[0])

                print(prediction)

    return render_template('index.html', prediction=prediction, error_message=error_message)




if __name__ == '__main__':
    app.run(debug=True)