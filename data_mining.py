import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
from sklearn.preprocessing import MinMaxScaler

# #CARGO DATA----
# # Cargo el data_set

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


# Busca si en la fila se encuentra un 1 en alguna celda, y devuelve el valor 1.99881. Si no hay ningun 1, devuelve 1.93303
def buscarUno(fila):
    if (fila == 1).any():
        return 1.99881
    else:
        return 1.93303


hay_tratamiento = []
# Apply genera una iteracion y va guardando interiormente los resultados devueltos.
hay_tratamiento = tratamiento_hta.apply(buscarUno, axis=1).tolist()

# Elimino las columnas que son ttos. Tambien las de ID
# indices_a_eliminar = list(range(11, 54+1)) + list(range(70, 78+1))
# Posibilidades de eliminar columnas:
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

# Agrego la columna que dice si hay tratamiento
data_set['hay_tto'] = hay_tratamiento

# Que tipos de dato tengo?
description = data_set.describe()
data_set.dtypes

# Sigo achicando el numero de columnas: IMC = Peso + talla. ICC = PC + PC
data_set = data_set.drop(['peso', 'talla', 'per_cin', 'per_cad', 'i_m_carotidea',
                          'localidad'], axis=1)

# Ahora ya tengo todas las columnas que me interesan. Voy a sacar las filas con NAN
# # Cuantos NA tengo?
data_set.isna().sum().sum()
# Tengo 465 NA
data_set.isna().any(axis=1).sum()
# Hay NA en 111 filas. Muchos pacientes tienen +1 datos con NA
# Que porcentaje de NA tengo en cada columna?
data_set.isna().sum() / data_set.shape[0] * 100

# Si bien esto deberiamos hacerlo despues de sacar todas las variables que no nos interesan, para simplificar
# el analisis, lo hacemos ahora.
data_set = data_set.dropna()

# vef1_cvf_pre_por y intima_m_c_d deberian ser numericos
# Primero lo paso a un tipo de dato str para que funcione str.replace. Antes era un object
intima_to_float = data_set['intima_m_c_d'].astype(str).str.replace(",", ".").str.replace("|", "")
data_set['intima_m_c_d'] = intima_to_float.astype(float)
data_set['vef1_cvf_pre_por'] = data_set['vef1_cvf_pre_por'].astype(float)
data_set[['gender', 'placas_atero']] = data_set[['gender', 'placas_atero']].astype(int)


# Algunas variables tienen 2=Si, 1=No. Lo cambio para normalizar con el resto de variables y binarizar luego
def two_to_one(fila):
    if fila == 2:
        return 1
    else:
        return 0


# La variable .apply() sabe cuantos ejes tiene el df que le estamos dando.
# Si tiene solo 1, no hay que ponerle axis. Sino se rompe.
data_set['expo_tab_otro'] = data_set['expo_tab_otro'].apply(two_to_one)
data_set['ant_p_enf'] = data_set['ant_p_enf'].apply(two_to_one)
data_set['dis_p'] = data_set['dis_p'].apply(two_to_one)
data_set['hta_p'] = data_set['hta_p'].apply(two_to_one)
data_set['ecv_p'] = data_set['ecv_p'].apply(two_to_one)
data_set['dm2_p'] = data_set['dm2_p'].apply(two_to_one)

# Hago y analizo un boxplot y violin plot de cada variable que no es binaria para ver los outliers
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

# Luego del analisis del boxplot elimino los outliers
# Teniendo en cuenta la cantidad de datos que tenemos y los outliers vistos,
# Voy a sacar los outliers segun el test de Tukey. Tomando rango intercuartilico:
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
# Teniendo 76 valores outliers, elimino esas filas
len(indices_a_eliminar)

data_set = data_set.drop(indices_a_eliminar)


# Normalizo los datos que no son binarios
def normalizacion_minmax(columna):
    maximo = columna.max()
    minimo = columna.min()
    columnas_normalizadas = ((columna - minimo) / (maximo - minimo))
    return columnas_normalizadas

# Haciendo data_set.items() se forma un generator.
for col_name, col in data_set.items():
    if col.dtype == float:
        data_set[col_name] = normalizacion_minmax(col)


data_set[['age', 'imc', 'i_cin_cad', 'pre_art_sis', 'pre_art_dias', 'cvf_pre_por',
          'vef1_cvf_pre_por', 'intima_m_c_d', 'intima_m_c_i']] = data_set[
    ['age', 'imc', 'i_cin_cad', 'pre_art_sis', 'pre_art_dias', 'cvf_pre_por',
     'vef1_cvf_pre_por', 'intima_m_c_d', 'intima_m_c_i']].apply(normalizacion_minmax, axis=0)

for i in range(0, len(description.columns)):
    print(description.iloc[:, i])

# # Elimino filas segun valores outliers definidos
# index_to_delete <- c()
# index_to_delete <- c(which(data_set$intima_m_c_i > 5), which(data_set$hba1c > 500),
#                      which(data_set$tri > 500), which(data_set$cldl < 0), which(data_set$cldl > 310),
#                      which(data_set$vef1_cvf_pre_por > 300)) %>% unique() %>% sort(decreasing = TRUE)
# data_set <- data_set[-c(index_to_delete), ]


# #ANALISIS----
# ## FORMULA ----
# # Factores de riesgo = (ln(Edad) * 3.06117) + (ln(Colesterol total) * 1.12370) - (ln(Colesterol HDL) * 0.93263) + (ln(TA sistólica) * Factor TA sis) + Cig + DM - 23.9802
# factores_de_riesgo <- (log(data_set$age) * 3.06117) + (log(data_set$ctotal) * 1.12370) - (log(data_set$chdl) * 0.93263) + (log(data_set$pre_art_sis) * data_set$hay_tto) + data_set$expo_tab_otro + data_set$dm2_p - 23.9802
# riesgo = 100 * (1 - 0.88936^ exp(factores_de_riesgo))
# summary(riesgo)
#
# # Agrego la variable de riesgo al data_set
# data_set <- cbind(data_set, riesgo)
# data_set$hay_tto <- NULL
#
# cols_data_set_no_pulm <- c('age','gender','dis_p_act','hta_p','ecv_p','dm2_p', 'expo_tab_otro','imc',
#                            'i_cin_cad', 'pre_art_sis','pre_art_dias', 'intima_m_c_d','intima_m_c_i',
#                            'placas_atero', 'riesgo')
#
# data_set <- data_set[, cols_data_set_no_pulm]
#
# # Elimino las filas que tienen NA. A otra cosa jajaja
# data_set <- na.omit(data_set)


# # Transformacion de los datos. Busco transformar el riesgo
# Value <- data_set$riesgo
# Group <- rep("riesgo", nrow(data_set))
# grafico <- ggplot(data_set, aes(x = Group, y = Value)) +
#   geom_violin() +
#   geom_boxplot(width = 0.2) +
#   labs(title = sprintf("%s", Group[1]))
#
# print(grafico)
#
# Value <- log(data_set$riesgo + 1 - min(data_set$riesgo), base = 10)
# Group <- rep("riesgo", nrow(data_set))
# grafico <- ggplot(data_set, aes(x = Group, y = Value)) +
#   geom_violin() +
#   geom_boxplot(width = 0.2) +
#   labs(title = sprintf("%s", Group[1]))
#
# print(grafico)
#
#
# data_set$riesgo <- log(data_set$riesgo + 1 - min(data_set$riesgo), base = 10)
# # Una vez con los datos transformados, hacemos el escalado y normalizado de los datos.
# # Tener en cuenta que despues de usar la funcion scale, los datos se guardan como arrays.
#
# # Normalizado: min-max
# for (i in (c(1,8,9,10,11,12,13,15))) {
#   data_set[, i] <- (data_set[, i] - min(data_set[, i])) / (max(data_set[, i]) - min(data_set[, i]))
# }
#
# # Estandarizado: Z-score
# for (i in (c(1,8,9,10,11,12,13,15))) {
#   data_set[, i] <- scale(data_set[, i]) %>% as.numeric()
# }
#
# for (i in (1: ncol(data_set))) {
#   Value <- data_set[, i]
#   Group <- rep(colnames(data_set)[i], nrow(data_set))
#   grafico <- ggplot(data_set, aes(x = Group, y = Value)) +
#     geom_violin() +
#     geom_boxplot(width = 0.2) +
#     labs(title = sprintf("%s", Group[1]))
#
#   print(grafico)
# }
#
# xlsx::write.xlsx(data_set, "/home/juan/Github/Data_Science_2023/Data_Science_2023/clean_data.xlsx", row.names = FALSE)
