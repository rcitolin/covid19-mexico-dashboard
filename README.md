# COVID-19 no México: quem corre mais risco

Dashboard interativo sobre 1.048.575 pacientes de COVID-19 atendidos no sistema de saúde do México. Mostra como idade, sexo, doenças preexistentes, gravidade do quadro e unidade médica se relacionam com a letalidade.

## Dados

- **Fonte:** [COVID-19 Dataset](https://www.kaggle.com/datasets/meirnizri/covid19-dataset) (Meir Nizri, Kaggle, licença CC0), a partir dos [dados abertos do governo do México](https://datos.gob.mx/busca/dataset/informacion-referente-a-casos-covid-19-en-mexico).
- **Arquivo usado no painel:** [`data/covid_mexico_agregado.csv`](data/covid_mexico_agregado.csv). As 1.048.575 linhas originais (58 MB) foram agrupadas em 88.646 combinações únicas com contagem (2,5 MB), sem perder os cruzamentos usados nos filtros.

| Coluna | Significado |
|---|---|
| `sexo` | `F` ou `M` |
| `faixa` | início da faixa etária de 5 anos (`90` = 90 anos ou mais) |
| `atendimento` | `A` ambulatorial, `H` internado |
| `resultado` | `pos` (classificação final 1–3) ou `neg` (negativo ou inconclusivo) |
| `unidade` | unidade médica (1 a 13) |
| `pneumonia`, `intubado`, `uti` | `1` sim, `0` não ou sem informação |
| `comorb` | bitmask das doenças preexistentes, na ordem: diabetes, DPOC, asma, imunossupressão, hipertensão, outra, cardiovascular, obesidade, renal crônica, tabagismo |
| `mes_obito` | mês do óbito (`AAAA-MM`), vazio se sobreviveu |
| `pacientes` | quantidade de pacientes com essa combinação |

## Principais achados (pacientes com teste positivo)

- Letalidade de **13,8%** (54.236 óbitos entre 391.979 pacientes).
- A partir dos 60 anos a letalidade é **18 vezes maior** que abaixo dos 40 (40,2% contra 2,2%).
- Doença renal crônica (44,7%), DPOC (41,4%), doença cardiovascular (33,6%) e diabetes (32,7%) são as condições mais associadas a óbito. Asma não eleva o risco.
- O risco se acumula: 7,1% sem nenhuma doença preexistente, 37,3% com três ou mais.
- Homens morreram mais que mulheres: 16,8% contra 10,4%.
- Pico de óbitos entre maio e julho de 2020.

## O painel

- **Filtros:** resultado do teste, sexo, tipo de atendimento, faixa etária, unidade médica e doenças preexistentes.
- **Filtros pelos gráficos:** clicar numa faixa etária, num lado da pirâmide, numa doença ou numa unidade médica filtra todo o painel.
- **Gráficos:** indicadores principais, letalidade por faixa etária, pirâmide etária, letalidade com e sem cada doença, efeito do número de doenças, cascata de gravidade, óbitos por mês e dispersão das unidades médicas.

## Estrutura

```
index.html                     versão standalone (abre direto no navegador ou no GitHub Pages)
artifact/covid-dashboard.html  página original, escrita para o tipo Dashboard dos artefatos do Claude
data/covid_mexico_agregado.csv base agregada usada pelo painel
scripts/build_dataset.py       gera a base agregada a partir do CSV original
scripts/profile_dataset.py     análise exploratória usada para escolher os gráficos
scripts/make_standalone.py     gera index.html a partir de artifact/covid-dashboard.html
```

## Como rodar

O painel carrega o CSV com `fetch`, então precisa de um servidor HTTP (abrir o arquivo direto com `file://` não funciona):

```bash
python3 -m http.server 8000
```

Depois abra http://localhost:8000. No GitHub Pages, publique a branch `main` na raiz.

Para regenerar a base a partir do CSV original do Kaggle (`Covid Data.csv`):

```bash
python3 scripts/build_dataset.py "Covid Data.csv" data/covid_mexico_agregado.csv
```

Depois de alterar `artifact/covid-dashboard.html`, regenere a versão standalone:

```bash
python3 scripts/make_standalone.py
```

## Observações de método

- **Letalidade** é a parcela de pacientes com data de óbito registrada. Não é a taxa de mortalidade da população.
- Doença preexistente sem informação foi tratada como ausente. Intubação e UTI só existem para pacientes internados.
- A base traz apenas a data do óbito, não a data de entrada. Óbitos registrados em janeiro e fevereiro de 2020 são provável erro de cadastro e aparecem em cinza.
