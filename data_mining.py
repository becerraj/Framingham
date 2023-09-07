import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl

# #CARGO DATA----
# # Cargo el data_set

data_set = pd.read_excel("/home/juan/Github/Data_Science_2023/CartagenaCohortStudy_DATA.xlsx")

# #EXTRACT DATA----
tratamiento_hta = data_set.iloc[:, 11:54]

hay_tratamiento = []
hay_tratamiento = tratamiento_hta.apply(buscarUno, axis = 1)

def buscarUno(tratamiento_hta):
    if (tratamiento_hta[:] == 1).any():
        hay_tratamiento.append(1.99881)
    else:
        hay_tratamiento.append(1.93303)
    return(hay_tratamiento)


hay_tratamiento = []
# Tener en cuenta que la dimension real de los datos es de len(), pero su indexacion comienza en 0.
# Entonces los range si bien no toman el ultimo valor, al quedarse con el anterior no afectan al bucle.
for i in range(0, len(data_set)):
    if (tratamiento_HTA.iloc[i] == 1).any():
        hay_tratamiento.append(1.99881)
    else:
        hay_tratamiento.append(0)

# Elimino las columnas que son ttos
indices_a_eliminar = list(range(11, 54+1)) + list(range(70, 78+1))
data_set = data_set.drop(data_set.columns[indices_a_eliminar], axis = 1)
data_set['hay_tto'] = hay_tratamiento

# Que tipos de dato tengo?
data_set.dtypes
# vef1_cvf_pre_por y intima_m_c_d deberian ser numericos
data_set['intima_m_c_d'] = data_set['intima_m_c_d'].str.replace(",", ".").str.replace(r'[^0-9]', "")

data_set['intima_m_c_d'] = data_set['intima_m_c_d'].astype(float)

data_set['vef1_cvf_pre_por'] = (data_set['vef1_cvf_pre_por'].astype(float)

# Paso los valores de gender a factores:
mapeo = {0: 'Male', 1: 'Female'}
data_set['gender'] = data_set['gender'].map(mapeo)


# # Cuantos NA tengo?
data_set.isna().sum().sum()
# Tengo 590 NA
data_set.isna().any(axis=1).sum()
# Hay NA en 111 filas. Muchos pacientes tienen +1 datos con NA
# Que porcentaje de NA tengo en cada columna?
data_set.isna().sum() / data_set.shape[0] * 100

data_set = data_set.dropna()
# Teniendo en cuenta que me voy a quedar sin las columnas de parametros sericos (analisis de sangre)
# primero voy a analizar esos datos, eliminar los datos que sean outliers, y luego eliminar esas columnas
# Despues de esto analizo los datos NA faltantes para ver como tratarlos.
sns.boxplot(x = 'gender', y = 'dis_p', data = data_set)
sns.boxplot(x = 'gender', y = 'dis_p', data = data_set)

sns.violinplot(x = 'gender', y = 'dis_p', data = data_set)
# Elimino las filas que tienen NA. A otra cosa jajaja
# data_set <- na.omit(data_set)



# hay_tto <- c()
# for (i in (1:nrow(cols_tto_hta))) {
#   if (1 %in% cols_tto_hta[i, ]) {
#     hay_tto <- c(hay_tto, 1.99881)
#   } else {
#     hay_tto <- c(hay_tto, 1.93303)
#   }
# }

# # Elimino las columnas que son ttos
# data_set <- data_set[, -c(11:54, 70:78)]
# data_set <- as.data.frame(data_set)
# data_set <- cbind(data_set, hay_tto)
#
# # Que tipos de dato tengo?
# for (i in (1:ncol(data_set))) {
#   print(sprintf("%s: %s", colnames(data_set[i]), class(data_set[, i])))
# }
#
# # Cuantos NA tengo?
# colSums(is.na(data_set))
#
# # Que porcentaje de cada columna es eso?
# # print(sprintf("%s %s",(na_counts/nrow(data_set))*100, "%"))
#
# # Elimino las columnas con muy alta proporcion de NA
# # data_set <- data_set[, -c(34, 37)]
#
# # Para hacer boxplot + violin plot de los datos voy a sacar a las variables que no sean numericas
# # study_id, tipo_id, gender, num_indi_vivienda_v2, ingresos,
# data_clean <- data_set
# data_set$study_id <- NULL
# data_set$tipo_id <- NULL
#
#
# for (i in (1:ncol(data_set))) {
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
# index_F<- grep(0, data_set$gender)
# index_M <- grep(1, data_set$gender)
# data_set$gender[index_F] <- 1
# data_set$gender[index_M] <- 0
#
# index_no <- grep(1, data_set$expo_tab_otro)
# index_si <- grep(2, data_set$expo_tab_otro)
# data_set$expo_tab_otro[index_no] <- 0
# data_set$expo_tab_otro[index_si] <- 1
#
# index_no <- grep(1, data_set$dis_p)
# index_si <- grep(2, data_set$dis_p)
# data_set$dis_p[index_no] <- 0
# data_set$dis_p[index_si] <- 1
#
# index_no <- grep(1, data_set$hta_p)
# index_si <- grep(2, data_set$hta_p)
# data_set$hta_p[index_no] <- 0
# data_set$hta_p[index_si] <- 1
#
# index_no <- grep(1, data_set$ecv_p)
# index_si <- grep(2, data_set$ecv_p)
# data_set$ecv_p[index_no] <- 0
# data_set$ecv_p[index_si] <- 1
#
# index_no <- grep(1, data_set$dm2_p)
# index_si <- grep(2, data_set$dm2_p)
# data_set$dm2_p[index_no] <- 0
# data_set$dm2_p[index_si] <- 1
#
# data_set$intima_m_c_d <- as.numeric(data_set$intima_m_c_d)
# data_set$vef1_cvf_pre_por <- as.numeric(data_set$vef1_cvf_pre_por)
#
# # Elimino filas segun valores outliers definidos
# index_to_delete <- c()
# index_to_delete <- c(which(data_set$intima_m_c_i > 5), which(data_set$hba1c > 500),
#                      which(data_set$tri > 500), which(data_set$cldl < 0), which(data_set$cldl > 310),
#                      which(data_set$vef1_cvf_pre_por > 300)) %>% unique() %>% sort(decreasing = TRUE)
# data_set <- data_set[-c(index_to_delete), ]
#
#
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
#
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