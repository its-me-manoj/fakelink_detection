import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from joblib import dump

df = pd.read_csv(r"dataset_phishing.csv")

df['status'] = df['status'].astype('category')
df['status'] = df['status'].cat.codes
x = df.drop(columns=['status', 'url'])
x = x[['length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_qm', 'nb_eq',
       'nb_slash', 'nb_www', 'ratio_digits_url', 'ratio_digits_host',
       'tld_in_subdomain', 'prefix_suffix', 'shortest_word_host',
       'longest_words_raw', 'longest_word_path', 'phish_hints',
       'nb_hyperlinks', 'ratio_intHyperlinks', 'empty_title',
       'domain_in_title', 'domain_age', 'google_index', 'page_rank']]
y = df['status']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)

scalar = StandardScaler()
x_train_scale = scalar.fit_transform(x_train)
x_test_scale = scalar.transform(x_test) 

lr = LogisticRegression(solver='saga', max_iter=5000, tol=1e-5)
lr.fit(x_train_scale, y_train)

dump(lr, 'model.joblib')
dump(scalar, 'scaler.joblib')