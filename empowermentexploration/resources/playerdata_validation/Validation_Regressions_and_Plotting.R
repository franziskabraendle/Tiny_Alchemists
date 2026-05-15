library(ggplot2)

#required libraries
library(readr)
library(plyr)
library(ggplot2)
library(lme4)
library(lmerTest)
library(emmeans)

#house keeping
rm(list=ls())

#confidence interval function
ci<-function(x){1.96*sd(x)/sqrt(length(x))}
sd_error<-function(x){sd(x)/sqrt(length(x))}

## Using preprocessed datasets ##

#Bin Dataset Rating (Question 1)

d_bin<-read.csv("bin_answers_recreated_df.csv", head=TRUE, sep=",")
d_bin$Outcome <- as.numeric(d_bin$True.Success == "True")
d_bin$AgeScaled <- scale(d_bin$Age)
d_bin$RatingScaled <- scale(d_bin$Rating)
d_bin$RecBinScaled <- scale(d_bin$Recreated.Binary)

d_bin$Group <- "childrenold"
d_bin$Group[d_bin$Age <9] <- "childrenyoung"
d_bin$Group[d_bin$Age >=18] <- "adults"

#decide on reference level
d_bin$Group<-relevel(factor(d_bin$Group), ref='childrenyoung')

bin_regression <- lmer(Rating ~ 1 + RecBinScaled + Group*RecBinScaled + (1 | Id), data=d_bin)
summary(bin_regression)

trends <- emtrends(bin_regression, ~ Group, var = "RecBinScaled")
trends_df <- as.data.frame(trends)
print(trends_df)
test(trends)

#plotting 

# assign estimates and SEs by group
estimate_kidsy  <- trends_df[trends_df$Group == "childrenyoung", "RecBinScaled.trend"]
se_kidsy        <- trends_df[trends_df$Group == "childrenyoung", "SE"]
estimate_kidso  <- trends_df[trends_df$Group == "childrenold",   "RecBinScaled.trend"]
se_kidso        <- trends_df[trends_df$Group == "childrenold",   "SE"]
estimate_adults <- trends_df[trends_df$Group == "adults",        "RecBinScaled.trend"]
se_adults       <- trends_df[trends_df$Group == "adults",        "SE"]

both_col <- c("Children\nyoung" = "#e97b0d", "Children\nold" = "#99023E", "Adults" = "#007268")
both_custom_labels <- c("Children\nyoung", "Children\nold", "Adults")  # for x-axis

bin_regression_df <- data.frame(
  group = factor(c("Children\nyoung", "Children\nold", "Adults"),
                             levels = c("Children\nyoung", "Children\nold", "Adults")),
  estimate = c(estimate_kidsy, estimate_kidso, estimate_adults),
  se = c(se_kidsy, se_kidso, se_adults)
)

ggplot(bin_regression_df, aes(x = group, y = estimate, fill = group)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.8) + 
  geom_point() +
  geom_errorbar(aes(ymin = estimate - se, ymax = estimate + se), color = 'black', width = 0.0, size = 1) +
  xlab("") +
  ylim(0, 0.46)+
  ylab(expression(hat(beta))) + 
  theme_classic() +
  geom_hline(yintercept = 0) +
  scale_fill_manual(values = both_col) +
  scale_x_discrete(labels = both_custom_labels) +
  theme(text = element_text(size = 28, family = "sans"),
        legend.position = "none")
#----------------------------------

#EmpDataset Rating

d_emp<-read.csv("emp_answers_rec_df.csv", head=TRUE, sep=",")

d_emp$Group <- "childrenold"
d_emp$Group[d_emp$Age <9] <- "childrenyoung"
d_emp$Group[d_emp$Age >=18] <- "adults"

d_emp$EmpowermentScaled <- scale(d_emp$Actual.Empowerment)
d_emp$RecEmpowermentScaled <- scale(d_emp$Recreated.Empowerment)

d_emp$Group<-relevel(factor(d_emp$Group), ref='childrenyoung')

emp_regression <- lmer(Rating ~ 1 + RecEmpowermentScaled + Group + Group*RecEmpowermentScaled + (1 | ID), data=d_emp)
summary(emp_regression)


trends <- emtrends(emp_regression, ~ Group, var = "RecEmpowermentScaled")
trends_df <- as.data.frame(trends)
print(trends_df)
test(trends)

#plotting 

estimate_kidsy  <- trends_df[trends_df$Group == "childrenyoung", "RecEmpowermentScaled.trend"]
se_kidsy        <- trends_df[trends_df$Group == "childrenyoung", "SE"]
estimate_kidso  <- trends_df[trends_df$Group == "childrenold",   "RecEmpowermentScaled.trend"]
se_kidso        <- trends_df[trends_df$Group == "childrenold",   "SE"]
estimate_adults <- trends_df[trends_df$Group == "adults",        "RecEmpowermentScaled.trend"]
se_adults       <- trends_df[trends_df$Group == "adults",        "SE"]

both_col <- c("Children\nyoung" = "#e97b0d", "Children\nold" = "#99023E", "Adults" = "#007268")
both_custom_labels <- c("Children\nyoung", "Children\nold", "Adults")  # for x-axis

emp_regression_df <- data.frame(
  group = factor(c("Children\nyoung", "Children\nold", "Adults"),
                 levels = c("Children\nyoung", "Children\nold", "Adults")),
  estimate = c(estimate_kidsy, estimate_kidso, estimate_adults),
  se = c(se_kidsy, se_kidso, se_adults)
)

ggplot(emp_regression_df, aes(x = group, y = estimate, fill = group)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.8) + 
  geom_point() +
  geom_errorbar(aes(ymin = estimate - se, ymax = estimate + se), color = 'black', width = 0.0, size = 1) +
  xlab("") +
  ylim(0, 0.46)+
  ylab(expression(hat(beta))) + 
  theme_classic() +
  geom_hline(yintercept = 0) +
  scale_fill_manual(values = both_col) +
  scale_x_discrete(labels = both_custom_labels) +
  theme(text = element_text(size = 28, family = "sans"),
        legend.position = "none")
#----------------------------------

#IntDataset

d_bin<-read.csv("bin_answers_recreated_df.csv", head=TRUE, sep=",")
d_bin$Outcome <- as.numeric(d_bin$True.Success == "True")
d_emp<-read.csv("emp_answers_rec_df.csv", head=TRUE, sep=",")
d_int<-read.csv("int_answers_rec_full_df.csv", head=TRUE, sep=",")
d_int$Chosen<-abs(d_int$Chosen-2)
both_col <- c("Adults" = "#007268", "Children old" = "#99023E", "Children young" = "#e97b0d")

d_bin$Group <- "Children old"
d_bin$Group[d_bin$Age <9] <- "Children young"
d_bin$Group[d_bin$Age >=18] <- "Adults"

d_emp$Group <- "Children old"
d_emp$Group[d_emp$Age <9] <- "Children young"
d_emp$Group[d_emp$Age >=18] <- "Adults"

d_int$Group <- "Children old"
d_int$Group[d_int$Age <9] <- "Children young"
d_int$Group[d_int$Age >=18] <- "Adults"

d_bin_elements <- d_bin
d_bin_elements$Combination <- lapply(d_bin_elements$Combination, function(x) {
  x <- gsub("\\[|\\]", "", x)
  x <- strsplit(x, ",\\s*")[[1]]
  x <- x[1:(length(x) - 1)]
  x <- gsub("'", "", x)
  return(x)
})

d_bin_elements$Combination <- lapply(d_bin_elements$Combination, function(x) sort(x))
d_bin_elements$Combination <- sapply(d_bin_elements$Combination, function(x) paste(x, collapse = ", "))
d_bin_elements_summary<-ddply(d_bin_elements, .(Combination, Group), summarize,  m_bin=mean(Rating), se_bin=sd_error(Rating))


d_emp_elements <- d_emp
d_emp_elements$Combination <- lapply(d_emp_elements$Combination, function(x) {
  x <- gsub("\\[|\\]", "", x)
  x <- strsplit(x, ",\\s*")[[1]]
  x <- x[1:(length(x) - 1)]
  x <- gsub("'", "", x)
  return(x)
})

d_emp_elements$Combination <- lapply(d_emp_elements$Combination, function(x) sort(x))
d_emp_elements$Combination <- sapply(d_emp_elements$Combination, function(x) paste(x, collapse = ", "))
d_emp_elements_summary<-ddply(d_emp_elements, .(Combination, Group), summarize,  m_emp=mean(Rating), se_emp=sd_error(Rating))

elements_rating_summary <- merge(d_bin_elements_summary, d_emp_elements_summary, by=c("Group","Combination"))

d_int_elements<-d_int
d_int_elements$Combination.1 <- lapply(d_int_elements$Combination.1, function(x) {
  x <- gsub("\\[|\\]", "", x)
  x <- strsplit(x, ",\\s*")[[1]]
  x <- x[1:(length(x) - 1)]
  x <- gsub("'", "", x)
  return(x)
})

d_int_elements$Combination.1 <- lapply(d_int_elements$Combination.1, function(x) sort(x))
d_int_elements$Combination.1 <- sapply(d_int_elements$Combination.1, function(x) paste(x, collapse = ", "))


d_int_elements$Combination.2 <- lapply(d_int_elements$Combination.2, function(x) {
  x <- gsub("\\[|\\]", "", x)
  x <- strsplit(x, ",\\s*")[[1]]
  x <- x[1:(length(x) - 1)]
  x <- gsub("'", "", x)
  return(x)
})

d_int_elements$Combination.2 <- lapply(d_int_elements$Combination.2, function(x) sort(x))
d_int_elements$Combination.2 <- sapply(d_int_elements$Combination.2, function(x) paste(x, collapse = ", "))

d_int_elements_group1 <- merge(d_int_elements, elements_rating_summary, by.x = c("Group", "Combination.1"), by.y = c("Group", "Combination"), all.x = TRUE)

names(d_int_elements_group1)[names(d_int_elements_group1) == "m_bin"] <- "m_bin_Comb1"
names(d_int_elements_group1)[names(d_int_elements_group1) == "se_bin"] <- "se_bin_Comb1"
names(d_int_elements_group1)[names(d_int_elements_group1) == "m_emp"] <- "m_emp_Comb1"
names(d_int_elements_group1)[names(d_int_elements_group1) == "se_emp"] <- "se_emp_Comb1"

d_int_elements_both <- merge(d_int_elements_group1, elements_rating_summary, by.x = c("Group", "Combination.2"), by.y = c("Group", "Combination"), all.x = TRUE)

names(d_int_elements_both)[names(d_int_elements_both) == "m_bin"] <- "m_bin_Comb2"
names(d_int_elements_both)[names(d_int_elements_both) == "se_bin"] <- "se_bin_Comb2"
names(d_int_elements_both)[names(d_int_elements_both) == "m_emp"] <- "m_emp_Comb2"
names(d_int_elements_both)[names(d_int_elements_both) == "se_emp"] <- "se_emp_Comb2"

d_int_elements_both$delta_rated_emp <- d_int_elements_both$m_emp_Comb1 - d_int_elements_both$m_emp_Comb2
d_int_elements_both$delta_rated_bin <- d_int_elements_both$m_bin_Comb1 - d_int_elements_both$m_bin_Comb2

d_int_elements_both$RatingEmpScaled <- scale(d_int_elements_both$delta_rated_emp)
d_int_elements_both$RatingBinScaled <- scale(d_int_elements_both$delta_rated_bin)
d_int_elements_both$Group<-relevel(factor(d_int_elements_both$Group), ref='Adults')




## using bin ratings ##

int_regression_bin_rat <- glmer(Chosen ~ 1 + RatingBinScaled + Group + Group*RatingBinScaled + (1 | Id), data=d_int_elements_both, family="binomial")
summary(int_regression_bin_rat)

trends <- emtrends(int_regression_bin_rat, ~ Group, var = "RatingBinScaled")
trends_df <- as.data.frame(trends)
print(trends_df)
test(trends)

#plotting 

estimate_kidsy  <- trends_df[trends_df$Group == "Children young", "RatingBinScaled.trend"]
se_kidsy        <- trends_df[trends_df$Group == "Children young", "SE"]
estimate_kidso  <- trends_df[trends_df$Group == "Children old",   "RatingBinScaled.trend"]
se_kidso        <- trends_df[trends_df$Group == "Children old",   "SE"]
estimate_adults <- trends_df[trends_df$Group == "Adults",        "RatingBinScaled.trend"]
se_adults       <- trends_df[trends_df$Group == "Adults",        "SE"]

both_col <- c("Children\nyoung" = "#e97b0d", "Children\nold" = "#99023E", "Adults" = "#007268")
both_custom_labels <- c("Children\nyoung", "Children\nold", "Adults")  # for x-axis

int_regression_df <- data.frame(
  group = factor(c("Children\nyoung", "Children\nold", "Adults"),
                 levels = c("Children\nyoung", "Children\nold", "Adults")),
  estimate = c(estimate_kidsy, estimate_kidso, estimate_adults),
  se = c(se_kidsy, se_kidso, se_adults)
)

ggplot(int_regression_df, aes(x = group, y = estimate, fill = group)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.8) + 
  geom_point() +
  geom_errorbar(aes(ymin = estimate - se, ymax = estimate + se), color = 'black', width = 0.0, size = 1) +
  xlab("") +
  ylim(0, 0.46)+
  ylab(expression(hat(beta))) + 
  theme_classic() +
  geom_hline(yintercept = 0) +
  scale_fill_manual(values = both_col) +
  scale_x_discrete(labels = both_custom_labels) +
  theme(text = element_text(size = 28, family = "sans"),
        legend.position = "none")




## using emp ratings ##

int_regression_emp_rat <- glmer(Chosen ~ 1 + RatingEmpScaled + Group + Group*RatingEmpScaled + (1 | Id), data=d_int_elements_both, family="binomial")
summary(int_regression_emp_rat)

trends <- emtrends(int_regression_emp_rat, ~ Group, var = "RatingEmpScaled")
trends_df <- as.data.frame(trends)
print(trends_df)
test(trends)

#plotting 

estimate_kidsy  <- trends_df[trends_df$Group == "Children young", "RatingEmpScaled.trend"]
se_kidsy        <- trends_df[trends_df$Group == "Children young", "SE"]
estimate_kidso  <- trends_df[trends_df$Group == "Children old",   "RatingEmpScaled.trend"]
se_kidso        <- trends_df[trends_df$Group == "Children old",   "SE"]
estimate_adults <- trends_df[trends_df$Group == "Adults",        "RatingEmpScaled.trend"]
se_adults       <- trends_df[trends_df$Group == "Adults",        "SE"]

both_col <- c("Children\nyoung" = "#e97b0d", "Children\nold" = "#99023E", "Adults" = "#007268")
both_custom_labels <- c("Children\nyoung", "Children\nold", "Adults")  # for x-axis

int_regression_df <- data.frame(
  group = factor(c("Children\nyoung", "Children\nold", "Adults"),
                 levels = c("Children\nyoung", "Children\nold", "Adults")),
  estimate = c(estimate_kidsy, estimate_kidso, estimate_adults),
  se = c(se_kidsy, se_kidso, se_adults)
)

ggplot(int_regression_df, aes(x = group, y = estimate, fill = group)) +
  geom_bar(stat = "identity", position = "dodge", width = 0.8) + 
  geom_point() +
  geom_errorbar(aes(ymin = estimate - se, ymax = estimate + se), color = 'black', width = 0.0, size = 1) +
  xlab("") +
  ylim(0, 0.46)+
  ylab(expression(hat(beta))) + 
  theme_classic() +
  geom_hline(yintercept = 0) +
  scale_fill_manual(values = both_col) +
  scale_x_discrete(labels = both_custom_labels) +
  theme(text = element_text(size = 28, family = "sans"),
        legend.position = "none")

