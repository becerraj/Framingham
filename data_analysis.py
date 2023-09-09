import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from sklearn.decomposition import PCA

# #LOAD DATA----
# I load the data set.
data_set = pd.read_excel("/home/juan/Github/Framingham/clean_data.xlsx")

# # DATA TRANSFORMATION ----
# Data transformation. I'm looking to transform the risk variable.
# Let's first visualize it graphically with a logarithmic transformation.
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
axs[0].violinplot(data_set['riesgo'],
                  showmeans=False,
                  showmedians=True)
axs[0].set_title('Riesgo')

# plot box plot
axs[1].violinplot(np.log10(data_set['riesgo'] + 1 - data_set['riesgo'].min()))
axs[1].set_title('Riesgo Transformado')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_ylabel('Value')

plt.show()

# The graph shows that the data takes on a more normal distribution.
# This is beneficial when building a machine learning (ML) or deep learning (DL) model.
data_set['riesgo'] = np.log10(data_set['riesgo'] + 1 - data_set['riesgo'].min())

# We can say that the data has been cleaned and is ready for ML or DL techniques.
# Depending on the method, we will either normalize or standardize the data.

# Para hacer el analisis que estamos buscando, primero sacamos los datos de parametros serologicos
data_set = data_set.drop(['ctotal', 'chdl', 'cldl', 'tri', 'gli', 'hba1c'], axis=1)

# # NORMALIZATION AND STANDARDIZATION
# Normalizo los datos que no son binarios
def normalizacion_minmax(columna):
    maximo = columna.max()
    minimo = columna.min()
    columna_normalizada = ((columna - minimo) / (maximo - minimo))
    return columna_normalizada


def estandarizado_zscore(columna):
    media = np.mean(columna)
    varianza = np.var(columna)
    columna_estandarizada = (columna - media) / varianza
    return columna_estandarizada


# Using data_set.items() creates a generator.
for col_name, col in data_set.items():
    if not (col.max == 1) & (col.min == 0):
        data_set[col_name] = normalizacion_minmax(estandarizado_zscore(col))

description = data_set.describe()

# # CORRELATION MATRIX----
# Matriz de correlacion de variables
matriz_correlacion = data_set.corr()
# Etiquetas
labs = data_set.columns
# Mapa de calor
fig, ax = plt.subplots()
im = ax.imshow(matriz_correlacion, cmap='Blues')

# Agregar las etiquetas
ax.set_xticks(np.arange(len(labs)), labels=labs)
ax.set_yticks(np.arange(len(labs)), labels=labs)

# Rotar las etiquetas del eje X
plt.setp(ax.get_xticklabels(), rotation=40,
         ha="right", rotation_mode="anchor")

cbar = ax.figure.colorbar(im, ax=ax)

plt.show()

data_set.to_excel("/home/juan/Github/Framingham/normalized_data.xlsx", index=False)
