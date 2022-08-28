library("lme4")

fname = "C:/Users/Harshit Gujral/OneDrive - University of Toronto/Projects/Environmental Discrimination/odds_ratio_module/data/2016_2017_2018_2019_2020/df_EPA Region 0 Odds Ratio CHILD.csv"
wfname = "C:/Users/Harshit Gujral/OneDrive - University of Toronto/Projects/Environmental Discrimination/odds_ratio_module/data/2016_2017_2018_2019_2020/R_model.txt"

data <- read.csv(fname)

formula = "ASTHMA  ~ ZEV_MANDATES + GENDER + RACE + POVERTY + DENSITY + (1|STATE) + (1|EPA_REGION)"

model <- lmer(formula = formula, data    = data )

sink(wfname)
print(summary(model))
sink()