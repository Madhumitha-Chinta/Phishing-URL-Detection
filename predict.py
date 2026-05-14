import argparse
import joblib
from feature_extraction import extract_features_df

def predict_url(url):
    print(f"Analyzing URL: {url}\n")
    
    try:
        model = joblib.load("best_model.pkl")
    except FileNotFoundError:
        print("Error: best_model.pkl not found. Please run train_models.py first.")
        return

    # Extract features
    df_features = extract_features_df([url])
    
    # Reorder columns to match training set (if necessary), but here they match exactly
    # because feature_extraction.py yields dictionary keys in same order.
    
    # Predict
    prediction = model.predict(df_features)
    probability = model.predict_proba(df_features)[0] if hasattr(model, "predict_proba") else None
    
    result_label = "Phishing" if prediction[0] == 1 else "Legitimate"
    
    print(f"Prediction: **{result_label}**")
    
    if probability is not None:
        phishing_prob = probability[1] * 100
        legit_prob = probability[0] * 100
        print(f"Probability: {phishing_prob:.2f}% Phishing, {legit_prob:.2f}% Legitimate")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict if a URL is Phishing or Legitimate")
    parser.add_argument("url", type=str, help="The URL to analyze")
    args = parser.parse_args()
    
    predict_url(args.url)
