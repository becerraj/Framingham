library(pls)
library(e1071)
library(ggplot2)

# Carga Datos ----
data_set <- read_excel("/home/juan/Github/Data_Science_2023/Data_Science_2023/clean_data.xlsx") %>% as.data.frame()
# Saque columnas: ,'ctotal','chdl','cldl','tri','gli','hba1c' -- Todas las que provienen de analisis de sangre
data_set <- data_set[, -c(12:17)]

# Train - Test ----
# Data set for model selection Training
set.seed(42)
indices <- sample(nrow(data_set), round(0.7*nrow(data_set), 0))

# Indices de 70% de la base de datos = 265 de 378
data_train <- data_set[indices, ]
data_test <- data_set[-indices, ]

# Modelo ----
svm_model_reg <- svm(riesgo~ ., # El parametro debe ser una columna del siguiente parametro "data". En nuestro caso es la columna Ueq
                     data = data_train, # Como data se le pasa la tabla train
                     type = "eps-regression",
                     kernel = "linear",
                     scale = FALSE)

svm_model_reg$SV #resulting support vectors: las demas variables que no son Ueq
svm_model_reg$index
svm_model_reg$coefs
summary(svm_model_reg)

# Prediccion ----
pred_reg <- predict(svm_model_reg, data_test)

# Resultados ----
datos <- data.frame(media = as.vector(data_test$riesgo), diferencia = (as.vector(data_test$riesgo) - as.vector(pred_reg)))
mse = sum(datos$diferencia ^ 2) / length(datos$diferencia)

BA_plot <- ggplot(data = datos, aes(x = datos$media, y = datos$diferencia)) +
  geom_point(pch = 1, size = 1.5, col = "black") +
  labs(title = "Bland-Altman plot", x = "Método SVM linear",
       y = sprintf("Error MSE: %s", mse)) +
  ylim(mean(datos$diferencia) - 4 * sd(datos$diferencia),
       mean(datos$diferencia) + 4 * sd(datos$diferencia)) +
  # Línea de bias
  geom_hline(yintercept = mean(datos$diferencia), lwd = 1) +
  # Línea en y=0
  geom_hline(yintercept = 0, lty = 3, col = "grey30") +
  # Limits of Agreement
  geom_hline(yintercept = mean(datos$diferencia) +
               1.96 * sd(datos$diferencia),
             lty = 2, col = "firebrick") +
  geom_hline(yintercept = mean(datos$diferencia) -
               1.96 * sd(datos$diferencia),
             lty = 2, col = "firebrick") +
  theme(panel.grid.major = element_blank(),
        panel.grid.minor = element_blank()) +
  geom_text(label = "Bias", x = 991, y = -18, size = 3,
            colour = "black") +
  geom_text(label = "+1.96SD", x = 960, y = 50, size = 3,
            colour = "firebrick") +
  geom_text(label = "-1.96SD", x = 960, y = -103, size = 3,
            colour = "firebrick") +
  theme_bw() + theme(plot.title = element_text(hjust = 0.5))

BA_plot +
  geom_smooth(method = "lm", se = TRUE, fill = "lightgrey", lwd = 0.1, lty = 5)


