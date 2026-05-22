"""
train_models.py
===============
Master training script for the Smart Agriculture Decision Support System.
Runs the full pipeline: preprocessing → training → evaluation → serialization
→ results plots.

Run from the project root:
    python src/train_models.py

Author  : BSE-6 Student, Bahria University Islamabad
Course  : Artificial Intelligence (CLO-2 OEL)
Version : 1.0.0
""" 

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Allow imports from src/
sys.path.insert(0, os.path.dirname(__file__))

from preprocessing import prepare_pipeline, save_artifacts, FEATURE_COLS
from models import (
    train_decision_tree,   evaluate_decision_tree,
    train_kmeans_clustering, evaluate_clustering,
    train_linear_regression, evaluate_regression,
    save_model,
)
from utils import (
    format_metrics_dt, format_metrics_reg, format_metrics_clust,
    save_metrics_json, get_cluster_profile, CLUSTER_PROFILES,
)

# ─────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────
ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH   = os.path.join(ROOT, 'data', 'Crop_recommendation.csv')
MODELS_DIR  = os.path.join(ROOT, 'models')
RESULTS_DIR = os.path.join(ROOT, 'results')
os.makedirs(MODELS_DIR,  exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# Plot settings
# ─────────────────────────────────────────────
PALETTE    = 'viridis'
FIG_DPI    = 150
PLOT_STYLE = 'seaborn-v0_8-whitegrid'
try:
    plt.style.use(PLOT_STYLE)
except:
    plt.style.use('ggplot')

COLORS = {
    'primary'  : '#2c7a3a',
    'secondary': '#5aaa6f',
    'accent'   : '#e8f5e9',
    'dark'     : '#1a3a22',
    'warning'  : '#e67e22',
    'info'     : '#2980b9',
}


# ═══════════════════════════════════════════════════════════════
# Plot helpers
# ═══════════════════════════════════════════════════════════════
def plot_feature_importance(dt_metrics, save_path):
    fi   = dt_metrics['feature_importance']
    keys = sorted(fi, key=fi.get, reverse=True)
    vals = [fi[k] for k in keys]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(keys, vals, color=[COLORS['primary'] if v == max(vals)
                                       else COLORS['secondary'] for v in vals],
                   edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', fontsize=10, color=COLORS['dark'])
    ax.set_xlabel('Gini Importance', fontsize=12, fontweight='bold')
    ax.set_title('Decision Tree – Feature Importance Vector', fontsize=14,
                 fontweight='bold', color=COLORS['dark'], pad=14)
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) + 0.05)
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIG_DPI, bbox_inches='tight')
    plt.close()
    print(f"  [Plot] {save_path}")


def plot_cluster_scatter(km_metrics, X_full_df, save_path):
    labels  = km_metrics['labels']
    X_arr   = X_full_df.values if hasattr(X_full_df, 'values') else X_full_df

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # PCA-like: use first 2 principal features (N vs K)
    scatter = axes[0].scatter(X_arr[:, 0], X_arr[:, 2], c=labels,
                               cmap=PALETTE, alpha=0.6, s=18, linewidths=0)
    axes[0].set_xlabel('N (Nitrogen) – scaled', fontsize=11)
    axes[0].set_ylabel('K (Potassium) – scaled', fontsize=11)
    axes[0].set_title('Soil Cluster Distribution\n(N vs K feature space)',
                       fontsize=13, fontweight='bold')
    plt.colorbar(scatter, ax=axes[0], label='Cluster ID')

    # Temperature vs Humidity
    scatter2 = axes[1].scatter(X_arr[:, 3], X_arr[:, 4], c=labels,
                                cmap=PALETTE, alpha=0.6, s=18, linewidths=0)
    axes[1].set_xlabel('Temperature – scaled', fontsize=11)
    axes[1].set_ylabel('Humidity – scaled', fontsize=11)
    axes[1].set_title('Soil Cluster Distribution\n(Temperature vs Humidity space)',
                       fontsize=13, fontweight='bold')
    plt.colorbar(scatter2, ax=axes[1], label='Cluster ID')

    plt.suptitle(f'KMeans Soil Zone Segmentation  '
                 f'(Silhouette={km_metrics["silhouette"]:.3f})',
                 fontsize=15, fontweight='bold', color=COLORS['dark'], y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIG_DPI, bbox_inches='tight')
    plt.close()
    print(f"  [Plot] {save_path}")


def plot_residuals(reg_metrics, save_path):
    y_pred    = reg_metrics['y_pred']
    residuals = reg_metrics['residuals']
    y_test    = reg_metrics['y_test']

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 1. Actual vs Predicted
    mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
    axes[0].scatter(y_test, y_pred, alpha=0.4, color=COLORS['primary'], s=18)
    axes[0].plot([mn, mx], [mn, mx], 'r--', lw=1.5, label='Perfect fit')
    axes[0].set_xlabel('Actual Yield (q/ha)', fontsize=11)
    axes[0].set_ylabel('Predicted Yield (q/ha)', fontsize=11)
    axes[0].set_title(f'Actual vs Predicted\nR²={reg_metrics["r2"]:.4f}',
                       fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=9)

    # 2. Residual vs Predicted
    axes[1].scatter(y_pred, residuals, alpha=0.4, color=COLORS['warning'], s=18)
    axes[1].axhline(0, color='black', lw=1.2, linestyle='--')
    axes[1].set_xlabel('Predicted Yield (q/ha)', fontsize=11)
    axes[1].set_ylabel('Residuals', fontsize=11)
    axes[1].set_title(f'Residual Analysis\nRMSE={reg_metrics["rmse"]:.3f}',
                       fontsize=12, fontweight='bold')

    # 3. Residual histogram
    axes[2].hist(residuals, bins=40, color=COLORS['info'], edgecolor='white',
                  linewidth=0.4, alpha=0.85)
    axes[2].axvline(0, color='red', lw=1.2, linestyle='--')
    axes[2].set_xlabel('Residual Value', fontsize=11)
    axes[2].set_ylabel('Frequency', fontsize=11)
    axes[2].set_title(f'Residual Distribution\nMAE={reg_metrics["mae"]:.3f}',
                       fontsize=12, fontweight='bold')

    plt.suptitle('Linear Regression – Crop Yield Residual Analysis',
                 fontsize=15, fontweight='bold', color=COLORS['dark'], y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIG_DPI, bbox_inches='tight')
    plt.close()
    print(f"  [Plot] {save_path}")


def plot_model_comparison(dt_m, km_m, reg_m, save_path):
    """Summary dashboard of all three model metrics."""
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle('Multi-Model Performance Summary Dashboard',
                 fontsize=16, fontweight='bold', color=COLORS['dark'])

    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

    # ─ DT metrics bar ─
    ax1 = fig.add_subplot(gs[0, 0])
    dt_vals  = [dt_m['accuracy'], dt_m['precision'], dt_m['recall'], dt_m['f1']]
    dt_names = ['Accuracy', 'Precision', 'Recall', 'F1']
    bars = ax1.bar(dt_names, dt_vals, color=[COLORS['primary'], COLORS['secondary'],
                                              '#4caf50', '#81c784'],
                   edgecolor='white')
    for b, v in zip(bars, dt_vals):
        ax1.text(b.get_x()+b.get_width()/2, b.get_height()+0.005,
                 f'{v:.3f}', ha='center', va='bottom', fontsize=9)
    ax1.set_ylim(0, 1.08)
    ax1.set_title('Decision Tree\nClassifier', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Score')

    # ─ Cluster size pie ─
    ax2 = fig.add_subplot(gs[0, 1])
    sizes  = list(km_m['cluster_sizes'].values())
    clabels= [f'Zone {i}' for i in km_m['cluster_sizes'].keys()]
    ax2.pie(sizes, labels=clabels, autopct='%1.1f%%',
            colors=sns.color_palette('viridis', len(sizes)),
            startangle=90, textprops={'fontsize':9})
    ax2.set_title(f'KMeans Cluster Sizes\nSilhouette={km_m["silhouette"]:.3f}',
                   fontsize=11, fontweight='bold')

    # ─ Reg metrics ─
    ax3 = fig.add_subplot(gs[0, 2])
    reg_names  = ['RMSE', 'MAE', 'R²']
    reg_vals_d = [reg_m['rmse'], reg_m['mae'], reg_m['r2']]
    bar_colors = [COLORS['warning'], '#e74c3c', COLORS['info']]
    bars2 = ax3.bar(reg_names, reg_vals_d, color=bar_colors, edgecolor='white')
    for b, v in zip(bars2, reg_vals_d):
        ax3.text(b.get_x()+b.get_width()/2, b.get_height()+0.3,
                 f'{v:.3f}', ha='center', va='bottom', fontsize=9)
    ax3.set_title('Linear Regression\nYield Predictor', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Value')

    # ─ Confusion matrix (abbreviated) ─
    ax4 = fig.add_subplot(gs[1, :])
    fi = dt_m['feature_importance']
    keys = sorted(fi, key=fi.get, reverse=True)
    vals = [fi[k] for k in keys]
    ax4.barh(keys, vals, color=COLORS['secondary'], edgecolor='white')
    ax4.set_xlabel('Feature Importance (Gini)')
    ax4.set_title('Feature Importance Vector – Decision Tree', fontweight='bold')
    ax4.invert_yaxis()

    plt.savefig(save_path, dpi=FIG_DPI, bbox_inches='tight')
    plt.close()
    print(f"  [Plot] {save_path}")


# ═══════════════════════════════════════════════════════════════
# Main pipeline
# ═══════════════════════════════════════════════════════════════
def main():
    print("\n" + "═"*56)
    print("  Smart Agriculture Decision Support System — Trainer")
    print("═"*56)

    # ── Preprocessing ──────────────────────────────────────────
    pipe = prepare_pipeline(DATA_PATH)
    save_artifacts(pipe['le'], pipe['scaler'], MODELS_DIR)

    # ── Decision Tree ──────────────────────────────────────────
    print("\n[1/3] Training Decision Tree Classifier …")
    dt_model   = train_decision_tree(pipe['X_train'], pipe['y_clf_train'])
    dt_metrics = evaluate_decision_tree(dt_model, pipe['X_test'],
                                        pipe['y_clf_test'], pipe['le'])
    save_model(dt_model, os.path.join(MODELS_DIR, 'decision_tree.pkl'))

    print("\n──── Decision Tree Report ────")
    print(format_metrics_dt(dt_metrics))

    # ── KMeans Clustering ──────────────────────────────────────
    print("\n[2/3] Training KMeans Clustering …")
    km_model   = train_kmeans_clustering(pipe['X_full'])
    km_metrics = evaluate_clustering(km_model, pipe['X_full'])
    save_model(km_model, os.path.join(MODELS_DIR, 'kmeans_clustering.pkl'))

    print("\n──── Clustering Report ────")
    print(format_metrics_clust(km_metrics))

    # ── Linear Regression ─────────────────────────────────────
    print("\n[3/3] Training Linear (Ridge) Regression …")
    reg_model   = train_linear_regression(pipe['X_train'], pipe['y_reg_train'])
    reg_metrics = evaluate_regression(reg_model, pipe['X_test'], pipe['y_reg_test'])
    save_model(reg_model, os.path.join(MODELS_DIR, 'linear_regression.pkl'))

    print("\n──── Regression Report ────")
    print(format_metrics_reg(reg_metrics))

    # ── Plots ──────────────────────────────────────────────────
    print("\n[Generating plots …]")
    plot_feature_importance(dt_metrics,
        os.path.join(RESULTS_DIR, 'feature_importance.png'))
    plot_cluster_scatter(km_metrics, pipe['X_full'],
        os.path.join(RESULTS_DIR, 'cluster_scatter.png'))
    plot_residuals(reg_metrics,
        os.path.join(RESULTS_DIR, 'residual_analysis.png'))
    plot_model_comparison(dt_metrics, km_metrics, reg_metrics,
        os.path.join(RESULTS_DIR, 'model_comparison_dashboard.png'))

    # ── Save metrics ───────────────────────────────────────────
    save_metrics_json(
        {'decision_tree': dt_metrics,
         'clustering'   : km_metrics,
         'regression'   : reg_metrics},
        RESULTS_DIR
    )

    print("\n" + "═"*56)
    print("  Training complete.  All artefacts saved.")
    print(f"  Models  → {MODELS_DIR}")
    print(f"  Results → {RESULTS_DIR}")
    print("═"*56 + "\n")

    return dt_metrics, km_metrics, reg_metrics


if __name__ == '__main__':
    main()
