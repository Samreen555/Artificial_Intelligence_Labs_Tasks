# 🌾 Smart Agriculture Decision Support System

> **Integration and Deployment of a Multi-Model Agricultural Intelligence System**  
> Bahria University Islamabad · Department of Software Engineering · BSE-6 (A/B)  
> Course: Artificial Intelligence · OEL [CLO-2] · Instructor: Engr. Saad Mazhar Khan

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Models & Algorithms](#models--algorithms)
4. [Performance Summary](#performance-summary)
5. [Installation](#installation)
6. [Execution](#execution)
7. [Project Structure](#project-structure)
8. [Dataset](#dataset)
9. [GUI Features](#gui-features)
10. [Future Work](#future-work)
11. [References](#references)

---

## Overview

The **Smart Agriculture Decision Support System (SADSS)** is a production-grade, multi-model AI pipeline that integrates three classical machine learning paradigms into a single, unified Tkinter GUI application.

The system answers three core questions for farm managers and agronomists:

| Question | Model | Output |
|----------|-------|--------|
| Which crop should I plant? | Decision Tree Classifier | Crop name (22 classes) |
| What soil zone am I in? | KMeans Clustering | Soil zone ID + agronomic guidance |
| How much yield can I expect? | Linear Regression (Ridge) | Yield in q/ha + confidence interval |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SADSS — System Architecture                   │
├──────────────┬──────────────────────────┬───────────────────────┤
│  DATA LAYER  │      MODEL LAYER         │  PRESENTATION LAYER   │
│              │                          │                        │
│  CSV Dataset │  ┌─ Decision Tree ──────►│  Crop Recommendation  │
│  ↓           │  │                       │                        │
│  Missing val │  ├─ KMeans Clustering ──►│  Soil Zone Profile    │
│  Imputation  │  │                       │                        │
│  ↓           │  └─ Linear Regression ──►│  Yield Forecast       │
│  IQR Outlier │                          │                        │
│  Clipping    │  joblib serialization    │  Tkinter + Matplotlib │
│  ↓           │  (.pkl artifacts)        │  Embedded Plots       │
│  StandardScl │                          │                        │
└──────────────┴──────────────────────────┴───────────────────────┘
       preprocessing.py    models.py              gui.py
```

---

## Models & Algorithms

### 1. Decision Tree Classifier
- **Purpose**: Crop recommendation based on soil NPK + climate features
- **Parameters**: `max_depth=12`, `criterion='gini'`, `class_weight='balanced'`
- **Metrics**: Accuracy, Precision, Recall, F1-Score (weighted)

### 2. KMeans Soil Clustering
- **Purpose**: Segment soil profiles into 5 homogeneous farm zones
- **Parameters**: `k=5`, `init='k-means++'`, `n_init=20`
- **Metrics**: Silhouette Score, Davies-Bouldin Index, Inertia

### 3. Linear Regression (Ridge)
- **Purpose**: Quantitative crop yield prediction in q/ha
- **Parameters**: `alpha=1.0` (L2 regularisation), `fit_intercept=True`
- **Metrics**: RMSE, MAE, R²

---

## Performance Summary

| Model | Metric | Value |
|-------|--------|-------|
| Decision Tree | Accuracy | **98.41%** |
| Decision Tree | Precision (weighted) | **98.47%** |
| Decision Tree | Recall (weighted) | **98.41%** |
| Decision Tree | F1-Score (weighted) | **98.41%** |
| KMeans | Silhouette Score | **0.3096** |
| KMeans | Davies-Bouldin | **1.2877** |
| Linear Regression | RMSE | **30.997 q/ha** |
| Linear Regression | MAE | **24.185 q/ha** |
| Linear Regression | R² | **0.5256** |

---

## Installation

### Prerequisites
- Python 3.9+
- pip

### Steps

```bash
# Clone the repository
git clone https://github.com/<your-username>/smart-agriculture-system.git
cd smart-agriculture-system

# Install dependencies
pip install -r requirements.txt
```

---

## Execution

### Step 1 — Train Models (one-time)
```bash
python src/train_models.py
```
This generates all `.pkl` model files in `models/` and evaluation plots in `results/`.

### Step 2 — Launch GUI
```bash
python src/gui.py
```

---

## Project Structure

```
smart_agriculture_system/
├── data/
│   ├── Crop_recommendation.csv     # 2,200 samples × 9 features
│   ├── generate_dataset.py         # Dataset generator
│   └── data_dictionary.md          # Feature documentation
├── src/
│   ├── preprocessing.py            # Data engineering layer
│   ├── models.py                   # Algorithmic core (DT + KMeans + LR)
│   ├── gui.py                      # Tkinter GUI application
│   ├── utils.py                    # Agronomic guidance & helpers
│   └── train_models.py             # Master training script
├── models/
│   ├── decision_tree.pkl
│   ├── kmeans_clustering.pkl
│   ├── linear_regression.pkl
│   ├── label_encoder.pkl
│   └── scaler.pkl
├── results/
│   ├── feature_importance.png
│   ├── cluster_scatter.png
│   ├── residual_analysis.png
│   └── model_comparison_dashboard.png
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Dataset

**Source**: Kaggle Crop Recommendation Dataset (Atharva Ingle, 2020)  
**Structure**: 2,200 rows × 9 columns  
**Classes**: 22 crop types (100 samples each — balanced)

| Feature | Description | Unit | Range |
|---------|-------------|------|-------|
| N | Nitrogen content in soil | kg/ha | 0–140 |
| P | Phosphorous content in soil | kg/ha | 5–145 |
| K | Potassium content in soil | kg/ha | 5–205 |
| temperature | Ambient temperature | °C | 8–44 |
| humidity | Relative humidity | % | 14–100 |
| ph | Soil pH value | — | 3.5–9.9 |
| rainfall | Annual rainfall | mm | 20–300 |
| label | Target crop class | — | 22 classes |
| yield | Crop yield (derived) | q/ha | 1–350 |

---

## GUI Features

- **Dark green agricultural theme** with professional typography
- **7 interactive slider+entry input cards** with real-time validation
- **4 quick presets**: Rice, Maize, Banana, Coffee
- **5-tab interface**:
  - 🔍 Prediction — Integrated 3-model output with agronomic guidance
  - 📊 Feature Importance — Live bar chart
  - 🗺️ Soil Clusters — Dual-axis scatter plots with user-point overlay
  - 📈 Yield Analysis — Actual vs Predicted, Residual, Distribution plots
  - 📋 Model Metrics — Full ASCII metrics report
- **Matplotlib plots embedded** directly in the GUI frame

---

## Future Work

### 1. IoT Sensor Stream Integration
Replace manual slider inputs with a real-time MQTT data pipeline from soil sensor nodes (e.g., NPK probes, DHT22 temperature/humidity sensors, rain gauges). An edge-computing microservice would buffer sensor readings, run inference locally, and push alerts to farm managers' mobile devices — enabling continuous, autonomous monitoring across large farms.

### 2. Ensemble Deep Learning with Satellite Imagery
Augment the current feature set with Sentinel-2 multispectral satellite imagery (NDVI, EVI, moisture indices). A multimodal ensemble comprising the current classical pipeline for tabular data plus a lightweight CNN (MobileNetV3) for spatial features could substantially improve yield prediction accuracy (R² > 0.85) and detect crop stress zones invisible to ground sensors.

---

## References

1. Ingle, A. (2020). *Crop Recommendation Dataset*. Kaggle. https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
2. Breiman, L., Friedman, J., Olshen, R., & Stone, C. (1984). *Classification and Regression Trees*. Wadsworth.
3. MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the 5th Berkeley Symposium*, 1, 281–297.
4. Hoerl, A. E., & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55–67.
5. Liakos, K. G., et al. (2018). Machine learning in agriculture: A review. *Sensors*, 18(8), 2674.
6. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830.

---

*© 2026 Samreen Farhat, Department of Software Engineering, Bahria School of Engineering and Applied Sciences, Islamabad. MIT License.*
