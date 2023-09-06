# library(readr)
import pandas as pd
# library(stringr)
# library(readxl)
# library(xlsx)
# #CARGO DATA----
# # Cargo el data_set

data_set = pd.read_excel("/home/juan/Github/Data_Science_2023/CartagenaCohortStudy_DATA.xlsx")
#
# #EXTRACT DATA----
tratamiento_HTA = data_set.iloc[:, 11:54]

hay_tratamiento = []
# Tener en cuenta que la dimension real de los datos es de len(), pero su indexacion comienza en 0.
# Entonces los range si bien no toman el ultimo valor, al quedarse con el anterior no afectan al bucle.
for i in range(0, len(data_set)):
    if (tratamiento_HTA.iloc[i] == 1).any():
        hay_tratamiento.append(1)
    else:
        hay_tratamiento.append(0)

# Elimino las columnas que son ttos
indices_a_eliminar = list(range(11, 54+1)) + list(range(70, 78+1))
data_set = data_set.drop(data_set.columns[indices_a_eliminar], axis = 1)
data_set['hay_tto'] = hay_tratamiento

# Que tipos de dato tengo?
data_set.dtypes

# # Cuantos NA tengo?
data_set.isna().sum().sum()
# Tengo 590 NA
data_set.isna().any(axis=1).sum()
# Hay NA en 111 filas. Muchos pacientes tienen +1 datos con NA
# Que porcentaje de NA tengo en cada columna?
data_set.isna().sum() / data_set.shape[0] * 100




#
# # Elimino las filas que tienen NA. A otra cosa jajaja
# data_set <- na.omit(data_set)
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
# # Elimino filas segun valores outliers definidos
# index_to_delete <- c()
# index_to_delete <- c(which(data_set$intima_m_c_i > 5), which(data_set$hba1c > 500),
#                      which(data_set$tri > 500), which(data_set$cldl < 0), which(data_set$cldl > 310),
#                      which(data_set$vef1_cvf_pre_por > 300)) %>% unique() %>% sort(decreasing = TRUE)
# data_set <- data_set[-c(index_to_delete), ]
#
# # columnas iniciales eliminadas: vivienda_hab_v22, vivienda_hab_v2, ingresos, vivienda_v2, ocupacion_op, ocupacion, escolaridad, localidad
# data_set <- data_set[, c('age', 'gender', 'dis_p', 'hta_p', 'ecv_p', 'dm2_p', 'expo_tab_otro','imc',
#                          'i_cin_cad', 'pre_art_sis', 'pre_art_dias', 'ctotal', 'chdl', 'cldl', 'tri', 'gli', 'hba1c', 'cvf_pre_por',
#                          'vef1_cvf_pre_por', 'intima_m_c_d', 'intima_m_c_i', 'placas_atero', 'hay_tto')]
#
#
# #ANALISIS----
# ## FORMULA 1 ----
# #mu <- 15.5305 + 28.441 * data_set$gender - 1.4792 * log(data_set$age) - 14.4588 * data_set$gender * log(data_set$age) + 1.8515 * data_set$gender * (log(data_set$age))^2 - 0.9119 * log(data_set$pre_art_sis) - 0.2767 * data_set$expo_tab_otro - 0.7181 * log(data_set$ctotal / data_set$chdl) - 0.1759 * data_set$dm2_p - 0.1999 * data_set$dm2_p *data_set$gender
# #sigma <- exp(0.9145 - (0.2784 * mu))
# #porcentaje_10_anios <- (1- exp(-log(10) - mu) / sigma) * 100
#
# ## FORMULA 2 ----
# # Factores de riesgo = (ln(Edad) * 3.06117) + (ln(Colesterol total) * 1.12370) - (ln(Colesterol HDL) * 0.93263) + (ln(TA sistólica) * Factor TA sis) + Cig + DM - 23.9802
# factores_de_riesgo <- (log(data_set$age) * 3.06117) + (log(data_set$ctotal) * 1.12370) - (log(data_set$chdl) * 0.93263) + (log(data_set$pre_art_sis) * data_set$hay_tto) + data_set$expo_tab_otro + data_set$dm2_p - 23.9802
# riesgo = 100 * (1 - 0.88936^ exp(factores_de_riesgo))
# summary(riesgo)
#
# # Agrego la variable de riesgo al data_set
# data_set <- cbind(data_set, riesgo)
# data_set$hay_tto <- NULL
#
# data_set$intima_m_c_d <- as.numeric(data_set$intima_m_c_d)
# data_set$vef1_cvf_pre_por <- as.numeric(data_set$vef1_cvf_pre_por)
#
# xlsx::write.xlsx(data_set, "/home/juan/Github/Data_Science_2023/Data_Science_2023/clean_data.xlsx", row.names = FALSE)
#
# # Saque columnas: 'intima_m_c_d','intima_m_c_i', 'placas_atero','cvf_pos','vef1_pos' -- Provenientes de ecografia y espirometria
# columnas_para_framingham_1 <- c('age','expo_tab_otro','dis_p_act','hta_p','ecv_p','dm2_p','per_cin','per_cad','i_cin_cad',
#                               'pre_art_sis','pre_art_dias','ctotal','chdl','cldl','tri','gli','hba1c','cvf_prev','vef1_prev')
#
# # Saque columnas: ,'ctotal','chdl','cldl','tri','gli','hba1c' -- Todas las que provienen de analisis de sangre
# columnas_para_framingham_2 <- c('age','expo_tab_otro','dis_p_act','hta_p','ecv_p','dm2_p','per_cin','per_cad','i_cin_cad',
#                                 'pre_art_sis','pre_art_dias','intima_m_c_d','intima_m_c_i', 'placas_atero','cvf_prev','vef1_prev',
#                                 'cvf_pos','vef1_pos')
#
# # Falta agregar la etiqueta: RIESGO PULMONAR
# # Saque columnas: 'vef1_prev','cvf_pos'
# columnas_para_riesgo_pulmonar <- c('age','expo_tab_otro','dis_p_act','hta_p','ecv_p','dm2_p','per_cin','per_cad','i_cin_cad',
#                                    'pre_art_sis','pre_art_dias','ctotal','chdl','cldl','tri','gli','hba1c','intima_m_c_d','intima_m_c_i',
#                                    'placas_atero')
#
#
# data_to_plot <- data.frame()
# for (i in c(12,13,14,15,16, 17)) {
#   data_to_add <- data.frame(Value = rep(colnames(data_set)[i], nrow(data_set)), Group = data_set[, i])
#   data_to_plot <- rbind(data_to_plot, data_to_add)
# }
# colnames(data_to_plot) <- c("Value", "Group")
#
# ggplot(data = data_to_plot, aes(x = Value, y = Group)) +
#   stat_boxplot(geom = "errorbar", # Bigotes
#                width = 0.2) +
#   geom_violin() +
#   geom_boxplot(fill = "#4271AE", colour = "#1F3552", # Colores
#                alpha = 0.9, outlier.colour = "red") +
#   scale_y_continuous(name = "Value") +  # Etiqueta de la variable continua
#   scale_x_discrete(name = "Group") +        # Etiqueta de los grupos
#   ggtitle("Datos Cardiovasculares") +       # Título del plot
#   theme(axis.line = element_line(colour = "black", # Personalización del tema
#                                  size = 0.25))