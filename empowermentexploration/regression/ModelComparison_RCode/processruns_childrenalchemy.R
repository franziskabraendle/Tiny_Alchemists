library(lmerTest)
library(dplyr)
library(ggplot2)

rm(list=ls())
st_error<-function(x){sd(x)/sqrt(length(x))}
ci<-function(x){1.96*sd(x)/sqrt(length(x))}

dch<-read.csv('..\\..\\data\\regression\\20240619-1522-childrenalchemy-valuedifferences-human-1-children.csv') # Children
dad<-read.csv('..\\..\\data\\regression\\20240619-1236-childrenalchemy-valuedifferences-human-1-adults.csv') # Adults


# Get Age of the Children
df_age<-read.csv('..\\..\\resources\\playerdata\\data\\childrenalchemyHumandataChildrenComplementedMemory.csv')

match_indices <- match(dch$id, df_age$id)

dch$age <- df_age$age[match_indices]
dad$age <- 18

#### process for ordinal coding analysis ######

dch$group <- if_else(dch$age<9, 1, 2)
dad$group <-3

d1 <- dch
d2 <- dad

dat<-data.frame(run=paste(c(d1$Run, d2$Run)),
                trial=scale(c(d1$trial, d2$trial)),
                id=paste(c(d1$id, d2$id)), 
                cbu=scale(c(d1$delta_cbu, d2$delta_cbu)),
                emp=scale(c(d1$delta_emp, d2$delta_emp)),
                bin=scale(c(d1$delta_bin, d2$delta_bin)),
                rand = scale(c(d1$delta_rand, d2$delta_rand)), #remove this one for run 1
                truebin=scale(c(d1$delta_truebin, d2$delta_truebin)),
                trueemp=scale(c(d1$delta_trueemp, d2$delta_trueemp)),
                rec=scale(c(d1$delta_rec, d2$delta_rec)),
                decision=c(d1$decision, d2$decision),
                group=as.numeric(c(d1$group, d2$group)))


nrruns = max(dat$run)

regression_df <- data.frame(Run=integer(),
                            Intercept=double(),
                            Emp=double(), 
                            Unc=double(), 
                            Trial=double(),
                            GroupEmp=double(),
                            GroupUnc=double(),
                            TriAge=double(),
                            TriEmp=double(),
                            TriUnc=double(),
                            Singularity=logical(),
                            GroupEmpSign=double(),
                            GroupUncSign=double()) 

for (i in 0:nrruns){
  dftemp <- dat[dat$run == i,]
   #get model with empowerment and uncertainty as fixed effect
  meu <- glmer(decision ~ -1 + emp + cbu + group + trial + group*emp + group*cbu + trial*emp + trial*cbu + (1 | id), data=dftemp, control=glmerControl(optimizer ='optimx', optCtrl=list(method='nlminb')), family="binomial")
  summary(meu)
  
  new_row <- data.frame(Run = i, Emp = as.numeric(summary(meu)$coef[1,1]), Unc = as.numeric(summary(meu)$coef[2,1]), Group = as.numeric(summary(meu)$coef[3,1]), Trial = as.numeric(summary(meu)$coef[4,1]), GroupEmp = as.numeric(summary(meu)$coef[5,1]), GroupUnc = as.numeric(summary(meu)$coef[6,1]), TriEmp = as.numeric(summary(meu)$coef[7,1]), TriUnc = as.numeric(summary(meu)$coef[8,1]), GroupEmpSign = as.numeric(summary(meu)$coef[5,4]), GroupUncSign = as.numeric(summary(meu)$coef[6,4]), Singularity = isSingular(meu))

  # Append the new row to the existing data frame
  regression_df <- rbind(regression_df, new_row)
  print(i)
  
}

#saveRDS(regression_df,file="groups_orinal_regression.Rda")


###### process for comparisons between two groups ########

#split dch based on age into younger and older children
dch_y <- dch[dch$age <9, ]
dch_o <- dch[dch$age >=9, ]

#decide which ones to compare
d1 <- dch
d2 <- dad

dat<-data.frame(run=paste(c(d1$Run, d2$Run)),
                trial=scale(c(d1$trial, d2$trial)),
                id=paste(c(d1$id, d2$id)), 
                cbu=scale(c(d1$delta_cbu, d2$delta_cbu)),
                emp=scale(c(d1$delta_emp, d2$delta_emp)),
                bin=scale(c(d1$delta_bin, d2$delta_bin)),
                rand = scale(c(d1$delta_rand, d2$delta_rand)), #remove this one for run 1
                truebin=scale(c(d1$delta_truebin, d2$delta_truebin)),
                trueemp=scale(c(d1$delta_trueemp, d2$delta_trueemp)),
                rec=scale(c(d1$delta_rec, d2$delta_rec)),
                decision=c(d1$decision, d2$decision),
                group=c(rep('group1', nrow(d1)) ,rep('group2', nrow(d2))))


# Choose reference level
dat$group<-relevel(factor(dat$group), ref='group1') 

nrruns = max(dat$run)

regression_df <- data.frame(Run=integer(),
                            #Intercept=double(),
                            Emp=double(), 
                            Unc=double(), 
                            Trial=double(),
                            GroupEmp=double(),
                            GroupUnc=double(),
                            TriAge=double(),
                            TriEmp=double(),
                            TriUnc=double(),
                            Singularity=logical(),
                            GroupEmpSign=double(),
                            GroupUncSign=double()) 

for (i in 0:nrruns){
  dftemp <- dat[dat$run == i,]
  #get model with empowerment and uncertainty as fixed effect
  meu <- glmer(decision ~ -1 + emp + cbu + group + trial + group*emp + group*cbu + trial*emp + trial*cbu + (1 | id), data=dftemp, control=glmerControl(optimizer ='optimx', optCtrl=list(method='nlminb')), family="binomial")
  summary(meu)
  
  new_row <- data.frame(Run = i, Emp = as.numeric(summary(meu)$coef[1,1]), Unc = as.numeric(summary(meu)$coef[2,1]), Group1 = as.numeric(summary(meu)$coef[3,1]), Group2 = as.numeric(summary(meu)$coef[4,1]), Trial = as.numeric(summary(meu)$coef[5,1]), GroupEmp = as.numeric(summary(meu)$coef[6,1]), GroupUnc = as.numeric(summary(meu)$coef[7,1]), TriEmp = as.numeric(summary(meu)$coef[8,1]), TriUnc = as.numeric(summary(meu)$coef[9,1]), GroupEmpSign = as.numeric(summary(meu)$coef[6,4]), GroupUncSign = as.numeric(summary(meu)$coef[7,4]), Singularity = isSingular(meu))
  
  # Append the new row to the existing data frame
  regression_df <- rbind(regression_df, new_row)
  print(i)
  
}

#saveRDS(regression_df,file="kidso_adults_regression.Rda")



##### process for individual analyses ###########

#decide which one 
ca <- dch_y

cadf<-data.frame(run=ca$Run,
                 trial=scale(ca$trial),
                 id=paste(ca$id), 
                 cbu=scale(ca$delta_cbu),
                 emp=scale(ca$delta_emp),
                 bin=scale(ca$delta_bin),
                 cbv=scale(ca$delta_cbv),
                 truebin=scale(ca$delta_truebin),
                 trueemp=scale(ca$delta_trueemp),
                 decision=ca$decision,
                 age = scale(ca$age))

nrruns = max(cadf$run)

regression_df <- data.frame(Run=integer(),
                            #Intercept=double(),
                            Emp=double(), 
                            Unc=double(), 
                            Trial=double(),
                            TriEmp=double(),
                            TriUnc=double(),
                            Singularity=logical()) 

for (i in 0:nrruns){
  
  dftemp <- cadf[cadf$run == i,]
  # get model with empowerment and uncertainty as fixed effect
  meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu + (1 | id), data=dftemp, control=glmerControl(optimizer = "nloptwrap"), family="binomial")
  summary(meu)
  
  new_row <- data.frame(Run = i, Emp = as.numeric(summary(meu)$coef[1,1]), Unc = as.numeric(summary(meu)$coef[2,1]), Trial = as.numeric(summary(meu)$coef[3,1]), TriEmp = as.numeric(summary(meu)$coef[4,1]), TriUnc = as.numeric(summary(meu)$coef[5,1]), Singularity = isSingular(meu))
  
  # Append the new row to the existing data frame
  regression_df <- rbind(regression_df, new_row)
  print(i)
  
}

#saveRDS(regression_df,file="kidsy_regression.Rda")