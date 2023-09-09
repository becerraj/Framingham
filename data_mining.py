import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from sklearn.preprocessing import MinMaxScaler

# #LOAD DATA----
# I load the data set
data_set = pd.read_excel("/home/juan/Github/Data_Science_2023/CartagenaCohortStudy_DATA.xlsx")

# #EXTRACT DATA----
tratamiento_hta = data_set.loc[:, ['tto_hta_p___1',
                                   'tto_hta_p___2', 'tto_hta_p___3', 'tto_hta_p___4', 'tto_hta_p___5',
                                   'tto_hta_p___6', 'tto_hta_p___7', 'tto_hta_p___8', 'tto_hta_p___9',
                                   'cual_araii___1', 'cual_araii___2', 'cual_araii___3', 'cual_araii___4',
                                   'cual_ca___1', 'cual_ca___2', 'cual_ca___3', 'cual_ca___4',
                                   'cual_ca___5', 'cual_ca___6', 'cual_ca___7', 'cual_ca___8',
                                   'cual_ca___9', 'cual_bb___1', 'cual_bb___2', 'cual_bb___3',
                                   'cual_bb___4', 'cual_bb___5', 'cual_bb___6', 'cual_bb___7',
                                   'cual_bb___8', 'cual_bb___9', 'cual_bb___10', 'cual_ieca___1',
                                   'cual_ieca___2', 'cual_ieca___3', 'cual_ieca___4', 'cual_ieca___5',
                                   'cual_diu___1', 'cual_diu___2', 'cual_diu___3', 'cual_diu___4',
                                   'cual_digi___1', 'cual_digi___2', 'tto_hta_p_otro']]


# Check if a 1 is present in any cell of the row, and return the value 1.99881. If there are no 1s, return 1.93303.
def buscarUno(fila):
    if (fila == 1).any():
        return 1.99881
    else:
        return 1.93303


hay_tratamiento = []
# Apply generates an iteration and internally stores the returned results.
hay_tratamiento = tratamiento_hta.apply(buscarUno, axis=1).tolist()

# Remove columns that are irrelevant. Also remove ID columns.
# indices_a_eliminar = list(range(11, 54+1)) + list(range(70, 78+1))
# Possible column removal:
# data_set = data_set.drop(data_set.columns[indices_a_eliminar], axis = 1)
data_set = data_set.drop(['study_id', 'tto_hta_p___1', 'dis_p_act',
                          'tto_hta_p___2', 'tto_hta_p___3', 'tto_hta_p___4', 'tto_hta_p___5',
                          'tto_hta_p___6', 'tto_hta_p___7', 'tto_hta_p___8', 'tto_hta_p___9',
                          'cual_araii___1', 'cual_araii___2', 'cual_araii___3', 'cual_araii___4',
                          'cual_ca___1', 'cual_ca___2', 'cual_ca___3', 'cual_ca___4',
                          'cual_ca___5', 'cual_ca___6', 'cual_ca___7', 'cual_ca___8',
                          'cual_ca___9', 'cual_bb___1', 'cual_bb___2', 'cual_bb___3',
                          'cual_bb___4', 'cual_bb___5', 'cual_bb___6', 'cual_bb___7',
                          'cual_bb___8', 'cual_bb___9', 'cual_bb___10', 'cual_ieca___1',
                          'cual_ieca___2', 'cual_ieca___3', 'cual_ieca___4', 'cual_ieca___5',
                          'cual_diu___1', 'cual_diu___2', 'cual_diu___3', 'cual_diu___4',
                          'cual_digi___1', 'cual_digi___2', 'tto_hta_p_otro', 'cvf_prev',
                          'vef1_prev', 'vef1_cvf_prev', 'pef_prev', 'vef1_pre', 'cvf_pre',
                          'vef1_cvf_pre', 'pef_pre', 'vef1_pre_por', 'a_vertebral',
                          'insuficiencia_vb'], axis=1)

# Add the column indicating if there is treatment.
data_set['hay_tto'] = hay_tratamiento

# What data types do I have?
description = data_set.describe()
data_set.dtypes

# I continue reducing the number of columns: BMI = Weight + Height. WHR = WC + HC.
data_set = data_set.drop(['peso', 'talla', 'per_cin', 'per_cad', 'i_m_carotidea',
                          'localidad'], axis=1)

# How many NA values do I have?
data_set.isna().sum().sum()
# I have 465 NA
data_set.isna().any(axis=1).sum()
# There are NA values in 111 rows. Many patients have +1 data with NA.
# What percentage of NA do I have in each column?
data_set.isna().sum() / data_set.shape[0] * 100

# Now that I have all the columns I'm interested in, I'm going to remove rows with NaN values.
data_set = data_set.dropna()

# vef1_cvf_pre_por y intima_m_c_d must be numeric
# First, I convert it to a string data type so that str.replace works. It was previously an object.
intima_to_float = data_set['intima_m_c_d'].astype(str).str.replace(",", ".").str.replace("|", "")
data_set['intima_m_c_d'] = intima_to_float.astype(float)
data_set['vef1_cvf_pre_por'] = data_set['vef1_cvf_pre_por'].astype(float)
data_set[['gender', 'placas_atero']] = data_set[['gender', 'placas_atero']].astype(int)


# Some variables have 2=Yes, 1=No. I'm changing them to normalize with the rest of the variables and then binarize.
def two_to_one(fila):
    if fila == 2:
        return 1
    else:
        return 0

# The .apply() function knows how many axes the DataFrame we're giving it has.
# If it has only one, we don't need to specify 'axis.' Otherwise, it breaks.
data_set['expo_tab_otro'] = data_set['expo_tab_otro'].apply(two_to_one)
data_set['ant_p_enf'] = data_set['ant_p_enf'].apply(two_to_one)
data_set['dis_p'] = data_set['dis_p'].apply(two_to_one)
data_set['hta_p'] = data_set['hta_p'].apply(two_to_one)
data_set['ecv_p'] = data_set['ecv_p'].apply(two_to_one)
data_set['dm2_p'] = data_set['dm2_p'].apply(two_to_one)

# I create and analyze a boxplot and violin plot for each non-binary variable to observe the outliers.
for i in range(0, len(data_set.columns)):
    if data_set.iloc[:, i].dtypes == float:
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
        axs[0].violinplot(data_set.iloc[:, i],
                          showmeans=False,
                          showmedians=True)
        axs[0].set_title('Violin plot')

        # plot box plot
        axs[1].boxplot(data_set.iloc[:, i])
        axs[1].set_title('Box plot')

        # adding horizontal grid lines
        for ax in axs:
            ax.yaxis.grid(True)
            ax.set_xlabel(data_set.columns[i])
            ax.set_ylabel('Values')

        plt.show()

# After analyzing the boxplot, I remove the outliers.
# Considering the amount of data we have and the observed outliers,
# I'm going to remove the outliers according to the Tukey test, using the interquartile range.
description = data_set.describe()
indices_a_eliminar = []
for i in range(0, len(data_set.columns) - 1):
    if data_set.iloc[:, i].dtypes == float:
        limite_superior = ((description.iloc[:, i]['75%'] - description.iloc[:, i]['25%']) * 2) + \
                          description.iloc[:, i]['75%']
        limite_inferior = description.iloc[:, i]['25%'] - (
                    (description.iloc[:, i]['75%'] - description.iloc[:, i]['25%']) * 2)
        indices = list(data_set.iloc[:, i][
                           (data_set.iloc[:, i] > limite_superior) | (data_set.iloc[:, i] < limite_inferior)].index)
        indices_a_eliminar.extend(indices)

indices_a_eliminar = set(sorted(indices_a_eliminar))
# With 76 outlier values, I remove those rows.len(indices_a_eliminar)
data_set = data_set.drop(indices_a_eliminar)


#ANALISIS----
## FORMULA ----
# Risk Factor = (ln(Age) * 3.06117) + (ln(Total Cholesterol) * 1.12370) - (ln(HDL Cholesterol) * 0.93263) + (ln(BP Systolic) * BP factor Systolic) + Smoker + DM - 23.9802
factores_de_riesgo = (np.log(data_set['age']) * 3.06117) + (np.log(data_set['ctotal']) * 1.12370) - (np.log(data_set['chdl']) * 0.93263) + (np.log(data_set['pre_art_sis']) * data_set['hay_tto']) + data_set['expo_tab_otro'] + data_set['dm2_p'] - 23.9802
riesgo = 100 * (1 - 0.88936 ** np.exp(factores_de_riesgo))

# I add the risk variable to the data set.
data_set = data_set.drop('hay_tto', axis = 1)
data_set['riesgo'] = riesgo

# Data transformation. I'm looking to transform the risk variable.
# Let's first visualize it graphically with a logarithmic transformation.
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
axs[0].violinplot(riesgo,
                  showmeans=False,
                  showmedians=True)
axs[0].set_title('Riesgo')

# plot box plot
axs[1].violinplot(np.log10(riesgo + 1 - riesgo.min()))
axs[1].set_title('Riesgo Transformado')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_ylabel('Value')

plt.show()

# The graph shows that the data takes on a more normal distribution.
# This is beneficial when building a machine learning (ML) or deep learning (DL) model.
# We can say that the data has been cleaned and is ready for ML or DL techniques.
# Depending on the method, we will either normalize or standardize the data.
# This process will be found in the next respective scripts.

# Using data_set.items() creates a generator.
for col_name, col in data_set.items():
    if col.dtype == float:
        data_set[col_name] = estandarizado_zscore(normalizacion_minmax(col))

data_set.to_excel("/home/juan/Github/Framingham/clean_data.xlsx", index=False)
