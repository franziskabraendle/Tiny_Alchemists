
#house keeping
rm(list=ls())

#required libraries
library(readr)
library(plyr)
library(ggplot2)
library(lme4)
library(lmerTest)
library(dplyr)
library(effsize)


#confidence interval function
ci<-function(x){1.96*sd(x)/sqrt(length(x))}

#confidence interval function
se<-function(x){sd(x)/sqrt(length(x))}



df<-read.csv("../data/childrenalchemyHumanDataCombinedMemory.csv", head=TRUE, sep=",")

grouped_df <- group_by(df, id)
grouped_df$trial <- as.numeric(df$trial)
grouped_df$inventory <- as.numeric(df$inventory)
max_trial_df <- filter(grouped_df, trial == max(trial))
max_trial_df <- ungroup(max_trial_df)

df_copy <- max_trial_df

#print summary stats
kdf <- subset(df_copy, group=="Children")
mean(kdf$trial)
sd(kdf$trial)
min(kdf$trial)
max(kdf$trial)
mean(kdf$inventory)
sd(kdf$inventory)
adf <- subset(df_copy, group=="Adults")
mean(adf$trial)
sd(adf$trial)
min(adf$trial)
max(adf$trial)
mean(adf$inventory)
sd(adf$inventory)

#stat tests
t.test(df_copy$trial ~ df_copy$group)
cohen.d(df_copy$trial ~ df_copy$group)
wilcox.test(df_copy$trial ~ df_copy$group)

t.test(df_copy$inventory ~ df_copy$group)
cohen.d(df_copy$inventory ~ df_copy$group)
wilcox.test(df_copy$inventory ~ df_copy$group)

max_trial_df$group <- as.factor(max_trial_df$group)

#plotting
both_col <- c("Adults" = "#007268", "Children" = "#e97b0d")

inventory_plot <- ggplot(max_trial_df, aes(x = group, y = inventory, fill = group)) +
  geom_boxplot()+
  stat_summary(fun.y=mean, geom="point", shape=4, size=2, color="white", fill="white")+
  theme_classic()+
  theme(text = element_text(size=18,  family="sans"), legend.position = "none")+
  xlab("")+ylab("Inventory")+
  scale_fill_manual(values = both_col)
inventory_plot

trials_plot <- ggplot(max_trial_df, aes(x = group, y = trial, fill = group)) +
  geom_boxplot()+
  stat_summary(fun.y=mean, geom="point", shape=4, size=2, color="white", fill="white")+
  theme_classic()+
  theme(text = element_text(size=18,  family="sans"), legend.position = "none")+
  xlab("")+ylab("Trials")+
  scale_fill_manual(values = both_col)
trials_plot

kidsdf <- subset(max_trial_df, group=="Children")
kidsdf_summary <- ddply(kidsdf, ~age, summarize,  m=mean(trial), se=se(trial))

trials_age_plot <- ggplot(kidsdf_summary, aes(x = age, y = m)) +
  geom_line(color = "#b82e00", size = 1.5)+
  geom_errorbar(width=0, aes(ymin=m-se, ymax=m+se), size=1, color="#b82e00") +
  geom_point(size=2.5)+
  theme_classic()+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")+
  xlab("Age (Years)")+ylab("Trials")
trials_age_plot

kidsdf_summary2 <- ddply(kidsdf, ~age, summarize,  m=mean(inventory), se=se(inventory))
inv_age_plot <- ggplot(kidsdf_summary2, aes(x = age, y = m)) +
  geom_line(color = "#b82e00", size = 1.5)+
  geom_errorbar(width=0, aes(ymin=m-se, ymax=m+se), size=1, color="#b82e00") +
  geom_point(size=2.5)+
  theme_classic()+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")+
  xlab("Age (Years)")+ylab("Inventory")
inv_age_plot

kidsdf$agescaled <- scale(kidsdf$age)
trialagereg <- lm(trial ~ 1 + agescaled, kidsdf)
summary(trialagereg)
invagereg <- lm(inventory ~ 1 + agescaled, kidsdf)
summary(invagereg)

######## split into two children groups#########

df$group <- "Children old"
df$group[df$age <9] <- "Children young"
df$group[df$age >=18] <- "Adults"

grouped_df <- group_by(df, id)
grouped_df$trial <- as.numeric(df$trial)
grouped_df$inventory <- as.numeric(df$inventory)
max_trial_df <- filter(grouped_df, trial == max(trial))
max_trial_df <- ungroup(max_trial_df)
max_trial_df$group <- as.factor(max_trial_df$group)
sum(max_trial_df$group == "Children young")
sum(max_trial_df$group == "Children old")

#analysis
anova_result <- aov(trial ~ group, data = max_trial_df)
summary(anova_result)
tukey_result <- TukeyHSD(anova_result)
summary(tukey_result)
pairwise_result <- pairwise.wilcox.test(max_trial_df$inventory, max_trial_df$group, p.adjust.method = "bonferroni")
pairwise_result
pairwise_result2 <- pairwise.wilcox.test(max_trial_df$trial, max_trial_df$group, p.adjust.method = "bonferroni")
pairwise_result2

df_ratio1 <- aggregate(inventory ~ group + trial, data = df, FUN = mean)
df_ratio2 <- aggregate(inventory ~ group + trial, data = df, FUN = se)
colnames(df_ratio1)[3] = "ratio"
colnames(df_ratio2)[3] = "ratio_error"
df_ratio <- merge (df_ratio1, df_ratio2)
df_ratio <- df_ratio[df_ratio$trial <= 100, ]

max_trial_df$discovery <- max_trial_df$inventory / max_trial_df$trial
pairwise_result3 <- pairwise.wilcox.test(max_trial_df$discovery, max_trial_df$group, p.adjust.method = "bonferroni")
pairwise_result3

df$trial_scaled <- scale(df$trial)
inventory_reg <- lmer(inventory ~1+trial_scaled+ group+ group*trial_scaled + (1|id), df)
summary(inventory_reg)

df$group <- relevel(factor(df$group), ref = "Children old")

# Poisson 
model <- glmer(inventory ~ trial_scaled * group + (1 + trial_scaled | id),
               data = df,
               family = poisson)

summary(model)


#plot
df_ratio$group <- factor(df_ratio$group, levels = c("Children young", "Children old", "Adults"))
both_col <- c("Children young" = "#e97b0d", "Children old" = "#99023E", "Adults" = "#007268")
ratio_plot <- ggplot(df_ratio, aes(x = trial, y = ratio, color = group)) +
  geom_line(size = 1.5)+
  #geom_errorbar(width=0, aes(ymin=ratio-ratio_error, ymax=ratio+ratio_error), size=1) +
  #geom_point(size=2)+
  theme_classic()+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")+
  #ggtitle(expression("Rating over Emp"))+
  xlab("Trials")+ylab("Inventory")+
  labs(color = "Group") +
  scale_color_manual(values = both_col)+
  theme(
    legend.position = c(0.7, 0.3),      # Position of the legend
    legend.title = element_text(size = 22, ),  # Legend title styling
    legend.text = element_text(size = 20))
ratio_plot

max_trial_df$group <- gsub("Children young", "Children\nyoung", max_trial_df$group)
max_trial_df$group <- gsub("Children old", "Children\nold", max_trial_df$group)
max_trial_df$group <- factor(max_trial_df$group, levels = c("Children\nyoung", "Children\nold", "Adults"))

both_col <- c("Children\nyoung" = "#e97b0d", "Children\nold" = "#99023E", "Adults" = "#007268")

inventory_plot <- ggplot(max_trial_df, aes(x = group, y = inventory, fill = group)) +
  geom_boxplot()+
  stat_summary(fun.y=mean, geom="point", shape=4, size=2, color="white", fill="white")+
  theme_classic()+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")+
  #ggtitle(expression("Rating over Emp"))+
  xlab("")+ylab("Inventory")+
  scale_fill_manual(values = both_col)
inventory_plot

trials_plot <- ggplot(max_trial_df, aes(x = group, y = trial, fill = group)) +
  geom_boxplot()+
  stat_summary(fun.y=mean, geom="point", shape=4, size=2, color="white", fill="white")+
  theme_classic()+
  theme(text = element_text(size=28,  family="sans"), legend.position = "none")+
  #ggtitle(expression("Rating over Emp"))+
  xlab("")+ylab("Trials")+
  scale_fill_manual(values = both_col)
trials_plot



#only look at first trials
df_short <- df[df$trial<20,]
df_short$trial_scaled <- scale(df_short$trial)

grouped_df_short <- group_by(df_short, id)
max_trial_df_short <- filter(grouped_df_short, trial == max(trial))
max_trial_df_short <- ungroup(max_trial_df_short)
max_trial_df_short$group <- as.factor(max_trial_df_short$group)

max_trial_df_short$discovery <- max_trial_df_short$inventory / max_trial_df_short$trial
pairwise_result3 <- pairwise.wilcox.test(max_trial_df_short$discovery, max_trial_df_short$group, p.adjust.method = "bonferroni")
pairwise_result3

summary_stats <- aggregate(discovery ~ group, data = max_trial_df_short, 
                           FUN = function(x) c(n = length(x), 
                                               mean = mean(x), 
                                               median = median(x), 
                                               sd = sd(x)))
summary_stats
