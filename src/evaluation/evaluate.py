"""
Evaluation Module: Unified Metrics Computation and Visualization.
Calculates PR-AUC, ROC-AUC, F1-Score, Precision, Recall, Confusion Matrix,
and produces publication-ready comparison curves.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    precision_recall_curve,
    roc_curve,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)

from src.config import PLOTS_DIR, ensure_directories, get_logger

logger = get_logger("evaluate")


def compute_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    model_name: str,
    feature_count: int,
    fit_time: float,
    threshold: float = 0.5,
    threshold_source: str = "fixed_0.5",
) -> dict:
    """
    Computes comprehensive evaluation metrics with primary emphasis on threshold-free
    PR-AUC and ROC-AUC. Threshold metrics default to fixed 0.5 to avoid optimistic bias.
    """
    # Clip probabilities
    y_prob = np.clip(y_prob, 1e-7, 1.0 - 1e-7)

    roc_auc = float(roc_auc_score(y_true, y_prob))
    pr_auc = float(average_precision_score(y_true, y_prob))

    # Reference optimal F1 threshold (exploratory diagnostic only)
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_prob)
    f1_curve = 2 * (precisions * recalls) / (precisions + recalls + 1e-9)
    best_idx = np.argmax(f1_curve)
    best_f1_threshold_ref = float(thresholds[best_idx]) if best_idx < len(thresholds) else 0.5

    # Evaluation predictions based on designated threshold (default 0.5)
    eval_threshold = threshold if threshold is not None else 0.5
    y_pred = (y_prob >= eval_threshold).astype(int)

    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    accuracy = float(accuracy_score(y_true, y_pred))

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    return {
        "model_name": model_name,
        "feature_count": feature_count,
        "pr_auc": round(pr_auc, 4),
        "roc_auc": round(roc_auc, 4),
        "f1_score": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "threshold": round(eval_threshold, 4),
        "threshold_source": threshold_source,
        "best_f1_threshold_ref": round(best_f1_threshold_ref, 4),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "fit_time_seconds": round(fit_time, 2),
    }


def plot_comparison_curves(eval_data: dict, output_dir: Path = PLOTS_DIR):
    """
    Plots ROC Curves, Precision-Recall Curves, and Confusion Matrices for compared models.
    eval_data format: {model_name: {'y_true': ..., 'y_prob': ..., 'y_pred': ...}}
    """
    ensure_directories()
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. ROC Curve
    plt.figure(figsize=(8, 6))
    for name, data in eval_data.items():
        fpr, tpr, _ = roc_curve(data["y_true"], data["y_prob"])
        auc = roc_auc_score(data["y_true"], data["y_prob"])
        plt.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {auc:.3f})")
    plt.plot([0, 1], [0, 1], "k--", lw=1.5, alpha=0.7)
    plt.title("Receiver Operating Characteristic (ROC) Comparison", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("False Positive Rate", fontsize=11)
    plt.ylabel("True Positive Rate", fontsize=11)
    plt.legend(loc="lower right", frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(output_dir / "roc_curve.png", dpi=200)
    plt.close()
    logger.info("Saved roc_curve.png")

    # 2. Precision-Recall Curve
    plt.figure(figsize=(8, 6))
    for name, data in eval_data.items():
        p, r, _ = precision_recall_curve(data["y_true"], data["y_prob"])
        pr_auc = average_precision_score(data["y_true"], data["y_prob"])
        plt.plot(r, p, lw=2, label=f"{name} (PR-AUC = {pr_auc:.3f})")
    plt.title("Precision-Recall (PR) Curve Comparison", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Recall", fontsize=11)
    plt.ylabel("Precision", fontsize=11)
    plt.legend(loc="upper right", frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(output_dir / "precision_recall_curve.png", dpi=200)
    plt.close()
    logger.info("Saved precision_recall_curve.png")

    # 3. Confusion Matrix Grid
    n_models = len(eval_data)
    cols = min(3, n_models)
    rows = (n_models + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4.5 * rows), squeeze=False)

    for idx, (name, data) in enumerate(eval_data.items()):
        r_idx = idx // cols
        c_idx = idx % cols
        ax = axes[r_idx, c_idx]
        cm = confusion_matrix(data["y_true"], data["y_pred"])
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        ax.set_title(f"{name}", fontsize=11, fontweight="bold")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Pred 0", "Pred 1"])
        ax.set_yticklabels(["Actual 0", "Actual 1"])
        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{cm[i, j]:,}", ha="center", va="center", color="white" if cm[i, j] > cm.max()/2 else "black", fontweight="bold")

    # Hide extra subplots
    for idx in range(n_models, rows * cols):
        axes[idx // cols, idx % cols].axis("off")

    plt.tight_layout()
    plt.savefig(output_dir / "confusion_matrix.png", dpi=200)
    plt.close()
    logger.info("Saved confusion_matrix.png")
