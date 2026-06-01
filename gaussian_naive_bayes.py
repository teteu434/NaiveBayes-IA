import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

from visualization import (
    plot_confusion_matrix,
    plot_log_contributions,
    plot_feature_ranking,
    plot_accuracy_comparison,
)


class GaussianNaiveBayes:
    """
    Gaussian Naive Bayes classifier implementado do zero.

    Para cada classe Ck:
      - Prior:      P(Ck) = contagem(Ck) / total
      - Likelihood: P(xi | Ck) = Gaussiana(xi ; mu_ki, sigma²_ki)
      - Posterior:  log P(Ck | x) = log P(Ck) + sum_i log P(xi | Ck)

    var_smoothing adiciona epsilon à variância para evitar divisão por zero
    em features com variância nula ou muito baixa.
    """

    def __init__(self, var_smoothing: float = 1e-9):
        self.var_smoothing = var_smoothing
        self.classes_: np.ndarray = None
        self.log_priors_: dict = {}
        self.means_: dict = {}
        self.vars_: dict = {}

    # ------------------------------------------------------------------
    # Treinamento
    # ------------------------------------------------------------------

    def fit(self, X: np.ndarray, y: np.ndarray) -> "GaussianNaiveBayes":
        self.classes_ = np.unique(y)
        n_samples = X.shape[0]

        for c in self.classes_:
            X_c = X[y == c]
            self.log_priors_[c] = np.log(len(X_c) / n_samples)
            self.means_[c] = np.mean(X_c, axis=0)
            self.vars_[c] = np.var(X_c, axis=0) + self.var_smoothing

        return self

    # ------------------------------------------------------------------
    # Inferência
    # ------------------------------------------------------------------

    def _log_gaussian_pdf(self, x: float, mean: float, var: float) -> float:
        """
        Log da função densidade de probabilidade Gaussiana:
          log N(x; mu, sigma²) = -0.5 * log(2*pi*var) - (x - mu)² / (2*var)
        """
        return -0.5 * np.log(2 * np.pi * var) - ((x - mean) ** 2) / (2 * var)

    def _log_posterior(self, x: np.ndarray) -> dict:
        """Log da probabilidade posterior para cada classe (sem normalização)."""
        return {
            c: self.log_priors_[c]
            + np.sum(self._log_gaussian_pdf(x, self.means_[c], self.vars_[c]))
            for c in self.classes_
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions = []
        for x in X:
            log_posts = self._log_posterior(x)
            predictions.append(max(log_posts, key=log_posts.get))
        return np.array(predictions)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Probabilidades normalizadas via softmax nos log-posteriors."""
        proba = []
        for x in X:
            log_posts = self._log_posterior(x)
            log_vals = np.array([log_posts[c] for c in sorted(self.classes_)])
            log_vals -= np.max(log_vals)          # estabilidade numérica
            probs = np.exp(log_vals)
            proba.append(probs / probs.sum())
        return np.array(proba)

    def explain_sample(self, x: np.ndarray, feature_names: list) -> dict:
        """
        Retorna explicação detalhada para uma amostra:
          - log_priors           : log P(Ck) por classe
          - log_likelihoods      : log P(xi|Ck) por feature e classe (ordem decrescente)
          - log_posteriors       : log P(Ck|x) por classe
          - probabilities        : probabilidade normalizada por classe
          - predicted_class      : classe com maior posterior
        """
        log_priors = {c: self.log_priors_[c] for c in self.classes_}

        log_likelihoods = {}
        for c in self.classes_:
            ll = {
                feature_names[i]: self._log_gaussian_pdf(
                    x[i], self.means_[c][i], self.vars_[c][i]
                )
                for i in range(len(x))
            }
            log_likelihoods[c] = dict(
                sorted(ll.items(), key=lambda kv: kv[1], reverse=True)
            )

        log_posteriors = self._log_posterior(x)

        log_vals = np.array([log_posteriors[c] for c in sorted(self.classes_)])
        log_vals -= np.max(log_vals)
        probs = np.exp(log_vals)
        probs /= probs.sum()
        probabilities = {c: float(probs[i]) for i, c in enumerate(sorted(self.classes_))}

        return {
            "log_priors": log_priors,
            "log_likelihoods": log_likelihoods,
            "log_posteriors": log_posteriors,
            "probabilities": probabilities,
            "predicted_class": max(log_posteriors, key=log_posteriors.get),
        }


# ------------------------------------------------------------------
# Utilitários
# ------------------------------------------------------------------

def compute_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, classes: list) -> np.ndarray:
    idx = {c: i for i, c in enumerate(classes)}
    cm = np.zeros((len(classes), len(classes)), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[idx[t]][idx[p]] += 1
    return cm


def load_and_prepare_data():
    """Carrega o dataset Diabetes e binariza o target pela média."""
    data = load_diabetes()
    X = data.data
    feature_names = list(data.feature_names)
    mean_target = float(np.mean(data.target))
    y = (data.target > mean_target).astype(int)
    return X, y, feature_names, mean_target


# ------------------------------------------------------------------
# Partes da atividade
# ------------------------------------------------------------------

def run_part1(X: np.ndarray, y: np.ndarray, feature_names: list):
    """
    Parte 1 — Naive Bayes com todas as features.
    - Mostra distribuição das classes
    - 10 execuções com splits aleatórios → média e desvio da acurácia
    - Matriz de confusão do último treinamento
    - Explicação detalhada de uma amostra do conjunto de teste
    """
    print("\n" + "=" * 62)
    print("PARTE 1 - Naive Bayes Gaussiano (todas as features)")
    print("=" * 62)

    unique, counts = np.unique(y, return_counts=True)
    print("\nDistribuicao das classes apos binarizacao:")
    labels = {0: "<= media  (0)", 1: " > media  (1)"}
    for c, n in zip(unique, counts):
        print(f"  Classe {labels[c]}: {n} amostras")

    accuracies = []
    last_model = last_X_test = last_y_test = None

    for seed in range(10):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed
        )
        model = GaussianNaiveBayes()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracies.append(float(np.mean(y_pred == y_test)))
        last_model, last_X_test, last_y_test = model, X_test, y_test

    mean_acc = float(np.mean(accuracies))
    std_acc = float(np.std(accuracies))
    print(f"\nAcuracia media (10 execucoes): {mean_acc:.4f}")
    print(f"Desvio padrao:                {std_acc:.4f}")

    # ---- i) Matriz de confusao ----
    y_pred_last = last_model.predict(last_X_test)
    cm = compute_confusion_matrix(last_y_test, y_pred_last, [0, 1])
    tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
    print("\ni) Matriz de Confusao (ultimo treinamento):")
    print(f"       Pred 0   Pred 1")
    print(f"  Real 0  {tn:4d}    {fp:4d}")
    print(f"  Real 1  {fn:4d}    {tp:4d}")
    plot_confusion_matrix(
        cm, "Matriz de Confusao - Todas as Features",
        "output/confusion_matrix_all.png"
    )

    # ---- ii) Explicação de uma amostra ----
    sample = last_X_test[0]
    true_label = int(last_y_test[0])
    exp = last_model.explain_sample(sample, feature_names)

    print(f"\nii) Explicacao da amostra #0 do conjunto de teste")
    print(f"    Rotulo real: {true_label}")

    print("\n    a) Log das probabilidades a priori:")
    for c in sorted(exp["log_priors"]):
        print(f"       Classe {c}: {exp['log_priors'][c]:.4f}")

    print("\n    b) Log das probabilidades condicionais (Gaussiana) - ordem decrescente:")
    for c in sorted(exp["log_likelihoods"]):
        total_ll = sum(exp["log_likelihoods"][c].values())
        print(f"\n       Classe {c}  (soma log-likelihoods = {total_ll:.4f}):")
        for fname, val in exp["log_likelihoods"][c].items():
            print(f"         {fname:>6}: {val:8.4f}")

    print("\n    c) Probabilidades normalizadas (posterior softmax):")
    for c in sorted(exp["probabilities"]):
        print(f"       Classe {c}: {exp['probabilities'][c] * 100:.2f}%")

    print(f"\n    d) Classe predita: {exp['predicted_class']}")

    plot_log_contributions(exp, feature_names, "output/log_contributions.png")

    return mean_acc, std_acc


def run_part2(X: np.ndarray, y: np.ndarray, feature_names: list) -> list:
    """
    Parte 2 — Treina um modelo por feature (10 features → 10 modelos).
    Para cada modelo calcula a média da acurácia em 10 divisões treino/teste.
    Retorna lista ordenada (feature, acurácia_média) decrescente.
    """
    print("\n" + "=" * 62)
    print("PARTE 2 - Uma feature por vez")
    print("=" * 62)

    feature_accs: dict = {}
    for i, fname in enumerate(feature_names):
        X_feat = X[:, i: i + 1]
        accs = []
        for seed in range(10):
            X_tr, X_te, y_tr, y_te = train_test_split(
                X_feat, y, test_size=0.2, random_state=seed
            )
            model = GaussianNaiveBayes()
            model.fit(X_tr, y_tr)
            accs.append(float(np.mean(model.predict(X_te) == y_te)))
        feature_accs[fname] = float(np.mean(accs))

    sorted_features = sorted(feature_accs.items(), key=lambda kv: kv[1], reverse=True)

    print("\nRanking de features (acuracia media de 10 execucoes):")
    for rank, (fname, acc) in enumerate(sorted_features, 1):
        bar = "#" * int(acc * 30)
        print(f"  {rank:2}. {fname:>6}: {acc:.4f}  {bar}")

    plot_feature_ranking(sorted_features, "output/feature_ranking.png")

    return sorted_features


def run_part3(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: list,
    sorted_features: list,
    acc_all: float,
    std_all: float,
):
    """
    Parte 3 — Treina com as 3 features mais relevantes (ranking da Parte 2).
    Compara acurácia média com o modelo de todas as features.
    """
    print("\n" + "=" * 62)
    print("PARTE 3 - Top 3 features")
    print("=" * 62)

    top3_names = [f[0] for f in sorted_features[:3]]
    top3_idx = [list(feature_names).index(n) for n in top3_names]
    print(f"\nFeatures selecionadas: {top3_names}")

    X_top3 = X[:, top3_idx]
    accs = []
    for seed in range(10):
        X_tr, X_te, y_tr, y_te = train_test_split(
            X_top3, y, test_size=0.2, random_state=seed
        )
        model = GaussianNaiveBayes()
        model.fit(X_tr, y_tr)
        accs.append(float(np.mean(model.predict(X_te) == y_te)))

    mean_acc = float(np.mean(accs))
    std_acc = float(np.std(accs))

    print(f"\nAcuracia media (top 3 features, 10 execucoes): {mean_acc:.4f}")
    print(f"Desvio padrao:                                {std_acc:.4f}")

    print("\nComparacao final:")
    print(f"  Todas as features (10): {acc_all:.4f} +/- {std_all:.4f}")
    print(f"  Top 3 features:         {mean_acc:.4f} +/- {std_acc:.4f}")

    diff = mean_acc - acc_all
    direction = "superior" if diff > 0 else "inferior" if diff < 0 else "igual"
    print(f"\n  Diferenca: {diff:+.4f}  -> top-3 e {direction} ao modelo completo.")

    plot_accuracy_comparison(
        [
            ("Todas as features\n(10 features)", acc_all, std_all),
            ("Top 3 features", mean_acc, std_acc),
        ],
        "output/accuracy_comparison.png",
    )

    return mean_acc, std_acc