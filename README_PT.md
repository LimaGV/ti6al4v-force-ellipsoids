# Elipsoides de Covariância das Forças de Usinagem e Modelagem da Rugosidade

Repositório de reprodutibilidade do trabalho:

**“Representações Elipsoidais Multivariadas das Forças de Usinagem para Modelagem da Rugosidade Superficial no Torneamento de Ti-6Al-4V.”**

O estudo utiliza um Planejamento Composto Central com 19 experimentos, sinais tridimensionais das forças de usinagem, elipsoides de covariância, descritores geométricos e regressão linear múltipla para modelar a rugosidade média `Ra`.

## Modelo reproduzido desde os sinais brutos

Usando os sinais originais e a precisão numérica completa das características extraídas:

```text
Ra = -1,758866 + 0,531748(a/b) + 0,00740784[dM × (b/c)]
```

A regressão obtida com os valores arredondados apresentados na tabela do artigo é praticamente idêntica:

```text
Ra = -1,758970 + 0,531757(a/b) + 0,007408[dM × (b/c)]
```

Resultados da reprodução completa:

| Métrica | Valor |
|---|---:|
| R² ajustado | 0,9463 |
| R² LOOCV | 0,9294 |
| MAE LOOCV | 0,3394 |
| RMSE LOOCV | 0,4040 |

## Notebook principal

```text
notebooks/00_metodologia_reprodutivel_dados_reais.ipynb
```

O notebook:

1. lê a planilha original com os sinais dos 19 experimentos;
2. remove 10% do início e 10% do final de cada ensaio;
3. calcula a matriz de covariância 3D e sua decomposição espectral;
4. extrai `a/b`, `b/c` e a distância de Mahalanobis;
5. compara os resultados com a planilha usada no ajuste original;
6. ajusta o modelo OLS e executa a validação LOOCV;
7. exporta coeficientes, predições, figuras e o resumo de reprodutibilidade.

As diferenças máximas entre as características recalculadas e a planilha original são inferiores a `1e-9`.

## Estrutura principal

```text
.
├── data/
│   ├── raw/Forcas_C50_R08.xlsx
│   ├── metadata/DOE_titanio_C50_R08_CCD.xlsx
│   ├── validation/teste_OLS_referencia.xlsx
│   └── processed/experiment_summary.csv
├── notebooks/
│   ├── 00_metodologia_reprodutivel_dados_reais.ipynb
│   ├── 00_metodologia_resumida.ipynb
│   ├── 01_reproduce_published_model.ipynb
│   └── 02_extract_ellipsoid_features_template.ipynb
├── src/machining_ellipsoids/
├── scripts/
├── tests/
├── figures/
├── results/
└── CITATION.cff
```

## Execução

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
jupyter lab notebooks/00_metodologia_reprodutivel_dados_reais.ipynb
```

Para executar os testes:

```bash
pytest
```

## Situação dos dados

A planilha dos sinais brutos, o DOE e a tabela de validação estão incluídos neste pacote. Antes de tornar o repositório público, todos os coautores devem confirmar que a distribuição pública dos dados está autorizada.

## Antes de publicar

1. Substitua `SEU-USUARIO` no `CITATION.cff`.
2. Inclua os ORCIDs autorizados.
3. Confirme a licença aplicável aos sinais brutos.
4. Não publique a versão diagramada pelo evento sem conferir os direitos autorais.
5. Crie uma release `v1.0.0` e arquive-a no Zenodo para obter um DOI.
