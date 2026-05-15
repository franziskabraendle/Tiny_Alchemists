library(lmerTest)
library(dplyr)
library(ggplot2)

rm(list=ls())
st_error<-function(x){sd(x)/sqrt(length(x))}
ci<-function(x){1.96*sd(x)/sqrt(length(x))}


####comparisons between groups###

#decide which file
#regression_df<- readRDS(file="kidso_adults_regression.Rda")
regression_df<- readRDS(file="groups_ordinal_regression.Rda")

mean_values <- array()
error_values <- array()
variable_names <- array()
quantiles05 <- array()
quantiles95 <- array()

for (reg_variable in colnames(regression_df)) {
  mean_values[[reg_variable]] <- mean(regression_df[[reg_variable]])
  error_values[[reg_variable]] <- ci(regression_df[[reg_variable]])
  variable_names[[reg_variable]] <- reg_variable
  quantiles95[[reg_variable]] <- quantile(regression_df[[reg_variable]],probs=c(.95))
  quantiles05[[reg_variable]] <- quantile(regression_df[[reg_variable]],probs=c(.05))
  
} 

regresults_df <- data.frame(variable_name=variable_names, mean_val=mean_values, error_val=error_values, quan95=quantiles95, quan05 = quantiles05)
regresults_df <- na.omit(regresults_df)

regresults_df <- subset(regresults_df, variable_name != "Run")
regresults_df <- subset(regresults_df, variable_name != "Singularity")
regresults_df <- subset(regresults_df, variable_name != "GroupUncSign")
regresults_df <- subset(regresults_df, variable_name != "GroupEmpSign")

regresults_df$variable_name_plot<-factor(regresults_df$variable_name, levels = regresults_df$variable_name)
regresults_df_plot <-subset(regresults_df, variable_name == "GroupEmp" | variable_name == "GroupUnc")

both_col <- c("GroupEmp" = "#0C2E8A", "GroupUnc" = "#FF796C")
both_custom_labels <- c("GroupEmp" = "Group*Emp", "GroupUnc" = "Group*Unc")


regresults_plot <- ggplot(regresults_df_plot, aes(y=mean_val, x=variable_name_plot, fill = variable_name_plot)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  stat_summary(fun.y = mean, geom = "bar", position = "dodge", width=0.8) + 
  geom_point()+
  geom_errorbar(aes(ymin=quan05, ymax=quan95),color='black', width = .0, size=1) +
  xlab("")+
  ylab(expression(hat(beta)))+ 
  theme_classic()+
  geom_hline(yintercept = 0)+
  scale_fill_manual(values=both_col)+
  scale_x_discrete(labels = both_custom_labels)+
  ylim(-0.75, 0.25)+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")
regresults_plot

regression_df_wo_sin <-subset(regression_df, Singularity == "FALSE") # 376/1000 are not singular

cat("Singularity TRUE:", nrow(subset(regression_df, Singularity == TRUE)), "\n")
cat("GroupUncSign <= 0.05:", nrow(subset(regression_df, GroupUncSign <= 0.05)), "\n")
cat("GroupUncSign <= 0.05 (wo_sin):", nrow(subset(regression_df_wo_sin, GroupUncSign <= 0.05)), "\n")
cat("GroupEmpSign <= 0.05:", nrow(subset(regression_df, GroupEmpSign <= 0.05)), "\n")
cat("GroupEmpSign <= 0.05 (wo_sin):", nrow(subset(regression_df_wo_sin, GroupEmpSign <= 0.05)), "\n")

betas_plot_emp <- ggplot(regression_df, aes(x=GroupEmp)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  geom_histogram(color="black",fill="#007268", binwidth = 0.01)+
  ylab("Count")+
  xlab(expression(hat(beta)))+ 
  theme_classic()+
  geom_vline(aes(xintercept=quantile(GroupEmp,probs=c(.05))), color="orange", size=1)+
  geom_vline(aes(xintercept=quantile(GroupEmp,probs=c(.95))), color="orange", size=1)+
  theme(text = element_text(size=18,  family="sans"))#+
betas_plot_emp

betas_plot_unc <- ggplot(regression_df, aes(x=GroupUnc)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  geom_histogram(color="black",fill="#007268", binwidth = 0.01)+
  ylab("Count")+
  xlab(expression(hat(beta)))+ 
  theme_classic()+
  geom_vline(aes(xintercept=quantile(GroupUnc,probs=c(.05))), color="orange", size=1)+
  geom_vline(aes(xintercept=quantile(GroupUnc,probs=c(.95))), color="orange", size=1)+
  theme(text = element_text(size=18,  family="sans"))#+
betas_plot_unc



#### same analysis for individual groups ####

regression_df<- readRDS(file="kidso_regression.Rda") ## decide which one


mean_values <- array()
error_values <- array()
variable_names <- array()
quantiles05 <- array()
quantiles95 <- array()

for (reg_variable in colnames(regression_df)) {
  mean_values[[reg_variable]] <- mean(regression_df[[reg_variable]])
  error_values[[reg_variable]] <- ci(regression_df[[reg_variable]])
  variable_names[[reg_variable]] <- reg_variable
  quantiles95[[reg_variable]] <- quantile(regression_df[[reg_variable]],probs=c(.95))
  quantiles05[[reg_variable]] <- quantile(regression_df[[reg_variable]],probs=c(.05))
} 


regresults_df <- data.frame(variable_name=variable_names, mean_val=mean_values, error_val=error_values, quan95=quantiles95, quan05 = quantiles05)
regresults_df <- na.omit(regresults_df)
regresults_df <- subset(regresults_df, variable_name != "Run")
regresults_df <- subset(regresults_df, variable_name != "Singularity")
regresults_df <- subset(regresults_df, variable_name != "GroupUncSign")
regresults_df <- subset(regresults_df, variable_name != "GroupEmpSign")

regresults_df$variable_name_plot<-factor(regresults_df$variable_name, levels = regresults_df$variable_name)

regresults_df_plot <-subset(regresults_df, variable_name == "Emp" | variable_name == "Unc")

both_col <- c("Emp" = "#0C2E8A", "Unc" = "#FF796C")
both_custom_labels <- c("Emp" = "Emp", "Unc" = "Unc")

regresults_plot <- ggplot(regresults_df_plot, aes(y=mean_val, x=variable_name_plot, fill = variable_name_plot)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  stat_summary(fun.y = mean, geom = "bar", position = "dodge", width=0.8) + 
  geom_point()+
  geom_errorbar(aes(ymin=quan05, ymax=quan95),color='black', width = .0, size=1) +
  xlab("")+
  ylab(expression(hat(beta)))+ 
  theme_classic()+
  geom_hline(yintercept = 0)+
  scale_fill_manual(values=both_col)+
  scale_x_discrete(labels = both_custom_labels)+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")
regresults_plot

regression_df_wo_sin <-subset(regression_df, Singularity == "FALSE") # 376/1000 are not singular

cat("Singularity TRUE:", nrow(subset(regression_df, Singularity == TRUE)), "\n")

betas_plot_emp <- ggplot(regression_df, aes(x=Emp)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  geom_histogram(color="black",fill="#007268", binwidth = 0.01)+
  ylab("Count")+
  xlab(expression(hat(beta)))+ 
  theme_classic()+
  geom_vline(aes(xintercept=quantile(Emp,probs=c(.05))), color="orange", size=1)+
  geom_vline(aes(xintercept=quantile(Emp,probs=c(.95))), color="orange", size=1)+
  theme(text = element_text(size=18,  family="sans"))#+
betas_plot_emp

betas_plot_unc <- ggplot(regression_df, aes(x=Unc)) + #choose if regresults_df or regresults_df_plot, dependent on what should be plotted
  geom_histogram(color="black",fill="#007268", binwidth = 0.01)+
  ylab("Count")+
  xlab(expression(hat(beta)))+ 
  theme_classic()+
  geom_vline(aes(xintercept=quantile(Unc,probs=c(.05))), color="orange", size=1)+
  geom_vline(aes(xintercept=quantile(Unc,probs=c(.95))), color="orange", size=1)+
  theme(text = element_text(size=18,  family="sans"))#+
betas_plot_unc

