"""
main.py - Atividade Pratica 2: Naive Bayes Gaussiano
Dataset: Diabetes (scikit-learn)

Executa as tres partes da atividade em sequencia:
  Parte 1 - Classificador com todas as features (10 runs)
  Parte 2 - Um modelo por feature (ranking de relevancia)
  Parte 3 - Modelo com top-3 features (comparacao com Parte 1)
"""

import os
from gaussian_naive_bayes import load_and_prepare_data, run_part1, run_part2, run_part3

os.makedirs("output", exist_ok=True)


def main():
    print("=" * 62)
    print("ATIVIDADE PRATICA 2 - Naive Bayes Gaussiano")
    print("Dataset: Diabetes (scikit-learn)")
    print("=" * 62)

    # Carrega e binariza o dataset
    X, y, feature_names, mean_target = load_and_prepare_data()

    print(f"\nDataset carregado:")
    print(f"  Amostras  : {X.shape[0]}")
    print(f"  Features  : {X.shape[1]}  ->  {feature_names}")
    print(f"  Limiar    : media do target = {mean_target:.4f}")
    print(f"  Classes   : 0 (progressao <= media)  /  1 (progressao > media)")

    # ---------------------------------------------------------------
    acc_all, std_all = run_part1(X, y, feature_names)

    # ---------------------------------------------------------------
    sorted_features = run_part2(X, y, feature_names)

    # ---------------------------------------------------------------
    run_part3(X, y, feature_names, sorted_features, acc_all, std_all)

    # ---------------------------------------------------------------
    print("\n" + "=" * 62)
    print("Concluido. Imagens geradas em: output/")
    print("  - output/confusion_matrix_all.png")
    print("  - output/log_contributions.png")
    print("  - output/feature_ranking.png")
    print("  - output/accuracy_comparison.png")
    print("=" * 62)


if __name__ == "__main__":
    main()