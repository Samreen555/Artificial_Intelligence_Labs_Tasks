"""
preprocessing.py
================
Data Engineering Layer for Smart Agriculture Decision Support System.
Handles loading, cleaning, feature engineering, and splitting of the
Crop Recommendation dataset.

Author  : BSE-6 Student, Bahria University Islamabad
Course  : Artificial Intelligence (CLO-2 OEL)
Version : 1.0.0
"""

import os 
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
FEATURE_COLS  = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
TARGET_CLASS  = 'label'
TARGET_YIELD  = 'yield'
RANDOM_STATE  = 42

DATA_DICTIONARY = {
    'N':           'Ratio of Nitrogen content in soil (kg/ha)',
    'P':           'Ratio of Phosphorous content in soil (kg/ha)',
    'K':           'Ratio of Potassium content in soil (kg/ha)',
    'temperature': 'Temperature in degree Celsius (°C)',
    'humidity':    'Relative humidity in percentage (%)',
    'ph':          'pH value of the soil (0–14)',
    'rainfall':    'Rainfall in mm',
    'label':       'Target crop recommendation (22 crop classes)',
    'yield':       'Estimated crop yield in quintals/hectare (q/ha)',
}


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────
def load_dataset(filepath: str) -> pd.DataFrame:
    """Load CSV and perform a structural integrity check."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    df = pd.read_csv(filepath)
    required = set(FEATURE_COLS + [TARGET_CLASS])
    missing  = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")
    print(f"[✓] Loaded dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Impute numeric missing values with column median."""
    df = df.copy()
    for col in FEATURE_COLS:
        n_miss = df[col].isnull().sum()
        if n_miss > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"  [Imputed] {col}: {n_miss} missing → median={median_val:.3f}")
    return df


def handle_outliers(df: pd.DataFrame, method: str = 'iqr') -> pd.DataFrame:
    """
    Clip extreme values using the IQR fence method.
    Values beyond [Q1 - 1.5·IQR, Q3 + 1.5·IQR] are clamped.
    """
    df = df.copy()
    for col in FEATURE_COLS:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = df[col].clip(lower, upper)
        if n_outliers:
            print(f"  [Outlier] {col}: {n_outliers} values clamped to [{lower:.2f}, {upper:.2f}]")
    return df


def encode_labels(df: pd.DataFrame):
    """Fit a LabelEncoder on the crop label column. Returns (df, encoder)."""
    le = LabelEncoder()
    df = df.copy()
    df['label_encoded'] = le.fit_transform(df[TARGET_CLASS])
    print(f"[✓] Encoded {len(le.classes_)} crop classes")
    return df, le


def scale_features(X: pd.DataFrame):
    """Standard-scale feature matrix. Returns (X_scaled, scaler)."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return pd.DataFrame(X_scaled, columns=X.columns), scaler


def ensure_yield_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    If 'yield' column is absent, generate a synthetic but agronomically
    plausible yield value using a weighted linear combination + per-crop
    baseline noise.  This is used for the Linear Regression module.
    """
    if TARGET_YIELD in df.columns:
        return df
    df = df.copy()
    np.random.seed(RANDOM_STATE)

    CROP_YIELD_BASE = {
        'rice':38,'maize':55,'chickpea':18,'kidneybeans':22,'pigeonpeas':15,
        'mothbeans':12,'mungbean':14,'blackgram':13,'lentil':16,'pomegranate':20,
        'banana':180,'mango':60,'grapes':85,'watermelon':110,'muskmelon':90,
        'apple':45,'orange':55,'papaya':120,'coconut':70,'cotton':25,
        'jute':32,'coffee':8
    }

    base  = df[TARGET_CLASS].map(CROP_YIELD_BASE).fillna(30)
    noise = np.random.normal(0, base * 0.08)

    df[TARGET_YIELD] = (
        base
        + 0.05 * df['N']
        + 0.04 * df['P']
        + 0.03 * df['K']
        + 0.20 * df['temperature']
        + 0.02 * df['humidity']
        - 1.50 * (df['ph'] - 6.5) ** 2
        + 0.01 * df['rainfall']
        + noise
    ).clip(1, 350).round(2)

    print("[✓] Synthetic yield column generated")
    return df


def prepare_pipeline(data_path: str, test_size: float = 0.20):
    """
    Full preprocessing pipeline.

    Returns
    -------
    dict with keys:
        df_raw, df_clean, le, scaler,
        X_train, X_test, y_clf_train, y_clf_test,
        y_reg_train, y_reg_test
    """
    print("\n━━━ Data Engineering Layer ━━━")
    df = load_dataset(data_path)
    df = handle_missing_values(df)
    df = handle_outliers(df)
    df = ensure_yield_column(df)
    df, le = encode_labels(df)

    X_raw = df[FEATURE_COLS]
    X_scaled, scaler = scale_features(X_raw)

    y_clf = df['label_encoded'].values
    y_reg = df[TARGET_YIELD].values

    # Classification splits (stratified)
    X_tr, X_te, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
        X_scaled, y_clf, y_reg,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y_clf
    )

    print(f"[✓] Train: {X_tr.shape[0]:,}  |  Test: {X_te.shape[0]:,}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    return dict(
        df_raw     = df,
        le         = le,
        scaler     = scaler,
        X_full     = X_scaled,
        X_train    = X_tr,
        X_test     = X_te,
        y_clf_train= yc_tr,
        y_clf_test = yc_te,
        y_reg_train= yr_tr,
        y_reg_test = yr_te,
    )


def save_artifacts(le, scaler, models_dir: str):
    """Persist label encoder and scaler to disk."""
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(le,     os.path.join(models_dir, 'label_encoder.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    print(f"[✓] Artifacts saved → {models_dir}")


def load_artifacts(models_dir: str):
    """Reload label encoder and scaler from disk."""
    le     = joblib.load(os.path.join(models_dir, 'label_encoder.pkl'))
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    return le, scaler
