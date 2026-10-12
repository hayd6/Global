"""
Phase 7: Binary Particle Swarm Optimization (Binary PSO) for Feature Selection.
Implements a custom, vectorized Binary PSO with sigmoid transfer function,
velocity clamping, caching, sparsity regularization, and checkpointing.
"""

import sys
import time
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

from src.config import (
    OUTPUTS_DIR,
    FEATURE_SEL_DIR,
    PLOTS_DIR,
    CONFIGS_DIR,
    RANDOM_STATE,
    ensure_directories,
    get_logger,
)

logger = get_logger("pso_optimizer")


class BinaryPSO:
    """
    Binary Particle Swarm Optimization for Feature Selection.
    """
    def __init__(
        self,
        n_particles: int = 16,
        n_iterations: int = 12,
        w: float = 0.729,
        c1: float = 1.494,
        c2: float = 1.494,
        alpha: float = 0.92,
        v_max: float = 4.0,
        random_state: int = RANDOM_STATE,
    ):
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.alpha = alpha  # Weight for PR-AUC; (1 - alpha) weight for feature sparsity
        self.v_max = v_max
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        self.cache = {}
        self.history = []
        self.gbest_position = None
        self.gbest_fitness = -1.0
        self.gbest_pr_auc = -1.0
        self.gbest_n_features = 0

        self.n_evaluations = 0

    @staticmethod
    def sigmoid(v):
        """Sigmoid transfer function mapping continuous velocity to probability [0, 1]."""
        return 1.0 / (1.0 + np.exp(-np.clip(v, -10.0, 10.0)))

    def evaluate_fitness(self, mask: np.ndarray, X_tr: np.ndarray, y_tr: np.ndarray, X_va: np.ndarray, y_val: np.ndarray) -> tuple:
        """
        Calculates fitness = alpha * PR-AUC + (1 - alpha) * (1 - k/D).
        Returns (fitness, pr_auc, k_features).
        """
        self.n_evaluations += 1
        k = int(np.sum(mask))
        total_d = len(mask)
        if k == 0:
            return 0.0, 0.0, 0

        key = tuple(mask)
        if key in self.cache:
            return self.cache[key]

        X_tr_sub = X_tr[:, mask]
        X_va_sub = X_va[:, mask]

        clf = LogisticRegression(max_iter=300, random_state=self.random_state, class_weight="balanced")
        clf.fit(X_tr_sub, y_tr)
        probs = clf.predict_proba(X_va_sub)[:, 1]
        pr_auc = float(average_precision_score(y_val, probs))

        sparsity_bonus = 1.0 - (k / total_d)
        fitness = (self.alpha * pr_auc) + ((1.0 - self.alpha) * sparsity_bonus)

        res = (float(fitness), float(pr_auc), k)
        self.cache[key] = res
        return res

    def optimize(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray, feature_names: list) -> dict:
        """
        Runs the PSO swarm search across n_iterations.
        Tracks search_time_seconds and total unique masks evaluated.
        """
        start_search_time = time.time()
        D = X_train.shape[1]
        logger.info(f"Initializing PSO Swarm: {self.n_particles} particles, {self.n_iterations} iterations, {D} dimensions.")

        # Initialize particles
        # Random initial binary mask with probability ~0.5
        positions = self.rng.binomial(1, 0.5, size=(self.n_particles, D))
        # Ensure at least 1 feature per particle
        for i in range(self.n_particles):
            if np.sum(positions[i]) == 0:
                positions[i, self.rng.randint(0, D)] = 1

        velocities = self.rng.uniform(-self.v_max, self.v_max, size=(self.n_particles, D))

        pbest_positions = positions.copy()
        pbest_fitnesses = np.zeros(self.n_particles)
        pbest_pr_aucs = np.zeros(self.n_particles)

        # Initial evaluation
        for i in range(self.n_particles):
            fit, pr, k = self.evaluate_fitness(positions[i], X_train, y_train, X_val, y_val)
            pbest_fitnesses[i] = fit
            pbest_pr_aucs[i] = pr
            if fit > self.gbest_fitness:
                self.gbest_fitness = fit
                self.gbest_pr_auc = pr
                self.gbest_position = positions[i].copy()
                self.gbest_n_features = k

        logger.info(f"Iteration 0 (Init) | GBest Fitness: {self.gbest_fitness:.4f} | PR-AUC: {self.gbest_pr_auc:.4f} | Features: {self.gbest_n_features}/{D}")
        self.history.append({
            "iteration": 0,
            "best_fitness": round(self.gbest_fitness, 4),
            "best_pr_auc": round(self.gbest_pr_auc, 4),
            "mean_fitness": round(float(np.mean(pbest_fitnesses)), 4),
            "best_feature_count": self.gbest_n_features,
            "elapsed_seconds": round(time.time() - start_search_time, 2),
        })

        # Main Swarm Iteration Loop
        for it in range(1, self.n_iterations + 1):
            t0 = time.time()
            for i in range(self.n_particles):
                # Update velocity
                r1 = self.rng.rand(D)
                r2 = self.rng.rand(D)
                velocities[i] = (
                    self.w * velocities[i]
                    + self.c1 * r1 * (pbest_positions[i] - positions[i])
                    + self.c2 * r2 * (self.gbest_position - positions[i])
                )
                velocities[i] = np.clip(velocities[i], -self.v_max, self.v_max)

                # Update position via sigmoid transfer function
                probs = self.sigmoid(velocities[i])
                rand_draws = self.rng.rand(D)
                positions[i] = (rand_draws < probs).astype(int)

                # Ensure at least 1 feature
                if np.sum(positions[i]) == 0:
                    positions[i, self.rng.randint(0, D)] = 1

                # Evaluate fitness
                fit, pr, k = self.evaluate_fitness(positions[i], X_train, y_train, X_val, y_val)

                # Update Personal Best
                if fit > pbest_fitnesses[i]:
                    pbest_fitnesses[i] = fit
                    pbest_pr_aucs[i] = pr
                    pbest_positions[i] = positions[i].copy()

                # Update Global Best
                if fit > self.gbest_fitness:
                    self.gbest_fitness = fit
                    self.gbest_pr_auc = pr
                    self.gbest_position = positions[i].copy()
                    self.gbest_n_features = k

            it_time = time.time() - t0
            iter_record = {
                "iteration": it,
                "best_fitness": round(self.gbest_fitness, 4),
                "best_pr_auc": round(self.gbest_pr_auc, 4),
                "mean_fitness": round(float(np.mean(pbest_fitnesses)), 4),
                "best_feature_count": self.gbest_n_features,
                "elapsed_seconds": round(time.time() - start_search_time, 2),
            }
            self.history.append(iter_record)
            logger.info(f"Iteration {it:2d}/{self.n_iterations} ({it_time:.2f}s) | GBest Fitness: {self.gbest_fitness:.4f} | PR-AUC: {self.gbest_pr_auc:.4f} | Selected: {self.gbest_n_features}/{D}")

        total_search_time = time.time() - start_search_time
        selected_feature_indices = np.where(self.gbest_position == 1)[0]
        selected_features = [feature_names[idx] for idx in selected_feature_indices]

        logger.info(f"PSO search completed in {total_search_time:.2f}s. Evaluated {self.n_evaluations} particles ({len(self.cache)} unique masks).")

        return {
            "gbest_fitness": self.gbest_fitness,
            "gbest_pr_auc": self.gbest_pr_auc,
            "gbest_n_features": self.gbest_n_features,
            "total_features": D,
            "selected_features": selected_features,
            "selected_indices": selected_feature_indices.tolist(),
            "history": self.history,
            "search_time_seconds": round(total_search_time, 2),
            "n_evaluations": self.n_evaluations,
            "n_unique_masks": len(self.cache),
        }


from src.models.split_manager import create_or_load_splits


def run_pso_optimization():
    """Runs Phase 7 PSO Feature Selection pipeline using strictly inner train tuning split."""
    ensure_directories()
    splits = create_or_load_splits()
    df = splits["df"]

    drop_cols = [
        "customer_id",
        "split_type",
        "target",
        "dominant_geo_ip_region",
        "dominant_campaign_id",
        "primary_campaign_type",
        "primary_campaign_budget",
        "country_code",
        "region",
        "customer_tier",
        "region_tier",
    ]
    candidate_cols = [
        c for c in df.columns 
        if c not in drop_cols and not (pd.api.types.is_string_dtype(df[c]) or pd.api.types.is_object_dtype(df[c]))
    ]
    
    # Inner tuning partitions derived strictly from the Train pool (never holdout!)
    inner_tr_idx = splits["pso_inner_train_idx"]
    inner_va_idx = splits["pso_inner_val_idx"]

    # Subsample for responsive CPU optimization (20k inner train, 10k inner val)
    sub_tr = inner_tr_idx[:min(20000, len(inner_tr_idx))]
    sub_va = inner_va_idx[:min(10000, len(inner_va_idx))]

    X_tr_raw = df[candidate_cols].iloc[sub_tr]
    X_va_raw = df[candidate_cols].iloc[sub_va]
    y_tr = splits["y"][sub_tr]
    y_va = splits["y"][sub_va]

    logger.info(f"PSO Partition: Inner Train={X_tr_raw.shape}, Inner Val={X_va_raw.shape} (Holdout strictly untouched).")

    # Fit imputer and scaler EXCLUSIVELY on inner train partition (harmonized with pipeline median imputation)
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(imputer.fit_transform(X_tr_raw))
    X_va = scaler.transform(imputer.transform(X_va_raw))

    pso = BinaryPSO(
        n_particles=16,
        n_iterations=12,
        w=0.729,
        c1=1.494,
        c2=1.494,
        alpha=0.92,
        random_state=RANDOM_STATE,
    )

    result = pso.optimize(X_tr, y_tr, X_va, y_va, candidate_cols)

    # 1. Save selected features
    sel_df = pd.DataFrame({
        "feature_name": result["selected_features"],
        "is_selected": 1,
    })
    sel_path = FEATURE_SEL_DIR / "pso_selected_features.csv"
    sel_df.to_csv(sel_path, index=False)
    logger.info(f"Saved PSO selected features ({len(sel_df)} features) to {sel_path}")

    # 2. Save convergence CSV
    conv_df = pd.DataFrame(result["history"])
    conv_path = FEATURE_SEL_DIR / "pso_convergence.csv"
    conv_df.to_csv(conv_path, index=False)
    logger.info(f"Saved PSO convergence log to {conv_path}")

    # 3. Plot convergence chart
    plt.figure(figsize=(9, 5))
    plt.plot(conv_df["iteration"], conv_df["best_fitness"], "o-", color="#4C72B0", lw=2, label="Best Swarm Fitness")
    plt.plot(conv_df["iteration"], conv_df["mean_fitness"], "s--", color="#55A868", lw=1.5, label="Mean Particle Fitness")
    plt.title(f"Binary PSO Convergence History ({len(sel_df)}/{result['total_features']} Features Selected)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Iteration Step", fontsize=11)
    plt.ylabel("Multi-Objective Fitness", fontsize=11)
    plt.legend(frameon=True, facecolor="white")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "pso_convergence.png", dpi=200)
    plt.close()
    logger.info("Saved pso_convergence.png")

    # 4. Save experiment configuration with full search cost tracking
    exp_cfg = {
        "split_id": "stratified_80_20_v1",
        "selection_partition": "inner_train_tuning_partition",
        "n_particles": pso.n_particles,
        "n_iterations": pso.n_iterations,
        "inertia_w": pso.w,
        "cognitive_c1": pso.c1,
        "social_c2": pso.c2,
        "alpha_pr_weight": pso.alpha,
        "random_state": RANDOM_STATE,
        "total_candidate_features": result["total_features"],
        "selected_features_count": len(sel_df),
        "sparsity_reduction_pct": round((1.0 - len(sel_df)/result["total_features"]) * 100, 2),
        "best_fitness": round(result["gbest_fitness"], 4),
        "best_pr_auc": round(result["gbest_pr_auc"], 4),
        "search_time_seconds": result["search_time_seconds"],
        "n_evaluations": result["n_evaluations"],
        "n_unique_masks": result["n_unique_masks"],
    }
    with open(CONFIGS_DIR / "pso_experiment_config.json", "w") as f:
        json.dump(exp_cfg, f, indent=4)

    return result


if __name__ == "__main__":
    run_pso_optimization()
