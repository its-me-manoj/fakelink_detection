import requests
from bs4 import BeautifulSoup
import tldextract
import socket
from datetime import datetime
from googlesearch import search
import pandas as pd
import whois
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def google_ranking(url):

    if "https://" not in url and "http://" not in url:  
        url = "https://" + url

    if url == "":
        print("Empty URL provided.")
        return None

    try:
        print(url)
        response = requests.get(url)
        html = response.content
        result = 1
    except requests.exceptions.RequestException as e:
        print(f"Failed to send a GET request to the URL due to the following error: {e}")
        return {
            "error": "Failed to connect to the URL. Please make sure the URL is correct and try again."
        }


    soup = BeautifulSoup(html, 'html.parser')

    length_url = len(url)

    hostname = tldextract.extract(url).domain
    length_hostname = len(hostname)

    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = 0

    nb_dots = url.count('.')

    nb_qm = url.count('?')

    nb_eq = url.count('=')

    nb_slash = url.count('/')

    nb_www = url.count('www')

    ratio_digits_url = sum(c.isdigit() for c in url) / len(url)

    ratio_digits_host = sum(c.isdigit() for c in hostname) / len(hostname)

    tld_in_subdomain = int(tldextract.extract(url).subdomain.count('.') > 0)

    prefix_suffix = int(bool(hostname.startswith('www.') or hostname.endswith('.com')))

    shortest_word_host = min(len(word) for word in hostname.split('.'))

    try:
        longest_words_raw = max(len(word) for word in soup.get_text().split())
        longest_word_path = max(len(word) for word in url.split('/'))
    except:
        longest_words_raw = 0
        longest_word_path = 0

    phish_hints_list = ['login', 'signin', 'verify', 'banking', 'password', 'security', 'update', 'support']
    phish_hints = int(any(i in url for i in phish_hints_list))

    try:
        nb_hyperlinks = len(soup.find_all('a'))
    except Exception as e:
        print(f"Failed to count the number of hyperlinks on the page: {e}")
        nb_hyperlinks = 0

    domain = tldextract.extract(url).registered_domain

    try:
        internal_links = [link.get('href') for link in soup.find_all('a') if
                        tldextract.extract(link.get('href')).registered_domain == domain]
    except:
        internal_links = []

    if nb_hyperlinks != 0:
        ratio_intHyperlinks = len(internal_links) / nb_hyperlinks
    else:
        ratio_intHyperlinks = 0

    try:
        empty_title = int(bool(soup.title.string))
    except:
        empty_title = 0

    try:
        domain_in_title = int(bool(domain in soup.title.string))
    except:
        domain_in_title = 0

    try:
        whois_info = whois.whois(url)
        if 'creation_date' in whois_info:
            domain_age = (datetime.now().date() - whois_info['creation_date'].date()).days
        else:
            domain_age = 0
    except:
        domain_age = 0

    try:
        google_index = int('google.com' in requests.get(f"https://www.google.com/search?q={url}").text)
    except:
        google_index = 0

    try:
        search_results = list(search(f"info:{url}", num=1))
        page_rank = 0
        if search_results:
            page_rank_url = search_results[0]
            if 'google.com' in page_rank_url:
                page_rank = 1
    except:
        page_rank = 0

    input_df = pd.DataFrame({
        'length_url': [length_url],
        'length_hostname': [length_hostname],
        'ip': [ip],
        'nb_dots': [nb_dots],
        'nb_qm': [nb_qm],
        'nb_eq': [nb_eq],
        'nb_slash': [nb_slash],
        'nb_www': [nb_www],
        'ratio_digits_url': [ratio_digits_url],
        'ratio_digits_host': [ratio_digits_host],
        'tld_in_subdomain': [tld_in_subdomain],
        'prefix_suffix': [prefix_suffix],
        'shortest_word_host': [shortest_word_host],
        'longest_words_raw': [longest_words_raw],
        'longest_word_path': [longest_word_path],
        'phish_hints': [phish_hints],
        'nb_hyperlinks': [nb_hyperlinks],
        'ratio_intHyperlinks': [ratio_intHyperlinks],
        'empty_title': [empty_title],
        'domain_in_title': [domain_in_title],
        'domain_age': [domain_age],
        'google_index': [google_index],
        'page_rank': [page_rank]
    })
    
    print(input_df)
    return input_df