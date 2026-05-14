import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
import joblib

def evaluate_model(y_true, y_pred, model_name):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    print(f"--- {model_name} ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}\n")
    return {'model': model_name, 'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}

def main():
    print("Loading dataset...")
    try:
        df = pd.read_csv("dataset.csv")
    except FileNotFoundError:
        print("Error: dataset.csv not found. Please run data_generation.py first.")
        return

    # Assuming 'label' is the target column
    X = df.drop('label', axis=1)
    y = df['label']

    print("Splitting dataset into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize models
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    xgb_model = XGBClassifier(eval_metric='logloss', random_state=42)
    svm_model = SVC(probability=True, random_state=42)

    models = {
        "Random Forest": rf_model,
        "XGBoost": xgb_model,
        "SVM": svm_model
    }

    results = []

    print("Training models...\n")
    best_f1 = 0
    best_model = None
    best_model_name = ""

    for name, model in models.items():
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Evaluate
        res = evaluate_model(y_test, y_pred, name)
        results.append(res)
        
        # Select best model based on F1 Score
        if res['f1'] > best_f1:
            best_f1 = res['f1']
            best_model = model
            best_model_name = name

    print(f"Best Model based on F1 Score: {best_model_name} (F1: {best_f1:.4f})")
    
    # Save the best model
    model_filename = "best_model.pkl"
    joblib.dump(best_model, model_filename)
    print(f"Saved the best model to {model_filename}")

if __name__ == "__main__":
    main()
