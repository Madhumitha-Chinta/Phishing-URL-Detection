import re
from urllib.parse import urlparse
import tldextract
import pandas as pd

def extract_features(url):
    """
    Extracts features from a given URL string.
    Returns a dictionary of features.
    """
    features = {}
    
    # Basic URL length features
    features['url_length'] = len(url)
    
    # Parse URL
    try:
        parsed_url = urlparse(url)
        features['hostname_length'] = len(parsed_url.netloc) if parsed_url.netloc else 0
        features['path_length'] = len(parsed_url.path) if parsed_url.path else 0
    except Exception:
        features['hostname_length'] = 0
        features['path_length'] = 0

    # Presence of IP address in the URL
    # IPv4 regex
    ipv4_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])'
    )
    features['has_ip'] = 1 if ipv4_pattern.search(url) else 0
    
    # Character counts
    features['count_dot'] = url.count('.')
    features['count_at'] = url.count('@')
    features['count_dash'] = url.count('-')
    features['count_slash'] = url.count('/')
    features['count_question_mark'] = url.count('?')
    features['count_equals'] = url.count('=')
    
    # HTTPS
    features['has_https'] = 1 if url.startswith("https://") else 0
    
    # TLD extract features
    ext = tldextract.extract(url)
    features['count_subdomains'] = ext.subdomain.count('.') + 1 if ext.subdomain else 0
    
    # Suspicious words
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm', 'password', 'free']
    lower_url = url.lower()
    features['count_suspicious_words'] = sum(1 for word in suspicious_words if word in lower_url)
    
    return features

def extract_features_df(url_list):
    """
    Extracts features for a list of URLs and returns a pandas DataFrame.
    """
    feature_list = [extract_features(url) for url in url_list]
    return pd.DataFrame(feature_list)

if __name__ == "__main__":
    # Test
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/login.php",
        "http://secure-update-account-paypal.com/verify",
        "https://github.com/login"
    ]
    df = extract_features_df(test_urls)
    print(df.head())
