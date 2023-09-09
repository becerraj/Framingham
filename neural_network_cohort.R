library(tensorflow)
library(keras)
library(readxl)
library(magrittr)

# Carga Datos ----
data_set <- read_excel("/home/juan/Github/Data_Science_2023/Data_Science_2023/clean_data.xlsx") %>% as.data.frame()

# Train - Test ----
# Data set for model selection Training
set.seed(42)
indices <- sample(nrow(data_set), round(0.7*nrow(data_set), 0))

# Indices de 70% de la base de datos = 265 de 378
train_NN <- data_set[indices,] %>% as.matrix()

train_X <- train_NN[, -ncol(train_NN)] %>% as.matrix()
train_Y <- train_NN[, ncol(train_NN)] %>% as.matrix()

train_X <- as_tensor(train_X, shape = c(nrow(train_X),ncol(train_X)))
test_Y <- as_tensor(train_Y, shape = c(nrow(train_Y),ncol(train_Y)))

test_NN <- data_set[-indices,] %>% as.matrix()

test_X <- test_NN[, -ncol(test_NN)] %>% as.matrix()
test_Y <- test_NN[, ncol(test_NN)] %>% as.matrix()

test_X <- as_tensor(test_X, shape = c(nrow(test_X),ncol(test_X)))
test_Y <- as_tensor(test_Y, shape = c(nrow(test_Y),ncol(test_Y)))

# Modelo NN ----
model <- keras_model_sequential()

# Atencion a los parametros:
# Units: Cantidad de neuronas
# Activation: Funcion de transferencia
# Input_Shape: Cantidad de dimensiones del tensor de entrada?
# Atencion con la ultima capa de todas y la funcion de activacion que le ponemos!
model %>%
  layer_dense(units = 14, activation = "linear", input_shape = 14, name = "Input_layer" ) %>%
  layer_dense(units = 14, activation = "linear", name = "Central_Layer") %>%
  layer_dense(units = 4, activation = "linear", name = "Pre_Last_Layer") %>%
  layer_dense(units = 1, activation = "linear")

model

model %>% compile(
  loss = "mse",
  optimizer = optimizer_adam(),
  metric = c("mse")
)

# Entrenamiento del modelo. Hay que pasarle los datos de entrenamiento y las de test
model %>% fit(
  train_X, train_Y,
  epochs = 50, batch_size = 20,
  validation_split = 0.2, verbose = 2
)


metrics <- model %>% evaluate(test_X, test_Y)
predictions <- model %>% predict(test_X)

library(BlandAltmanLeh)

data <- data.frame(Real = as.vector(test_Y), Predicciones = as.vector(predictions))
bland.altman.plot(data$Real, data$Predicciones, title = "Gráfico de Bland-Altman", xlab = "Media", ylab = "Diferencia")


# Resultados ----
datos <- data.frame(media = as.vector(test_Y), diferencia = (as.vector(test_Y) - as.vector(predictions)))
mse = sum(datos$diferencia ^ 2) / length(datos$diferencia)

BA_plot <- ggplot(data = datos, aes(x = datos$media, y = datos$diferencia)) +
  geom_point(pch = 1, size = 1.5, col = "black") +
  labs(title = "Bland-Altman plot", x = "Método NN",
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

print(BA_plot)
