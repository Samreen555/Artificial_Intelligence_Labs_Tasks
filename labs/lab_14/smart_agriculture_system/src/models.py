"""
models.py
=========
Algorithmic Core for the Smart Agriculture Decision Support System.
Contains three mandatory model modules:
  1. Decision Tree Classifier  – crop recommendation
  2. KMeans Clustering (KNN-style) – soil zone segmentation
  3. Linear Regression  – crop yield prediction

Author  : BSE-6 Student, Bahria University Islamabad
Course  : Artificial Intelligence (CLO-2 OEL)
Version : 1.0.0
"""
 
import os
import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    silhouette_score, davies_bouldin_score,
    mean_squared_error, mean_absolute_error, r2_score
)

FEATURE_COLS = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
RANDOM_STATE = 42
N_CLUSTERS   = 5   # soil zones


# ═══════════════════════════════════════════════════════════════
# MODULE 1 – Decision Tree Classifier
# ═══════════════════════════════════════════════════════════════
def train_decision_tree(X_train, y_train,
                        max_depth=12, min_samples_split=4,
                        min_samples_leaf=2, criterion='gini'):
    """
    Train a tuned Decision Tree Classifier.
    Returns the fitted model.
    """
    model = DecisionTreeClassifier(
        max_depth          = max_depth,
        min_samples_split  = min_samples_split,
        min_samples_leaf   = min_samples_leaf,
        criterion          = criterion,
        class_weight       = 'balanced',
        random_state       = RANDOM_STATE,
    )
    model.fit(X_train, y_train)
    print("[✓] Decision Tree trained")
    return model


def evaluate_decision_tree(model, X_test, y_test, le):
    """
    Compute and return a metrics dictionary for the classifier.
    """
    y_pred = model.predict(X_test)
    metrics = dict(
        accuracy  = accuracy_score(y_test, y_pred),
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0),
        recall    = recall_score(y_test, y_pred,    average='weighted', zero_division=0),
        f1        = f1_score(y_test, y_pred,        average='weighted', zero_division=0),
        conf_mat  = confusion_matrix(y_test, y_pred),
        clf_report= classification_report(y_test, y_pred,
                                          target_names=le.classes_,
                                          zero_division=0),
        feature_importance = dict(zip(FEATURE_COLS, model.feature_importances_)),
        y_pred    = y_pred,
        y_test    = y_test,
    )
    print(f"[✓] DT  Accuracy={metrics['accuracy']:.4f}  "
          f"Precision={metrics['precision']:.4f}  "
          f"Recall={metrics['recall']:.4f}  "
          f"F1={metrics['f1']:.4f}")
    return metrics


# ═══════════════════════════════════════════════════════════════
# MODULE 2 – KMeans Soil Clustering (KNN-style zone segmentation)
# ═══════════════════════════════════════════════════════════════
def train_kmeans_clustering(X_full, n_clusters=N_CLUSTERS):
    """
    Segment soil profiles into homogeneous farm zones using KMeans.
    Returns the fitted KMeans model.
    """
    model = KMeans(
        n_clusters   = n_clusters,
        init         = 'k-means++',
        n_init       = 20,
        max_iter     = 500,
        random_state = RANDOM_STATE,
    )
    model.fit(X_full)
    print(f"[✓] KMeans clustering trained  (k={n_clusters})")
    return model


def find_optimal_k(X_full, k_range=range(2, 11)):
    """Return silhouette scores for each k to help select optimal clusters."""
    scores = {}
    for k in k_range:
        km     = KMeans(n_clusters=k, n_init=10, random_state=RANDOM_STATE)
        labels = km.fit_predict(X_full)
        scores[k] = silhouette_score(X_full, labels)
    return scores


def evaluate_clustering(model, X_full):
    """
    Compute clustering quality metrics.
    Returns metrics dict.
    """
    labels   = model.predict(X_full)
    sil      = silhouette_score(X_full, labels)
    db       = davies_bouldin_score(X_full.values
                                    if hasattr(X_full, 'values')
                                    else X_full, labels)
    inertia  = model.inertia_

    cluster_sizes = pd.Series(labels).value_counts().sort_index().to_dict()

    metrics = dict(
        silhouette       = sil,
        davies_bouldin   = db,
        inertia          = inertia,
        cluster_sizes    = cluster_sizes,
        labels           = labels,
        n_clusters       = model.n_clusters,
        centers          = model.cluster_centers_,
    )
    print(f"[✓] KMeans  Silhouette={sil:.4f}  Davies-Bouldin={db:.4f}  "
          f"Inertia={inertia:.1f}")
    return metrics


# ═══════════════════════════════════════════════════════════════
# MODULE 3 – Linear Regression Yield Predictor
# ═══════════════════════════════════════════════════════════════
def train_linear_regression(X_train, y_train, alpha=1.0):
    """
    Train a Ridge Regression model (regularised Linear Regression)
    for yield prediction.
    Returns the fitted model.
    """
    model = Ridge(alpha=alpha, fit_intercept=True, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    print("[✓] Linear (Ridge) Regression trained")
    return model


def evaluate_regression(model, X_test, y_test):
    """
    Compute and return regression performance metrics.
    """
    y_pred = model.predict(X_test)
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    mae    = mean_absolute_error(y_test, y_pred)
    r2     = r2_score(y_test, y_pred)

    # Residuals
    residuals = y_test - y_pred

    # Confidence bounds: ±1.96 * residual std
    std_resid  = residuals.std()
    ci_lower   = y_pred - 1.96 * std_resid
    ci_upper   = y_pred + 1.96 * std_resid

    metrics = dict(
        rmse       = rmse,
        mae        = mae,
        r2         = r2,
        residuals  = residuals,
        y_pred     = y_pred,
        y_test     = y_test,
        ci_lower   = ci_lower,
        ci_upper   = ci_upper,
        std_resid  = std_resid,
        coef       = dict(zip(FEATURE_COLS, model.coef_)),
    )
    print(f"[✓] Regression  RMSE={rmse:.4f}  MAE={mae:.4f}  R²={r2:.4f}")
    return metrics


# ═══════════════════════════════════════════════════════════════
# Serialization helpers
# ═══════════════════════════════════════════════════════════════
def save_model(model, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"  [Saved] {filepath}")


def load_model(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    return joblib.load(filepath)


# ═══════════════════════════════════════════════════════════════
# Inference helpers (used by GUI)
# ═══════════════════════════════════════════════════════════════
def predict_crop(dt_model, le, scaler, input_array: np.ndarray) -> str:
    """Return predicted crop name for a single input sample."""
    X_scaled = scaler.transform(input_array.reshape(1, -1))
    label_id = dt_model.predict(X_scaled)[0]
    return le.inverse_transform([label_id])[0]


def predict_cluster(km_model, scaler, input_array: np.ndarray) -> int:
    """Return cluster ID for a single input sample."""
    X_scaled = scaler.transform(input_array.reshape(1, -1))
    return int(km_model.predict(X_scaled)[0])


def predict_yield(reg_model, scaler, input_array: np.ndarray):
    """Return (yield_estimate, ci_lower, ci_upper) for a single input."""
    X_scaled  = scaler.transform(input_array.reshape(1, -1))
    pred_val  = float(reg_model.predict(X_scaled)[0])
    # Use a conservative 10% CI when calling from GUI
    ci_lower  = max(0, pred_val * 0.90)
    ci_upper  = pred_val * 1.10
    return round(pred_val, 2), round(ci_lower, 2), round(ci_upper, 2)
