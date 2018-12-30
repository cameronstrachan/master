library(ggplot2)
library(tidyverse)
library(drc)
library(Deriv)

df <- read.csv("~/master/nitrospina/dataflow/01-microresp/Anna_A10_28.11.18_Chamber2.csv")
colnames(df) <- c("date", "time_ms", "time_start_ms", "measurement", "sensor_mv", "sensor_uM")

plot(df$time_start_ms, df$sensor_uM)

df_select <- df %>%
  filter(time_start_ms > 25000) %>%
  filter(time_start_ms < 50000)

plot(df_select$time_start_ms, df_select$sensor_uM)

df_select2 <- df %>%
  filter(time_start_ms > 27000) %>%
  filter(time_start_ms < 40000)

model <- lm(sensor_uM ~ time_start_ms, data = df_select2)

coeff=coefficients(model)

eq = paste0("y = ", round(coeff[2],4), "*x ", round(coeff[1],4))

plot(df_select2$time_start_ms, df_select2$sensor_uM, main = eq)
abline(model, col="red", lwd=5)


###


df_select3 <- df %>%
  filter(time_start_ms > 43500) %>%
  filter(time_start_ms < 45000)


fit <- lm(sensor_uM ~ poly(time_start_ms,62,raw=TRUE), data = df_select3)

plot(df_select3$time_start_ms, df_select3$sensor_uM)
lines(df_select3$time_start_ms,predict(fit),col="red",lty=2,lwd=3)

df_select4 <- sample_n(df_select3, 100)

plot(df_select4$time_start_ms, df_select4$sensor_uM)

a_start<-3.4
b_start<-2*log(2)/a_start 

fit <-nls(sensor_uM ~ a * exp(-b*time_start_ms), data = df_select4, start=list(a=a_start, b=b_start))

plot(df_select3$time_start_ms, df_select3$sensor_uM)
lines(df_select3$time_start_ms,predict(fit),col="red",lty=2,lwd=3)


deriv_coef<-function(x) {
  x <- coef(x)
  stopifnot(names(x)[1]=="(Intercept)")
  y <- x[-1]
  stopifnot(all(grepl("^poly", names(y))))
  px <- as.numeric(gsub("poly\\(.*\\)","",names(y)))
  rr <- setNames(c(y * px, 0), names(x))
  rr[is.na(rr)] <- 0
  rr
}


df_select3$slope <- model.matrix(fit) %*% matrix(deriv_coef(fit), ncol=1)

plot(df_select3$time_start_ms, df_select3$slope)



