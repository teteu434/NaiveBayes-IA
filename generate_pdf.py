"""
generate_pdf.py
Gera o PDF de documentacao do projeto Naive Bayes Gaussiano.
Salva em: C:/Users/people4tech.matheus/Downloads/NaiveBayes_Explicacao.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ---------------------------------------------------------------------------
# Estilos
# ---------------------------------------------------------------------------

BASE = getSampleStyleSheet()

TITLE      = ParagraphStyle("title",      fontSize=22, leading=28, alignment=TA_CENTER,
                             fontName="Helvetica-Bold", textColor=colors.HexColor("#1a237e"),
                             spaceAfter=6)
SUBTITLE   = ParagraphStyle("subtitle",   fontSize=13, leading=18, alignment=TA_CENTER,
                             fontName="Helvetica", textColor=colors.HexColor("#455a64"),
                             spaceAfter=4)
H1         = ParagraphStyle("h1",         fontSize=16, leading=20, fontName="Helvetica-Bold",
                             textColor=colors.HexColor("#1565c0"), spaceBefore=18, spaceAfter=6,
                             borderPad=2)
H2         = ParagraphStyle("h2",         fontSize=13, leading=17, fontName="Helvetica-Bold",
                             textColor=colors.HexColor("#0277bd"), spaceBefore=14, spaceAfter=4)
H3         = ParagraphStyle("h3",         fontSize=11, leading=15, fontName="Helvetica-Bold",
                             textColor=colors.HexColor("#37474f"), spaceBefore=10, spaceAfter=3)
BODY       = ParagraphStyle("body",       fontSize=10, leading=15, fontName="Helvetica",
                             textColor=colors.HexColor("#212121"), alignment=TA_JUSTIFY,
                             spaceAfter=4)
BODY_SMALL = ParagraphStyle("bodysmall",  fontSize=9,  leading=13, fontName="Helvetica",
                             textColor=colors.HexColor("#424242"), alignment=TA_JUSTIFY,
                             spaceAfter=3)
CODE_STYLE = ParagraphStyle("code",       fontSize=8.5, leading=13, fontName="Courier",
                             textColor=colors.HexColor("#212121"),
                             backColor=colors.HexColor("#f5f5f5"),
                             leftIndent=10, rightIndent=10,
                             borderPad=4, spaceAfter=2, spaceBefore=2)
CODE_CMT   = ParagraphStyle("codecmt",    fontSize=8.5, leading=13, fontName="Courier",
                             textColor=colors.HexColor("#388e3c"),
                             backColor=colors.HexColor("#f5f5f5"),
                             leftIndent=10, rightIndent=10,
                             borderPad=4, spaceAfter=2, spaceBefore=0)
LABEL_BOX  = ParagraphStyle("labelbox",   fontSize=9, leading=13, fontName="Helvetica-Bold",
                             textColor=colors.white,
                             backColor=colors.HexColor("#1565c0"),
                             leftIndent=6, rightIndent=6, borderPad=3,
                             spaceAfter=2, spaceBefore=8)
FORMULA    = ParagraphStyle("formula",    fontSize=10, leading=16, fontName="Courier-Bold",
                             textColor=colors.HexColor("#4a148c"),
                             backColor=colors.HexColor("#ede7f6"),
                             leftIndent=12, borderPad=5, spaceAfter=4, spaceBefore=4,
                             alignment=TA_CENTER)
CALLOUT    = ParagraphStyle("callout",    fontSize=9.5, leading=14, fontName="Helvetica-Oblique",
                             textColor=colors.HexColor("#1b5e20"),
                             backColor=colors.HexColor("#e8f5e9"),
                             leftIndent=10, rightIndent=10, borderPad=5,
                             spaceAfter=6, spaceBefore=4)
WARNING    = ParagraphStyle("warning",    fontSize=9.5, leading=14, fontName="Helvetica",
                             textColor=colors.HexColor("#b71c1c"),
                             backColor=colors.HexColor("#ffebee"),
                             leftIndent=10, rightIndent=10, borderPad=5,
                             spaceAfter=6, spaceBefore=4)

def hr():
    return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#90caf9"),
                      spaceAfter=4, spaceBefore=4)

def spacer(h=0.3):
    return Spacer(1, h * cm)

def p(text, style=BODY):
    return Paragraph(text, style)

def code(line):
    return Paragraph(line, CODE_STYLE)

def code_comment(line):
    return Paragraph(line, CODE_CMT)

def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)


# ---------------------------------------------------------------------------
# Tabela de linha de codigo
# ---------------------------------------------------------------------------

def code_table(rows):
    """
    rows: list of (code_str, explanation_str)
    Renders a two-column table: left=code (Courier), right=explanation (normal).
    """
    table_data = []
    for code_str, expl_str in rows:
        c_para = Paragraph(code_str, ParagraphStyle(
            "ct", fontSize=8, leading=12, fontName="Courier",
            textColor=colors.HexColor("#1a237e")))
        e_para = Paragraph(expl_str, ParagraphStyle(
            "et", fontSize=9, leading=13, fontName="Helvetica",
            textColor=colors.HexColor("#212121")))
        table_data.append([c_para, e_para])

    col_widths = [7.5 * cm, 9.5 * cm]
    tbl = Table(table_data, colWidths=col_widths, repeatRows=0)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e3f2fd")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#fafafa")),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#bdbdbd")),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return tbl


# ===========================================================================
# CONTEUDO
# ===========================================================================

def build_content():
    story = []

    # -----------------------------------------------------------------------
    # CAPA
    # -----------------------------------------------------------------------
    story += [
        spacer(3),
        p("Atividade Pratica 2", TITLE),
        p("Naive Bayes Gaussiano — Documentacao Tecnica do Codigo", SUBTITLE),
        p("Dataset: Diabetes (scikit-learn) | Classificacao Binaria de Progressao da Doenca", SUBTITLE),
        spacer(0.5),
        hr(),
        spacer(0.3),
        p("Arquivos documentados: main.py  |  gaussian_naive_bayes.py", SUBTITLE),
        spacer(4),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # SUMARIO (manual)
    # -----------------------------------------------------------------------
    story += [
        h1("Sumario"),
        hr(),
        p("1. Por que Naive Bayes Gaussiano? (Justificativa detalhada)"),
        p("2. Visao geral da arquitetura do codigo"),
        p("3. Arquivo: main.py"),
        p("   3.1  Imports e inicializacao"),
        p("   3.2  Funcao main()"),
        p("4. Arquivo: gaussian_naive_bayes.py"),
        p("   4.1  Imports"),
        p("   4.2  Classe GaussianNaiveBayes — __init__"),
        p("   4.3  Metodo fit()"),
        p("   4.4  Metodo _log_gaussian_pdf()"),
        p("   4.5  Metodo _log_posterior()"),
        p("   4.6  Metodo predict()"),
        p("   4.7  Metodo predict_proba()"),
        p("   4.8  Metodo explain_sample()"),
        p("   4.9  Funcao compute_confusion_matrix()"),
        p("   4.10 Funcao load_and_prepare_data()"),
        p("   4.11 Funcao run_part1()"),
        p("   4.12 Funcao run_part2()"),
        p("   4.13 Funcao run_part3()"),
        p("5. Fluxo completo de execucao"),
        p("6. Resultados obtidos"),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # 1. JUSTIFICATIVA DA GAUSSIANA
    # -----------------------------------------------------------------------
    story += [
        h1("1. Por que Naive Bayes Gaussiano?"),
        hr(),
        spacer(0.2),
        h2("1.1 Os tres tipos de Naive Bayes"),
        p("O algoritmo Naive Bayes tem tres variantes principais, cada uma adequada a um tipo de dado:"),
        spacer(0.2),
    ]

    comparison_data = [
        [
            Paragraph("<b>Variante</b>", ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                       textColor=colors.white)),
            Paragraph("<b>Tipo de dado</b>", ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                       textColor=colors.white)),
            Paragraph("<b>Como modela P(xi|Ck)</b>", ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                       textColor=colors.white)),
            Paragraph("<b>Exemplo de uso</b>", ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                       textColor=colors.white)),
        ],
        [
            Paragraph("Multinomial", BODY_SMALL),
            Paragraph("Discreto (contagens)", BODY_SMALL),
            Paragraph("Frequencia relativa de ocorrencias", BODY_SMALL),
            Paragraph("Classificacao de texto, spam", BODY_SMALL),
        ],
        [
            Paragraph("Bernoulli", BODY_SMALL),
            Paragraph("Binario (0 ou 1)", BODY_SMALL),
            Paragraph("Probabilidade de presenca/ausencia", BODY_SMALL),
            Paragraph("Presenca de palavra em doc", BODY_SMALL),
        ],
        [
            Paragraph("Gaussiano", BODY_SMALL),
            Paragraph("Continuo (real)", BODY_SMALL),
            Paragraph("Funcao densidade de probabilidade normal", BODY_SMALL),
            Paragraph("Dados medicos, sensoriais", BODY_SMALL),
        ],
    ]
    comp_tbl = Table(comparison_data, colWidths=[3.5*cm, 3.5*cm, 5*cm, 5.2*cm])
    comp_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#e3f2fd")),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.HexColor("#90caf9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    story += [comp_tbl, spacer(0.4)]

    story += [
        h2("1.2 Caracteristicas do dataset Diabetes"),
        p("O dataset Diabetes do scikit-learn possui <b>442 amostras</b> e <b>10 features "
          "numericas continuas</b>, todas normalizadas na escala [-1, 1]:"),
        spacer(0.1),
    ]

    feat_data = [
        [Paragraph("<b>Feature</b>", BODY_SMALL), Paragraph("<b>Descricao</b>", BODY_SMALL),
         Paragraph("<b>Tipo real</b>", BODY_SMALL)],
        [Paragraph("age", BODY_SMALL),  Paragraph("Idade do paciente", BODY_SMALL),          Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("sex", BODY_SMALL),  Paragraph("Sexo (codificado numericamente)", BODY_SMALL), Paragraph("Continuo*", BODY_SMALL)],
        [Paragraph("bmi", BODY_SMALL),  Paragraph("Indice de Massa Corporal", BODY_SMALL),    Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("bp",  BODY_SMALL),  Paragraph("Pressao arterial media", BODY_SMALL),      Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s1",  BODY_SMALL),  Paragraph("Colesterol total (TC)", BODY_SMALL),       Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s2",  BODY_SMALL),  Paragraph("LDL — colesterol ruim", BODY_SMALL),       Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s3",  BODY_SMALL),  Paragraph("HDL — colesterol bom", BODY_SMALL),        Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s4",  BODY_SMALL),  Paragraph("Relacao colesterol total / HDL", BODY_SMALL), Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s5",  BODY_SMALL),  Paragraph("Log dos triglicerideos sericos", BODY_SMALL), Paragraph("Continuo", BODY_SMALL)],
        [Paragraph("s6",  BODY_SMALL),  Paragraph("Nivel de glicose no sangue", BODY_SMALL), Paragraph("Continuo", BODY_SMALL)],
    ]
    ft = Table(feat_data, colWidths=[2*cm, 9*cm, 3*cm])
    ft.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0277bd")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e1f5fe")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b0bec5")),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story += [ft, spacer(0.4)]

    story += [
        h2("1.3 Por que nao Multinomial?"),
        p("O Naive Bayes Multinomial espera <b>contagens inteiras nao-negativas</b> — tipicamente "
          "a frequencia de uma palavra em um documento. As features do dataset Diabetes sao valores "
          "reais normalizados que podem ser negativos (ex: age pode ser -0.07, bmi pode ser 0.06). "
          "Usar Multinomial aqui seria conceitualmente errado: a formula de suavizacao de Laplace "
          "N_ki / (N_k + alpha*d) pressupoe contagens, nao densidades. Aplicar esse modelo a dados "
          "continuos produziria probabilidades sem sentido fisico."),
        spacer(0.2),
        h2("1.4 Por que nao Bernoulli?"),
        p("O Naive Bayes Bernoulli trabalha com features <b>estritamente binarias</b> (0 ou 1). "
          "A formula P(xi|Ck) = p^xi * (1-p)^(1-xi) modela apenas presenca ou ausencia. "
          "Embora fosse possivel binarizar as features do diabetes (ex: bmi > 0 = 1, caso contrario 0), "
          "isso implicaria em uma perda massiva de informacao: a diferenca entre bmi = 0.001 e "
          "bmi = 0.9 seria completamente ignorada, pois ambas seriam tratadas como '1'. "
          "Para dados medicos continuos, isso seria uma simplificacao inaceitavel que degradaria "
          "significativamente a acuracia do modelo."),
        spacer(0.2),
        h2("1.5 Por que Gaussiano e a escolha correta?"),
        p("O Naive Bayes Gaussiano assume que cada feature, condicionada a uma classe, segue uma "
          "<b>distribuicao normal (gaussiana)</b>. Essa suposicao e altamente adequada ao dataset "
          "Diabetes pelos seguintes motivos:"),
        p("(1) <b>Features continuas:</b> Todas as 10 features sao valores reais, exatamente o que "
          "a distribuicao gaussiana foi projetada para modelar."),
        p("(2) <b>Pre-normalizacao:</b> O scikit-learn ja entrega o dataset com features normalizadas "
          "(media zero, desvio unitario), o que favorece a suposicao gaussiana."),
        p("(3) <b>Dados biomedicos tipicamente seguem distribuicoes aproximadamente normais:</b> "
          "Pressao arterial, indice de massa corporal e niveis de glicose, quando coletados em "
          "populacoes suficientemente grandes, tendem a seguir distribuicoes simetrico-campaniformes."),
        p("(4) <b>Nenhuma discretizacao necessaria:</b> Ao contrario de Multinomial e Bernoulli, "
          "o modelo Gaussiano usa o valor continuo diretamente na formula da densidade, preservando "
          "toda a informacao numerica."),
        spacer(0.2),
        p("Formula da densidade gaussiana utilizada:", H3),
        p("P(xi | Ck) = (1 / sqrt(2*pi*sigma^2)) * exp( -(xi - mu_ki)^2 / (2*sigma^2_ki) )", FORMULA),
        p("Onde mu_ki e a media e sigma^2_ki e a variancia da feature i para todos os exemplos "
          "da classe Ck no conjunto de treinamento. Esses dois parametros sao aprendidos durante o fit()."),
        spacer(0.2),
        p("NOTA IMPORTANTE: O resultado numerico obtido (acuracia media ~69% com todas as features "
          "e ~72% com as top-3 features) confirma que a escolha foi adequada para o problema. "
          "Interessantemente, o modelo com apenas 3 features (s5, bmi, bp) superou o modelo completo, "
          "o que sugere que as demais features introduzem ruido — fenomeno conhecido como 'curse of "
          "dimensionality' e exacerbado pela hipotese de independencia do Naive Bayes.", CALLOUT),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # 2. ARQUITETURA
    # -----------------------------------------------------------------------
    story += [
        h1("2. Visao Geral da Arquitetura"),
        hr(),
        spacer(0.2),
        p("O projeto e dividido em tres arquivos Python com responsabilidades bem separadas:"),
        spacer(0.2),
    ]

    arch_data = [
        [Paragraph("<b>Arquivo</b>", BODY_SMALL), Paragraph("<b>Responsabilidade</b>", BODY_SMALL)],
        [Paragraph("main.py", BODY_SMALL),
         Paragraph("Ponto de entrada. Carrega dados, chama as tres partes, exibe resumo final.", BODY_SMALL)],
        [Paragraph("gaussian_naive_bayes.py", BODY_SMALL),
         Paragraph("Contem a classe GaussianNaiveBayes (algoritmo puro) e as funcoes run_part1/2/3 "
                   "que orquestram treinamento, avaliacao e impressao de resultados.", BODY_SMALL)],
        [Paragraph("visualization.py", BODY_SMALL),
         Paragraph("Responsavel por gerar e salvar todos os graficos PNG na pasta output/. "
                   "Usa matplotlib com backend Agg (sem janela).", BODY_SMALL)],
    ]
    at = Table(arch_data, colWidths=[5*cm, 12.2*cm])
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#90caf9")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 7),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    story += [at, spacer(0.4)]

    story += [
        p("Fluxo de chamadas:", H3),
        code("main.py"),
        code("  └─> load_and_prepare_data()         # carrega e binariza"),
        code("  └─> run_part1(X, y, features)        # 10 runs, matriz confusao, amostra"),
        code("       └─> GaussianNaiveBayes.fit()"),
        code("       └─> GaussianNaiveBayes.predict()"),
        code("       └─> compute_confusion_matrix()"),
        code("       └─> GaussianNaiveBayes.explain_sample()"),
        code("       └─> plot_confusion_matrix()     # visualization.py"),
        code("       └─> plot_log_contributions()    # visualization.py"),
        code("  └─> run_part2(X, y, features)        # 10 modelos x 10 seeds"),
        code("       └─> GaussianNaiveBayes.fit/predict"),
        code("       └─> plot_feature_ranking()      # visualization.py"),
        code("  └─> run_part3(X, y, features, ...)   # top-3 features"),
        code("       └─> GaussianNaiveBayes.fit/predict"),
        code("       └─> plot_accuracy_comparison()  # visualization.py"),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # 3. MAIN.PY
    # -----------------------------------------------------------------------
    story += [
        h1("3. Arquivo: main.py"),
        hr(),
    ]

    story += [
        h2("3.1 Imports e inicializacao"),
        code_table([
            ("import os", "Modulo padrao do Python para operacoes com o sistema de arquivos."),
            ("from gaussian_naive_bayes import ...", "Importa as 4 funcoes principais do modulo do algoritmo."),
            ("os.makedirs('output', exist_ok=True)", "Cria a pasta 'output/' se ela nao existir. exist_ok=True evita erro caso a pasta ja exista."),
        ]),
        spacer(0.3),
        h2("3.2 Funcao main()"),
        p("Funcao principal que orquestra toda a execucao. Corresponde ao padrao de projeto "
          "<i>entry point</i>: quando o arquivo e executado diretamente (python main.py), "
          "o bloco <b>if __name__ == '__main__'</b> garante que main() seja chamada."),
        spacer(0.2),
        code_table([
            ("X, y, feature_names, mean_target", "X: matriz de features (442x10). y: vetor de classes binarias (0 ou 1). "
             "feature_names: lista com os nomes das 10 features. mean_target: media do target original (152.13)."),
            ("= load_and_prepare_data()", "Chama a funcao que carrega o dataset e binariza o target pela media."),
            ("acc_all, std_all = run_part1(...)", "Executa a Parte 1. Retorna media e desvio da acuracia em 10 runs com todas as features."),
            ("sorted_features = run_part2(...)", "Executa a Parte 2. Retorna lista de (feature, acuracia_media) em ordem decrescente."),
            ("run_part3(..., acc_all, std_all)", "Executa a Parte 3. Recebe o ranking da Parte 2 e as metricas da Parte 1 para comparacao final."),
            ("if __name__ == '__main__':", "Garante que main() so e chamada quando o script e executado diretamente, nao quando importado."),
        ]),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # 4. GAUSSIAN_NAIVE_BAYES.PY
    # -----------------------------------------------------------------------
    story += [
        h1("4. Arquivo: gaussian_naive_bayes.py"),
        hr(),
    ]

    # 4.1 Imports
    story += [
        h2("4.1 Imports"),
        code_table([
            ("import numpy as np", "NumPy: biblioteca para computacao numerica vetorizada. Usada em todas as operacoes matriciais e estatisticas."),
            ("from sklearn.datasets import load_diabetes", "Unica funcao do scikit-learn no algoritmo: carrega os dados. O classificador em si e implementado do zero."),
            ("from sklearn.model_selection import train_test_split", "Divide o dataset em treino e teste de forma aleatoria controlada pelo parametro random_state."),
            ("from visualization import (...)", "Importa as 4 funcoes de plotagem do modulo de visualizacao."),
        ]),
        spacer(0.3),
    ]

    # 4.2 __init__
    story += [
        h2("4.2 Classe GaussianNaiveBayes — __init__"),
        p("O construtor define os atributos de instancia que serao populados durante o treinamento (fit). "
          "Antes do fit, o modelo nao sabe nada sobre os dados."),
        spacer(0.2),
        code_table([
            ("def __init__(self, var_smoothing=1e-9):", "Define o unico hiperparametro: var_smoothing. Valor padrao 1e-9 (0,000000001), igual ao scikit-learn."),
            ("self.var_smoothing = var_smoothing", "Armazena o epsilon que sera somado a todas as variancias para evitar divisao por zero."),
            ("self.classes_: np.ndarray = None", "Sera preenchido com os valores unicos de y (ex: [0, 1]). None indica modelo nao treinado."),
            ("self.log_priors_: dict = {}", "Dicionario {classe: log(P(Ck))}. Ex: {0: -0.614, 1: -0.779}."),
            ("self.means_: dict = {}", "Dicionario {classe: array de medias por feature}. Ex: {0: [0.01, -0.04, ...], 1: [...]}."),
            ("self.vars_: dict = {}", "Dicionario {classe: array de variancias por feature + var_smoothing}."),
        ]),
        spacer(0.3),
    ]

    # 4.3 fit
    story += [
        h2("4.3 Metodo fit(X, y)"),
        p("<b>Resumo teorico:</b> O metodo fit() corresponde a fase de treinamento do Naive Bayes. "
          "Dado que as probabilidades condicionais sao calculadas de forma analitica (sem otimizacao iterativa), "
          "o 'treinamento' consiste simplesmente em calcular e armazenar estatisticas suficientes para cada classe: "
          "a probabilidade a priori P(Ck) e, para cada feature, a media e a variancia condicionadas a classe. "
          "Matematicamente:"),
        p("P(Ck) = |{xi: yi = k}| / N", FORMULA),
        p("mu_ki = media de xi para todos os exemplos da classe k", FORMULA),
        p("sigma^2_ki = variancia de xi para todos os exemplos da classe k", FORMULA),
        spacer(0.2),
        code_table([
            ("def fit(self, X, y):", "Recebe X (matriz n_amostras x n_features) e y (vetor de classes)."),
            ("self.classes_ = np.unique(y)", "Encontra os valores unicos de y. Para problema binario: array([0, 1])."),
            ("n_samples = X.shape[0]", "Total de amostras de treinamento. Shape[0] e o numero de linhas."),
            ("for c in self.classes_:", "Itera sobre cada classe (0 e 1) para calcular as estatisticas de cada uma."),
            ("    X_c = X[y == c]", "Seleciona apenas as linhas de X cujo rotulo e igual a classe c. Boolean indexing do NumPy."),
            ("    self.log_priors_[c] = np.log(len(X_c) / n_samples)", "Calcula o log do prior: log(proporcao de amostras da classe c). Usa log para evitar underflow numerico."),
            ("    self.means_[c] = np.mean(X_c, axis=0)", "Calcula a media de cada feature para a classe c. axis=0 opera ao longo das linhas, retornando vetor de shape (n_features,)."),
            ("    self.vars_[c] = np.var(X_c, axis=0) + self.var_smoothing", "Calcula a variancia por feature. Soma var_smoothing (1e-9) para garantir que nenhuma variancia seja zero (evita log(0) e divisao por zero na formula gaussiana)."),
            ("return self", "Retorna a propria instancia (padrao sklearn). Permite encadeamento: model.fit(X,y).predict(X_test)."),
        ]),
        spacer(0.3),
    ]

    # 4.4 _log_gaussian_pdf
    story += [
        h2("4.4 Metodo _log_gaussian_pdf(x, mean, var)"),
        p("<b>Resumo teorico:</b> Calcula o logaritmo natural da Funcao Densidade de Probabilidade (FDP) "
          "da distribuicao gaussiana. O prefixo '_' indica metodo privado (convencao Python). "
          "Em vez de calcular a probabilidade P(xi|Ck) diretamente e depois tomar o log, "
          "esta funcao calcula o log diretamente usando a forma analitica expandida, evitando "
          "calcular exp() e depois log() desnecessariamente."),
        p("log N(x; mu, sigma^2) = -0.5 * log(2*pi*sigma^2) - (x - mu)^2 / (2*sigma^2)", FORMULA),
        spacer(0.2),
        code_table([
            ("def _log_gaussian_pdf(self, x, mean, var):", "Recebe o valor da feature (x), a media (mean) e a variancia (var) para aquela feature e classe."),
            ("-0.5 * np.log(2 * np.pi * var)", "Primeiro termo: -0.5 * log(2*pi*sigma^2). E a constante de normalizacao da gaussiana no dominio logaritmico. Quanto maior a variancia, mais esta constante penaliza (distribuicao mais espalhada = menor pico)."),
            ("- ((x - mean) ** 2) / (2 * var)", "Segundo termo: -(x-mu)^2 / (2*sigma^2). E o expoente da gaussiana. Quanto mais x se afasta da media, mais negativo este valor fica, penalizando a probabilidade. Se x == mean, este termo e zero (maximo da gaussiana)."),
            ("return (soma dos dois termos)", "Retorna o log da densidade. Valores mais altos (menos negativos) indicam maior verossimilhanca de x pertencer a esta classe."),
        ]),
        spacer(0.2),
        p("DETALHE IMPORTANTE: Esta funcao opera de forma vetorizada quando x, mean e var sao arrays "
          "NumPy (como ocorre na pratica). Ao chamar _log_gaussian_pdf(x_amostra, means_[c], vars_[c]), "
          "x_amostra tem shape (10,), means_[c] tem shape (10,) e vars_[c] tem shape (10,). "
          "O resultado e um array de 10 log-densidades, um por feature.", CALLOUT),
        spacer(0.3),
    ]

    # 4.5 _log_posterior
    story += [
        h2("4.5 Metodo _log_posterior(x)"),
        p("<b>Resumo teorico:</b> Implementa o nucleo do Teorema de Bayes no dominio logaritmico. "
          "A classificacao Naive Bayes escolhe a classe que maximiza a probabilidade posterior P(Ck|x). "
          "Pela regra de Bayes: P(Ck|x) proporcional P(Ck) * P(x|Ck). Com a hipotese 'naive' "
          "(independencia condicional das features), P(x|Ck) = produto de P(xi|Ck). "
          "Tomando o logaritmo, o produto vira uma soma:"),
        p("log P(Ck|x) = log P(Ck) + sum_i [ log P(xi|Ck) ]", FORMULA),
        spacer(0.2),
        code_table([
            ("def _log_posterior(self, x):", "Recebe um unico vetor de features x com shape (n_features,)."),
            ("return {", "Retorna um dicionario Python com o log-posterior para cada classe."),
            ("    c: self.log_priors_[c]", "Para cada classe c: comeca com o log do prior log P(Ck)."),
            ("    + np.sum(", "Soma todos os log P(xi|Ck) de cada feature."),
            ("        self._log_gaussian_pdf(x, self.means_[c], self.vars_[c])", "Calcula o array de log-densidades (uma por feature) e np.sum() os soma todos, produzindo um escalar."),
            ("    for c in self.classes_", "Faz isso para cada classe. Resultado: {0: -17.3, 1: -21.1} (por exemplo)."),
        ]),
        spacer(0.2),
        p("NOTA: O denominador P(x) do Teorema de Bayes e omitido propositalmente. "
          "Como P(x) e o mesmo para todas as classes, nao afeta qual classe tem maior posterior. "
          "Por isso usamos 'proporcional' e nao 'igual'. A normalizacao so e feita em predict_proba().", WARNING),
        spacer(0.3),
    ]

    # 4.6 predict
    story += [
        h2("4.6 Metodo predict(X)"),
        p("<b>Resumo teorico:</b> Aplica a regra de decisao MAP (Maximum A Posteriori): "
          "para cada amostra, escolhe a classe com maior log-posterior. Como o logaritmo e uma "
          "funcao monotonica crescente, argmax do log-posterior equivale a argmax do posterior."),
        p("y_pred = argmax_k  [log P(Ck) + sum_i log P(xi|Ck)]", FORMULA),
        spacer(0.2),
        code_table([
            ("def predict(self, X):", "Recebe a matriz X com shape (n_amostras, n_features)."),
            ("predictions = []", "Cria lista vazia para acumular as predicoes."),
            ("for x in X:", "Itera sobre cada amostra (linha) da matriz X."),
            ("    log_posts = self._log_posterior(x)", "Calcula o dicionario {classe: log_posterior} para esta amostra."),
            ("    predictions.append(max(log_posts, key=log_posts.get))", "Encontra a chave (classe) que maximiza o valor do dicionario. max() com key=dict.get itera pelas chaves e compara pelos valores. Retorna a classe com maior log-posterior."),
            ("return np.array(predictions)", "Converte lista em array NumPy. Shape: (n_amostras,). Valores: 0 ou 1."),
        ]),
        spacer(0.3),
    ]

    # 4.7 predict_proba
    story += [
        h2("4.7 Metodo predict_proba(X)"),
        p("<b>Resumo teorico:</b> Converte os log-posteriors em probabilidades normalizadas "
          "usando a operacao de softmax numericamente estavel. O desafio e que os log-posteriors "
          "sao numeros grandes e negativos (ex: -124), e exp(-124) seria numericamente zero "
          "(underflow). A solucao e subtrair o maximo antes de aplicar exp():"),
        p("prob_k = exp(log_p_k - max(log_p)) / sum_j exp(log_p_j - max(log_p))", FORMULA),
        spacer(0.2),
        code_table([
            ("proba = []", "Lista para acumular arrays de probabilidades."),
            ("for x in X:", "Itera amostra por amostra."),
            ("    log_posts = self._log_posterior(x)", "Obtem {classe: log-posterior} para esta amostra."),
            ("    log_vals = np.array([log_posts[c] for c in sorted(self.classes_)])", "Extrai os valores em ordem de classe (0, 1) como array NumPy."),
            ("    log_vals -= np.max(log_vals)", "TRUCQUE DE ESTABILIDADE NUMERICA: subtrai o maior valor. Garante que o maior log-posterior vira 0, e exp(0)=1. Os outros ficam entre 0 e 1. Evita overflow/underflow."),
            ("    probs = np.exp(log_vals)", "Aplica a exponencial. Agora os valores sao proporcoes positivas, mas ainda nao somam 1."),
            ("    proba.append(probs / probs.sum())", "Normaliza para que as probabilidades somem 1. Cada elemento e entre 0 e 1."),
            ("return np.array(proba)", "Array de shape (n_amostras, n_classes). Cada linha soma 1."),
        ]),
        spacer(0.3),
    ]

    # 4.8 explain_sample
    story += [
        h2("4.8 Metodo explain_sample(x, feature_names)"),
        p("<b>Resumo teorico:</b> Metodo pedagogico que expoe todos os calculos intermediarios "
          "do Naive Bayes para uma unica amostra. Isso corresponde ao que o slide da materia mostra "
          "manualmente: calcular P(N) * P(Dear|N) * P(Friend|N), mas aqui de forma automatica e "
          "para qualquer numero de features e classes."),
        spacer(0.2),
        code_table([
            ("log_priors = {c: self.log_priors_[c] ...}", "Coleta log P(Ck) de cada classe ja calculado no fit(). Responde ao item 'a)' da atividade."),
            ("ll = {feature_names[i]: _log_gaussian_pdf(...)}", "Para cada feature, calcula log P(xi|Ck) usando a gaussiana. Resultado: dicionario feature -> valor."),
            ("log_likelihoods[c] = dict(sorted(ll.items(), key=lambda kv: kv[1], reverse=True))", "Ordena as features do maior para o menor log-likelihood. Permite ver quais features mais contribuem para aquela classe. Responde ao item 'b)'."),
            ("log_posteriors = self._log_posterior(x)", "Calcula o log-posterior total para cada classe (prior + soma likelihoods). Necessario para a normalizacao."),
            ("log_vals -= np.max(log_vals)", "Mesma estabilizacao numerica do predict_proba."),
            ("probs = np.exp(log_vals); probs /= probs.sum()", "Softmax para converter em probabilidades percentuais. Responde ao item 'c)'."),
            ("'predicted_class': max(log_posteriors, key=log_posteriors.get)", "Classe com maior log-posterior. Responde ao item 'd)'."),
            ("return {...}", "Dicionario com todos os dados intermediarios para impressao e visualizacao."),
        ]),
        spacer(0.3),
        PageBreak(),
    ]

    # 4.9 compute_confusion_matrix
    story += [
        h2("4.9 Funcao compute_confusion_matrix(y_true, y_pred, classes)"),
        p("<b>Resumo teorico:</b> A matriz de confusao e uma tabela NxN onde N e o numero de classes. "
          "Cada celula [i][j] conta quantas amostras da classe real i foram preditas como classe j. "
          "Para classificacao binaria:"),
        spacer(0.1),
    ]

    cm_data = [
        [Paragraph("", BODY_SMALL), Paragraph("<b>Pred: 0</b>", BODY_SMALL), Paragraph("<b>Pred: 1</b>", BODY_SMALL)],
        [Paragraph("<b>Real: 0</b>", BODY_SMALL), Paragraph("TN (Verdadeiro Negativo)", BODY_SMALL), Paragraph("FP (Falso Positivo)", BODY_SMALL)],
        [Paragraph("<b>Real: 1</b>", BODY_SMALL), Paragraph("FN (Falso Negativo)", BODY_SMALL), Paragraph("TP (Verdadeiro Positivo)", BODY_SMALL)],
    ]
    cmt = Table(cm_data, colWidths=[3.5*cm, 5.5*cm, 5.5*cm])
    cmt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#37474f")),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#37474f")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("TEXTCOLOR", (0,0), (0,-1), colors.white),
        ("BACKGROUND", (1,1), (1,1), colors.HexColor("#e8f5e9")),
        ("BACKGROUND", (2,2), (2,2), colors.HexColor("#e8f5e9")),
        ("BACKGROUND", (1,2), (1,2), colors.HexColor("#ffebee")),
        ("BACKGROUND", (2,1), (2,1), colors.HexColor("#fff8e1")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#90a4ae")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    story += [cmt, spacer(0.3)]

    story += [
        code_table([
            ("idx = {c: i for i, c in enumerate(classes)}", "Cria mapeamento classe -> indice. Ex: {0: 0, 1: 1}. Permite usar qualquer conjunto de classes, nao apenas 0 e 1."),
            ("cm = np.zeros((len(classes), len(classes)), dtype=int)", "Inicializa a matriz de zeros com tipo inteiro. Shape: (2, 2) para problema binario."),
            ("for t, p in zip(y_true, y_pred):", "Itera simultaneamente sobre rotulos reais (t) e preditos (p)."),
            ("    cm[idx[t]][idx[p]] += 1", "Incrementa a celula correta. Se t=1 e p=0, incrementa cm[1][0] (Falso Negativo)."),
            ("return cm", "Retorna a matriz 2x2 preenchida."),
        ]),
        spacer(0.3),
    ]

    # 4.10 load_and_prepare_data
    story += [
        h2("4.10 Funcao load_and_prepare_data()"),
        p("<b>Resumo teorico:</b> O dataset Diabetes originalmente e um problema de regressao "
          "(prever um valor continuo). Para aplicar classificacao, precisamos discretizar o target. "
          "A estrategia adotada e a binarizacao pela media: amostras com target acima da media "
          "recebem classe 1 (alta progressao), as demais recebem classe 0. Isso cria um problema "
          "balanceado quase equilibrado (247 vs 195 amostras)."),
        spacer(0.2),
        code_table([
            ("data = load_diabetes()", "Carrega o dataset do scikit-learn. Retorna objeto Bunch com .data (features), .target (alvo), .feature_names."),
            ("X = data.data", "Matriz numpy de shape (442, 10). Features ja normalizadas pelo scikit-learn."),
            ("feature_names = list(data.feature_names)", "Lista: ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']."),
            ("mean_target = float(np.mean(data.target))", "Calcula a media do target original (escalar ~152.13). Sera o limiar de binarizacao."),
            ("y = (data.target > mean_target).astype(int)", "Cria array binario: True onde target > media, False caso contrario. .astype(int) converte True->1 e False->0."),
            ("return X, y, feature_names, mean_target", "Retorna os 4 componentes necessarios para a atividade."),
        ]),
        spacer(0.3),
    ]

    # 4.11 run_part1
    story += [
        h2("4.11 Funcao run_part1(X, y, feature_names)"),
        p("<b>Resumo teorico:</b> Implementa a Parte 1 completa da atividade. O loop de 10 execucoes "
          "com seeds diferentes (0 a 9) serve para obter uma estimativa robusta da acuracia real do modelo. "
          "Usar uma unica divisao treino/teste pode dar resultados enviesados dependendo de quais amostras "
          "caem em cada conjunto. A media e desvio padrao das 10 acuracias dao uma visao mais confiavel "
          "do desempenho real."),
        spacer(0.2),
        code_table([
            ("unique, counts = np.unique(y, return_counts=True)", "Conta amostras por classe para exibir o balanceamento."),
            ("accuracies = []", "Lista para acumular as 10 acuracias."),
            ("last_model = last_X_test = last_y_test = None", "Variaveis que guardam o estado do ultimo treinamento para gerar a matriz de confusao e a explicacao."),
            ("for seed in range(10):", "Loop de 10 execucoes. seed vai de 0 a 9, controlando a aleatoriedade do split."),
            ("    X_train, X_test, y_train, y_test = train_test_split(..., test_size=0.2, random_state=seed)",
             "Divide 80% para treino e 20% para teste de forma reproduzivel. random_state=seed garante splits diferentes a cada iteracao."),
            ("    model = GaussianNaiveBayes()", "Instancia um NOVO modelo a cada iteracao (sem reutilizar pesos anteriores)."),
            ("    model.fit(X_train, y_train)", "Treina o modelo com os dados de treino desta iteracao."),
            ("    y_pred = model.predict(X_test)", "Gera predicoes para o conjunto de teste."),
            ("    accuracies.append(float(np.mean(y_pred == y_test)))", "Calcula acuracia: proporcao de predicoes corretas. y_pred == y_test gera array booleano; mean() converte para fracao."),
            ("    last_model, last_X_test, last_y_test = model, X_test, y_test", "Salva o estado do ultimo loop para uso posterior."),
            ("mean_acc = float(np.mean(accuracies))", "Media das 10 acuracias."),
            ("std_acc = float(np.std(accuracies))", "Desvio padrao das 10 acuracias. Indica a variabilidade do modelo dependendo do split."),
            ("y_pred_last = last_model.predict(last_X_test)", "Re-prediz com o ultimo modelo treinado para gerar a matriz de confusao."),
            ("cm = compute_confusion_matrix(..., [0, 1])", "Gera a matriz 2x2 de TN/FP/FN/TP."),
            ("sample = last_X_test[0]", "Seleciona a primeira amostra do conjunto de teste para a explicacao detalhada."),
            ("exp = last_model.explain_sample(sample, feature_names)", "Obtem todos os calculos intermediarios do Naive Bayes para essa amostra."),
        ]),
        spacer(0.3),
    ]

    # 4.12 run_part2
    story += [
        h2("4.12 Funcao run_part2(X, y, feature_names)"),
        p("<b>Resumo teorico:</b> Avaliacao de importancia de feature por treinamento univariado. "
          "Cada feature e usada como unico preditor (modelo 1D). Isso permite medir a capacidade "
          "discriminativa individual de cada feature, sem interferencia das outras. "
          "E uma forma simples de selecao de features (feature selection) baseada em desempenho preditivo."),
        spacer(0.2),
        code_table([
            ("feature_accs: dict = {}", "Dicionario para armazenar {feature_name: acuracia_media}."),
            ("for i, fname in enumerate(feature_names):", "Itera sobre as 10 features. i e o indice, fname e o nome."),
            ("    X_feat = X[:, i: i + 1]", "Seleciona apenas a coluna i de X. O slice 'i: i+1' mantém o shape 2D (n, 1) ao inves de (n,). Necessario para o fit()."),
            ("    accs = []", "Lista de acuracias para as 10 seeds desta feature."),
            ("    for seed in range(10):", "10 seeds para estimativa robusta de cada feature."),
            ("        model.fit(X_tr, y_tr); model.predict(X_te)", "Treino e predicao com modelo univariado."),
            ("        accs.append(float(np.mean(model.predict(X_te) == y_te)))", "Calcula e armazena a acuracia deste seed."),
            ("    feature_accs[fname] = float(np.mean(accs))", "Media das 10 seeds para esta feature. Salva no dicionario."),
            ("sorted_features = sorted(..., key=lambda kv: kv[1], reverse=True)", "Ordena o dicionario pelo valor (acuracia) em ordem decrescente. Resultado: [(s5, 0.73), (bmi, 0.71), ...]."),
        ]),
        spacer(0.3),
    ]

    # 4.13 run_part3
    story += [
        h2("4.13 Funcao run_part3(X, y, feature_names, sorted_features, acc_all, std_all)"),
        p("<b>Resumo teorico:</b> Aplica a selecao de features baseada no ranking da Parte 2. "
          "A hipotese e que as features com melhor poder discriminativo individual tambem contribuirao "
          "de forma mais significativa no modelo multivariado. Alem disso, remover features ruidosas ou "
          "redundantes pode melhorar o modelo porque a hipotese de independencia do Naive Bayes e violada "
          "quando features sao correlacionadas entre si."),
        spacer(0.2),
        code_table([
            ("top3_names = [f[0] for f in sorted_features[:3]]", "Extrai os nomes das 3 primeiras features do ranking. Ex: ['s5', 'bmi', 'bp']."),
            ("top3_idx = [list(feature_names).index(n) for n in top3_names]", "Obtem os indices dessas features na matriz X original. Necessario para o fatiamento."),
            ("X_top3 = X[:, top3_idx]", "Cria nova matriz com apenas as 3 colunas selecionadas. Shape: (442, 3)."),
            ("for seed in range(10): ... accs.append(...)", "Mesmo loop de 10 seeds para estimativa robusta com o modelo reduzido."),
            ("diff = mean_acc - acc_all", "Diferenca entre acuracia do modelo com top-3 e o modelo completo. Positivo = top-3 e melhor."),
            ("direction = 'superior' if diff > 0 else 'inferior' ...", "Interpretacao automatica da comparacao."),
        ]),
        spacer(0.2),
        p("RESULTADO OBSERVADO: O modelo top-3 (s5=0.7315, bmi=0.7067, bp=0.6730) obteve acuracia "
          "media ~71.9% vs ~69.4% do modelo completo. Isso demonstra que as features s1, s2, s3, s4, "
          "s6, age e sex introduzem mais ruido do que informacao util para este classificador, "
          "provavelmente devido a correlacoes entre elas que violam a hipotese de independencia "
          "condicional do Naive Bayes.", CALLOUT),
        PageBreak(),
    ]

    # -----------------------------------------------------------------------
    # 5. FLUXO COMPLETO
    # -----------------------------------------------------------------------
    story += [
        h1("5. Fluxo Completo de Execucao"),
        hr(),
        spacer(0.2),
        p("O diagrama abaixo resume como os dados fluem pelo sistema durante uma execucao completa:"),
        spacer(0.3),
    ]

    flow_data = [
        [Paragraph("<b>Etapa</b>", BODY_SMALL), Paragraph("<b>Funcao</b>", BODY_SMALL),
         Paragraph("<b>Entrada</b>", BODY_SMALL), Paragraph("<b>Saida</b>", BODY_SMALL)],
        [Paragraph("1. Carga", BODY_SMALL), Paragraph("load_and_prepare_data()", BODY_SMALL),
         Paragraph("Dataset bruto", BODY_SMALL), Paragraph("X (442x10), y (442,), feature_names", BODY_SMALL)],
        [Paragraph("2. Split", BODY_SMALL), Paragraph("train_test_split()", BODY_SMALL),
         Paragraph("X, y, seed", BODY_SMALL), Paragraph("X_train, X_test, y_train, y_test", BODY_SMALL)],
        [Paragraph("3. Treino", BODY_SMALL), Paragraph("model.fit()", BODY_SMALL),
         Paragraph("X_train, y_train", BODY_SMALL), Paragraph("log_priors, means, vars por classe", BODY_SMALL)],
        [Paragraph("4. Inferencia", BODY_SMALL), Paragraph("model.predict()", BODY_SMALL),
         Paragraph("X_test", BODY_SMALL), Paragraph("y_pred (array de 0s e 1s)", BODY_SMALL)],
        [Paragraph("5. Avaliacao", BODY_SMALL), Paragraph("np.mean(y_pred == y_test)", BODY_SMALL),
         Paragraph("y_pred, y_test", BODY_SMALL), Paragraph("acuracia (float 0..1)", BODY_SMALL)],
        [Paragraph("6. Repeticao", BODY_SMALL), Paragraph("loop seeds 0..9", BODY_SMALL),
         Paragraph("seeds diferentes", BODY_SMALL), Paragraph("lista de 10 acuracias", BODY_SMALL)],
        [Paragraph("7. Relatorio", BODY_SMALL), Paragraph("mean, std, explain_sample, plots", BODY_SMALL),
         Paragraph("lista de acuracias", BODY_SMALL), Paragraph("console + 4 PNGs em output/", BODY_SMALL)],
    ]
    ft2 = Table(flow_data, colWidths=[2.5*cm, 4.5*cm, 4*cm, 6.2*cm])
    ft2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#e3f2fd")]),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#90caf9")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story += [ft2, spacer(0.3), PageBreak()]

    # -----------------------------------------------------------------------
    # 6. RESULTADOS
    # -----------------------------------------------------------------------
    story += [
        h1("6. Resultados Obtidos"),
        hr(),
        spacer(0.2),
        h2("6.1 Distribuicao das classes"),
        p("Apos binarizacao do target pela media (152.13):"),
        p("  Classe 0 (progressao <= media): 247 amostras (55.9%)", CODE_STYLE),
        p("  Classe 1 (progressao >  media): 195 amostras (44.1%)", CODE_STYLE),
        p("Dataset razoavelmente balanceado — nenhuma tecnica de re-amostragem foi necessaria."),
        spacer(0.3),

        h2("6.2 Parte 1 — Todas as features"),
        p("  Acuracia media (10 runs): 0.6944  (+/- 0.0507)", CODE_STYLE),
        p("  Matriz de confusao (ultimo treinamento): TN=43, FP=13, FN=6, TP=27", CODE_STYLE),
        spacer(0.3),

        h2("6.3 Parte 2 — Ranking de features"),
    ]

    rank_data = [
        [Paragraph("<b>Rank</b>", BODY_SMALL), Paragraph("<b>Feature</b>", BODY_SMALL),
         Paragraph("<b>Acuracia media</b>", BODY_SMALL), Paragraph("<b>Interpretacao</b>", BODY_SMALL)],
        [Paragraph("1", BODY_SMALL), Paragraph("s5", BODY_SMALL), Paragraph("0.7315", BODY_SMALL),
         Paragraph("Log dos triglicerideos — forte marcador de diabetes", BODY_SMALL)],
        [Paragraph("2", BODY_SMALL), Paragraph("bmi", BODY_SMALL), Paragraph("0.7067", BODY_SMALL),
         Paragraph("IMC — fator de risco bem estabelecido para diabetes", BODY_SMALL)],
        [Paragraph("3", BODY_SMALL), Paragraph("bp", BODY_SMALL), Paragraph("0.6730", BODY_SMALL),
         Paragraph("Pressao arterial — correlacionada com sindrome metabolica", BODY_SMALL)],
        [Paragraph("4", BODY_SMALL), Paragraph("s4", BODY_SMALL), Paragraph("0.6483", BODY_SMALL),
         Paragraph("Razao colesterol total/HDL", BODY_SMALL)],
        [Paragraph("5-10", BODY_SMALL), Paragraph("...", BODY_SMALL), Paragraph("0.5562-0.6270", BODY_SMALL),
         Paragraph("Contribuicao individual menor", BODY_SMALL)],
    ]
    rkt = Table(rank_data, colWidths=[1.5*cm, 2*cm, 3.5*cm, 10.2*cm])
    rkt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,3), colors.HexColor("#e8f5e9")),
        ("BACKGROUND", (0,4), (-1,-1), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#90caf9")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story += [rkt, spacer(0.3)]

    story += [
        h2("6.4 Parte 3 — Top 3 features vs Todas"),
    ]

    comp2_data = [
        [Paragraph("<b>Modelo</b>", BODY_SMALL), Paragraph("<b>Features</b>", BODY_SMALL),
         Paragraph("<b>Acuracia media</b>", BODY_SMALL), Paragraph("<b>Desvio padrao</b>", BODY_SMALL)],
        [Paragraph("Todas as features", BODY_SMALL), Paragraph("10 features", BODY_SMALL),
         Paragraph("0.6944", BODY_SMALL), Paragraph("+/- 0.0507", BODY_SMALL)],
        [Paragraph("Top 3 features", BODY_SMALL), Paragraph("s5, bmi, bp", BODY_SMALL),
         Paragraph("0.7191", BODY_SMALL), Paragraph("+/- 0.0389", BODY_SMALL)],
    ]
    c2t = Table(comp2_data, colWidths=[4*cm, 4*cm, 4*cm, 5.2*cm])
    c2t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1565c0")),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,2), (-1,2), colors.HexColor("#e8f5e9")),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#90caf9")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (2,0), (-1,-1), "CENTER"),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    story += [c2t, spacer(0.3)]

    story += [
        p("CONCLUSAO: O modelo com 3 features foi +2.47 pontos percentuais superior ao modelo "
          "com 10 features. Isso e consistente com a teoria do Naive Bayes: quanto mais features "
          "correlacionadas existem, mais a hipotese de independencia e violada, degradando a "
          "qualidade das estimativas de probabilidade. s5 (triglicerideos), bmi (IMC) e bp "
          "(pressao arterial) sao os tres fatores clinicos mais associados a progressao do diabetes, "
          "o que tambem valida o resultado do ponto de vista medico.", CALLOUT),
    ]

    return story


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    output_path = os.path.join(
        os.path.expanduser("~"), "Downloads", "NaiveBayes_Explicacao.pdf"
    )

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.2*cm,
        bottomMargin=2*cm,
        title="Naive Bayes Gaussiano - Documentacao Tecnica",
        author="Atividade Pratica 2",
    )

    story = build_content()
    doc.build(story)
    print(f"PDF gerado com sucesso:\n  {output_path}")


if __name__ == "__main__":
    main()
