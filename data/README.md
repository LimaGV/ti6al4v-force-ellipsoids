# Dados do estudo

## `raw/Forcas_C50_R08.xlsx`

Sinais temporais originais dos 19 experimentos. A primeira coluna está vazia e cada ensaio ocupa quatro colunas consecutivas:

```text
Tempo [s] | Fc [N] | Ff [N] | Fp [N]
```

## `metadata/DOE_titanio_C50_R08_CCD.xlsx`

Planejamento Composto Central e respostas experimentais. O notebook utiliza `experimento`, `Vc`, `f`, `ap` e `Ra`.

## `validation/teste_OLS_referencia.xlsx`

Tabela usada para conferir `mahalanobis_centroide`, `razao_a_b` e `razao_b_c` após a extração desde os sinais.

## `processed/experiment_summary.csv`

Tabela arredondada apresentada no artigo. Ela reproduz praticamente o mesmo modelo, com pequenas diferenças nas últimas casas decimais.

## Regra de processamento

Para cada experimento, removem-se 10% das amostras iniciais e 10% das finais. A covariância tridimensional é calculada com os 80% centrais. As características recalculadas coincidem com a planilha de referência com erro absoluto inferior a `1e-9`.
