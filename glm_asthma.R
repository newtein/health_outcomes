library("MASS")

fname = "C:/Users/Harshit Gujral/OneDrive - University of Toronto/Projects/Environmental Discrimination/odds_ratio_module/data/2016_2017_2018_2019_2020/df_EPA Region 0 Odds Ratio CHILD.csv"
wfname = "C:/Users/Harshit Gujral/OneDrive - University of Toronto/Projects/Environmental Discrimination/odds_ratio_module/data/2016_2017_2018_2019_2020/R_model.txt"

data <- read.csv(fname)

formula = "ASTHMA  ~ ZEV_MANDATES + GENDER + RACE + POVERTY + DENSITY "

model <- glm(formula = formula, data    = data, family="binomial")


sink(wfname)
print(summary(model))
sink()