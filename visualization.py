"""
visualization.py
Funções de geração de imagens para a Atividade Prática 2 — Naive Bayes.

Todas as funções salvam PNGs na pasta output/ e não exibem janelas
(backend Agg — compatível com ambientes sem display).
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")          # backend sem janela — deve vir antes do import pyplot
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _ensure_output():
    os.makedirs("output", exist_ok=True)


def _save_and_close(fig: plt.Figure, filename: str):
    fig.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [img] salvo -> {filename}")


# ------------------------------------------------------------------
# Matriz de confusão
# ------------------------------------------------------------------

def plot_confusion_matrix(cm: np.ndarray, title: str, filename: str):
    """
    Plota a matriz de confusão 2×2 com anotações de TN/FP/FN/TP.

    Args:
        cm       : array (2,2) — [[TN, FP], [FN, TP]]
        title    : título do gráfico
        filename : caminho de saída (PNG)
    """
    _ensure_output()
    fig, ax = plt.subplots(figsize=(5, 4))

    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    class_labels = ["Classe 0\n(<= media)", "Classe 1\n(> media)"]
    ticks = np.arange(2)
    ax.set_xticks(ticks);  ax.set_xticklabels(class_labels, fontsize=10)
    ax.set_yticks(ticks);  ax.set_yticklabels(class_labels, fontsize=10)
    ax.set_xlabel("Rótulo Previsto", fontsize=11)
    ax.set_ylabel("Rótulo Real", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)

    cell_labels = [["TN", "FP"], ["FN", "TP"]]
    thresh = cm.max() / 2.0
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > thresh else "black"
            ax.text(
                j, i,
                f"{cell_labels[i][j]}\n{cm[i, j]}",
                ha="center", va="center",
                color=color, fontsize=13, fontweight="bold",
            )

    _save_and_close(fig, filename)


# ------------------------------------------------------------------
# Contribuições de log-verossimilhança por feature
# ------------------------------------------------------------------

def plot_log_contributions(explanation: dict, feature_names: list, filename: str):
    """
    Gera um gráfico de barras horizontais para cada classe mostrando
    o log P(xi | Ck) de cada feature, ordenado de forma decrescente.
    Inclui no título as probabilidades normalizadas e a classe predita.

    Args:
        explanation  : dicionário retornado por GaussianNaiveBayes.explain_sample()
        feature_names: lista de nomes das features (ordem original)
        filename     : caminho de saída (PNG)
    """
    _ensure_output()
    classes = sorted(explanation["log_likelihoods"].keys())
    palette = {0: "#4C9BE8", 1: "#E84C4C"}

    fig, axes = plt.subplots(1, len(classes), figsize=(14, 5))
    if len(classes) == 1:
        axes = [axes]

    for ax, c in zip(axes, classes):
        ll = explanation["log_likelihoods"][c]        # já ordenado desc
        fnames = list(ll.keys())
        values = list(ll.values())
        color = palette.get(c, "#7F8C8D")

        y_pos = range(len(fnames))
        bars = ax.barh(
            list(y_pos), values,
            color=color, alpha=0.80, edgecolor="black", linewidth=0.5,
        )
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(fnames, fontsize=9)
        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlabel("log P(xi | Ck)", fontsize=9)

        prob_pct = explanation["probabilities"][c] * 100
        sum_ll = sum(values)
        ax.set_title(
            f"Classe {c}\nlog-posterior = {explanation['log_posteriors'][c]:.2f}"
            f"\nP(Classe {c}) = {prob_pct:.1f}%",
            fontsize=10, fontweight="bold",
        )

        for bar, val in zip(bars, values):
            offset = max(abs(v) for v in values) * 0.02
            x_pos = val + offset if val >= 0 else val - offset
            ha = "left" if val >= 0 else "right"
            ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                    f"{val:.2f}", va="center", ha=ha, fontsize=7)

    pred = explanation["predicted_class"]
    p0 = explanation["probabilities"][0] * 100
    p1 = explanation["probabilities"][1] * 100
    fig.suptitle(
        f"Contribuições log-verossimilhança por feature\n"
        f"Classe 0: {p0:.1f}%  |  Classe 1: {p1:.1f}%  "
        f"|  Classe predita: {pred}",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    _save_and_close(fig, filename)


# ------------------------------------------------------------------
# Ranking de features
# ------------------------------------------------------------------

def plot_feature_ranking(sorted_features: list, filename: str):
    """
    Gráfico de barras horizontais com o ranking de features pela
    acurácia média. As 3 primeiras aparecem em verde (top-3).

    Args:
        sorted_features : lista de (feature_name, mean_accuracy) em ordem decrescente
        filename        : caminho de saída (PNG)
    """
    _ensure_output()
    names = [f[0] for f in sorted_features]
    accs  = [f[1] for f in sorted_features]
    n     = len(names)

    # top-3 verde, demais azul
    colors = ["#2ECC71" if i < 3 else "#3498DB" for i in range(n)]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(
        names[::-1], accs[::-1],
        color=colors[::-1],
        edgecolor="black", linewidth=0.5,
    )

    for bar, acc in zip(bars, accs[::-1]):
        ax.text(
            bar.get_width() + 0.003,
            bar.get_y() + bar.get_height() / 2,
            f"{acc:.4f}",
            va="center", fontsize=9,
        )

    ax.set_xlabel("Acuracia Media (10 execucoes / 10 seeds)", fontsize=11)
    ax.set_title(
        "Ranking de Features - Naive Bayes Gaussiano\n(uma feature por modelo)",
        fontsize=12, fontweight="bold",
    )
    ax.set_xlim(0, max(accs) + 0.08)
    ax.axvline(0.5, color="red", linestyle="--", alpha=0.4, linewidth=1.2, label="Baseline 50%")

    legend_elements = [
        Patch(facecolor="#2ECC71", edgecolor="black", label="Top 3"),
        Patch(facecolor="#3498DB", edgecolor="black", label="Demais"),
        plt.Line2D([0], [0], color="red", linestyle="--", alpha=0.6, label="Baseline 50%"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=9)

    plt.tight_layout()
    _save_and_close(fig, filename)


# ------------------------------------------------------------------
# Comparação de acurácias (Parte 1 vs Parte 3)
# ------------------------------------------------------------------

def plot_accuracy_comparison(results: list, filename: str):
    """
    Gráfico de barras comparando acurácia média ± desvio padrão entre modelos.

    Args:
        results  : lista de (label, mean_acc, std_acc)
        filename : caminho de saída (PNG)
    """
    _ensure_output()
    labels = [r[0] for r in results]
    means  = [r[1] for r in results]
    stds   = [r[2] for r in results]

    palette = ["#3498DB", "#2ECC71", "#E67E22", "#9B59B6"]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(
        x, means,
        yerr=stds, capsize=9,
        color=palette[: len(labels)],
        edgecolor="black", linewidth=0.8, alpha=0.85,
        error_kw={"elinewidth": 2, "ecolor": "black", "capthick": 2},
    )

    for bar, mean, std in zip(bars, means, stds):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + std + 0.007,
            f"{mean:.4f}\n±{std:.4f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel("Acurácia Média", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.set_title(
        "Comparação de Modelos\nTodas as Features vs Top 3 Features",
        fontsize=12, fontweight="bold",
    )
    ax.axhline(0.5, color="red", linestyle="--", alpha=0.45, linewidth=1.2, label="Baseline 50%")
    ax.legend(fontsize=9)

    plt.tight_layout()
    _save_and_close(fig, filename)