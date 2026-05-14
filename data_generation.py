import pandas as pd
import random
from feature_extraction import extract_features_df

def generate_synthetic_urls(num_samples=1000):
    legitimate_domains = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "apple.com", "microsoft.com",
        "github.com", "stackoverflow.com", "reddit.com", "netflix.com", "yahoo.com"
    ]
    
    phishing_keywords = [
        "login", "verify", "update", "secure", "account", "banking", "confirm", 
        "password", "free", "admin", "support", "service", "webscr", "billing"
    ]
    
    urls = []
    labels = []
    
    for _ in range(num_samples // 2):
        # Generate Legitimate URL
        domain = random.choice(legitimate_domains)
        protocol = "https" if random.random() > 0.1 else "http"
        path_length = random.randint(0, 3)
        path = "/".join(["".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5)) for _ in range(path_length)])
        url = f"{protocol}://www.{domain}/{path}"
        urls.append(url)
        labels.append(0)  # 0 for Legitimate
        
    for _ in range(num_samples // 2):
        # Generate Phishing URL
        protocol = "http" if random.random() > 0.3 else "https"
        
        # Sometimes use IP instead of domain
        if random.random() > 0.7:
            domain = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        else:
            base_domain = random.choice(legitimate_domains)
            # Typosquatting or subdomain trickery
            trick = random.choice(["-", ".", ""])
            kw = random.choice(phishing_keywords)
            domain = f"{kw}{trick}{base_domain}"
            if random.random() > 0.5:
                domain = f"www.{domain}"
                
        path = random.choice(phishing_keywords) + ".php?id=" + str(random.randint(1000, 9999))
        
        url = f"{protocol}://{domain}/{path}"
        urls.append(url)
        labels.append(1)  # 1 for Phishing

    # Shuffle the dataset
    combined = list(zip(urls, labels))
    random.shuffle(combined)
    urls, labels = zip(*combined)
    
    return list(urls), list(labels)

if __name__ == "__main__":
    print("Generating synthetic URLs...")
    urls, labels = generate_synthetic_urls(2000)
    
    print("Extracting features (this may take a few seconds)...")
    df = extract_features_df(urls)
    df['label'] = labels
    
    df.to_csv("dataset.csv", index=False)
    print(f"Generated dataset with {len(df)} samples and saved to 'dataset.csv'.")
    print(df.head())
