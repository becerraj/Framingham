import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import pdb
import statsmodels.api as sm
import openpyxl

# LOAD DATA----
# I load the data set
data_set = pd.read_excel("/home/juan/Github/Framingham/normalized_data.xlsx")

# 2 maneras de separar en train y test:
# Opcion 1: Va a separar las filas. Despues dividimos en columnas de prediccion y variables.
train, test = train_test_split(data_set, test_size=0.3, train_size=0.7,
                               random_state=0)

# Opcion 2: Pasando las variables y la columna predictora hace la separacion
x = data_set.iloc[:, range(0, len(data_set.columns) - 2)]
y = data_set.iloc[:, len(data_set.columns) - 1]
x_train, y_train, x_test, y_test = train_test_split(x, y,
                                                    test_size=0.3, train_size=0.7,
                                                    random_state=0)
# Probablemente para un approach facilmente visible podriamos hacer un PCA y quedarnos
# solo con los dos primeros componentes. De ahi en mas seguir con el analisis para poder
# graficarlo. No tiene mucho sentido en el caso de querer usar todas las variables, pero
# si los resultados son correctos, podria probarse para mostrarle al cliente.


# 3 Feature Scaling
# from sklearn.preprocessing import StandardScaler
# sc_X = StandardScaler()
# sc_y = StandardScaler()
# X = sc_X.fit_transform(X)
# y = sc_y.fit_transform(y)

# Fitting the Support Vector Regression Model to the dataset
# most important SVR parameter is Kernel type.
# It can be linear, polynomial or gaussian SVR. Kernel coefficient for 'linear', 'rbf', 'poly' and 'sigmoid'.
model = SVR(kernel='linear',
            C=1, epsilon=0.1)

model.fit(x_train, x_test)

prediction = model.predict(y_train)


def bland_altman_plot(data1, data2, *args, **kwargs):
    data1 = np.asarray(data1)
    data2 = np.asarray(data2)
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2  # Difference between data1 and data2
    md = np.mean(diff)  # Mean of the difference
    sd = np.std(diff, axis=0)  # Standard deviation of the difference
    CI_low = md - 1.96 * sd
    CI_high = md + 1.96 * sd
    lowess = sm.nonparametric.lowess(diff, mean, frac=0.5)

    plt.scatter(mean, diff, *args, **kwargs)
    plt.plot(lowess[:, 0], lowess[:, 1])
    plt.axhline(md, color='black', linestyle='-')
    plt.axhline(md + 1.96 * sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96 * sd, color='gray', linestyle='--')
    return md, sd, mean, CI_low, CI_high


md, sd, mean, CI_low, CI_high = bland_altman_plot(prediction, y_test)
plt.title(r"$\mathbf{Bland-Altman}$" + " " + r"$\mathbf{SVM Plot}$")
plt.xlabel("Risk")
plt.ylabel("Error")
plt.ylim(md - 3.5 * sd, md + 3.5 * sd)

BA_plot = np.min(mean) + (np.max(mean) - np.min(mean)) * 1.14

plt.text(BA_plot, md - 1.96 * sd,
         r'-1.96SD:' + "\n" + "%.2f" % CI_low,
         ha="center",
         va="center",
         )
plt.text(BA_plot, md + 1.96 * sd,
         r'+1.96SD:' + "\n" + "%.2f" % CI_high,
         ha="center",
         va="center",
         )
plt.text(BA_plot, md,
         r'Mean:' + "\n" + "%.2f" % md,
         ha="center",
         va="center",
         )
plt.subplots_adjust(right=0.85)

plt.show()
