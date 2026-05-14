# Phishing URL Detection

A machine learning pipeline designed to detect phishing URLs. This project extracts various lexical and structural features from URLs and trains multiple classifiers (Random Forest, XGBoost, and Support Vector Machines) to classify them as either Phishing or Legitimate.

## Project Structure

- `data_generation.py`: Generates a synthetic dataset of legitimate and phishing URLs and extracts their features into a CSV file (`dataset.csv`).
- `feature_extraction.py`: Contains the core logic for extracting features from a URL (e.g., URL length, domain length, presence of IP address, use of HTTPS, presence of suspicious keywords).
- `train_models.py`: Trains Random Forest, XGBoost, and SVM models on the generated dataset. It evaluates the models based on Accuracy, Precision, Recall, and F1 Score, and automatically saves the best performing model as `best_model.pkl`.
- `predict.py`: A command-line script to predict whether a given URL is phishing or legitimate using the trained `best_model.pkl`.
- `requirements.txt`: A list of required Python dependencies for the project.

## Installation

1. Clone this repository or download the project files.
2. Ensure you have Python installed (3.7+ recommended).
3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

### 1. (Optional) Generate Dataset
If you want to generate a new dataset of synthetic URLs, you can run the data generation script. (A default `dataset.csv` may already be provided).

```bash
python data_generation.py
```
This will create `dataset.csv` containing extracted features and labels (0 for Legitimate, 1 for Phishing).

### 2. Train Models
Run the training script to train the classifiers and select the best model. 

```bash
python train_models.py
```

**Example Output:**
```
Loading dataset...
Splitting dataset into training and testing sets...
Training models...

--- Random Forest ---
Accuracy:  1.0000
Precision: 1.0000
Recall:    1.0000
F1 Score:  1.0000

--- XGBoost ---
Accuracy:  1.0000
Precision: 1.0000
Recall:    1.0000
F1 Score:  1.0000

--- SVM ---
Accuracy:  1.0000
Precision: 1.0000
Recall:    1.0000
F1 Score:  1.0000

Best Model based on F1 Score: Random Forest (F1: 1.0000)
Saved the best model to best_model.pkl
```

This script will output the performance metrics for Random Forest, XGBoost, and SVM, and save the model with the highest F1 Score to `best_model.pkl`.

### 3. Predict a URL
Use the prediction script to test individual URLs. Pass the URL as an argument in the terminal.

```bash
python predict.py "http://example.com"
```

**Example Output:**
```
Analyzing URL: http://example.com

Prediction: **Legitimate**
Probability: 20.00% Phishing, 80.00% Legitimate
```

## Features Extracted
The model relies on several features extracted directly from the URL string, such as:
- URL and Domain Length
- Presence of an IP Address instead of a domain name
- Protocol used (HTTP vs HTTPS)
- Count of specific characters (`@`, `-`, `.`, `//`)
- Presence of suspicious keywords often used in phishing (e.g., 'login', 'verify', 'update')

